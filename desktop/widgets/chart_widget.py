from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class ChartWidget(QWidget):
    """Widget for displaying matplotlib charts."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QHBoxLayout()
        
        # Create figure with two subplots
        self.figure = Figure(figsize=(12, 4))
        self.canvas = FigureCanvas(self.figure)
        
        # Create subplots
        self.ax_pie = self.figure.add_subplot(121)
        self.ax_bar = self.figure.add_subplot(122)
        
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        
        # Initial empty charts
        self.ax_pie.text(0.5, 0.5, 'No data', ha='center', va='center')
        self.ax_bar.text(0.5, 0.5, 'No data', ha='center', va='center')
        self.canvas.draw()
    
    def update_charts(self, summary):
        """Update charts with new data."""
        # Clear previous plots
        self.ax_pie.clear()
        self.ax_bar.clear()
        
        # Pie chart - Equipment type distribution
        type_dist = summary['type_distribution']
        labels = list(type_dist.keys())
        sizes = list(type_dist.values())
        colors = ['#ff6384', '#36a2eb', '#ffce56', '#4bc0c0', '#9966ff', '#ff9f40']
        
        self.ax_pie.pie(sizes, labels=labels, autopct='%1.1f%%', 
                       colors=colors[:len(labels)], startangle=90)
        self.ax_pie.set_title('Equipment Type Distribution', fontsize=12, fontweight='bold')
        
        # Bar chart - Average parameters
        parameters = ['Flowrate', 'Pressure', 'Temperature']
        values = [
            summary['avg_flowrate'],
            summary['avg_pressure'],
            summary['avg_temperature']
        ]
        bar_colors = ['#36a2eb', '#ff6384', '#ffce56']
        
        bars = self.ax_bar.bar(parameters, values, color=bar_colors)
        self.ax_bar.set_title('Average Parameters', fontsize=12, fontweight='bold')
        self.ax_bar.set_ylabel('Value')
        self.ax_bar.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            self.ax_bar.text(bar.get_x() + bar.get_width()/2., height,
                           f'{height:.2f}',
                           ha='center', va='bottom', fontsize=9)
        
        # Adjust layout and redraw
        self.figure.tight_layout()
        self.canvas.draw()
