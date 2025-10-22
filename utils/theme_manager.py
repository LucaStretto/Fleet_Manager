"""Theme Manager with Icon Support"""

class Theme:
    def __init__(self):
        self.current_theme = "light"
        self.themes = {
            "light": {
                "primary": "#5E81AC",
                "secondary": "#81A1C1",
                "background": "#ECEFF4",
                "surface": "#FFFFFF",
                "text": "#2E3440",
                "text_secondary": "#4C566A",
                "border": "#D8DEE9",
                "hover": "#E5E9F0",
                "selected": "#5E81AC",
                "selected_text": "#FFFFFF"
            },
            "dark": {
                "primary": "#88C0D0",
                "secondary": "#81A1C1",
                "background": "#2E3440",
                "surface": "#3B4252",
                "text": "#ECEFF4",
                "text_secondary": "#D8DEE9",
                "border": "#4C566A",
                "hover": "#434C5E",
                "selected": "#88C0D0",
                "selected_text": "#2E3440"
            }
        }
    
    def set_theme(self, theme_name):
        """Set current theme"""
        if theme_name in self.themes:
            self.current_theme = theme_name
            
            # Update icon manager
            from utils.icon_manager import icon_manager
            icon_manager.set_theme(theme_name)
    
    def get(self, key):
        """Get theme color value"""
        return self.themes[self.current_theme].get(key, "#000000")
    
    def get_stylesheet(self):
        """Generate theme stylesheet"""
        t = self.themes[self.current_theme]
        
        return f"""
        /* Theme Colors */
        QMainWindow {{
            background-color: {t['background']};
        }}
        
        QWidget#navigation_menu {{
            background-color: {t['surface']};
        }}
        
        QWidget#content_area {{
            background-color: {t['surface']};
        }}
        
        QPushButton#nav_button {{
            color: {t['text']};
            background-color: transparent;
        }}
        
        QPushButton#nav_button:hover {{
            background-color: {t['hover']};
        }}
        
        QPushButton#nav_button:checked {{
            background-color: {t['selected']};
            color: {t['selected_text']};
        }}
        
        QLabel {{
            color: {t['text']};
        }}
        
        /* Table Text Colors */
        QTableWidget::item {{
            color: {t['text']};
        }}
        
        QTableWidget::item:selected {{
            background-color: {t['selected']};
            color: {t['selected_text']};
        }}
        
        QTableWidget {{
            background-color: {t['surface']};
            border: 1px solid {t['border']};
        }}
        
        QTableWidget QTableCornerButton::section {{
            background-color: {t['surface']};
            border: none;
        }}
        
        QHeaderView::section {{
            color: {t['text_secondary']};
            background-color: {t['surface']};
        }}

        
        /* Search Box */
        QLineEdit {{
            background-color: {t['surface']};
            color: {t['text']};
            border: 1px solid {t['border']};
        }}
        
        QLineEdit:focus {{
            border: 1px solid {t['primary']};
        }}
        """


theme = Theme()
