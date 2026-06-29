"""
Dashboard widget showing system overview and statistics
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QPushButton, QGroupBox, QScrollArea, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from ui.styles import COLORS, SIZES
from utils.logger import setup_logger

logger = setup_logger(__name__)


class Dashboard(QWidget):
    """Dashboard showing system overview"""
    
    refresh_requested = pyqtSignal()
    
    def __init__(self, orchestrator):
        super().__init__()
        self.orchestrator = orchestrator
        self.init_ui()
        self.refresh_data()
    
    def init_ui(self):
        """Initialize UI"""
        main_layout = QVBoxLayout()
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("Dashboard")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        header_layout.addWidget(title)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setMaximumWidth(100)
        refresh_btn.clicked.connect(self.refresh_data)
        header_layout.addStretch()
        header_layout.addWidget(refresh_btn)
        
        main_layout.addLayout(header_layout)
        main_layout.addSpacing(10)
        
        # Content area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout()
        
        # Statistics Grid
        stats_group = QGroupBox("System Statistics")
        stats_layout = QGridLayout()
        
        # Stat cards
        self.batches_label = self._create_stat_card("Active Batches", "0", stats_layout, 0, 0)
        self.trainees_label = self._create_stat_card("Total Trainees", "0", stats_layout, 0, 1)
        self.sessions_label = self._create_stat_card("Scheduled Sessions", "0", stats_layout, 1, 0)
        self.completion_label = self._create_stat_card("Completion Rate", "0%", stats_layout, 1, 1)
        
        stats_group.setLayout(stats_layout)
        scroll_layout.addWidget(stats_group)
        
        scroll_layout.addSpacing(10)
        
        # Recent Activity
        activity_group = QGroupBox("Recent Activity")
        activity_layout = QVBoxLayout()
        
        self.activity_list = QWidget()
        activity_inner = QVBoxLayout()
        self.activity_list.setLayout(activity_inner)
        
        activity_layout.addWidget(self.activity_list)
        activity_group.setLayout(activity_layout)
        scroll_layout.addWidget(activity_group)
        
        scroll_layout.addSpacing(10)
        
        # Quick Actions
        actions_group = QGroupBox("Quick Actions")
        actions_layout = QHBoxLayout()
        
        new_batch_btn = QPushButton("Create New Batch")
        new_batch_btn.setMinimumHeight(40)
        new_batch_btn.setStyleSheet(f"background-color: {COLORS['success']}; color: white; font-weight: bold;")
        actions_layout.addWidget(new_batch_btn)
        
        execute_session_btn = QPushButton("Execute Session")
        execute_session_btn.setMinimumHeight(40)
        actions_layout.addWidget(execute_session_btn)
        
        view_reports_btn = QPushButton("View Reports")
        view_reports_btn.setMinimumHeight(40)
        actions_layout.addWidget(view_reports_btn)
        
        actions_group.setLayout(actions_layout)
        scroll_layout.addWidget(actions_group)
        
        scroll_layout.addStretch()
        
        scroll_content.setLayout(scroll_layout)
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)
        
        self.setLayout(main_layout)
    
    def _create_stat_card(self, title: str, value: str, layout, row: int, col: int):
        """Create a statistic card"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['light']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
                padding: 15px;
            }}
        """)
        
        card_layout = QVBoxLayout()
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        title_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
        card_layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        value_label.setStyleSheet(f"color: {COLORS['primary']};")
        card_layout.addWidget(value_label)
        
        card_layout.setContentsMargins(10, 10, 10, 10)
        card.setLayout(card_layout)
        card.setMinimumHeight(100)
        
        layout.addWidget(card, row, col)
        
        return value_label
    
    def refresh_data(self):
        """Refresh dashboard data"""
        try:
            logger.info("Refreshing dashboard")
            
            # Query database for statistics
            session = self.orchestrator.db_manager.get_session()
            
            # Get batch count
            from database.models import TrainingBatch
            batch_count = session.query(TrainingBatch).count()
            self.batches_label.setText(str(batch_count))
            
            # Get trainee count
            from database.models import Trainee
            trainee_count = session.query(Trainee).count()
            self.trainees_label.setText(str(trainee_count))
            
            # Get session count
            from database.models import TrainingSession
            session_count = session.query(TrainingSession).count()
            self.sessions_label.setText(str(session_count))
            
            # Calculate completion rate
            from database.models import AttendanceLog
            total_sessions = session.query(TrainingSession).count()
            completed_sessions = session.query(TrainingSession).filter_by(status='completed').count()
            completion_rate = (completed_sessions / total_sessions * 100) if total_sessions > 0 else 0
            self.completion_label.setText(f"{completion_rate:.1f}%")
            
            session.close()
            
            logger.info(f"Dashboard refreshed: {batch_count} batches, {trainee_count} trainees")
            
        except Exception as e:
            logger.error(f"Error refreshing dashboard: {str(e)}")
