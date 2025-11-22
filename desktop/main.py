import sys
from PyQt5.QtWidgets import QApplication
from windows.login_window import LoginWindow
from windows.main_window import MainWindow
from services.api_client import APIClient


def main():
    """Main application entry point."""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Show login window
    login_window = LoginWindow()
    
    if login_window.exec_() == LoginWindow.Accepted:
        # Login successful, show main window
        main_window = MainWindow(login_window.api_client)
        main_window.show()
        sys.exit(app.exec_())
    else:
        # Login cancelled or failed
        sys.exit(0)


if __name__ == '__main__':
    main()
