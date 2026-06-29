"""
Splash screen with loading animation for application startup
"""

from PyQt6.QtWidgets import QSplashScreen, QApplication, QLabel, QVBoxLayout, QWidget, QProgressBar
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QTimer
from PyQt6.QtGui import QPixmap, QFont, QColor, QPainter
import sys
from ui.styles import COLORS, SIZES

class SplashScreen(QSplashScreen):
    """Custom splash screen with branding and progress"""
    
    finished = pyqtSignal()
    
    def __init__(self):
        # Create a pixmap for the splash screen
        pixmap = self._create_splash_pixmap()
        super().__init__(pixmap)
        
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.progress_value = 0
        self.progress_timer = QTimer()
        self.progress_timer.timeout.connect(self._update_progress)
    
    def _create_splash_pixmap(self) -> QPixmap:
        """Create a splash screen pixmap"""
        pixmap = QPixmap(600, 500)
        pixmap.fill(QColor(COLORS['primary']))
        
        painter = QPainter(pixmap)
        
        # Draw background gradient
        from PyQt6.QtGui import QLinearGradient
        gradient = QLinearGradient(0, 0, 600, 500)
        gradient.setColorAt(0, QColor(COLORS['primary']))
        gradient.setColorAt(1, QColor(COLORS['secondary']))
        painter.fillRect(pixmap.rect(), gradient)
        
        # Draw title
        font = QFont("Segoe UI", 24, QFont.Weight.Bold)
        painter.setFont(font)
        painter.setPen(QColor("white"))
        painter.drawText(pixmap.rect().adjusted(0, 100, 0, 0), 
                        Qt.AlignmentFlag.AlignCenter | Qt.TextFlag.TextWordWrap,
                        "Training Orchestration System")
        
        # Draw subtitle
        font = QFont("Segoe UI", 12)
        painter.setFont(font)
        painter.setPen(QColor("rgba(255, 255, 255, 200)"))
        painter.drawText(pixmap.rect().adjusted(0, 180, 0, 0),
                        Qt.AlignmentFlag.AlignCenter | Qt.TextFlag.TextWordWrap,
                        "AI-Driven Internship Training Management")
        
        painter.end()
        return pixmap
    
    def show_message(self, message: str):
        """Show a message on the splash screen"""
        self.showMessage(message, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter,
                        QColor("white"))
        QApplication.instance().processEvents()
    
    def start_loading(self):
        """Start the loading animation"""
        self.show_message("Loading system components...")
        self.progress_timer.start(50)
    
    def _update_progress(self):
        """Update progress animation"""
        self.progress_value += 1
        if self.progress_value >= 100:
            self.progress_timer.stop()
            self.finished.emit()
        else:
            self.show_message(f"Loading system components... {self.progress_value}%")
    
    def finish(self, widget):
        """Finish splash screen and show main widget"""
        super().finish(widget)


class AnimatedSplashScreen(QWidget):
    """Alternative animated splash screen"""
    
    finished = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.progress = 0
        
        # Setup timer for animation
        self.timer = QTimer()
        self.timer.timeout.connect(self._animate)
    
    def init_ui(self):
        """Initialize UI"""
        self.setWindowFlags(Qt.WindowType.SplashScreen | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Title
        title = QLabel("Training Orchestration System")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"color: {COLORS['primary']};")
        
        # Subtitle
        subtitle = QLabel("AI-Driven Internship Training Management")
        subtitle.setFont(QFont("Segoe UI", 10))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet(f"color: {COLORS['text_secondary']};")
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 2px solid {COLORS['border']};
                border-radius: 5px;
                text-align: center;
                background-color: {COLORS['light']};
                height: 20px;
            }}
            QProgressBar::chunk {{
                background-color: {COLORS['success']};
                border-radius: 3px;
            }}
        """)
        
        # Status message
        self.status_label = QLabel("Initializing...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
        
        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(20)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.status_label)
        layout.addStretch()
        
        self.setLayout(layout)
        self.setGeometry(400, 200, 600, 400)
    
    def start_loading(self, steps: list = None):
        """Start loading with optional steps"""
        self.steps = steps or [
            "Initializing database...",
            "Loading orchestrator...",
            "Configuring engines...",
            "Preparing UI components...",
            "Ready!"
        ]
        self.current_step = 0
        self.progress = 0
        self.timer.start(100)
    
    def _animate(self):
        """Animate progress"""
        step_size = 100 // len(self.steps)
        
        self.progress += step_size // 5
        self.progress_bar.setValue(min(self.progress, 100))
        
        if self.progress >= (self.current_step + 1) * step_size and self.current_step < len(self.steps):
            self.status_label.setText(self.steps[self.current_step])
            self.current_step += 1
        
        if self.progress >= 100:
            self.timer.stop()
            self.finished.emit()
    
    def update_status(self, message: str, progress: int = None):
        """Update status message"""
        self.status_label.setText(message)
        if progress is not None:
            self.progress_bar.setValue(progress)
        QApplication.instance().processEvents()
    
    def finish(self, widget):
        """Finish splash screen and show widget"""
        self.close()
