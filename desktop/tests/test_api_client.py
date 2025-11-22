import pytest
from unittest.mock import Mock, patch, mock_open
from services.api_client import APIClient
import json


class TestAPIClient:
    """Tests for API client."""
    
    @pytest.fixture
    def api_client(self):
        """Create API client instance."""
        return APIClient()
    
    @pytest.fixture
    def mock_response(self):
        """Create mock response."""
        mock = Mock()
        mock.status_code = 200
        mock.json.return_value = {'token': 'test-token', 'user_id': 1, 'username': 'testuser'}
        return mock
    
    def test_login_success(self, api_client, mock_response):
        """Test successful login."""
        with patch('requests.post', return_value=mock_response):
            success, message, data = api_client.login('testuser', 'testpass123')
            
            assert success is True
            assert message == 'Login successful'
            assert data['token'] == 'test-token'
            assert api_client.token == 'test-token'
    
    def test_login_invalid_credentials(self, api_client):
        """Test login with invalid credentials."""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {'error': 'Invalid credentials'}
        
        with patch('requests.post', return_value=mock_response):
            success, message, data = api_client.login('testuser', 'wrongpass')
            
            assert success is False
            assert 'Invalid credentials' in message
            assert data is None
    
    def test_login_connection_error(self, api_client):
        """Test login with connection error."""
        with patch('requests.post', side_effect=Exception('Connection failed')):
            success, message, data = api_client.login('testuser', 'testpass123')
            
            assert success is False
            assert 'Connection error' in message
            assert data is None
    
    def test_upload_csv_success(self, api_client):
        """Test successful CSV upload."""
        api_client.token = 'test-token'
        
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            'dataset_id': 1,
            'filename': 'test.csv',
            'data': [],
            'summary': {}
        }
        
        with patch('requests.post', return_value=mock_response):
            with patch('builtins.open', mock_open(read_data=b'test data')):
                success, message, data = api_client.upload_csv('test.csv')
                
                assert success is True
                assert message == 'Upload successful'
                assert data['dataset_id'] == 1
    
    def test_upload_csv_file_not_found(self, api_client):
        """Test upload with non-existent file."""
        api_client.token = 'test-token'
        
        success, message, data = api_client.upload_csv('nonexistent.csv')
        
        assert success is False
        assert 'File not found' in message
        assert data is None
    
    def test_upload_csv_error_response(self, api_client):
        """Test upload with error response."""
        api_client.token = 'test-token'
        
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {'error': 'Invalid CSV'}
        
        with patch('requests.post', return_value=mock_response):
            with patch('builtins.open', mock_open(read_data=b'test data')):
                success, message, data = api_client.upload_csv('test.csv')
                
                assert success is False
                assert 'Invalid CSV' in message
                assert data is None
    
    def test_get_history_success(self, api_client):
        """Test successful history retrieval."""
        api_client.token = 'test-token'
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'datasets': [
                {'id': 1, 'filename': 'test.csv', 'summary': {}}
            ]
        }
        
        with patch('requests.get', return_value=mock_response):
            success, message, data = api_client.get_history()
            
            assert success is True
            assert message == 'History retrieved'
            assert len(data['datasets']) == 1
    
    def test_get_history_error(self, api_client):
        """Test history retrieval with error."""
        api_client.token = 'test-token'
        
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {'error': 'Server error'}
        
        with patch('requests.get', return_value=mock_response):
            success, message, data = api_client.get_history()
            
            assert success is False
            assert data is None
    
    def test_get_summary_success(self, api_client):
        """Test successful summary retrieval."""
        api_client.token = 'test-token'
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'id': 1,
            'filename': 'test.csv',
            'summary': {'total_count': 10}
        }
        
        with patch('requests.get', return_value=mock_response):
            success, message, data = api_client.get_summary(1)
            
            assert success is True
            assert data['id'] == 1
            assert data['summary']['total_count'] == 10
    
    def test_get_pdf_success(self, api_client):
        """Test successful PDF download."""
        api_client.token = 'test-token'
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'PDF content'
        
        with patch('requests.get', return_value=mock_response):
            with patch('builtins.open', mock_open()) as mock_file:
                success, message = api_client.get_pdf(1, 'report.pdf')
                
                assert success is True
                assert 'downloaded successfully' in message
                mock_file.assert_called_once_with('report.pdf', 'wb')
    
    def test_get_pdf_error(self, api_client):
        """Test PDF download with error."""
        api_client.token = 'test-token'
        
        mock_response = Mock()
        mock_response.status_code = 404
        
        with patch('requests.get', return_value=mock_response):
            success, message = api_client.get_pdf(1, 'report.pdf')
            
            assert success is False
            assert 'Failed to download' in message
    
    def test_logout(self, api_client):
        """Test logout clears token."""
        api_client.token = 'test-token'
        
        with patch('utils.config.clear_token'):
            api_client.logout()
            
            assert api_client.token is None
