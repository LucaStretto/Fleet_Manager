"""
Sidebar Navigation Component
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QButtonGroup
from PyQt6.QtCore import pyqtSignal, Qt

class Sidebar(QWidget):
    view_changed = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.setObjectName("sidebar")
        self.setFixedWidth(300)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup sidebar UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 80, 16, 16)
        layout.setSpacing(4)
        
        # Button group for exclusive selection
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)
        
        # Create navigation buttons
        self.vehicles_btn = self.create_nav_button("🚗  Vehicles", "Vehicles")
        self.service_btn = self.create_nav_button("🔧  Service", "Service")
        self.reminders_btn = self.create_nav_button("🔔  Reminders", "Reminders")
        self.reports_btn = self.create_nav_button("📊  Reports", "Reports")
        self.settings_btn = self.create_nav_button("⚙️  Settings", "Settings")
        
        # Add buttons to layout
        layout.addWidget(self.vehicles_btn)
        layout.addWidget(self.service_btn)
        layout.addWidget(self.reminders_btn)
        layout.addWidget(self.reports_btn)
        layout.addWidget(self.settings_btn)
        
        layout.addStretch()
        
        # Set Vehicles as default
        self.vehicles_btn.setChecked(True)
    
    def create_nav_button(self, text, view_name):
        """Create navigation button"""
        btn = QPushButton(text)
        btn.setObjectName("sidebar_button")
        btn.setCheckable(True)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(lambda: self.view_changed.emit(view_name))
        
        self.button_group.addButton(btn)
        
        return btn
