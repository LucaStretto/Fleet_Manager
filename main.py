"""
Fleet Manager - Main Entry Point
"""
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from database.db_manager import DatabaseManager
from ui.main_window import MainWindow

def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    
    # High DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    # Initialize database
    db = DatabaseManager()
    
    # Create main window
    window = MainWindow(db)
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
