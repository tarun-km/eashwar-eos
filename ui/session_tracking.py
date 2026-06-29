"""
Session tracking widget for monitoring and executing training sessions
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
                             QTableWidgetItem, QLabel, QComboBox, QMessageBox, QHeaderView,
                             QProgressBar)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QColor
from datetime import datetime
from database.models import TrainingSession, TrainingBatch
from ui.styles import COLORS
from utils.logger import setup_logger

logger = setup_logger(__name__)


class SessionTrackingWidget(QWidget):
    """Widget for session tracking and execution"""
    
    def __init__(self, orchestrator):
        super().__init__()
        self.orchestrator = orchestrator
        self.selected_batch = None
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_sessions)
        self.init_ui()
        self.refresh_sessions()
    
    def init_ui(self):
        """Initialize UI"""
        main_layout = QVBoxLayout()
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("Session Tracking")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        header_layout.addWidget(title)
        
        header_layout.addSpacing(20)
        
        # Batch selector
        batch_label = QLabel("Select Batch:")
        header_layout.addWidget(batch_label)
        
        self.batch_combo = QComboBox()
        self.batch_combo.currentIndexChanged.connect(self._on_batch_changed)
        header_layout.addWidget(self.batch_combo)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setMaximumWidth(100)
        refresh_btn.clicked.connect(self.refresh_sessions)
        
        header_layout.addStretch()
        header_layout.addWidget(refresh_btn)
        
        main_layout.addLayout(header_layout)
        main_layout.addSpacing(10)
        
        # Sessions table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Session ID", "Date", "Time", "Topic", "Duration", "Status", "Actions"
        ])
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background-color: white;
                border: 1px solid {COLORS['border']};
            }}
            QTableWidget::item:selected {{
                background-color: {COLORS['primary']};
                color: white;
            }}
            QHeaderView::section {{
                background-color: {COLORS['light']};
                padding: 5px;
                border: 1px solid {COLORS['border']};
                font-weight: bold;
            }}
        """)
        
        main_layout.addWidget(self.table)
        self.setLayout(main_layout)
        
        # Start auto-refresh
        self.refresh_timer.start(30000)  # Refresh every 30 seconds
    
    def _on_batch_changed(self):
        """Handle batch selection change"""
        self.refresh_sessions()
    
    def refresh_sessions(self):
        """Refresh sessions list"""
        try:
            session = self.orchestrator.db_manager.get_session()
            
            # Load batches
            batches = session.query(TrainingBatch).all()
            current_selection = self.batch_combo.currentText()
            
            self.batch_combo.blockSignals(True)
            self.batch_combo.clear()
            for batch in batches:
                self.batch_combo.addItem(batch.batch_name, batch.id)
            
            # Restore selection
            index = self.batch_combo.findText(current_selection)
            if index >= 0:
                self.batch_combo.setCurrentIndex(index)
            
            self.batch_combo.blockSignals(False)
            
            # Load sessions
            batch_id = self.batch_combo.currentData()
            if batch_id:
                sessions = session.query(TrainingSession).filter_by(batch_id=batch_id).all()
                
                self.table.setRowCount(len(sessions))
                
                for row, sess in enumerate(sessions):
                    # Session ID
                    self.table.setItem(row, 0, QTableWidgetItem(str(sess.id)))
                    
                    # Date
                    date_str = sess.start_time.strftime("%Y-%m-%d") if sess.start_time else "N/A"
                    self.table.setItem(row, 1, QTableWidgetItem(date_str))
                    
                    # Time
                    time_str = sess.start_time.strftime("%H:%M") if sess.start_time else "N/A"
                    self.table.setItem(row, 2, QTableWidgetItem(time_str))
                    
                    # Topic
                    self.table.setItem(row, 3, QTableWidgetItem(sess.topic or "N/A"))
                    
                    # Duration
                    if sess.start_time and sess.end_time:
                        duration = int((sess.end_time - sess.start_time).total_seconds() / 60)
                        duration_str = f"{duration} min"
                    else:
                        duration_str = "N/A"
                    self.table.setItem(row, 4, QTableWidgetItem(duration_str))
                    
                    # Status
                    status_item = QTableWidgetItem(sess.status or "pending")
                    if sess.status == "completed":
                        status_item.setBackground(QColor(COLORS['success']))
                    elif sess.status == "in-progress":
                        status_item.setBackground(QColor(COLORS['info']))
                    elif sess.status == "pending":
                        status_item.setBackground(QColor(COLORS['warning']))
                    self.table.setItem(row, 5, status_item)
                    
                    # Actions
                    actions_widget = self._create_actions_widget(batch_id, sess.id, sess.status)
                    self.table.setCellWidget(row, 6, actions_widget)
                
                logger.info(f"Loaded {len(sessions)} sessions")
            
            session.close()
            
        except Exception as e:
            logger.error(f"Error loading sessions: {str(e)}")
    
    def _create_actions_widget(self, batch_id: int, session_id: int, status: str) -> QWidget:
        """Create actions widget"""
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        
        if status != "completed":
            execute_btn = QPushButton("Execute")
            execute_btn.setMaximumWidth(80)
            execute_btn.setStyleSheet(f"background-color: {COLORS['success']}; color: white;")
            execute_btn.clicked.connect(lambda: self._execute_session(batch_id, session_id))
            layout.addWidget(execute_btn)
        
        details_btn = QPushButton("Details")
        details_btn.setMaximumWidth(80)
        details_btn.clicked.connect(lambda: self._view_details(batch_id, session_id))
        layout.addWidget(details_btn)
        
        widget.setLayout(layout)
        return widget
    
    def _execute_session(self, batch_id: int, session_id: int):
        """Execute a session"""
        try:
            logger.info(f"Executing session {session_id} from batch {batch_id}")
            
            result = self.orchestrator.execute_scheduled_session(batch_id, session_id)
            
            QMessageBox.information(self, "Success", 
                f"Session executed successfully!\n\n"
                f"Duration: {result.get('actual_duration', 'N/A')} minutes")
            
            self.refresh_sessions()
            
        except Exception as e:
            logger.error(f"Error executing session: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to execute session:\n{str(e)}")
    
    def _view_details(self, batch_id: int, session_id: int):
        """View session details"""
        try:
            session = self.orchestrator.db_manager.get_session()
            sess = session.query(TrainingSession).filter_by(id=session_id).first()
            
            if sess:
                duration = ""
                if sess.start_time and sess.end_time:
                    duration = int((sess.end_time - sess.start_time).total_seconds() / 60)
                    duration = f"{duration} minutes"
                
                details = (
                    f"Session ID: {sess.id}\n"
                    f"Title: {sess.topic}\n"
                    f"Date: {sess.start_time.strftime('%Y-%m-%d') if sess.start_time else 'N/A'}\n"
                    f"Time: {sess.start_time.strftime('%H:%M') if sess.start_time else 'N/A'}\n"
                    f"Duration: {duration}\n"
                    f"Status: {sess.status}\n"
                    f"Content URL: {sess.content_url or 'N/A'}"
                )
                QMessageBox.information(self, "Session Details", details)
            
            session.close()
        except Exception as e:
            logger.error(f"Error viewing details: {str(e)}")
