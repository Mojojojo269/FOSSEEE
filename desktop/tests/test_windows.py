import pytest
from unittest.mock import Mock, patch
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from windows.login_window import LoginWindow
from windows.main_window import MainWindow
from services.api_client import APIClient
import sys


@pytest.fixture(scope='session')
def qapp():
    """Create QApplication instance."""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app


class TestLoginWindow:
    """Tests for LoginWindow."""
    
    def test_login_window_initialization(self, qapp, qtbot):
        """Test login window initializes correctly."""
        window = LoginWindow()
        qtbot.addWidget(window)
        
        assert window.windowTitle() == 'Chemical Equipment Visualizer - Login'
        assert window.username_input is not None
        assert window.password_input is not None
        assert window.login_button is not None
    
    def test_login_button_click_empty_fields(self, qapp, qtbot):
        """Test login with empty fields shows warning."""
        window = LoginWindow()
        qtbot.addWidget(window)
        
        with patch('PyQt5.QtWidgets.QMessageBox.warning') as mock_warning:
            qtbot.mouseClick(window.login_button, Qt.LeftButton)
            mock_warning.assert_called_once()
    
    def test_login_button_click_with_credentials(self, qapp, qtbot):
        """Test login with credentials calls API."""
        window = LoginWindow()
        qtbot.addWidget(window)
        
        # Set credentials
        window.username_input.setText('testuser')
        window.password_input.setText('testpass123')
        
        # Mock API response
        with patch.object(window.api_client, 'login', return_value=(True, 'Success', {'token': 'test'})):
            qtbot.mouseClick(window.login_button, Qt.LeftButton)
            
            # Window should be accepted
            assert window.result() == LoginWindow.Accepted
    
    def test_login_failure_shows_error(self, qapp, qtbot):
        """Test login failure shows error message."""
        window = LoginWindow()
        qtbot.addWidget(window)
        
        window.username_input.setText('testuser')
        window.password_input.setText('wrongpass')
        
        with patch.object(window.api_client, 'login', return_value=(False, 'Invalid credentials', None)):
            with patch('PyQt5.QtWidgets.QMessageBox.critical') as mock_error:
                qtbot.mouseClick(window.login_button, Qt.LeftButton)
                mock_error.assert_called_once()


class TestMainWindow:
    """Tests for MainWindow."""
    
    @pytest.fixture
    def api_client(self):
        """Create mock API client."""
        client = Mock(spec=APIClient)
        client.token = 'test-token'
        return client
    
    def test_main_window_initialization(self, qapp, qtbot, api_client):
        """Test main window initializes correctly."""
        window = MainWindow(api_client)
        qtbot.addWidget(window)
        
        assert window.windowTitle() == 'Chemical Equipment Parameter Visualizer'
        assert window.upload_button is not None
        assert window.table_widget is not None
        assert window.chart_widget is not None
    
    def test_upload_button_opens_file_dialog(self, qapp, qtbot, api_client):
        """Test upload button opens file dialog."""
        window = MainWindow(api_client)
        qtbot.addWidget(window)
        
        with patch('PyQt5.QtWidgets.QFileDialog.getOpenFileName', return_value=('', '')):
            qtbot.mouseClick(window.upload_button, Qt.LeftButton)
            # Should not crash
    
    def test_display_dataset_updates_ui(self, qapp, qtbot, api_client):
        """Test displaying dataset updates UI elements."""
        window = MainWindow(api_client)
        qtbot.addWidget(window)
        
        mock_data = {
            'dataset_id': 1,
            'filename': 'test.csv',
            'timestamp': '2025-11-22T18:30:00Z',
            'data': [
                {
                    'Equipment Name': 'Pump-A1',
                    'Type': 'Pump',
                    'Flowrate': 150.5,
                    'Pressure': 45.2,
                    'Temperature': 85.3
                }
            ],
            'summary': {
                'total_count': 1,
                'avg_flowrate': 150.5,
                'avg_pressure': 45.2,
                'avg_temperature': 85.3,
                'type_distribution': {'Pump': 1}
            }
        }
        
        window.display_dataset(mock_data)
        
        # Check table is populated
        assert window.table_widget.rowCount() == 1
        assert window.table_widget.item(0, 0).text() == 'Pump-A1'
        
        # Check info label is updated
        assert 'test.csv' in window.info_label.text()
    
    def test_menu_actions_exist(self, qapp, qtbot, api_client):
        """Test menu actions are created."""
        window = MainWindow(api_client)
        qtbot.addWidget(window)
        
        menubar = window.menuBar()
        assert menubar is not None
        
        # Check menus exist
        menus = [action.text() for action in menubar.actions()]
        assert 'File' in menus
        assert 'View' in menus
        assert 'Report' in menus
    
    def test_pdf_action_disabled_initially(self, qapp, qtbot, api_client):
        """Test PDF action is disabled when no dataset loaded."""
        window = MainWindow(api_client)
        qtbot.addWidget(window)
        
        assert window.pdf_action.isEnabled() is False
    
    def test_pdf_action_enabled_after_upload(self, qapp, qtbot, api_client):
        """Test PDF action is enabled after dataset upload."""
        window = MainWindow(api_client)
        qtbot.addWidget(window)
        
        mock_data = {
            'dataset_id': 1,
            'filename': 'test.csv',
            'timestamp': '2025-11-22T18:30:00Z',
            'data': [],
            'summary': {
                'total_count': 0,
                'avg_flowrate': 0,
                'avg_pressure': 0,
                'avg_temperature': 0,
                'type_distribution': {}
            }
        }
        
        window.current_dataset = mock_data
        window.pdf_action.setEnabled(True)
        
        assert window.pdf_action.isEnabled() is True
