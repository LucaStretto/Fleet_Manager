"""
Add Vehicle Dialog - FINAL Premium Version
Perfect Alignment & Modern Design with PNG Icons
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLineEdit, QPushButton, QMessageBox,
    QLabel, QSpinBox, QComboBox, QDateEdit, QTextEdit,
    QFileDialog, QScrollArea, QWidget
    
)
from PyQt6.QtCore import Qt, QDate, QSize
from PyQt6.QtGui import QIcon
from utils.translator import translator
from utils.icon_manager import icon_manager
from PyQt6.QtWidgets import QCheckBox
from PyQt6.QtWidgets import QCompleter 
from utils.brand_manager import BrandManager
from utils.config import Config
import os
import shutil

class AddVehicleDialog(QDialog):
    """Premium Add Vehicle Dialog - Final Version"""
    
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.parent = parent
        self.licence_file_path = None
        self.insurance_file_path = None
        self.kteo_file_path = None
        
        self.init_ui()
        self.apply_translations()
        
        # Apply theme
        if hasattr(parent, 'theme_manager'):
            self.apply_theme(parent.theme_manager.current_theme)
        else:
            self.apply_theme("light")
    
    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle("Νέο Όχημα")
        self.setFixedSize(1400, 900)
        self.setModal(True)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(0)
        
        container = QWidget()
        container.setObjectName("mainContainer")
        container.setStyleSheet("""
            QWidget#mainContainer {
                background-color: white;
                border: 1px solid #E5E9F0;
                border-radius: 12px;
            }
        """)
        
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(25, 25, 25, 25)
        container_layout.setSpacing(0)
        
        container_layout.addWidget(self.create_vehicle_info_section())
        container_layout.addSpacing(20)
        container_layout.addWidget(self.create_insurance_section())
        container_layout.addSpacing(20)
        container_layout.addWidget(self.create_kteo_section())
        container_layout.addSpacing(20)
        container_layout.addWidget(self.create_kek_section())
        container_layout.addSpacing(20)
        container_layout.addWidget(self.create_notes_section())
        
        scroll = QScrollArea()
        scroll.setWidget(container)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background-color: #ECEFF4;
                width: 8px;
                margin: 0px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background-color: #D8DEE9;
                min-height: 30px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #5E81AC;
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: none;
            }
        """)

        main_layout.addWidget(scroll, 1)
        
        button_container = QWidget()
        button_container.setStyleSheet("QWidget { background-color: transparent; border-top: 1px solid #E5E9F0; border-radius: 0px; }")
        button_layout = self.create_bottom_buttons()
        button_container.setLayout(button_layout)
        main_layout.addWidget(button_container)
    
    def create_section_header(self, icon_name, title):
        """Create section header"""
        header = QWidget()
        header.setObjectName("sectionHeader")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 8)
        header_layout.setSpacing(8)
        
        icon_label = QLabel()
        icon_label.setObjectName("headerIcon")
        icon_label.setPixmap(icon_manager.get_icon(icon_name).pixmap(QSize(18, 18)))
        header_layout.addWidget(icon_label)
        
        title_label = QLabel(title)
        title_label.setObjectName("headerTitle")
        title_label.setStyleSheet("QLabel#headerTitle { font-size: 13px; font-weight: 600; color: #2E3440; border: none; background: transparent; }")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        return header
    
    def create_vehicle_info_section(self):
        """Πληροφορίες Οχήματος"""
        section = QWidget()
        section.setObjectName("borderedSection")
        section.setStyleSheet("QWidget#borderedSection { background-color: transparent; border: 1px solid #E5E9F0; border-radius: 8px; }")
        
        layout = QVBoxLayout(section)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 20, 30, 20)
        
        self.vehicle_header = self.create_section_header("car", "Πληροφορίες Οχήματος")
        layout.addWidget(self.vehicle_header)
        
        grid = QGridLayout()
        grid.setHorizontalSpacing(20)
        grid.setVerticalSpacing(12)
        label_width = 100
        
        # ROW 1
        self.brand_label = QLabel("Μάρκα:")
        self.brand_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.brand_label.setFixedWidth(label_width)
        grid.addWidget(self.brand_label, 0, 0)
        
        self.brand_field = QComboBox()
        self.brand_field.setEditable(True)
        self.brand_field.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.brand_field.addItems(BrandManager.get_all_brands())
        self.brand_field.setCurrentIndex(-1)
        self.brand_field.setPlaceholderText("Επιλέξτε ή γράψτε μάρκα")
        self.brand_field.setCompleter(QCompleter(BrandManager.get_all_brands()))
        self.brand_field.completer().setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.brand_field.completer().setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.brand_field.setMinimumWidth(180)
        grid.addWidget(self.brand_field, 0, 1)
        
        self.model_label = QLabel("Μοντέλο:")
        self.model_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.model_label.setFixedWidth(label_width)
        grid.addWidget(self.model_label, 0, 2)
        
        self.model_field = QLineEdit()
        self.model_field.setPlaceholderText("π.χ. Corolla")
        self.model_field.setMinimumWidth(180)
        grid.addWidget(self.model_field, 0, 3)
        
        self.license_label = QLabel("Αρ. Κυκλοφορίας:")
        self.license_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.license_label.setFixedWidth(label_width)
        grid.addWidget(self.license_label, 0, 4)
        
        self.license_plate_field = QLineEdit()
        self.license_plate_field.setPlaceholderText("π.χ. XEP-4096")
        self.license_plate_field.setMinimumWidth(180)
        grid.addWidget(self.license_plate_field, 0, 5)
        
        # ROW 2
        self.vin_label = QLabel("VIN:")
        self.vin_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.vin_label.setFixedWidth(label_width)
        grid.addWidget(self.vin_label, 1, 0)
        
        self.vin_field = QLineEdit()
        self.vin_field.setPlaceholderText("17 χαρακτήρες")
        self.vin_field.setMaxLength(17)
        self.vin_field.setMinimumWidth(180)
        grid.addWidget(self.vin_field, 1, 1)
        
        self.type_label = QLabel("Τύπος:")
        self.type_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.type_label.setFixedWidth(label_width)
        grid.addWidget(self.type_label, 1, 2)
        
        self.type_field = QComboBox()
        self.type_field.addItems(Config.get_vehicle_types())
        self.type_field.setMinimumWidth(180)
        grid.addWidget(self.type_field, 1, 3)
        
        self.year_label = QLabel("Έτος:")
        self.year_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.year_label.setFixedWidth(label_width)
        grid.addWidget(self.year_label, 1, 4)
        
        self.year_field = QSpinBox()
        self.year_field.setRange(1900, 2030)
        self.year_field.setValue(2020)
        self.year_field.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)
        self.year_field.setMinimumWidth(180)
        grid.addWidget(self.year_field, 1, 5)
        
        # ROW 3
        self.cc_label = QLabel("Κυβικά (cc):")
        self.cc_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.cc_label.setFixedWidth(label_width)
        grid.addWidget(self.cc_label, 2, 0)
        
        self.engine_cc_field = QSpinBox()
        self.engine_cc_field.setRange(50, 10000)
        self.engine_cc_field.setValue(1600)
        self.engine_cc_field.setSuffix(" cc")
        self.engine_cc_field.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)
        self.engine_cc_field.setMinimumWidth(180)
        grid.addWidget(self.engine_cc_field, 2, 1)
        
        self.fuel_label = QLabel("Τύπος Καυσίμου:")
        self.fuel_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.fuel_label.setFixedWidth(label_width)
        grid.addWidget(self.fuel_label, 2, 2)
        
        self.fuel_type_field = QComboBox()
        self.fuel_type_field.addItems(Config.get_fuel_types())
        self.fuel_type_field.setMinimumWidth(180)
        grid.addWidget(self.fuel_type_field, 2, 3)
        
        self.color_label = QLabel("Χρώμα:")
        self.color_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.color_label.setFixedWidth(label_width)
        grid.addWidget(self.color_label, 2, 4)
        
        self.color_field = QComboBox()
        self.color_field.addItems(Config.get_colors())
        self.color_field.setMinimumWidth(180)
        grid.addWidget(self.color_field, 2, 5)
        
        # ROW 4
        self.mileage_label = QLabel("Χιλιόμετρα:")
        self.mileage_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.mileage_label.setFixedWidth(label_width)
        grid.addWidget(self.mileage_label, 3, 0)
        
        self.mileage_field = QSpinBox()
        self.mileage_field.setRange(0, 9999999)
        self.mileage_field.setValue(0)
        self.mileage_field.setSuffix(" km")
        self.mileage_field.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)
        self.mileage_field.setMinimumWidth(180)
        grid.addWidget(self.mileage_field, 3, 1)

        # GPS CHECKBOX
        gps_layout = QHBoxLayout()
        gps_layout.addStretch(1)
        
        self.gps_checkbox = QCheckBox("Διαθέτει GPS Tracker")
        self.gps_checkbox.setStyleSheet("""
            QCheckBox {
                color: #4C566A;
                font-size: 12px;
                font-weight: 500;
                spacing: 8px;
                background: transparent;
                border: none;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 2px solid #D8DEE9;
                border-radius: 3px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                background-color: #5E81AC;
                border-color: #5E81AC;
            }
            QCheckBox::indicator:hover {
                border-color: #5E81AC;
            }
        """)
        gps_layout.addWidget(self.gps_checkbox)
        gps_layout.addStretch(1)
        
        grid.addLayout(gps_layout, 3, 2, 1, 2)

        # LICENCE FILE
        licence_layout = QHBoxLayout()
        licence_layout.setSpacing(8)

        licence_title = QLabel("Άδεια Κυκλοφορίας:")
        licence_title.setStyleSheet("color: #4C566A; font-size: 12px; font-weight: 500; border: none;")
        licence_layout.addWidget(licence_title)

        self.licence_label = QLabel("Δεν έχει επισυναφθεί αρχείο")
        self.licence_label.setObjectName("fileLabel")
        self.licence_label.setStyleSheet("color: #95a5a6; font-style: italic; font-size: 11px; border: none;")
        licence_layout.addWidget(self.licence_label, 1)

        self.licence_attach_btn = QPushButton()
        self.licence_attach_btn.setIcon(icon_manager.get_icon("attachment"))
        self.licence_attach_btn.setIconSize(QSize(16, 16))
        self.licence_attach_btn.clicked.connect(lambda: self.upload_document('licence'))
        self.licence_attach_btn.setFixedSize(32, 32)
        self.licence_attach_btn.setToolTip("Επισύναψη αρχείου")
        self.licence_attach_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: rgba(94, 129, 172, 0.1);
            }
            QPushButton:pressed {
                background-color: rgba(94, 129, 172, 0.2);
            }
        """)
        licence_layout.addWidget(self.licence_attach_btn)

        self.licence_remove_btn = QPushButton()
        self.licence_remove_btn.setIcon(icon_manager.get_icon("delete"))
        self.licence_remove_btn.setIconSize(QSize(16, 16))
        self.licence_remove_btn.clicked.connect(lambda: self.remove_document('licence'))
        self.licence_remove_btn.setEnabled(False)
        self.licence_remove_btn.setFixedSize(32, 32)
        self.licence_remove_btn.setToolTip("Αφαίρεση αρχείου")
        self.licence_remove_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: rgba(191, 97, 106, 0.1);
            }
            QPushButton:pressed {
                background-color: rgba(191, 97, 106, 0.2);
            }
            QPushButton:disabled {
                opacity: 0.5;
            }
        """)
        licence_layout.addWidget(self.licence_remove_btn)

        grid.addLayout(licence_layout, 3, 4, 1, 2)
        
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(3, 1)
        grid.setColumnStretch(5, 1)
        
        layout.addLayout(grid)
        return section

    def create_insurance_section(self):
        """Ασφαλιστήριο"""
        section = QWidget()
        section.setObjectName("borderedSection")
        section.setStyleSheet("QWidget#borderedSection { background-color: transparent; border: 1px solid #E5E9F0; border-radius: 8px; }")
        
        layout = QVBoxLayout(section)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 20, 30, 20)
        
        self.insurance_header = self.create_section_header("shield", "Πληροφορίες Ασφαλιστηρίου")
        layout.addWidget(self.insurance_header)
        
        grid = QGridLayout()
        grid.setHorizontalSpacing(20)
        grid.setVerticalSpacing(12)
        label_width = 100
        
        # ROW 1 - Dates
        self.ins_from_label = QLabel("Από:")
        self.ins_from_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.ins_from_label.setFixedWidth(label_width)
        grid.addWidget(self.ins_from_label, 0, 0)
        self.insurance_from_field = QDateEdit()
        self.insurance_from_field.setDate(QDate.currentDate())
        self.insurance_from_field.setCalendarPopup(True)
        grid.addWidget(self.insurance_from_field, 0, 1)
        
        self.ins_to_label = QLabel("Έως:")
        self.ins_to_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.ins_to_label.setFixedWidth(label_width)
        grid.addWidget(self.ins_to_label, 0, 2)
        self.insurance_to_field = QDateEdit()
        self.insurance_to_field.setDate(QDate.currentDate().addYears(1))
        self.insurance_to_field.setCalendarPopup(True)
        grid.addWidget(self.insurance_to_field, 0, 3)
        
        self.ins_next_label = QLabel("Επόμενο:")
        self.ins_next_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.ins_next_label.setFixedWidth(label_width)
        grid.addWidget(self.ins_next_label, 0, 4)
        self.insurance_next_field = QDateEdit()
        self.insurance_next_field.setDate(QDate.currentDate().addYears(1))
        self.insurance_next_field.setCalendarPopup(True)
        grid.addWidget(self.insurance_next_field, 0, 5)
        
        # ROW 2 - File
        insurance_layout = QHBoxLayout()
        insurance_layout.setSpacing(8)
        
        insurance_title = QLabel("Ασφαλιστήριο:")
        insurance_title.setStyleSheet("color: #4C566A; font-size: 12px; font-weight: 500; border: none;")
        insurance_layout.addWidget(insurance_title)
        
        self.insurance_label = QLabel("Δεν έχει επισυναφθεί αρχείο")
        self.insurance_label.setObjectName("fileLabel")
        self.insurance_label.setStyleSheet("color: #95a5a6; font-style: italic; font-size: 11px; border: none;")
        insurance_layout.addWidget(self.insurance_label, 1)
        
        self.insurance_attach_btn = QPushButton()
        self.insurance_attach_btn.setIcon(icon_manager.get_icon("attachment"))
        self.insurance_attach_btn.setIconSize(QSize(16, 16))
        self.insurance_attach_btn.clicked.connect(lambda: self.upload_document('insurance'))
        self.insurance_attach_btn.setFixedSize(32, 32)
        self.insurance_attach_btn.setToolTip("Επισύναψη αρχείου")
        self.insurance_attach_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: rgba(94, 129, 172, 0.1);
            }
            QPushButton:pressed {
                background-color: rgba(94, 129, 172, 0.2);
            }
        """)
        insurance_layout.addWidget(self.insurance_attach_btn)
        
        self.insurance_remove_btn = QPushButton()
        self.insurance_remove_btn.setIcon(icon_manager.get_icon("delete"))
        self.insurance_remove_btn.setIconSize(QSize(16, 16))
        self.insurance_remove_btn.clicked.connect(lambda: self.remove_document('insurance'))
        self.insurance_remove_btn.setEnabled(False)
        self.insurance_remove_btn.setFixedSize(32, 32)
        self.insurance_remove_btn.setToolTip("Αφαίρεση αρχείου")
        self.insurance_remove_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: rgba(191, 97, 106, 0.1);
            }
            QPushButton:pressed {
                background-color: rgba(191, 97, 106, 0.2);
            }
            QPushButton:disabled {
                opacity: 0.5;
            }
        """)
        insurance_layout.addWidget(self.insurance_remove_btn)
        
        grid.addLayout(insurance_layout, 1, 4, 1, 2)
        
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(3, 1)
        grid.setColumnStretch(5, 1)
        
        layout.addLayout(grid)
        return section
    
    def create_kteo_section(self):
        """KTEO"""
        section = QWidget()
        section.setObjectName("borderedSection")
        section.setStyleSheet("QWidget#borderedSection { background-color: transparent; border: 1px solid #E5E9F0; border-radius: 8px; }")
        
        layout = QVBoxLayout(section)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 20, 30, 20)
        
        self.kteo_header = self.create_section_header("clipboard", "Πληροφορίες ΚΤΕΟ")
        layout.addWidget(self.kteo_header)
        
        grid = QGridLayout()
        grid.setHorizontalSpacing(20)
        grid.setVerticalSpacing(12)
        label_width = 100
        
        # ROW 1 - Dates
        self.kteo_from_label = QLabel("Από:")
        self.kteo_from_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.kteo_from_label.setFixedWidth(label_width)
        grid.addWidget(self.kteo_from_label, 0, 0)
        self.kteo_from_field = QDateEdit()
        self.kteo_from_field.setDate(QDate.currentDate())
        self.kteo_from_field.setCalendarPopup(True)
        grid.addWidget(self.kteo_from_field, 0, 1)
        
        self.kteo_to_label = QLabel("Έως:")
        self.kteo_to_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.kteo_to_label.setFixedWidth(label_width)
        grid.addWidget(self.kteo_to_label, 0, 2)
        self.kteo_to_field = QDateEdit()
        self.kteo_to_field.setDate(QDate.currentDate().addYears(1))
        self.kteo_to_field.setCalendarPopup(True)
        grid.addWidget(self.kteo_to_field, 0, 3)
        
        self.kteo_next_label = QLabel("Επόμενο:")
        self.kteo_next_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.kteo_next_label.setFixedWidth(label_width)
        grid.addWidget(self.kteo_next_label, 0, 4)
        self.kteo_next_field = QDateEdit()
        self.kteo_next_field.setDate(QDate.currentDate().addYears(1))
        self.kteo_next_field.setCalendarPopup(True)
        grid.addWidget(self.kteo_next_field, 0, 5)
        
        # ROW 2 - File
        kteo_layout = QHBoxLayout()
        kteo_layout.setSpacing(8)
        
        kteo_title = QLabel("ΚΤΕΟ:")
        kteo_title.setStyleSheet("color: #4C566A; font-size: 12px; font-weight: 500; border: none;")
        kteo_layout.addWidget(kteo_title)
        
        self.kteo_label = QLabel("Δεν έχει επισυναφθεί αρχείο")
        self.kteo_label.setObjectName("fileLabel")
        self.kteo_label.setStyleSheet("color: #95a5a6; font-style: italic; font-size: 11px; border: none;")
        kteo_layout.addWidget(self.kteo_label, 1)
        
        self.kteo_attach_btn = QPushButton()
        self.kteo_attach_btn.setIcon(icon_manager.get_icon("attachment"))
        self.kteo_attach_btn.setIconSize(QSize(16, 16))
        self.kteo_attach_btn.clicked.connect(lambda: self.upload_document('kteo'))
        self.kteo_attach_btn.setFixedSize(32, 32)
        self.kteo_attach_btn.setToolTip("Επισύναψη αρχείου")
        self.kteo_attach_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: rgba(94, 129, 172, 0.1);
            }
            QPushButton:pressed {
                background-color: rgba(94, 129, 172, 0.2);
            }
        """)
        kteo_layout.addWidget(self.kteo_attach_btn)
        
        self.kteo_remove_btn = QPushButton()
        self.kteo_remove_btn.setIcon(icon_manager.get_icon("delete"))
        self.kteo_remove_btn.setIconSize(QSize(16, 16))
        self.kteo_remove_btn.clicked.connect(lambda: self.remove_document('kteo'))
        self.kteo_remove_btn.setEnabled(False)
        self.kteo_remove_btn.setFixedSize(32, 32)
        self.kteo_remove_btn.setToolTip("Αφαίρεση αρχείου")
        self.kteo_remove_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: rgba(191, 97, 106, 0.1);
            }
            QPushButton:pressed {
                background-color: rgba(191, 97, 106, 0.2);
            }
            QPushButton:disabled {
                opacity: 0.5;
            }
        """)
        kteo_layout.addWidget(self.kteo_remove_btn)
        
        grid.addLayout(kteo_layout, 1, 4, 1, 2)
        
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(3, 1)
        grid.setColumnStretch(5, 1)
        
        layout.addLayout(grid)
        return section
    
    def create_kek_section(self):
        """KEK"""
        section = QWidget()
        section.setObjectName("borderedSection")
        section.setStyleSheet("QWidget#borderedSection { background-color: transparent; border: 1px solid #E5E9F0; border-radius: 8px; }")
        
        layout = QVBoxLayout(section)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 20, 30, 20)
        
        self.kek_header = self.create_section_header("leaf", "Κάρτα Ελέγχου Καυσαερίων (ΚΕΚ)")
        layout.addWidget(self.kek_header)
        
        grid = QGridLayout()
        grid.setHorizontalSpacing(20)
        grid.setVerticalSpacing(12)
        label_width = 100
        
        # ROW 1 - Dates
        self.kek_from_label = QLabel("Από:")
        self.kek_from_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.kek_from_label.setFixedWidth(label_width)
        grid.addWidget(self.kek_from_label, 0, 0)
        self.kek_from_field = QDateEdit()
        self.kek_from_field.setDate(QDate.currentDate())
        self.kek_from_field.setCalendarPopup(True)
        grid.addWidget(self.kek_from_field, 0, 1)
        
        self.kek_to_label = QLabel("Έως:")
        self.kek_to_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.kek_to_label.setFixedWidth(label_width)
        grid.addWidget(self.kek_to_label, 0, 2)
        self.kek_to_field = QDateEdit()
        self.kek_to_field.setDate(QDate.currentDate().addYears(1))
        self.kek_to_field.setCalendarPopup(True)
        grid.addWidget(self.kek_to_field, 0, 3)
        
        self.kek_next_label = QLabel("Επόμενο:")
        self.kek_next_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.kek_next_label.setFixedWidth(label_width)
        grid.addWidget(self.kek_next_label, 0, 4)
        self.kek_next_field = QDateEdit()
        self.kek_next_field.setDate(QDate.currentDate().addYears(1))
        self.kek_next_field.setCalendarPopup(True)
        grid.addWidget(self.kek_next_field, 0, 5)
        
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(3, 1)
        grid.setColumnStretch(5, 1)
        
        layout.addLayout(grid)
        return section
    
    def create_notes_section(self):
        """Σημειώσεις"""
        section = QWidget()
        section.setObjectName("borderedSection")
        section.setStyleSheet("QWidget#borderedSection { background-color: transparent; border: 1px solid #E5E9F0; border-radius: 8px; }")
        
        layout = QVBoxLayout(section)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 20, 30, 20)
        
        self.notes_header = self.create_section_header("note", "Σημειώσεις")
        layout.addWidget(self.notes_header)
        
        self.notes_field = QTextEdit()
        self.notes_field.setMaximumHeight(100)
        self.notes_field.setPlaceholderText("Προαιρετικές σημειώσεις για το όχημα...")
        layout.addWidget(self.notes_field)
        
        return section
    
    def create_bottom_buttons(self):
        """Bottom buttons"""
        layout = QHBoxLayout()
        layout.setContentsMargins(25, 15, 25, 15)
        layout.setSpacing(10)
        layout.addStretch()
        
        self.cancel_btn = QPushButton("Ακύρωση")
        self.cancel_btn.clicked.connect(self.reject)
        self.cancel_btn.setFixedSize(120, 40)
        self.cancel_btn.setStyleSheet("QPushButton { background-color: #E5E9F0; color: #2E3440; border: none; border-radius: 6px; font-weight: 600; font-size: 13px; } QPushButton:hover { background-color: #D8DEE9; }")
        layout.addWidget(self.cancel_btn)
        
        self.save_btn = QPushButton("Δημιουργία")
        self.save_btn.clicked.connect(self.save_vehicle)
        self.save_btn.setFixedSize(120, 40)
        self.save_btn.setStyleSheet("QPushButton { background-color: #5E81AC; color: white; border: none; border-radius: 6px; font-weight: 600; font-size: 13px; } QPushButton:hover { background-color: #81A1C1; }")
        layout.addWidget(self.save_btn)
        
        return layout

    def apply_theme(self, theme="light"):
        """Apply theme to dialog with icon support"""
        # Get icon paths
        chevron_down = icon_manager.get_icon_path_for_css("chevron-down")
        chevron_up = icon_manager.get_icon_path_for_css("chevron-up")
        calendar = icon_manager.get_icon_path_for_css("calendar")
        
        if theme == "dark":
            # DARK THEME
            self.setStyleSheet(f"""
                QDialog {{
                    background-color: #2E3440;
                }}
                QWidget#mainContainer {{
                    background-color: #3B4252;
                    border: 1px solid #4C566A;
                    border-radius: 12px;
                }}
                QWidget#borderedSection {{
                    background-color: transparent;
                    border: 1px solid #4C566A;
                    border-radius: 8px;
                }}
                QLabel {{
                    color: #ECEFF4;
                    font-size: 12px;
                    font-weight: 500;
                    background: transparent;
                    border: none;
                }}
                QLabel#fileLabel {{
                    color: #D8DEE9;
                    font-style: italic;
                    font-size: 11px;
                }}
                QLineEdit, QSpinBox, QComboBox, QDateEdit, QTextEdit {{
                    border: 1px solid #4C566A;
                    border-radius: 6px;
                    padding: 6px 12px;
                    background-color: #434C5E;
                    color: #ECEFF4;
                    font-size: 13px;
                }}
                QLineEdit:focus, QSpinBox:focus, QComboBox:focus, QDateEdit:focus, QTextEdit:focus {{
                    border: 2px solid #88C0D0;
                    padding: 5px 11px;
                }}
                QLineEdit::placeholder, QTextEdit::placeholder {{
                    color: #616E88;
                }}
                QComboBox::drop-down {{
                    border: none;
                    background: transparent;
                    width: 20px;
                }}
                QComboBox::down-arrow {{
                    image: url({chevron_down});
                    width: 12px;
                    height: 12px;
                }}
                QComboBox QAbstractItemView {{
                    background-color: #434C5E;
                    color: #ECEFF4;
                    border: 1px solid #4C566A;
                    selection-background-color: #5E81AC;
                }}
                QDateEdit::drop-down {{
                    border: none;
                    background: transparent;
                    width: 20px;
                }}
                QDateEdit::down-arrow {{
                    image: url({calendar});
                    width: 12px;
                    height: 12px;
                }}
                QSpinBox::up-button {{
                    background: transparent;
                    border: none;
                }}
                QSpinBox::down-button {{
                    background: transparent;
                    border: none;
                }}
                QSpinBox::up-arrow {{
                    image: url({chevron_up});
                    width: 10px;
                    height: 10px;
                }}
                QSpinBox::down-arrow {{
                    image: url({chevron_down});
                    width: 10px;
                    height: 10px;
                }}
                QCheckBox {{
                    color: #ECEFF4;
                    font-size: 12px;
                    font-weight: 500;
                    spacing: 8px;
                    background: transparent;
                    border: none;
                }}
                QCheckBox::indicator {{
                    width: 16px;
                    height: 16px;
                    border: 2px solid #4C566A;
                    border-radius: 3px;
                    background-color: #434C5E;
                }}
                QCheckBox::indicator:checked {{
                    background-color: #88C0D0;
                    border-color: #88C0D0;
                }}
                QCheckBox::indicator:hover {{
                    border-color: #88C0D0;
                }}
                QPushButton {{
                    background-color: transparent;
                    border: none;
                    border-radius: 4px;
                }}
                QPushButton:hover {{
                    background-color: rgba(136, 192, 208, 0.1);
                }}
                QPushButton:pressed {{
                    background-color: rgba(136, 192, 208, 0.2);
                }}
                QPushButton#saveButton {{
                    background-color: #88C0D0;
                    color: #2E3440;
                    border: none;
                    border-radius: 6px;
                    font-weight: 600;
                    font-size: 13px;
                    padding: 8px 16px;
                }}
                QPushButton#saveButton:hover {{
                    background-color: #8FBCBB;
                }}
                QPushButton#saveButton:pressed {{
                    background-color: #81A1C1;
                }}
                QPushButton#cancelButton {{
                    background-color: #4C566A;
                    color: #ECEFF4;
                    border: 1px solid #5E6875;
                    border-radius: 6px;
                    font-weight: 600;
                    font-size: 13px;
                    padding: 8px 16px;
                }}
                QPushButton#cancelButton:hover {{
                    background-color: #5E6875;
                }}
                QPushButton#cancelButton:pressed {{
                    background-color: #434C5E;
                }}
                QScrollArea {{
                    background-color: transparent;
                    border: none;
                }}
                QScrollBar:vertical {{
                    background-color: #3B4252;
                    width: 8px;
                    margin: 0px;
                    border-radius: 4px;
                }}
                QScrollBar::handle:vertical {{
                    background-color: #4C566A;
                    min-height: 30px;
                    border-radius: 4px;
                }}
                QScrollBar::handle:vertical:hover {{
                    background-color: #5E81AC;
                }}
                QScrollBar::add-line:vertical,
                QScrollBar::sub-line:vertical {{
                    height: 0px;
                }}
                QScrollBar::add-page:vertical,
                QScrollBar::sub-page:vertical {{
                    background: none;
                }}
            """)
        else:
            # LIGHT THEME
            self.setStyleSheet(f"""
                QDialog {{
                    background-color: #F5F7FA;
                }}
                QWidget#mainContainer {{
                    background-color: white;
                    border: 1px solid #E5E9F0;
                    border-radius: 12px;
                }}
                QWidget#borderedSection {{
                    background-color: transparent;
                    border: 1px solid #E5E9F0;
                    border-radius: 8px;
                }}
                QLabel {{
                    color: #4C566A;
                    font-size: 12px;
                    font-weight: 500;
                    background: transparent;
                    border: none;
                }}
                QLabel#fileLabel {{
                    color: #95a5a6;
                    font-style: italic;
                    font-size: 11px;
                }}
                QLineEdit, QSpinBox, QComboBox, QDateEdit, QTextEdit {{
                    border: 1px solid #D8DEE9;
                    border-radius: 6px;
                    padding: 6px 12px;
                    background-color: white;
                    color: #2E3440;
                    font-size: 13px;
                }}
                QLineEdit:focus, QSpinBox:focus, QComboBox:focus, QDateEdit:focus, QTextEdit:focus {{
                    border: 2px solid #5E81AC;
                    padding: 5px 11px;
                }}
                QLineEdit::placeholder, QTextEdit::placeholder {{
                    color: #A0AEC0;
                }}
                QComboBox::drop-down {{
                    border: none;
                    background: transparent;
                    width: 20px;
                }}
                QComboBox::down-arrow {{
                    image: url({chevron_down});
                    width: 12px;
                    height: 12px;
                }}
                QComboBox QAbstractItemView {{
                    background-color: white;
                    color: #2E3440;
                    border: 1px solid #D8DEE9;
                    selection-background-color: #5E81AC;
                    selection-color: white;
                }}
                QDateEdit::drop-down {{
                    border: none;
                    background: transparent;
                    width: 20px;
                }}
                QDateEdit::down-arrow {{
                    image: url({calendar});
                    width: 12px;
                    height: 12px;
                }}
                QSpinBox::up-button {{
                    background: transparent;
                    border: none;
                }}
                QSpinBox::down-button {{
                    background: transparent;
                    border: none;
                }}
                QSpinBox::up-arrow {{
                    image: url({chevron_up});
                    width: 10px;
                    height: 10px;
                }}
                QSpinBox::down-arrow {{
                    image: url({chevron_down});
                    width: 10px;
                    height: 10px;
                }}
                QCheckBox {{
                    color: #4C566A;
                    font-size: 12px;
                    font-weight: 500;
                    spacing: 8px;
                    background: transparent;
                    border: none;
                }}
                QCheckBox::indicator {{
                    width: 16px;
                    height: 16px;
                    border: 2px solid #D8DEE9;
                    border-radius: 3px;
                    background-color: white;
                }}
                QCheckBox::indicator:checked {{
                    background-color: #5E81AC;
                    border-color: #5E81AC;
                }}
                QCheckBox::indicator:hover {{
                    border-color: #5E81AC;
                }}
                QPushButton {{
                    background-color: transparent;
                    border: none;
                    border-radius: 4px;
                }}
                QPushButton:hover {{
                    background-color: rgba(94, 129, 172, 0.1);
                }}
                QPushButton:pressed {{
                    background-color: rgba(94, 129, 172, 0.2);
                }}
                QPushButton#saveButton {{
                    background-color: #5E81AC;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    font-weight: 600;
                    font-size: 13px;
                    padding: 8px 16px;
                }}
                QPushButton#saveButton:hover {{
                    background-color: #81A1C1;
                }}
                QPushButton#saveButton:pressed {{
                    background-color: #4C7AA0;
                }}
                QPushButton#cancelButton {{
                    background-color: #ECEFF4;
                    color: #4C566A;
                    border: 1px solid #D8DEE9;
                    border-radius: 6px;
                    font-weight: 600;
                    font-size: 13px;
                    padding: 8px 16px;
                }}
                QPushButton#cancelButton:hover {{
                    background-color: #E5E9F0;
                }}
                QPushButton#cancelButton:pressed {{
                    background-color: #D8DEE9;
                }}
                QScrollArea {{
                    background-color: transparent;
                    border: none;
                }}
                QScrollBar:vertical {{
                    background-color: #ECEFF4;
                    width: 8px;
                    margin: 0px;
                    border-radius: 4px;
                }}
                QScrollBar::handle:vertical {{
                    background-color: #D8DEE9;
                    min-height: 30px;
                    border-radius: 4px;
                }}
                QScrollBar::handle:vertical:hover {{
                    background-color: #5E81AC;
                }}
                QScrollBar::add-line:vertical,
                QScrollBar::sub-line:vertical {{
                    height: 0px;
                }}
                QScrollBar::add-page:vertical,
                QScrollBar::sub-page:vertical {{
                    background: none;
                }}
            """)
    
    def apply_translations(self):
        """Apply translations"""
        self.setWindowTitle(translator.get("add_vehicle_dialog.title"))
        
        vehicle_title_label = self.vehicle_header.findChild(QLabel, "headerTitle")
        if vehicle_title_label:
            vehicle_title_label.setText(translator.get("add_vehicle_dialog.sections.vehicle_info"))
        
        self.brand_label.setText(translator.get("vehicle.brand"))
        self.model_label.setText(translator.get("add_vehicle_dialog.model"))
        self.license_label.setText(translator.get("add_vehicle_dialog.license_plate"))
        self.vin_label.setText(translator.get("add_vehicle_dialog.vin"))
        self.type_label.setText(translator.get("add_vehicle_dialog.type"))
        self.year_label.setText(translator.get("add_vehicle_dialog.year"))
        self.cc_label.setText(translator.get("add_vehicle_dialog.engine_cc"))
        self.fuel_label.setText(translator.get("add_vehicle_dialog.fuel_type"))
        self.color_label.setText(translator.get("add_vehicle_dialog.color"))
        self.mileage_label.setText(translator.get("add_vehicle_dialog.mileage"))
        
        insurance_title_label = self.insurance_header.findChild(QLabel, "headerTitle")
        if insurance_title_label:
            insurance_title_label.setText(translator.get("add_vehicle_dialog.insurance_info"))
        
        self.ins_from_label.setText(translator.get("add_vehicle_dialog.from"))
        self.ins_to_label.setText(translator.get("add_vehicle_dialog.to"))
        self.ins_next_label.setText(translator.get("add_vehicle_dialog.next"))
        
        kteo_title_label = self.kteo_header.findChild(QLabel, "headerTitle")
        if kteo_title_label:
            kteo_title_label.setText(translator.get("add_vehicle_dialog.kteo_info"))
        
        self.kteo_from_label.setText(translator.get("add_vehicle_dialog.from"))
        self.kteo_to_label.setText(translator.get("add_vehicle_dialog.to"))
        self.kteo_next_label.setText(translator.get("add_vehicle_dialog.next"))
        
        kek_title_label = self.kek_header.findChild(QLabel, "headerTitle")
        if kek_title_label:
            kek_title_label.setText(translator.get("add_vehicle_dialog.kek_info"))
        
        self.kek_from_label.setText(translator.get("add_vehicle_dialog.from"))
        self.kek_to_label.setText(translator.get("add_vehicle_dialog.to"))
        self.kek_next_label.setText(translator.get("add_vehicle_dialog.next"))
        
        notes_title_label = self.notes_header.findChild(QLabel, "headerTitle")
        if notes_title_label:
            notes_title_label.setText(translator.get("add_vehicle_dialog.notes"))
        
        self.cancel_btn.setText(translator.get("common.cancel"))
        self.save_btn.setText(translator.get("common.save"))
    
    def upload_document(self, doc_type):
        """Upload document"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Επιλέξτε αρχείο", "", "All Files (*);;PDF Files (*.pdf);;Image Files (*.png *.jpg *.jpeg)")
        
        if file_path:
            try:
                license_plate = self.license_plate_field.text().strip()
                if not license_plate:
                    QMessageBox.warning(self, "Προσοχή", "Εισάγετε πρώτα τον αριθμό κυκλοφορίας!")
                    return
                
                clean_plate = license_plate.replace("-", "_").replace(" ", "").replace("/", "_").upper()
                
                if doc_type == "licence":
                    prefix = f"{clean_plate}_LICENCE"
                    label = self.licence_label
                    remove_btn = self.licence_remove_btn
                elif doc_type == "insurance":
                    prefix = f"{clean_plate}_INSURANCE"
                    label = self.insurance_label
                    remove_btn = self.insurance_remove_btn
                elif doc_type == "kteo":
                    prefix = f"{clean_plate}_KTEO"
                    label = self.kteo_label
                    remove_btn = self.kteo_remove_btn
                else:
                    return
                
                file_ext = os.path.splitext(file_path)[1]
                files_dir = os.path.join('database', 'files')
                os.makedirs(files_dir, exist_ok=True)
                
                dest_path = os.path.join(files_dir, f"{prefix}{file_ext}")
                
                for ext in ['.pdf', '.jpg', '.jpeg', '.png']:
                    old_file = os.path.join(files_dir, f"{prefix}{ext}")
                    if os.path.exists(old_file):
                        os.remove(old_file)
                
                shutil.copy2(file_path, dest_path)
                
                label.setText(f"✓ {os.path.basename(dest_path)}")
                label.setStyleSheet("color: #27ae60; font-weight: 600; font-size: 12px; border: none;")
                remove_btn.setEnabled(True)
                
            except Exception as e:
                QMessageBox.critical(self, "Σφάλμα", f"Σφάλμα: {str(e)}")
    
    def remove_document(self, doc_type):
        """Remove document"""
        if doc_type == "licence":
            label = self.licence_label
            remove_btn = self.licence_remove_btn
        elif doc_type == "insurance":
            label = self.insurance_label
            remove_btn = self.insurance_remove_btn
        elif doc_type == "kteo":
            label = self.kteo_label
            remove_btn = self.kteo_remove_btn
        else:
            return
        
        label.setText("Δεν έχει επισυναφθεί αρχείο")
        label.setStyleSheet("color: #95a5a6; font-style: italic; font-size: 12px; border: none;")
        remove_btn.setEnabled(False)
        
    def save_vehicle(self):
        """Save vehicle to database with validation"""
        license_plate = self.license_plate_field.text().strip()
        brand = self.brand_field.currentText().strip()
        model = self.model_field.text().strip()
        
        if not license_plate:
            QMessageBox.warning(self, "Σφάλμα", "Παρακαλώ εισάγετε αριθμό κυκλοφορίας!")
            self.license_plate_field.setFocus()
            return
        
        if not brand:
            QMessageBox.warning(self, "Σφάλμα", "Παρακαλώ εισάγετε μάρκα!")
            self.brand_field.setFocus()
            return
        
        if not model:
            QMessageBox.warning(self, "Σφάλμα", "Παρακαλώ εισάγετε μοντέλο!")
            self.model_field.setFocus()
            return
        
        vin = self.vin_field.text().strip()
        if vin and len(vin) != 17:
            QMessageBox.warning(self, "Σφάλμα", "Το VIN πρέπει να είναι 17 χαρακτήρες!")
            self.vin_field.setFocus()
            return
        
        current_year = QDate.currentDate().year()
        if self.year_field.value() > current_year + 1:
            QMessageBox.warning(self, "Σφάλμα", f"Το έτος δεν μπορεί να είναι > {current_year + 1}!")
            self.year_field.setFocus()
            return
        
        vehicle_data = {
            'license_plate': license_plate.upper(),
            'brand': brand,
            'model': model,
            'year': self.year_field.value(),
            'vehicle_type': self.type_field.currentText(),
            'vin_number': vin.upper() if vin else '',
            'mileage': self.mileage_field.value(),
            'engine_cc': self.engine_cc_field.value(),
            'fuel_type': self.fuel_type_field.currentText(),
            'color': self.color_field.currentText(),
            'notes': self.notes_field.toPlainText().strip(),
            'insurance_expiry': self.insurance_next_field.date().toString('yyyy-MM-dd'),
            'kteo_next': self.kteo_next_field.date().toString('yyyy-MM-dd'),
            'kek_renewal': self.kek_next_field.date().toString('yyyy-MM-dd'),
            'status': 'Active',
            'gps_enabled': 1 if self.gps_checkbox.isChecked() else 0
        }
        
        try:
            self.db.add_vehicle(vehicle_data)
            QMessageBox.information(self, "Επιτυχία", "Το όχημα προστέθηκε επιτυχώς!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Σφάλμα", f"Σφάλμα αποθήκευσης:\n{str(e)}")