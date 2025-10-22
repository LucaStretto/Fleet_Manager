"""Settings Dialog - Language & Theme Selection"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QComboBox, QPushButton, QWidget
)
from PyQt6.QtCore import Qt
import json
import os

# Global variables for current settings
current_language = "el"  # Default: Greek
current_theme = "light"  # Default: Light theme

def load_preferences():
    """Load saved preferences from file"""
    global current_language, current_theme
    
    try:
        if os.path.exists("preferences.json"):
            with open("preferences.json", "r", encoding="utf-8") as f:
                prefs = json.load(f)
                current_language = prefs.get("language", "el")
                current_theme = prefs.get("theme", "light")
                
                # Apply theme
                from utils.theme_manager import theme
                theme.set_theme(current_theme)
    except Exception as e:
        print(f"Error loading preferences: {e}")

def save_preferences(language, theme_name):
    """Save preferences to file"""
    global current_language, current_theme
    
    try:
        prefs = {
            "language": language,
            "theme": theme_name
        }
        
        with open("preferences.json", "w", encoding="utf-8") as f:
            json.dump(prefs, f, indent=4)
        
        # Update globals
        current_language = language
        current_theme = theme_name
        
        # Apply theme
        from utils.theme_manager import theme
        theme.set_theme(theme_name)
        
        print(f"✅ Preferences saved: {language}, {theme_name}")
    except Exception as e:
        print(f"❌ Error saving preferences: {e}")

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setModal(True)
        self.setFixedSize(500, 300)
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title = QLabel("Settings")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2E3440;")
        layout.addWidget(title)
        
        # Language selection
        lang_container = QWidget()
        lang_layout = QHBoxLayout(lang_container)
        lang_layout.setContentsMargins(0, 0, 0, 0)
        
        lang_label = QLabel("Language:")
        lang_label.setStyleSheet("font-size: 14px; color: #4C566A;")
        lang_label.setFixedWidth(120)
        
        self.language_combo = QComboBox()
        self.language_combo.addItem("Ελληνικά", "el")
        self.language_combo.addItem("English", "en")
        self.language_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #D8DEE9;
                border-radius: 6px;
                background: white;
                font-size: 14px;
            }
            QComboBox:hover {
                border: 1px solid #5E81AC;
            }
        """)
        
        # Set current language
        index = self.language_combo.findData(current_language)
        if index >= 0:
            self.language_combo.setCurrentIndex(index)
        
        lang_layout.addWidget(lang_label)
        lang_layout.addWidget(self.language_combo)
        layout.addWidget(lang_container)
        
        # Theme selection
        theme_container = QWidget()
        theme_layout = QHBoxLayout(theme_container)
        theme_layout.setContentsMargins(0, 0, 0, 0)
        
        theme_label = QLabel("Theme:")
        theme_label.setStyleSheet("font-size: 14px; color: #4C566A;")
        theme_label.setFixedWidth(120)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItem("Light", "light")
        self.theme_combo.addItem("Dark", "dark")
        self.theme_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #D8DEE9;
                border-radius: 6px;
                background: white;
                font-size: 14px;
            }
            QComboBox:hover {
                border: 1px solid #5E81AC;
            }
        """)
        
        # Set current theme
        index = self.theme_combo.findData(current_theme)
        if index >= 0:
            self.theme_combo.setCurrentIndex(index)
        
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_combo)
        layout.addWidget(theme_container)
        
        layout.addStretch()
        
        # Buttons
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(10)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedHeight(40)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #ECEFF4;
                border: none;
                border-radius: 6px;
                padding: 10px 24px;
                font-size: 14px;
                font-weight: 600;
                color: #4C566A;
            }
            QPushButton:hover {
                background-color: #D8DEE9;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        
        save_btn = QPushButton("Save")
        save_btn.setFixedHeight(40)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #5E81AC;
                border: none;
                border-radius: 6px;
                padding: 10px 24px;
                font-size: 14px;
                font-weight: 600;
                color: white;
            }
            QPushButton:hover {
                background-color: #81A1C1;
            }
        """)
        save_btn.clicked.connect(self.save_settings)
        
        button_layout.addStretch()
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(save_btn)
        
        layout.addWidget(button_container)
    
    def save_settings(self):
        """Save selected settings"""
        language = self.language_combo.currentData()
        theme = self.theme_combo.currentData()
        
        save_preferences(language, theme)
        
        self.accept()
