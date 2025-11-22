from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QListWidget, QListWidgetItem,
                             QLabel, QMessageBox, QPushButton)
from PyQt5.QtCore import Qt


class HistoryWindow(QDialog):
    """Window for displaying upload history."""
    
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.init_ui()
        self.load_history()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle('Upload History')
        self.setGeometry(200, 200, 700, 500)
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel('Last 5 Dataset Uploads')
        title.setStyleSheet('font-size: 16px; font-weight: bold; padding: 10px;')
        layout.addWidget(title)
        
        # List widget
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet('''
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 5px;
            }
            QListWidget::item {
                border-bottom: 1px solid #eee;
                padding: 10px;
                margin: 5px;
            }
            QListWidget::item:hover {
                background-color: #f5f5f5;
            }
        ''')
        layout.addWidget(self.list_widget)
        
        # Close button
        close_button = QPushButton('Close')
        close_button.clicked.connect(self.close)
        close_button.setStyleSheet('''
            QPushButton {
                background-color: #667eea;
                color: white;
                border: none;
                padding: 10px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #5568d3;
            }
        ''')
        layout.addWidget(close_button)
        
        self.setLayout(layout)
    
    def load_history(self):
        """Load and display history."""
        success, message, data = self.api_client.get_history()
        
        if not success:
            QMessageBox.critical(self, 'Error', message)
            return
        
        datasets = data.get('datasets', [])
        
        if not datasets:
            item = QListWidgetItem('No upload history available')
            item.setFlags(Qt.NoItemFlags)
            self.list_widget.addItem(item)
            return
        
        for dataset in datasets:
            # Format dataset info
            summary = dataset['summary']
            
            info_text = (
                f"Filename: {dataset['filename']}\n"
                f"Upload Time: {dataset['timestamp']}\n"
                f"Total Equipment: {summary['total_count']} | "
                f"Avg Flowrate: {summary['avg_flowrate']:.2f} | "
                f"Avg Pressure: {summary['avg_pressure']:.2f} | "
                f"Avg Temperature: {summary['avg_temperature']:.2f}\n"
                f"Equipment Types: "
            )
            
            # Add type distribution
            type_parts = [f"{k}: {v}" for k, v in summary['type_distribution'].items()]
            info_text += ", ".join(type_parts)
            
            item = QListWidgetItem(info_text)
            item.setFlags(Qt.ItemIsEnabled)
            self.list_widget.addItem(item)
