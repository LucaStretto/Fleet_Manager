"""
Vehicle Detail Widget - Inline vehicle information display with badges ONLY
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
from ui.dialogs import EditVehicleDialog
from PyQt6.QtWidgets import QMessageBox
from utils.translator import translator

import os


class VehicleDetailWidget(QWidget):
    """Widget to display vehicle details with badges only"""
    
    closed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vehicle = None
        self.db = None
        self.init_ui()
        self.hide()
    
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 20)
        layout.setSpacing(0)
        
        # Main card
        self.card = QFrame()
        self.card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E5E9F0;
                border-radius: 12px;
            }
        """)
        
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(30, 30, 30, 30)
        card_layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        
        self.title_label = QLabel()
        self.title_label.setStyleSheet("font-size: 24px; font-weight: 600; color: #2E3440;")
        self.update_translations()
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        
        card_layout.addLayout(header_layout)
        
        # === SEPARATOR ===
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setFixedHeight(1)
        sep.setStyleSheet("background: #e0e0e0; border: none;")
        card_layout.addWidget(sep)
        
        # === BADGES ONLY ===
        self.badges_layout = QHBoxLayout()
        self.badges_layout.setSpacing(10)
        self.badges_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        card_layout.addLayout(self.badges_layout)
        
        # === SEPARATOR ===
        sep2 = QFrame()
        sep2.setFrameShape(QFrame.Shape.HLine)
        sep2.setFixedHeight(1)
        sep2.setStyleSheet("background: #e0e0e0; border: none;")
        card_layout.addWidget(sep2)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # Edit button
        self.edit_btn = QPushButton("✏️ Edit")  # ΠΡΟΣΘΗΚΗ self.
        self.edit_btn.setFixedHeight(44)
        self.edit_btn.clicked.connect(self.edit_vehicle)
        self.edit_btn.setStyleSheet("""
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
        button_layout.addWidget(self.edit_btn)
        
        # Delete button
        self.delete_btn = QPushButton("🗑️ Delete")  # ΠΡΟΣΘΗΚΗ self.
        self.delete_btn.setFixedHeight(44)
        self.delete_btn.clicked.connect(self.delete_vehicle)
        self.delete_btn.setStyleSheet("""
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
        button_layout.addWidget(self.delete_btn)
        
        card_layout.addLayout(button_layout)
        
        layout.addWidget(self.card)
    
    def _create_badge(self, title, value, icon_path):
        """Create a badge with icon and text"""
        w = QWidget()
        w.setStyleSheet("background: transparent; border: none;")
        
        layout = QHBoxLayout(w)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        
        # Icon
        icon_label = QLabel()
        icon_label.setFixedSize(48, 48)
        
        if os.path.exists(icon_path):
            pixmap = QPixmap(icon_path)
            icon_label.setPixmap(pixmap.scaled(
                32, 32, 
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation
            ))
            icon_label.setStyleSheet("""
                background: #ECEFF4;
                border-radius: 24px;
                padding: 8px;
            """)
        else:
            icon_label.setText("📋")
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            icon_label.setStyleSheet("""
                background: #5E81AC;
                border-radius: 24px;
                color: white;
                font-size: 20px;
            """)
        
        # Text
        text_html = f'<span style="font-size:11px;color:#888">{title}</span><br><b style="font-size:13px;color:#2E3440">{value}</b>'
        text_label = QLabel(text_html)
        text_label.setStyleSheet("background: transparent; border: none;")
        
        layout.addWidget(icon_label)
        layout.addWidget(text_label)
        
        return w
    
    def show_vehicle(self, vehicle, db):
        """Show vehicle details - BADGES ONLY"""
        self.vehicle = vehicle
        self.db = db
        
        # Update title
        self.title_label.setText(f"{translator.get('vehicle_information')}")
        
        # Clear existing badges
        while self.badges_layout.count():
            item = self.badges_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Add badges ONLY
        badges = [
            ("Αρ. Κυκλοφορίας:", vehicle.get('license_plate', '-'), "resources/icons/license_plate.png"),
            ("Έτος Κυκλοφορίας:", str(vehicle.get('year', '-')), "resources/icons/year.png"),
            ("Ασφαλισμένο εως:", vehicle.get('insurance_expiry', '-'), "resources/icons/insurance.png"),
            ("Επόμενος ΚΤΕΟ:", vehicle.get('kteo_next', '-'), "resources/icons/inspection.png"),
            ("Ανανέωση ΚΕΚ:", vehicle.get('kek_renewal', '-'), "resources/icons/kek.png"),
        ]
        
        for title, value, icon_path in badges:
            badge = self._create_badge(title, value, icon_path)
            self.badges_layout.addWidget(badge)
        
        # Show the widget
        self.show()
    
    def update_translations(self):
    """Update UI text based on current language"""
    if self.vehicle:
        self.title_label.setText(f"📋 {translator.get('vehicle.information')}")
        self.brand_label.setText(translator.get("vehicle.brand"))
        self.model_label.setText(translator.get("vehicle.model"))
        self.license_label.setText(translator.get("vehicle.license_plate"))
        self.vin_label.setText(translator.get("vehicle.vin"))
        self.year_label.setText(translator.get("vehicle.year"))
        self.color_label.setText(translator.get("vehicle.color"))
        self.fuel_label.setText(translator.get("vehicle.fuel_type"))
        self.cc_label.setText(translator.get("vehicle.engine_cc"))
        self.mileage_label.setText(translator.get("vehicle.mileage"))
        self.gps_checkbox.setText(translator.get("vehicle.has_gps"))
    else:
        # Similar labels for driver if needed
        pass
    
    def close_panel(self):
        """Close the panel"""
        self.hide()
        self.closed.emit()

    def edit_vehicle(self):
        """Open edit dialog"""
        if not self.vehicle or not self.db:
            return
            
        dialog = EditVehicleDialog(self.db, self.vehicle, self)
        if dialog.exec():
            # Reload vehicle data
            updated_vehicle = self.db.get_vehicle_by_license(self.vehicle['license_plate'])
            if updated_vehicle:
                self.show_vehicle(updated_vehicle, self.db)
            # Reload table in parent vehicles_view
            if self.parent():
                self.parent().load_vehicles()

    def delete_vehicle(self):
        """Delete current vehicle"""
        try:
            # ✅ Check if we have a vehicle (could be self.vehicle or self.current_vehicle)
            vehicle = getattr(self, 'current_vehicle', None) or getattr(self, 'vehicle', None)
            
            if not vehicle:
                QMessageBox.warning(self, "Σφάλμα", "Δεν έχει επιλεγεί όχημα!")
                return
            
            license_plate = vehicle.get('license_plate', '')
            
            reply = QMessageBox.question(
                self,
                "Επιβεβαίωση Διαγραφής",
                f"Είστε σίγουροι ότι θέλετε να διαγράψετε το όχημα {license_plate};",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                # ✅ DELETE από database
                self.db.delete_vehicle(license_plate)
                
                QMessageBox.information(self, "Επιτυχία", "Το όχημα διαγράφηκε επιτυχώς!")
                
                # ✅ Close detail panel
                self.hide()
                self.closed.emit()
                
                # ✅ Refresh parent table
                parent_widget = self.parent()
                if parent_widget and hasattr(parent_widget, 'load_vehicles'):
                    parent_widget.load_vehicles()
                    
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Σφάλμα", f"Σφάλμα διαγραφής:\n{str(e)}")
