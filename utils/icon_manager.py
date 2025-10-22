"""Icon Manager - Runtime Icon Colorization"""
import os
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor
from PyQt6.QtCore import QSize, Qt

class IconManager:
    """Manages icon loading with runtime colorization"""
    
    def __init__(self):
        self.current_theme = "light"
        self.icon_size = QSize(24, 24)
        self.base_path = "resources/icons"
        
        # Theme-based color mapping
        self.colors = {
            "light": {
                "normal": "#4C566A",  # Dark gray για normal state
                "selected": "#FFFFFF"  # White για selected state
            },
            "dark": {
                "normal": "#FFFFFF",  # Light gray για normal state
                "selected": "#ECEFF4"  # White για selected state
            }
        }
    
    def set_theme(self, theme):
        """Update current theme"""
        self.current_theme = theme
    
    def get_base_icon_path(self, icon_name):
        """Get path to base icon (single black/dark icon)"""
        return os.path.join(self.base_path, f"{icon_name}.png")
    
    def get_icon_path_for_css(self, icon_name):
        """Get icon path formatted for CSS url() - ✅ ΝΕΑ ΜΕΘΟΔΟΣ"""
        path = self.get_base_icon_path(icon_name)
        # Make absolute and convert backslashes to forward slashes for CSS
        abs_path = os.path.abspath(path).replace('\\', '/')
        return abs_path
    
    def colorize_pixmap(self, pixmap, color_hex):
        """Colorize a pixmap to a specific color"""
        if pixmap.isNull():
            return pixmap
        
        # Create colored version
        colored = QPixmap(pixmap.size())
        colored.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(colored)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Source)
        painter.drawPixmap(0, 0, pixmap)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
        painter.fillRect(colored.rect(), QColor(color_hex))
        painter.end()
        
        return colored
    
    def get_icon(self, icon_name):
        """Load icon with theme-aware colorization for both states"""
        base_path = self.get_base_icon_path(icon_name)
        
        if not os.path.exists(base_path):
            return QIcon()
        
        # Load base pixmap
        base_pixmap = QPixmap(base_path)
        
        # Create QIcon with different states
        icon = QIcon()
        
        # Normal state - theme dependent color
        if self.current_theme == "light":
            normal_color = self.colors["light"]["normal"]
        else:
            normal_color = self.colors["dark"]["normal"]
        
        normal_pixmap = self.colorize_pixmap(base_pixmap, normal_color)
        icon.addPixmap(normal_pixmap, QIcon.Mode.Normal, QIcon.State.Off)
        
        # Selected state - always white
        if self.current_theme == "light":
            selected_color = self.colors["light"]["selected"]
        else:
            selected_color = self.colors["dark"]["selected"]
        
        selected_pixmap = self.colorize_pixmap(base_pixmap, selected_color)
        icon.addPixmap(selected_pixmap, QIcon.Mode.Normal, QIcon.State.On)
        icon.addPixmap(selected_pixmap, QIcon.Mode.Active, QIcon.State.On)
        
        return icon
    
    def get_pixmap(self, icon_name, size=None, color=None):
        """Load icon as QPixmap with optional size and color"""
        base_path = self.get_base_icon_path(icon_name)
        
        if not os.path.exists(base_path):
            return QPixmap()
        
        pixmap = QPixmap(base_path)
        
        # Colorize if color provided
        if color:
            pixmap = self.colorize_pixmap(pixmap, color)
        
        # Resize if size provided
        if size:
            pixmap = pixmap.scaled(size, Qt.AspectRatioMode.KeepAspectRatio,
                                  Qt.TransformationMode.SmoothTransformation)
        
        return pixmap

# Global icon manager instance
icon_manager = IconManager()
