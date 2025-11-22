from django.urls import path
from . import views

urlpatterns = [
    path('auth/login/', views.login_view, name='login'),
    path('upload/', views.upload_csv, name='upload'),
    path('history/', views.get_history, name='history'),
    path('summary/<int:dataset_id>/', views.get_summary, name='summary'),
    path('report/pdf/<int:dataset_id>/', views.generate_pdf_report, name='pdf_report'),
]
