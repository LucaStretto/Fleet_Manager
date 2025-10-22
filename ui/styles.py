"""
UI Styles - Light Professional Theme
Exact match to design specifications
"""

# Color Palette
COLORS = {
    'bg_primary': '#FFFFFF',
    'bg_secondary': '#F5F7FA',
    'bg_tertiary': '#FFFFFF',
    'card_bg': '#FFFFFF',
    
    'primary': '#4A90E2',
    'primary_hover': '#357ABD',
    'success': '#27AE60',
    'warning': '#F39C12',
    'danger': '#E74C3C',
    'info': '#3498DB',
    
    'text_primary': '#2C3E50',
    'text_secondary': '#7F8C8D',
    'text_tertiary': '#95A5A6',
    
    'border': '#E1E8ED',
    'border_light': '#ECF0F1',
    
    'sidebar_bg': '#F5F7FA',
    'sidebar_active': '#4A90E2',
    'sidebar_hover': '#E8EEF4',
    'sidebar_text': '#5A6C7D',
}

# Global Stylesheet
GLOBAL_STYLE = f"""
    * {{
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    
    QMainWindow {{
        background-color: {COLORS['bg_primary']};
    }}
    
    QWidget {{
        background-color: transparent;
        color: {COLORS['text_primary']};
    }}
    
    /* Top Header */
    QWidget#top_header {{
        background-color: {COLORS['bg_primary']};
        border-bottom: 1px solid {COLORS['border']};
    }}
    
    QLabel#logo_title {{
        font-size: 14px;
        font-weight: 700;
        color: {COLORS['text_primary']};
        letter-spacing: 1px;
    }}
    
    QLabel#logo_subtitle {{
        font-size: 11px;
        font-weight: 500;
        color: {COLORS['text_secondary']};
        letter-spacing: 0.5px;
    }}
    
    QLabel#user_label {{
        font-size: 14px;
        color: {COLORS['text_primary']};
    }}
    
    QPushButton#icon_button {{
        background-color: {COLORS['bg_secondary']};
        border: 1px solid {COLORS['border']};
        border-radius: 20px;
        font-size: 18px;
    }}
    
    QPushButton#icon_button:hover {{
        background-color: {COLORS['sidebar_hover']};
    }}
    
    /* Sidebar */
    QWidget#sidebar {{
        background-color: {COLORS['sidebar_bg']};
        border-right: 1px solid {COLORS['border']};
    }}
    
    QPushButton#sidebar_button {{
        background-color: transparent;
        color: {COLORS['sidebar_text']};
        border: none;
        border-radius: 8px;
        padding: 12px 16px;
        text-align: left;
        font-size: 14px;
        margin: 2px 8px;
    }}
    
    QPushButton#sidebar_button:hover {{
        background-color: {COLORS['sidebar_hover']};
        color: {COLORS['primary']};
    }}
    
    QPushButton#sidebar_button:checked {{
        background-color: {COLORS['primary']};
        color: white;
        font-weight: 500;
    }}
    
    /* Content Area */
    QWidget#content_area {{
        background-color: {COLORS['bg_primary']};
        padding: 24px;
    }}
    
    /* Header */
    QLabel#header_label {{
        font-size: 28px;
        font-weight: 600;
        color: {COLORS['text_primary']};
        padding: 0px;
        margin-bottom: 20px;
    }}
    
    /* Stat Cards */
    QWidget#stat_card {{
        background-color: {COLORS['card_bg']};
        border-radius: 12px;
        border: 1px solid {COLORS['border']};
        padding: 20px;
    }}
    
    QLabel#stat_number {{
        font-size: 32px;
        font-weight: 700;
        color: {COLORS['text_primary']};
    }}
    
    QLabel#stat_text {{
        font-size: 13px;
        font-weight: 500;
        color: {COLORS['text_secondary']};
    }}
    
    /* Search Box */
    QLineEdit#search_box {{
        background-color: {COLORS['bg_primary']};
        border: 1px solid {COLORS['border']};
        border-radius: 8px;
        padding: 10px 16px;
        font-size: 14px;
        color: {COLORS['text_primary']};
    }}
    
    QLineEdit#search_box:focus {{
        border: 1px solid {COLORS['primary']};
    }}
    
    /* Primary Button */
    QPushButton#primary_button {{
        background-color: {COLORS['primary']};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-size: 14px;
        font-weight: 600;
    }}
    
    QPushButton#primary_button:hover {{
        background-color: {COLORS['primary_hover']};
    }}
    
    QPushButton#primary_button:pressed {{
        background-color: #2E5F8A;
    }}
    
    /* Table */
    QTableWidget {{
        background-color: {COLORS['card_bg']};
        border: 1px solid {COLORS['border']};
        border-radius: 10px;
        gridline-color: {COLORS['border_light']};
        color: {COLORS['text_primary']};
        font-size: 13px;
    }}
    
    QTableWidget::item {{
        padding: 12px 8px;
        border-bottom: 1px solid {COLORS['border_light']};
    }}
    
    QTableWidget::item:selected {{
        background-color: {COLORS['sidebar_hover']};
        color: {COLORS['text_primary']};
    }}
    
    QHeaderView::section {{
        background-color: {COLORS['bg_secondary']};
        color: {COLORS['text_secondary']};
        padding: 12px 8px;
        border: none;
        border-bottom: 2px solid {COLORS['border']};
        font-weight: 600;
        font-size: 12px;
        text-transform: uppercase;
    }}
    
    QScrollBar:vertical {{
        background-color: {COLORS['bg_secondary']};
        width: 12px;
        border-radius: 6px;
    }}
    
    QScrollBar::handle:vertical {{
        background-color: {COLORS['border']};
        border-radius: 6px;
        min-height: 20px;
    }}
    
    QScrollBar::handle:vertical:hover {{
        background-color: {COLORS['text_tertiary']};
    }}
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
"""
