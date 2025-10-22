"""
Vehicle Detail Dialog - Shows full vehicle information
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QGridLayout, QWidget, QMessageBox
)
from PyQt6.QtCore import Qt

class VehicleDetailDialog(QDialog):
    def __init__(self, vehicle, db, parent=None):
        super().__init__(parent)
        self.vehicle = vehicle
        self.db = db
        
        self.setWindowTitle(f"Vehicle Details - {vehicle['license_plate']}")
        self.setModal(True)
        self.setMinimumSize(600, 700)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Title
        title = QLabel(f"📋 {self.vehicle['license_plate']}")
        title.setStyleSheet("font-size: 24px; font-weight: 600; color: #2E3440;")
        layout.addWidget(title)
        
        # Vehicle Info Card
        card = self.create_info_card()
        layout.addWidget(card)
        
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # Edit button
        edit_btn = QPushButton("✏️ Edit")
        edit_btn.setFixedHeight(44)
        edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #5E81AC;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 0 20px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #81A1C1;
            }
        """)
        edit_btn.clicked.connect(self.edit_vehicle)
        button_layout.addWidget(edit_btn)
        
        # Delete button
        delete_btn = QPushButton("🗑️ Delete")
        delete_btn.setFixedHeight(44)
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #BF616A;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 0 20px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #D08770;
            }
        """)
        delete_btn.clicked.connect(self.delete_vehicle)
        button_layout.addWidget(delete_btn)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.setFixedHeight(44)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #ECEFF4;
                color: #2E3440;
                border: none;
                border-radius: 8px;
                padding: 0 20px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #D8DEE9;
            }
        """)
        close_btn.clicked.connect(self.close)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
    
    def create_info_card(self):
        """Create the info card"""
        card = QWidget()
        card.setStyleSheet("""
            QWidget {
                background-color: #F7F9FB;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        
        grid = QGridLayout(card)
        grid.setSpacing(15)
        
        # Vehicle details
        details = [
            ("License Plate:", self.vehicle.get('license_plate', '-')),
            ("Brand:", self.vehicle.get('brand', '-')),
            ("Model:", self.vehicle.get('model', '-')),
            ("Year:", str(self.vehicle.get('year', '-'))),
            ("VIN:", self.vehicle.get('vin', '-')),
            ("Color:", self.vehicle.get('color', '-')),
            ("Fuel Type:", self.vehicle.get('fuel_type', '-')),
            ("Engine:", self.vehicle.get('engine', '-')),
            ("Transmission:", self.vehicle.get('transmission', '-')),
            ("Mileage:", f"{self.vehicle.get('mileage', 0)} km"),
            ("Status:", self.vehicle.get('status', 'Active')),
        ]
        
        row = 0
        for label_text, value_text in details:
            label = QLabel(label_text)
            label.setStyleSheet("font-weight: 600; color: #4C566A;")
            grid.addWidget(label, row, 0, Qt.AlignmentFlag.AlignLeft)
            
            value = QLabel(value_text)
            value.setStyleSheet("color: #2E3440;")
            grid.addWidget(value, row, 1, Qt.AlignmentFlag.AlignLeft)
            
            row += 1
        
        return card
    
    def edit_vehicle(self):
        """Edit vehicle"""
        QMessageBox.information(self, "Edit", "Edit functionality coming soon!")
    
    def delete_vehicle(self):
        """Delete vehicle"""
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete {self.vehicle['license_plate']}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.db.delete_vehicle(self.vehicle['id'])
            QMessageBox.information(self, "Success", "Vehicle deleted successfully!")
            self.accept()  # Close dialog
