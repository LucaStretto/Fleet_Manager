"""
Edit Vehicle Dialog - Same as Add but for EDITING
"""
from PyQt6.QtWidgets import QDialog, QMessageBox
from .add_vehicle_dialog import AddVehicleDialog

class EditVehicleDialog(AddVehicleDialog):
    """Edit Vehicle Dialog - Extends AddVehicleDialog"""
    
    def __init__(self, db, vehicle_data, parent=None):
        super().__init__(db, parent)
        self.vehicle_data = vehicle_data
        self.setWindowTitle("Επεξεργασία Οχήματος")
        self.save_btn.setText("Ενημέρωση")
        self.load_vehicle_data()
    
    def load_vehicle_data(self):
        """Load existing vehicle data into fields"""
        self.license_plate_field.setText(self.vehicle_data.get('license_plate', ''))
        self.license_plate_field.setEnabled(False)  # Can't change license plate
        self.brand_field.setCurrentText(self.vehicle_data.get('brand', ''))
        self.model_field.setText(self.vehicle_data.get('model', ''))
        # Add more fields...
    
    def save_vehicle(self):
        """UPDATE vehicle instead of INSERT"""
        # Similar validation as AddVehicleDialog
        license_plate = self.license_plate_field.text().strip()
        
        if not license_plate:
            QMessageBox.warning(self, "Σφάλμα", "Παρακαλώ εισάγετε αριθμό κυκλοφορίας!")
            return
        
        vehicle_data = {
            'license_plate': license_plate.upper(),
            'brand': self.brand_field.currentText().strip(),
            'model': self.model_field.text().strip(),
            # Add more fields...
        }
        
        try:
            self.db.update_vehicle(license_plate, vehicle_data)  # UPDATE!
            QMessageBox.information(self, "Επιτυχία", "Το όχημα ενημερώθηκε επιτυχώς!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Σφάλμα", f"Σφάλμα ενημέρωσης:\n{str(e)}")
