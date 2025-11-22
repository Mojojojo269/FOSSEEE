import requests
from utils.config import save_token, load_token, clear_token


class APIClient:
    """Client for interacting with the Django REST API."""
    
    def __init__(self, base_url='http://localhost:8000/api'):
        self.base_url = base_url
        self.token = load_token()
    
    def _get_headers(self):
        """Get headers with authentication token."""
        headers = {'Content-Type': 'application/json'}
        if self.token:
            headers['Authorization'] = f'Token {self.token}'
        return headers
    
    def login(self, username, password):
        """
        Authenticate user and store token.
        Returns: (success: bool, message: str, data: dict)
        """
        try:
            response = requests.post(
                f'{self.base_url}/auth/login/',
                json={'username': username, 'password': password}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data['token']
                save_token(self.token)
                return True, 'Login successful', data
            else:
                error = response.json().get('error', 'Login failed')
                return False, error, None
                
        except requests.exceptions.RequestException as e:
            return False, f'Connection error: {str(e)}', None
    
    def logout(self):
        """Clear authentication token."""
        self.token = None
        clear_token()
    
    def upload_csv(self, filepath):
        """
        Upload CSV file.
        Returns: (success: bool, message: str, data: dict)
        """
        try:
            headers = {}
            if self.token:
                headers['Authorization'] = f'Token {self.token}'
            
            with open(filepath, 'rb') as f:
                files = {'file': f}
                response = requests.post(
                    f'{self.base_url}/upload/',
                    headers=headers,
                    files=files
                )
            
            if response.status_code == 201:
                data = response.json()
                return True, 'Upload successful', data
            else:
                error = response.json().get('error', 'Upload failed')
                return False, error, None
                
        except requests.exceptions.RequestException as e:
            return False, f'Connection error: {str(e)}', None
        except FileNotFoundError:
            return False, 'File not found', None
    
    def get_history(self):
        """
        Get upload history.
        Returns: (success: bool, message: str, data: dict)
        """
        try:
            response = requests.get(
                f'{self.base_url}/history/',
                headers=self._get_headers()
            )
            
            if response.status_code == 200:
                data = response.json()
                return True, 'History retrieved', data
            else:
                error = response.json().get('error', 'Failed to get history')
                return False, error, None
                
        except requests.exceptions.RequestException as e:
            return False, f'Connection error: {str(e)}', None
    
    def get_summary(self, dataset_id):
        """
        Get summary for a specific dataset.
        Returns: (success: bool, message: str, data: dict)
        """
        try:
            response = requests.get(
                f'{self.base_url}/summary/{dataset_id}/',
                headers=self._get_headers()
            )
            
            if response.status_code == 200:
                data = response.json()
                return True, 'Summary retrieved', data
            else:
                error = response.json().get('error', 'Failed to get summary')
                return False, error, None
                
        except requests.exceptions.RequestException as e:
            return False, f'Connection error: {str(e)}', None
    
    def get_pdf(self, dataset_id, save_path):
        """
        Download PDF report.
        Returns: (success: bool, message: str)
        """
        try:
            response = requests.get(
                f'{self.base_url}/report/pdf/{dataset_id}/',
                headers=self._get_headers()
            )
            
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                return True, 'PDF downloaded successfully'
            else:
                return False, 'Failed to download PDF'
                
        except requests.exceptions.RequestException as e:
            return False, f'Connection error: {str(e)}'
        except IOError as e:
            return False, f'File error: {str(e)}'
