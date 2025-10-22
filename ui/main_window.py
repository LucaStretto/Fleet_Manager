import sys
from PyQt6.QtWidgets import (
    QMainWindow, 
    QStackedWidget, 
    QWidget, 
    QHBoxLayout, 
    QVBoxLayout, 
    QPushButton, 
    QLabel,
    QSpacerItem,
    QSizePolicy
)
from PyQt6.QtGui import QIcon, QPixmap, QPainter
from PyQt6.QtCore import QSize, Qt

from ui.views.vehicles_view import VehiclesView
from ui.settings_dialog import SettingsDialog, load_preferences
from utils.theme_manager import theme
from utils.icon_manager import icon_manager

# --- GLOBAL STYLESHEET ---
GLOBAL_STYLE = """
/* Main Window */
QMainWindow {
    background-color: #ECEFF4;
}

/* Header Area */
QWidget#header_widget {
    background-color: #FFFFFF;
    border-bottom: 1px solid #D8DEE9;
}

QLabel#header_logo_text {
    font-size: 10px;
    font-weight: 600;
    color: #4C566A;
    letter-spacing: 1.5px;
    line-height: 14px;
}

QLabel#header_user_label {
    color: #2E3440;
    font-size: 14px;
    font-weight: 500;
    padding-right: 10px;
}

QPushButton#header_icon_button {
    background-color: #ECEFF4;
    border: none;
    border-radius: 20px;
    padding: 8px;
    min-width: 36px;
    min-height: 36px;
    font-size: 16px;
}

QPushButton#header_icon_button:hover {
    background-color: #D8DEE9;
}

/* Body Container (gray background) */
QWidget#body_container {
    background-color: #ECEFF4;
}

/* Navigation Sidebar - WHITE CONTAINER */
QWidget#navigation_menu {
    background-color: #FFFFFF;
    border-radius: 12px;
}

/* Navigation Buttons */
QPushButton#nav_button {
    background-color: transparent;
    border: none;
    color: #4C566A;
    text-align: left;
    padding: 12px 20px;
    font-size: 14px;
    font-weight: 500;
    border-radius: 10px;
    margin: 5px 10px;
}

QPushButton#nav_button:hover {
    background-color: #ECEFF4;
}

QPushButton#nav_button:checked {
    background-color: #5E81AC;
    color: #FFFFFF;
}

/* Content Area - WHITE CONTAINER */
QWidget#content_area {
    background-color: #FFFFFF;
    border-radius: 12px;
}

/* Search & Button */
QLineEdit#search_box {
    background-color: #FFFFFF;
    border: 1px solid #D8DEE9;
    border-radius: 8px;
    padding: 10px 15px 10px 40px;
    font-size: 14px;
}

QLineEdit#search_box:focus {
    border: 1px solid #5E81AC;
}

QPushButton#add_button {
    background-color: #5E81AC;
    color: #FFFFFF;
    font-size: 14px;
    font-weight: 600;
    border: none;
    border-radius: 8px;
    padding: 10px 24px;
}

QPushButton#add_button:hover {
    background-color: #81A1C1;
}

/* Table */
QTableWidget {
    background-color: #FFFFFF;
    border: 1px solid #E5E9F0;
    gridline-color: transparent;
}
QTableWidget::item {
    padding: 14px;
    border-bottom: 1px solid #ECEFF4;
    color: #2E3440;
    border-left: none;
    border-right: none;
}
QTableWidget::item:selected {
    background-color: #5E81AC;
    color: #FFFFFF;
}
QHeaderView::section {
    background-color: #FFFFFF;
    padding: 12px 8px;
    border: none;
    border-bottom: 1px solid #E5E9F0;
    font-size: 10px;
    font-weight: 600;
    color: #4C566A;
    text-transform: uppercase;
    min-height: 50px;
}


"""

class MainWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db
        
        # Load saved preferences
        load_preferences()
        
        self.setWindowTitle("Vehicle Fleet Manager")
        self.setGeometry(100, 100, 1400, 900)
        
        # Initialize UI first (creates nav_items)
        self.init_ui()
        
        # Then apply theme (needs nav_items to exist)
        self.apply_theme()


    def init_ui(self):
        """Initialize the main UI."""
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        
        main_layout = QVBoxLayout(self.main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create header
        self.create_header()
        main_layout.addWidget(self.header_widget)
        
        # Create body with gray background
        body_widget = QWidget()
        body_widget.setObjectName("body_container")
        body_layout = QHBoxLayout(body_widget)
        body_layout.setContentsMargins(20, 20, 20, 20)
        body_layout.setSpacing(20)
        
        # Sidebar container (white)
        self.create_navigation_menu()
        body_layout.addWidget(self.nav_container)
        
        # Content container (white)
        self.create_content_area()
        body_layout.addWidget(self.content_wrapper)
        
        main_layout.addWidget(body_widget)
        
        # Set default view
        self.switch_view("Vehicles")
        
        # Apply initial language
        self.refresh_ui_text()

    def create_header(self):
        """Create the top header bar."""
        self.header_widget = QWidget()
        self.header_widget.setObjectName("header_widget")
        self.header_widget.setFixedHeight(80)
        
        header_layout = QHBoxLayout(self.header_widget)
        header_layout.setContentsMargins(25, 0, 25, 0)
        
        # Logo + Title container
        logo_container = QWidget()
        logo_layout = QHBoxLayout(logo_container)
        logo_layout.setContentsMargins(0, 0, 0, 0)
        logo_layout.setSpacing(15)
        
        # Logo (circular placeholder)
        self.logo_label = QLabel()
        self.logo_label.setFixedSize(50, 50)
        self.logo_label.setStyleSheet("""
            background-color: #5E81AC;
            border-radius: 25px;
        """)
        logo_layout.addWidget(self.logo_label)
        
        # Title
        self.title_label = QLabel("VEHICLE\nFLEET MANAGER")
        self.title_label.setObjectName("header_logo_text")
        logo_layout.addWidget(self.title_label)
        
        header_layout.addWidget(logo_container)
        header_layout.addStretch()
        
        # User label
        self.user_label = QLabel("User")
        self.user_label.setObjectName("header_user_label")
        header_layout.addWidget(self.user_label)
        
        # User icon button
        user_btn = QPushButton()
        user_btn.setObjectName("header_icon_button")
        user_btn.setIcon(icon_manager.get_icon("user"))
        user_btn.setIconSize(QSize(20, 20))
        header_layout.addWidget(user_btn)
        
        # Settings icon button - CONNECTED TO DIALOG
        settings_btn = QPushButton()
        settings_btn.setObjectName("header_icon_button")
        settings_btn.setIcon(icon_manager.get_icon("settings"))
        settings_btn.setIconSize(QSize(20, 20))
        settings_btn.clicked.connect(self.open_settings)
        header_layout.addWidget(settings_btn)

    def create_navigation_menu(self):
        """Create the left sidebar navigation with PNG icons."""
        
        self.nav_container = QWidget()
        self.nav_container.setObjectName("navigation_menu")
        self.nav_container.setFixedWidth(270)
        
        nav_layout = QVBoxLayout(self.nav_container)
        nav_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        nav_layout.setContentsMargins(10, 30, 10, 20)
        nav_layout.setSpacing(5)
        
        # Navigation items with PNG icons
        self.nav_buttons = {}
        self.nav_items = [
            ("Vehicles", "vehicles"),
            ("Service", "service"),
            ("Reminders", "reminders"),
            ("Reports", "reports"),
           
           ]
        
        for name, icon_name in self.nav_items:
            button = QPushButton()
            button.setObjectName("nav_button")
            button.setCheckable(True)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setIcon(icon_manager.get_icon(icon_name))
            button.setIconSize(QSize(20, 20))
            
            # Settings button opens dialog, others switch views
            if name == "Settings":
                button.clicked.connect(self.open_settings)
            else:
                button.clicked.connect(lambda _, n=name: self.switch_view(n))
            
            self.nav_buttons[name] = button
            nav_layout.addWidget(button)
        
        nav_layout.addStretch()
        
        # Apply initial text
        self.update_navigation_text()

    def update_navigation_text(self):
        """Update navigation button text with current language"""
        try:
            from ui.settings_dialog import current_language
        except ImportError:
            current_language = "el"
        
        if current_language == "en":
            translations = {
                "Vehicles": "Vehicles",
                "Service": "Service",
                "Reminders": "Reminders",
                "Reports": "Reports",
                           }
        else:
            translations = {
                "Vehicles": "Οχήματα",
                "Service": "Συντήρηση",
                "Reminders": "Υπενθυμίσεις",
                "Reports": "Αναφορές",
                        }
        
        for name, button in self.nav_buttons.items():
            button.setText(translations[name])

    def create_content_area(self):
        """Create the main content stack."""
        # Content wrapper (white container)
        self.content_wrapper = QWidget()
        self.content_wrapper.setObjectName("content_area")
        
        wrapper_layout = QVBoxLayout(self.content_wrapper)
        wrapper_layout.setContentsMargins(0, 0, 0, 0)
        wrapper_layout.setSpacing(0)
        
        self.view_stack = QStackedWidget()
        wrapper_layout.addWidget(self.view_stack)
        
        self.create_views()

    def create_views(self):
        """Create all views."""
        self.vehicles_view = VehiclesView(self.db)
        self.view_stack.addWidget(self.vehicles_view)
        
        # Placeholder views
        for name in ["Service", "Reminders", "Reports", "Settings"]:
            placeholder = QLabel(f"{name} View (Under Construction)")
            placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            placeholder.setStyleSheet("font-size: 20px; color: #4C566A;")
            self.view_stack.addWidget(placeholder)

    def switch_view(self, view_name):
        """Switch between views."""
        view_map = {
            "Vehicles": 0,
            "Service": 1,
            "Reminders": 2,
            "Reports": 3,
            
        }
        
        if view_name in view_map:
            self.view_stack.setCurrentIndex(view_map[view_name])
            
            # Update button states
            for name, button in self.nav_buttons.items():
                button.setChecked(name == view_name)
            
            # Refresh data if needed
            if view_name == "Vehicles" and hasattr(self.vehicles_view, 'refresh_data'):
                self.vehicles_view.refresh_data()
    
    def open_settings(self):
        """Open Settings Dialog"""
        dialog = SettingsDialog(self)
        result = dialog.exec()
        
        if result:  # Settings were saved
            # Apply new theme
            self.apply_theme()
            # Refresh translations
            self.refresh_ui_text()
    
    def apply_theme(self):
        """Apply current theme (GLOBAL_STYLE + theme colors + reload icons)"""
        from utils.icon_manager import icon_manager
        
        # Get theme stylesheet
        theme_style = theme.get_stylesheet()
        
        # Combine GLOBAL_STYLE + theme colors
        combined_style = GLOBAL_STYLE + "\n" + theme_style
        self.setStyleSheet(combined_style)
        
        # Reload all navigation icons (only if they exist)
        if hasattr(self, 'nav_items') and hasattr(self, 'nav_buttons'):
            for name, icon_name in self.nav_items:
                if name in self.nav_buttons:
                    self.nav_buttons[name].setIcon(icon_manager.get_icon(icon_name))

    
    def refresh_ui_text(self):
        """Refresh all UI text with current language"""
        try:
            from ui.settings_dialog import current_language
        except ImportError:
            current_language = "el"  # Default fallback
        
        if current_language == "en":
            # English
            self.setWindowTitle("Vehicle Fleet Manager")
            self.title_label.setText("VEHICLE\nFLEET MANAGER")
            self.user_label.setText("User")
        else:
            # Greek
            self.setWindowTitle(translator.get("app.title"))
            self.title_label.setText("ΔΙΑΧΕΙΡΙΣΗ\nΣΤΟΛΟΥ")
            self.user_label.setText("Χρήστης")
        
        # Update navigation buttons
        self.update_navigation_text()
