from django.contrib.auth import authenticate
from django.core.files.base import ContentFile
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import Dataset
from .utils import process_csv_file
import json
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch
from io import BytesIO
from datetime import datetime


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Authenticate user and return token.
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Please provide both username and password'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(username=username, password=password)
    
    if user is None:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    token, created = Token.objects.get_or_create(user=user)
    
    return Response({
        'token': token.key,
        'user_id': user.id,
        'username': user.username
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_csv(request):
    """
    Upload and process CSV file.
    """
    if 'file' not in request.FILES:
        return Response(
            {'error': 'No file provided'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    file = request.FILES['file']
    
    # Check file size (10MB limit)
    if file.size > 10 * 1024 * 1024:
        return Response(
            {'error': 'File size exceeds 10MB limit'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check file extension
    if not file.name.endswith('.csv'):
        return Response(
            {'error': 'File must be a CSV'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Process CSV
    data, summary, error = process_csv_file(file)
    
    if error:
        return Response(
            {'error': error},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Reset file pointer
    file.seek(0)
    
    # Create dataset record
    dataset = Dataset.objects.create(
        filename=file.name,
        summary_json=summary,
        csv_path=file,
        user=request.user
    )
    
    # Cleanup old datasets (keep only last 5)
    cleanup_old_datasets(request.user)
    
    return Response({
        'dataset_id': dataset.id,
        'filename': dataset.filename,
        'timestamp': dataset.upload_timestamp.isoformat(),
        'data': data,
        'summary': summary
    }, status=status.HTTP_201_CREATED)


def cleanup_old_datasets(user):
    """
    Keep only the last 5 datasets for a user.
    """
    datasets = Dataset.objects.filter(user=user).order_by('-upload_timestamp')
    
    if datasets.count() > 5:
        old_datasets = datasets[5:]
        for dataset in old_datasets:
            # Delete the file
            if dataset.csv_path:
                dataset.csv_path.delete()
            # Delete the record
            dataset.delete()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_history(request):
    """
    Get the last 5 dataset uploads for the authenticated user.
    """
    datasets = Dataset.objects.filter(user=request.user).order_by('-upload_timestamp')[:5]
    
    history_data = []
    for dataset in datasets:
        history_data.append({
            'id': dataset.id,
            'filename': dataset.filename,
            'timestamp': dataset.upload_timestamp.isoformat(),
            'summary': dataset.summary_json
        })
    
    return Response({
        'datasets': history_data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_summary(request, dataset_id):
    """
    Get summary for a specific dataset.
    """
    try:
        dataset = Dataset.objects.get(id=dataset_id, user=request.user)
        return Response({
            'id': dataset.id,
            'filename': dataset.filename,
            'timestamp': dataset.upload_timestamp.isoformat(),
            'summary': dataset.summary_json
        })
    except Dataset.DoesNotExist:
        return Response(
            {'error': 'Dataset not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_pdf_report(request, dataset_id):
    """
    Generate and return PDF report for a dataset.
    """
    try:
        dataset = Dataset.objects.get(id=dataset_id, user=request.user)
    except Dataset.DoesNotExist:
        return Response(
            {'error': 'Dataset not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Create PDF in memory
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=1  # Center
    )
    
    # Title
    title = Paragraph("Chemical Equipment Parameter Visualizer", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.3*inch))
    
    # Dataset info
    info_style = styles['Normal']
    elements.append(Paragraph(f"<b>Filename:</b> {dataset.filename}", info_style))
    elements.append(Paragraph(f"<b>Upload Date:</b> {dataset.upload_timestamp.strftime('%Y-%m-%d %H:%M:%S')}", info_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Summary section
    summary = dataset.summary_json
    elements.append(Paragraph("<b>Summary Statistics</b>", styles['Heading2']))
    elements.append(Spacer(1, 0.1*inch))
    
    summary_data = [
        ['Metric', 'Value'],
        ['Total Equipment Count', str(summary['total_count'])],
        ['Average Flowrate', f"{summary['avg_flowrate']:.2f}"],
        ['Average Pressure', f"{summary['avg_pressure']:.2f}"],
        ['Average Temperature', f"{summary['avg_temperature']:.2f}"],
    ]
    
    summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(summary_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Equipment type distribution
    elements.append(Paragraph("<b>Equipment Type Distribution</b>", styles['Heading2']))
    elements.append(Spacer(1, 0.1*inch))
    
    type_data = [['Equipment Type', 'Count']]
    for equip_type, count in summary['type_distribution'].items():
        type_data.append([equip_type, str(count)])
    
    type_table = Table(type_data, colWidths=[3*inch, 2*inch])
    type_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(type_table)
    
    # Build PDF
    doc.build(elements)
    
    # Get PDF from buffer
    pdf = buffer.getvalue()
    buffer.close()
    
    # Return as downloadable file
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="report_{dataset.filename}.pdf"'
    
    return response
