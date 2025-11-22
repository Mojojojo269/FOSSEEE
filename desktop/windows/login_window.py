from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from services.api_client import APIClient


class LoginWindow(QDialog):
    """Login window for user authentication."""
    
    def __init__(self):
        super().__init__()
        self.api_client = APIClient()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle('Chemical Equipment Visualizer - Login')
        self.setFixedSize(400, 300)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Title
        title = QLabel('Chemical Equipment\nParameter Visualizer')
        title.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        layout.addSpacing(20)
        
        # Username
        username_label = QLabel('Username:')
        layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Enter username')
        layout.addWidget(self.username_input)
        
        # Password
        password_label = QLabel('Password:')
        layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Enter password')
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)
        
        # Test credentials info
        test_info = QLabel('Test credentials: testuser / testpass123')
        test_info.setStyleSheet('color: #666; font-size: 10px;')
        test_info.setAlignment(Qt.AlignCenter)
        layout.addWidget(test_info)
        
        layout.addSpacing(10)
        
        # Login button
        self.login_button = QPushButton('Login')
        self.login_button.clicked.connect(self.handle_login)
        self.login_button.setStyleSheet('''
            QPushButton {
                background-color: #667eea;
                color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #5568d3;
            }
            QPushButton:pressed {
                background-color: #4557c2;
            }
        ''')
        layout.addWidget(self.login_button)
        
        # Connect Enter key to login
        self.username_input.returnPressed.connect(self.handle_login)
        self.password_input.returnPressed.connect(self.handle_login)
        
        self.setLayout(layout)
    
    def handle_login(self):
        """Handle login button click."""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Please enter both username and password')
            return
        
        # Disable button during login
        self.login_button.setEnabled(False)
        self.login_button.setText('Logging in...')
        
        # Attempt login
        success, message, data = self.api_client.login(username, password)
        
        # Re-enable button
        self.login_button.setEnabled(True)
        self.login_button.setText('Login')
        
        if success:
            self.accept()  # Close dialog with success
        else:
            QMessageBox.critical(self, 'Login Failed', message)
            self.password_input.clear()
            self.password_input.setFocus()
