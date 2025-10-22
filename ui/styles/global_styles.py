# ui/styles/global_styles.py

"""Global CSS Styles for Application"""

GLOBAL_STYLE = """
/* Main Window */
QMainWindow {
    background-color: #ECEFF4;
}

/* Header Widget */
#header_widget {
    background-color: #FFFFFF;
    border-bottom: 1px solid #D8DEE9;
}

#header_logo_text {
    color: #2E3440;
    font-size: 14px;
    font-weight: bold;
    line-height: 1.2;
}

#header_user_label {
    color: #4C566A;
    font-size: 13px;
    margin-right: 10px;
}

#header_icon_button {
    background-color: #E5E9F0;
    border: none;
    border-radius: 20px;
    padding: 8px;
}

#header_icon_button:hover {
    background-color: #D8DEE9;
}

/* Navigation Widget */
#nav_widget {
    background-color: #FFFFFF;
    border-right: 1px solid #D8DEE9;
}

#nav_button {
    background-color: transparent;
    border: none;
    border-radius: 8px;
    padding: 12px 15px;
    text-align: left;
    color: #4C566A;
    font-size: 14px;
}

#nav_button:hover {
    background-color: #E5E9F0;
}

#nav_button:checked {
    background-color: #5E81AC;
    color: #FFFFFF;
}

/* Content Stack */
#content_stack {
    background-color: #ECEFF4;
}

/* Vehicle View */
#vehicle_view {
    background-color: transparent;
}

/* Tables */
QTableWidget {
    background-color: #FFFFFF;
    border: 1px solid #D8DEE9;
    border-radius: 8px;
    gridline-color: #E5E9F0;
}

QTableWidget::item {
    padding: 8px;
    color: #2E3440;
}

QTableWidget::item:selected {
    background-color: #5E81AC;
    color: #FFFFFF;
}

QHeaderView::section {
    background-color: #F5F7FA;
    color: #4C566A;
    padding: 10px;
    border: none;
    border-bottom: 2px solid #D8DEE9;
    font-weight: bold;
}

/* Buttons */
QPushButton {
    background-color: #5E81AC;
    color: #FFFFFF;
    border: none;
    border-radius: 6px;
    padding: 10px 20px;
    font-size: 13px;
}

QPushButton:hover {
    background-color: #81A1C1;
}

QPushButton:pressed {
    background-color: #4C7A9D;
}

/* Line Edits */
QLineEdit {
    background-color: #FFFFFF;
    border: 1px solid #D8DEE9;
    border-radius: 6px;
    padding: 8px;
    color: #2E3440;
}

QLineEdit:focus {
    border: 2px solid #5E81AC;
}

/* Combo Boxes */
QComboBox {
    background-color: #FFFFFF;
    border: 1px solid #D8DEE9;
    border-radius: 6px;
    padding: 8px;
    color: #2E3440;
}

QComboBox:focus {
    border: 2px solid #5E81AC;
}

QComboBox::drop-down {
    border: none;
}

QComboBox::down-arrow {
    width: 12px;
    height: 12px;
}

/* Scrollbars */
QScrollBar:vertical {
    background-color: #E5E9F0;
    width: 12px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background-color: #D8DEE9;
    border-radius: 6px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #B8C0CC;
}

QScrollBar:horizontal {
    background-color: #E5E9F0;
    height: 12px;
    border-radius: 6px;
}

QScrollBar::handle:horizontal {
    background-color: #D8DEE9;
    border-radius: 6px;
    min-width: 20px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #B8C0CC;
}
"""
