"""
Global styling and theming for the Training Orchestration System UI
"""

# Color Scheme
COLORS = {
    'primary': '#2E86AB',
    'secondary': '#A23B72',
    'success': '#06D6A0',
    'warning': '#EF476F',
    'danger': '#E63946',
    'info': '#457B9D',
    'dark': '#1A1A2E',
    'light': '#F8F9FA',
    'border': '#E0E0E0',
    'text_primary': '#1A1A2E',
    'text_secondary': '#666666',
    'background': '#FFFFFF',
}

# Fonts
FONTS = {
    'title_large': ('Segoe UI', 18, 'bold'),
    'title': ('Segoe UI', 14, 'bold'),
    'subtitle': ('Segoe UI', 12, 'bold'),
    'body': ('Segoe UI', 10, 'normal'),
    'small': ('Segoe UI', 9, 'normal'),
    'mono': ('Courier New', 10, 'normal'),
}

# Sizes
SIZES = {
    'icon_small': 16,
    'icon_medium': 24,
    'icon_large': 32,
    'padding_small': 5,
    'padding_medium': 10,
    'padding_large': 20,
    'border_radius': 8,
    'window_width': 1200,
    'window_height': 800,
}

# Global Stylesheet
GLOBAL_STYLESHEET = f"""
QMainWindow {{
    background-color: {COLORS['background']};
}}

QWidget {{
    background-color: {COLORS['background']};
    color: {COLORS['text_primary']};
}}

QPushButton {{
    background-color: {COLORS['primary']};
    color: white;
    border: none;
    border-radius: {SIZES['border_radius']}px;
    padding: 8px 16px;
    font-weight: bold;
    font-size: 10pt;
}}

QPushButton:hover {{
    background-color: #2472A4;
}}

QPushButton:pressed {{
    background-color: #1E5A8E;
}}

QPushButton:disabled {{
    background-color: #CCCCCC;
    color: #999999;
}}

QLineEdit, QTextEdit {{
    background-color: {COLORS['light']};
    border: 1px solid {COLORS['border']};
    border-radius: {SIZES['border_radius']}px;
    padding: 8px;
    font-size: 10pt;
}}

QLineEdit:focus, QTextEdit:focus {{
    border: 2px solid {COLORS['primary']};
}}

QComboBox {{
    background-color: {COLORS['light']};
    border: 1px solid {COLORS['border']};
    border-radius: {SIZES['border_radius']}px;
    padding: 8px;
    font-size: 10pt;
}}

QComboBox:focus {{
    border: 2px solid {COLORS['primary']};
}}

QComboBox::drop-down {{
    border: none;
}}

QLabel {{
    color: {COLORS['text_primary']};
}}

QTabWidget::pane {{
    border: 1px solid {COLORS['border']};
}}

QTabBar::tab {{
    background-color: {COLORS['light']};
    color: {COLORS['text_secondary']};
    padding: 8px 20px;
    margin-right: 2px;
}}

QTabBar::tab:selected {{
    background-color: {COLORS['primary']};
    color: white;
    border-bottom: 3px solid {COLORS['primary']};
}}

QTableWidget {{
    background-color: {COLORS['background']};
    border: 1px solid {COLORS['border']};
    gridline-color: {COLORS['border']};
}}

QTableWidget::item {{
    padding: 5px;
}}

QTableWidget::item:selected {{
    background-color: {COLORS['primary']};
    color: white;
}}

QHeaderView::section {{
    background-color: {COLORS['light']};
    color: {COLORS['text_primary']};
    padding: 5px;
    border: 1px solid {COLORS['border']};
    font-weight: bold;
}}

QProgressBar {{
    border: 1px solid {COLORS['border']};
    border-radius: {SIZES['border_radius']}px;
    text-align: center;
    background-color: {COLORS['light']};
}}

QProgressBar::chunk {{
    background-color: {COLORS['success']};
    border-radius: {SIZES['border_radius'] - 2}px;
}}

QMessageBox {{
    background-color: {COLORS['background']};
}}

QScrollBar:vertical {{
    background-color: {COLORS['light']};
    width: 12px;
}}

QScrollBar::handle:vertical {{
    background-color: {COLORS['border']};
    border-radius: 6px;
    min-height: 20px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: #999999;
}}

QStatusBar {{
    background-color: {COLORS['light']};
    color: {COLORS['text_secondary']};
    border-top: 1px solid {COLORS['border']};
}}
"""

# Component Styles
def button_primary():
    return f"background-color: {COLORS['primary']}; color: white; padding: 10px 20px; border-radius: 5px; font-weight: bold;"

def button_success():
    return f"background-color: {COLORS['success']}; color: white; padding: 10px 20px; border-radius: 5px; font-weight: bold;"

def button_danger():
    return f"background-color: {COLORS['danger']}; color: white; padding: 10px 20px; border-radius: 5px; font-weight: bold;"

def button_warning():
    return f"background-color: {COLORS['warning']}; color: white; padding: 10px 20px; border-radius: 5px; font-weight: bold;"

def card_style():
    return f"""
    QFrame {{
        background-color: {COLORS['background']};
        border: 1px solid {COLORS['border']};
        border-radius: {SIZES['border_radius']}px;
        padding: {SIZES['padding_medium']}px;
    }}
    """

def section_title_style():
    return f"""
    QLabel {{
        color: {COLORS['primary']};
        font-size: 14pt;
        font-weight: bold;
    }}
    """
