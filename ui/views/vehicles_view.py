"""
Vehicles View - Main vehicle management interface
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView,
    QAbstractItemView, QMessageBox, QLabel
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from ui.widgets.vehicle_detail_widget import VehicleDetailWidget
from utils.translator import translator
from utils.icon_manager import icon_manager
from ui.dialogs import AddVehicleDialog, EditVehicleDialog


class VehiclesView(QWidget):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.current_selected_row = None
        self.init_ui()
        self.load_vehicles()
        self.update_translations()

    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # Vehicle detail widget (hidden by default)
        self.detail_widget = VehicleDetailWidget()
        self.detail_widget.closed.connect(self.on_detail_closed)
        layout.addWidget(self.detail_widget)

        # Top bar with search and add button
        top_bar = QHBoxLayout()

        # Search container with icon
        search_container = QWidget()
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(0, 0, 0, 0)
        search_layout.setSpacing(0)

        # Search icon
        self.search_icon_label = QLabel()
        self.search_icon_label.setPixmap(icon_manager.get_icon("search").pixmap(QSize(20, 20)))
        self.search_icon_label.setStyleSheet("""
            QLabel {
                padding-left: 12px;
                background-color: white;
                border: 1px solid #E5E9F0;
                border-right: none;
                border-top-left-radius: 8px;
                border-bottom-left-radius: 8px;
            }
        """)

        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search...")
        self.search_input.setFixedHeight(44)
        self.search_input.textChanged.connect(self.filter_vehicles)
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 1px solid #E5E9F0;
                border-left: none;
                border-top-right-radius: 8px;
                border-bottom-right-radius: 8px;
                padding: 0 16px;
                font-size: 14px;
                color: #2E3440;
            }
            QLineEdit:focus {
                border: 1px solid #5E81AC;
                border-left: none;
            }
        """)

        search_layout.addWidget(self.search_icon_label)
        search_layout.addWidget(self.search_input)
        top_bar.addWidget(search_container)

        # Add vehicle button
        self.add_btn = QPushButton("+ Add Vehicle")
        self.add_btn.setObjectName("add_vehicle_btn")
        self.add_btn.setFixedHeight(44)
        self.add_btn.setIcon(icon_manager.get_icon("add"))
        self.add_btn.setIconSize(QSize(20, 20))
        self.add_btn.clicked.connect(self.add_vehicle)
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #5E81AC;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 0 24px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #81A1C1;
            }
        """)
        top_bar.addWidget(self.add_btn)

        layout.addLayout(top_bar)

        # Vehicles table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "LICENSE PLATE", "BRAND", "MODEL", "YEAR", "MILEAGE", "INSURANCE_EXPIRY", "NOTES",
        ])

        # Table properties
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)

        # Column widths
        header = self.table.horizontalHeader()
        self.table.setColumnWidth(0, 140)  # LICENSE PLATE
        self.table.setColumnWidth(1, 110)  # BRAND
        self.table.setColumnWidth(2, 110)  # MODEL
        self.table.setColumnWidth(3, 140)   # YEAR
        self.table.setColumnWidth(4, 100)  # MILEAGE
        self.table.setColumnWidth(5, 140)  # INSURANCE_EXPIRY

        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Stretch)  # NOTES - stretch

        # Connect row click
        self.table.cellClicked.connect(self.on_row_clicked)
        layout.addWidget(self.table)

    def update_translations(self):
        """Update UI text based on current language"""
        if self.vehicle:
            self.title_label.setText(f"{translator.get('vehicle.information')}")
        else:
            self.title_label.setText(f"{translator.get('vehicle.information')}")
        
        # Update table headers
        self.table.setHorizontalHeaderLabels([
            translator.get("license_plate"),
            translator.get("brand"),
            translator.get("model"),
            translator.get("year_prod"),
            translator.get("mileage"),
            translator.get("insurance_expiry"),
            translator.get("notes"),
        ])

    def load_vehicles(self):
        """Load vehicles from database"""
        vehicles = self.db.get_all_vehicles()
        self.populate_table(vehicles)

    def populate_table(self, vehicles):
        """Populate table with vehicle data"""
        self.table.setRowCount(0)
        for vehicle in vehicles:
            row = self.table.rowCount()
            self.table.insertRow(row)

            # License Plate
            license_item = QTableWidgetItem(vehicle.get('license_plate', ''))
            license_item.setData(Qt.ItemDataRole.UserRole, vehicle)
            self.table.setItem(row, 0, license_item)

            # Brand
            self.table.setItem(row, 1, QTableWidgetItem(vehicle.get('brand', '')))

            # Model
            self.table.setItem(row, 2, QTableWidgetItem(vehicle.get('model', '')))

            # Year
            self.table.setItem(row, 3, QTableWidgetItem(str(vehicle.get('year', ''))))
            
            # Mileage
            self.table.setItem(row, 4, QTableWidgetItem(str(vehicle.get('mileage', ''))))          

            # Ασφαλισμένο εώς
            self.table.setItem(row, 5, QTableWidgetItem(str(vehicle.get('insurance_expiry', ''))))      

            # Επόμενο Κτεο
            self.table.setItem(row, 6, QTableWidgetItem(str(vehicle.get('kteo_next', ''))))    

            # Επόμενο ΚΕΚ
            self.table.setItem(row, 7, QTableWidgetItem(str(vehicle.get('kek_renewal', ''))))   

            # Σημειώσεις
            self.table.setItem(row, 8, QTableWidgetItem(str(vehicle.get('notes', ''))))

    def filter_vehicles(self):
        """Filter vehicles based on search input"""
        search_text = self.search_input.text().lower()
        for row in range(self.table.rowCount()):
            should_show = False
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item and search_text in item.text().lower():
                    should_show = True
                    break
            self.table.setRowHidden(row, not should_show)

    def on_row_clicked(self, row, column):
        """Handle row click - toggle detail view"""
        if self.current_selected_row == row and self.detail_widget.isVisible():
            self.detail_widget.hide()
            self.table.clearSelection()
            self.current_selected_row = None
        else:
            license_item = self.table.item(row, 0)
            if license_item:
                license_plate = license_item.text()
                self.show_vehicle_details(license_plate)
            self.current_selected_row = row

    def show_vehicle_details(self, license_plate):
        """Show vehicle details in detail widget"""
        vehicle = self.db.get_vehicle_by_license(license_plate)
        if vehicle:
            self.detail_widget.show_vehicle(vehicle, self.db)
        else:
            QMessageBox.warning(
                self,
                "Vehicle Not Found",
                f"Vehicle with license plate '{license_plate}' was not found."
            )

    def on_detail_closed(self):
        """Handle detail panel close"""
        self.table.clearSelection()
        self.current_selected_row = None

    def add_vehicle(self):
        """Add new vehicle"""
        dialog = AddVehicleDialog(self.db, self)
        if dialog.exec():
            self.load_vehicles()  # Reload table
            

