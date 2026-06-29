"""
Main application window for the Training Orchestration System UI
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTabWidget, QStatusBar, QMenuBar, QMenu, QMessageBox,
                             QTreeWidget, QTreeWidgetItem, QLabel, QDockWidget,
                             QProgressBar)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QIcon, QFont, QAction
from datetime import datetime
from orchestrator import TrainingOrchestrationSystem
from ui.styles import COLORS, SIZES, GLOBAL_STYLESHEET
from ui.splash_screen import AnimatedSplashScreen
from ui.onboarding_wizard import OnboardingWizard
from ui.dashboard import Dashboard
from ui.batch_management import BatchManagementWidget
from ui.session_tracking import SessionTrackingWidget
from ui.attendance_widget import AttendanceWidget
from ui.assessment_widget import AssessmentWidget
from ui.reports_widget import ReportsWidget
from utils.logger import setup_logger

logger = setup_logger(__name__)


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Training Orchestration System")
        self.setGeometry(100, 100, SIZES['window_width'], SIZES['window_height'])
        
        # Initialize orchestrator
        self.orchestrator = TrainingOrchestrationSystem()
        
        # Current batch ID
        self.current_batch_id = None
        
        # Setup UI
        self._setup_ui()
        self._setup_menu()
        self._setup_status_bar()
        
        # Apply stylesheet
        self.setStyleSheet(GLOBAL_STYLESHEET)
        
        logger.info("Main window initialized")
    
    def _setup_ui(self):
        """Setup main UI"""
        # Central widget
        central_widget = QWidget()
        layout = QVBoxLayout()
        
        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {COLORS['border']};
            }}
            QTabBar::tab {{
                background-color: {COLORS['light']};
                color: {COLORS['text_primary']};
                padding: 8px 20px;
                margin-right: 2px;
            }}
            QTabBar::tab:selected {{
                background-color: {COLORS['primary']};
                color: white;
            }}
        """)
        
        # Create tabs
        self.dashboard_tab = Dashboard(self.orchestrator)
        self.batch_tab = BatchManagementWidget(self.orchestrator)
        self.session_tab = SessionTrackingWidget(self.orchestrator)
        self.attendance_tab = AttendanceWidget(self.orchestrator)
        self.assessment_tab = AssessmentWidget(self.orchestrator)
        self.reports_tab = ReportsWidget(self.orchestrator)
        
        # Connect signals
        self.batch_tab.batch_created.connect(self._on_batch_created)
        self.batch_tab.batch_created.connect(self.dashboard_tab.refresh_data)
        
        # Add tabs
        self.tabs.addTab(self.dashboard_tab, "Dashboard")
        self.tabs.addTab(self.batch_tab, "Batches")
        self.tabs.addTab(self.session_tab, "Sessions")
        self.tabs.addTab(self.attendance_tab, "Attendance")
        self.tabs.addTab(self.assessment_tab, "Assessment")
        self.tabs.addTab(self.reports_tab, "Reports")
        
        layout.addWidget(self.tabs)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
    
    def _setup_menu(self):
        """Setup menu bar"""
        menubar = self.menuBar()
        menubar.setStyleSheet(f"""
            QMenuBar {{
                background-color: {COLORS['light']};
                border-bottom: 1px solid {COLORS['border']};
            }}
            QMenuBar::item:selected {{
                background-color: {COLORS['primary']};
                color: white;
            }}
            QMenu {{
                background-color: {COLORS['background']};
                border: 1px solid {COLORS['border']};
            }}
            QMenu::item:selected {{
                background-color: {COLORS['primary']};
                color: white;
            }}
        """)
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        new_batch_action = QAction("&New Batch", self)
        new_batch_action.setShortcut("Ctrl+N")
        new_batch_action.triggered.connect(self._new_batch)
        file_menu.addAction(new_batch_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("&Edit")
        
        settings_action = QAction("&Settings", self)
        settings_action.setShortcut("Ctrl+,")
        settings_action.triggered.connect(self._open_settings)
        edit_menu.addAction(settings_action)
        
        # View menu
        view_menu = menubar.addMenu("&View")
        
        refresh_action = QAction("&Refresh", self)
        refresh_action.setShortcut("F5")
        refresh_action.triggered.connect(self._refresh_all)
        view_menu.addAction(refresh_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
        
        docs_action = QAction("&Documentation", self)
        docs_action.triggered.connect(self._open_docs)
        help_menu.addAction(docs_action)
    
    def _setup_status_bar(self):
        """Setup status bar"""
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
        self.statusBar().addWidget(self.status_label, 1)
        
        # Progress bar in status bar
        self.status_progress = QProgressBar()
        self.status_progress.setMaximumWidth(200)
        self.status_progress.setVisible(False)
        self.statusBar().addPermanentWidget(self.status_progress)
    
    def _new_batch(self):
        """Create new batch"""
        wizard = OnboardingWizard(self)
        wizard.completed.connect(self._on_wizard_completed)
        wizard.exec()
    
    def _on_wizard_completed(self, config: dict):
        """Handle wizard completion"""
        try:
            self.status_label.setText("Creating training batch...")
            self.status_progress.setVisible(True)
            self.status_progress.setRange(0, 0)  # Indeterminate
            
            # Create batch
            result = self.orchestrator.create_training_batch(
                batch_name=config['batch_name'],
                num_trainees=config['num_trainees'],
                duration_weeks=config['duration_weeks'],
                start_date=datetime.now(),
                skill_area=config['skill_area'],
                training_type=config['training_type']
            )
            
            self.current_batch_id = result['batch_id']
            
            # Refresh dashboard
            self.dashboard_tab.refresh_data()
            self.tabs.setCurrentIndex(0)  # Switch to dashboard
            
            self.status_label.setText(f"Batch created successfully (ID: {self.current_batch_id})")
            self.status_progress.setVisible(False)
            
            QMessageBox.information(self, "Success", 
                f"Training batch '{config['batch_name']}' created successfully!")
            
            logger.info(f"Batch created via wizard: {self.current_batch_id}")
            
        except Exception as e:
            logger.error(f"Error creating batch: {str(e)}")
            self.status_label.setText("Error creating batch")
            self.status_progress.setVisible(False)
            QMessageBox.critical(self, "Error", f"Failed to create batch:\n{str(e)}")
    
    def _on_batch_created(self, batch_id: int):
        """Handle batch creation"""
        self.current_batch_id = batch_id
        self.dashboard_tab.refresh_data()
        self.status_label.setText(f"Current batch: {batch_id}")
    
    def _refresh_all(self):
        """Refresh all tabs"""
        self.status_label.setText("Refreshing...")
        self.dashboard_tab.refresh_data()
        self.batch_tab.refresh_batches()
        self.session_tab.refresh_sessions()
        self.attendance_tab.refresh_attendance()
        self.assessment_tab.refresh_assessments()
        self.reports_tab.refresh_reports()
        self.status_label.setText("Refreshed")
        logger.info("All views refreshed")
    
    def _open_settings(self):
        """Open settings dialog"""
        QMessageBox.information(self, "Settings", "Settings functionality coming soon!")
    
    def _show_about(self):
        """Show about dialog"""
        QMessageBox.about(self, "About Training Orchestration System",
            "Training Orchestration System v1.0\n\n"
            "AI-driven system for managing internship batch training.\n\n"
            "© 2024 All Rights Reserved")
    
    def _open_docs(self):
        """Open documentation"""
        QMessageBox.information(self, "Documentation", 
            "Documentation will open in your default browser.\n"
            "Feature coming soon!")
    
    def update_status(self, message: str, progress: int = None):
        """Update status bar"""
        self.status_label.setText(message)
        if progress is not None:
            self.status_progress.setVisible(True)
            if progress >= 0:
                self.status_progress.setRange(0, 100)
                self.status_progress.setValue(progress)
            else:
                self.status_progress.setRange(0, 0)
    
    def closeEvent(self, event):
        """Handle window close"""
        reply = QMessageBox.question(self, "Confirm Exit", 
            "Are you sure you want to close the Training Orchestration System?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.orchestrator.close()
                logger.info("Application closed")
                event.accept()
            except Exception as e:
                logger.error(f"Error closing application: {str(e)}")
                event.accept()
        else:
            event.ignore()
