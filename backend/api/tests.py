from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from .models import Dataset
from .utils import validate_csv_columns, calculate_summary, process_csv_file
import pandas as pd
from io import StringIO, BytesIO
import tempfile
import os


class CSVProcessingTests(TestCase):
    """Tests for CSV processing and validation."""
    
    def setUp(self):
        """Set up test data."""
        self.valid_csv_data = """Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-A1,Pump,150.5,45.2,85.3
Reactor-R1,Reactor,200.0,120.5,350.0
Heat Exchanger-HX1,Heat Exchanger,180.3,35.8,120.5"""
        
        self.invalid_csv_missing_column = """Equipment Name,Type,Flowrate,Pressure
Pump-A1,Pump,150.5,45.2
Reactor-R1,Reactor,200.0,120.5"""
        
        self.invalid_csv_non_numeric = """Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-A1,Pump,abc,45.2,85.3
Reactor-R1,Reactor,200.0,120.5,350.0"""
    
    def test_validate_csv_columns_valid(self):
        """Test CSV column validation with valid columns."""
        df = pd.read_csv(StringIO(self.valid_csv_data))
        is_valid, error = validate_csv_columns(df)
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_validate_csv_columns_missing(self):
        """Test CSV column validation with missing columns."""
        df = pd.read_csv(StringIO(self.invalid_csv_missing_column))
        is_valid, error = validate_csv_columns(df)
        self.assertFalse(is_valid)
        self.assertIn('Temperature', error)
    
    def test_calculate_summary(self):
        """Test summary calculation accuracy."""
        df = pd.read_csv(StringIO(self.valid_csv_data))
        summary = calculate_summary(df)
        
        self.assertEqual(summary['total_count'], 3)
        self.assertAlmostEqual(summary['avg_flowrate'], 176.93, places=2)
        self.assertAlmostEqual(summary['avg_pressure'], 67.17, places=2)
        self.assertAlmostEqual(summary['avg_temperature'], 185.27, places=2)
        self.assertEqual(summary['type_distribution']['Pump'], 1)
        self.assertEqual(summary['type_distribution']['Reactor'], 1)
        self.assertEqual(summary['type_distribution']['Heat Exchanger'], 1)
    
    def test_process_csv_file_valid(self):
        """Test processing valid CSV file."""
        csv_file = BytesIO(self.valid_csv_data.encode())
        data, summary, error = process_csv_file(csv_file)
        
        self.assertIsNone(error)
        self.assertIsNotNone(data)
        self.assertIsNotNone(summary)
        self.assertEqual(len(data), 3)
        self.assertEqual(summary['total_count'], 3)
    
    def test_process_csv_file_invalid_format(self):
        """Test processing invalid CSV format."""
        csv_file = BytesIO(b"not a csv file")
        data, summary, error = process_csv_file(csv_file)
        
        self.assertIsNone(data)
        self.assertIsNone(summary)
        self.assertIsNotNone(error)
    
    def test_process_csv_file_missing_columns(self):
        """Test processing CSV with missing columns."""
        csv_file = BytesIO(self.invalid_csv_missing_column.encode())
        data, summary, error = process_csv_file(csv_file)
        
        self.assertIsNone(data)
        self.assertIsNone(summary)
        self.assertIn('Missing required columns', error)
    
    def test_process_csv_file_non_numeric(self):
        """Test processing CSV with non-numeric values."""
        csv_file = BytesIO(self.invalid_csv_non_numeric.encode())
        data, summary, error = process_csv_file(csv_file)
        
        self.assertIsNone(data)
        self.assertIsNone(summary)
        self.assertIsNotNone(error)


class AuthenticationTests(TestCase):
    """Tests for authentication functionality."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_login_valid_credentials(self):
        """Test login with valid credentials."""
        response = self.client.post('/api/auth/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)
        self.assertIn('user_id', response.data)
        self.assertEqual(response.data['username'], 'testuser')
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        response = self.client.post('/api/auth/login/', {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        
        self.assertEqual(response.status_code, 401)
        self.assertIn('error', response.data)
    
    def test_login_missing_credentials(self):
        """Test login with missing credentials."""
        response = self.client.post('/api/auth/login/', {
            'username': 'testuser'
        })
        
        self.assertEqual(response.status_code, 400)
    
    def test_token_generation(self):
        """Test token generation on login."""
        response = self.client.post('/api/auth/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        
        token = response.data['token']
        self.assertTrue(Token.objects.filter(key=token).exists())
    
    def test_protected_endpoint_without_token(self):
        """Test accessing protected endpoint without token."""
        response = self.client.get('/api/history/')
        self.assertEqual(response.status_code, 401)
    
    def test_protected_endpoint_with_token(self):
        """Test accessing protected endpoint with valid token."""
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        
        response = self.client.get('/api/history/')
        self.assertEqual(response.status_code, 200)


class UploadWorkflowTests(TestCase):
    """Integration tests for upload workflow."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        self.csv_content = """Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-A1,Pump,150.5,45.2,85.3
Reactor-R1,Reactor,200.0,120.5,350.0"""
    
    def test_complete_upload_flow(self):
        """Test complete upload flow from file to database."""
        # Create temporary CSV file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(self.csv_content)
            temp_path = f.name
        
        try:
            with open(temp_path, 'rb') as f:
                response = self.client.post('/api/upload/', {
                    'file': f
                }, format='multipart')
            
            self.assertEqual(response.status_code, 201)
            self.assertIn('dataset_id', response.data)
            self.assertIn('data', response.data)
            self.assertIn('summary', response.data)
            
            # Verify dataset in database
            dataset = Dataset.objects.get(id=response.data['dataset_id'])
            self.assertEqual(dataset.user, self.user)
            self.assertIsNotNone(dataset.summary_json)
        finally:
            os.unlink(temp_path)
    
    def test_dataset_cleanup_after_sixth_upload(self):
        """Test dataset cleanup after 6th upload."""
        # Create 6 datasets
        for i in range(6):
            with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
                f.write(self.csv_content)
                temp_path = f.name
            
            try:
                with open(temp_path, 'rb') as f:
                    self.client.post('/api/upload/', {
                        'file': f
                    }, format='multipart')
            finally:
                os.unlink(temp_path)
        
        # Should only have 5 datasets
        count = Dataset.objects.filter(user=self.user).count()
        self.assertEqual(count, 5)
    
    def test_history_endpoint_returns_correct_data(self):
        """Test history endpoint returns correct data."""
        # Upload a dataset
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(self.csv_content)
            temp_path = f.name
        
        try:
            with open(temp_path, 'rb') as f:
                upload_response = self.client.post('/api/upload/', {
                    'file': f
                }, format='multipart')
            
            # Get history
            history_response = self.client.get('/api/history/')
            
            self.assertEqual(history_response.status_code, 200)
            self.assertIn('datasets', history_response.data)
            self.assertEqual(len(history_response.data['datasets']), 1)
            
            dataset = history_response.data['datasets'][0]
            self.assertEqual(dataset['id'], upload_response.data['dataset_id'])
        finally:
            os.unlink(temp_path)
