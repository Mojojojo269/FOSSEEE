from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QFileDialog, QMessageBox,
                             QTableWidget, QTableWidgetItem, QMenuBar, QAction,
                             QStatusBar)
from PyQt5.QtCore import Qt
from services.api_client import APIClient
from widgets.chart_widget import ChartWidget
from windows.history_window import HistoryWindow


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.current_dataset = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle('Chemical Equipment Parameter Visualizer')
        self.setGeometry(100, 100, 1200, 800)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        
        # Upload section
        upload_layout = QHBoxLayout()
        upload_label = QLabel('Upload CSV File:')
        upload_layout.addWidget(upload_label)
        
        self.upload_button = QPushButton('Choose File and Upload')
        self.upload_button.clicked.connect(self.handle_upload)
        self.upload_button.setStyleSheet('''
            QPushButton {
                background-color: #667eea;
                color: white;
                border: none;
                padding: 10px 20px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #5568d3;
            }
        ''')
        upload_layout.addWidget(self.upload_button)
        upload_layout.addStretch()
        
        main_layout.addLayout(upload_layout)
        
        # Dataset info label
        self.info_label = QLabel('No dataset loaded')
        self.info_label.setStyleSheet('color: #666; padding: 10px;')
        main_layout.addWidget(self.info_label)
        
        # Summary section
        self.summary_label = QLabel('')
        self.summary_label.setStyleSheet('''
            background-color: #f5f5f5;
            padding: 15px;
            border-radius: 5px;
            font-size: 12px;
        ''')
        main_layout.addWidget(self.summary_label)
        
        # Table widget
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels([
            'Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature'
        ])
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        main_layout.addWidget(self.table_widget)
        
        # Chart widget
        self.chart_widget = ChartWidget()
        main_layout.addWidget(self.chart_widget)
        
        central_widget.setLayout(main_layout)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage('Ready')
    
    def create_menu_bar(self):
        """Create menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        upload_action = QAction('Upload CSV', self)
        upload_action.triggered.connect(self.handle_upload)
        file_menu.addAction(upload_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu('View')
        
        history_action = QAction('History', self)
        history_action.triggered.connect(self.show_history)
        view_menu.addAction(history_action)
        
        # Report menu
        report_menu = menubar.addMenu('Report')
        
        self.pdf_action = QAction('Download PDF', self)
        self.pdf_action.triggered.connect(self.download_pdf)
        self.pdf_action.setEnabled(False)
        report_menu.addAction(self.pdf_action)
    
    def handle_upload(self):
        """Handle CSV file upload."""
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            'Select CSV File',
            '',
            'CSV Files (*.csv)'
        )
        
        if not filepath:
            return
        
        self.status_bar.showMessage('Uploading...')
        self.upload_button.setEnabled(False)
        
        success, message, data = self.api_client.upload_csv(filepath)
        
        self.upload_button.setEnabled(True)
        
        if success:
            self.current_dataset = data
            self.display_dataset(data)
            self.status_bar.showMessage('Upload successful')
            self.pdf_action.setEnabled(True)
        else:
            QMessageBox.critical(self, 'Upload Failed', message)
            self.status_bar.showMessage('Upload failed')
    
    def display_dataset(self, data):
        """Display dataset in table and charts."""
        # Update info label
        self.info_label.setText(
            f"Filename: {data['filename']} | "
            f"Upload Time: {data['timestamp']}"
        )
        
        # Update summary
        summary = data['summary']
        summary_text = (
            f"Total Equipment: {summary['total_count']} | "
            f"Avg Flowrate: {summary['avg_flowrate']:.2f} | "
            f"Avg Pressure: {summary['avg_pressure']:.2f} | "
            f"Avg Temperature: {summary['avg_temperature']:.2f}"
        )
        self.summary_label.setText(summary_text)
        
        # Populate table
        equipment_data = data['data']
        self.table_widget.setRowCount(len(equipment_data))
        
        for row, item in enumerate(equipment_data):
            self.table_widget.setItem(row, 0, QTableWidgetItem(str(item['Equipment Name'])))
            self.table_widget.setItem(row, 1, QTableWidgetItem(str(item['Type'])))
            self.table_widget.setItem(row, 2, QTableWidgetItem(str(item['Flowrate'])))
            self.table_widget.setItem(row, 3, QTableWidgetItem(str(item['Pressure'])))
            self.table_widget.setItem(row, 4, QTableWidgetItem(str(item['Temperature'])))
        
        # Update charts
        self.chart_widget.update_charts(summary)
    
    def show_history(self):
        """Show history window."""
        history_window = HistoryWindow(self.api_client, self)
        history_window.exec_()
    
    def download_pdf(self):
        """Download PDF report."""
        if not self.current_dataset:
            QMessageBox.warning(self, 'No Dataset', 'Please upload a dataset first')
            return
        
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            'Save PDF Report',
            f"report_{self.current_dataset['filename']}.pdf",
            'PDF Files (*.pdf)'
        )
        
        if not filepath:
            return
        
        self.status_bar.showMessage('Generating PDF...')
        
        success, message = self.api_client.get_pdf(
            self.current_dataset['dataset_id'],
            filepath
        )
        
        if success:
            QMessageBox.information(self, 'Success', 'PDF report downloaded successfully')
            self.status_bar.showMessage('PDF downloaded')
        else:
            QMessageBox.critical(self, 'Error', message)
            self.status_bar.showMessage('PDF download failed')
