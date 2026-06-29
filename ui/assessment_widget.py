"""
Assessment management widget for generating and tracking assessments
"""

import json
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
                             QTableWidgetItem, QLabel, QComboBox, QMessageBox, QHeaderView,
                             QProgressBar, QSpinBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor
from database.models import Assessment, TrainingBatch, TrainingSession
from ui.styles import COLORS
from utils.logger import setup_logger

logger = setup_logger(__name__)


class AssessmentWidget(QWidget):
    """Widget for assessment management"""
    
    def __init__(self, orchestrator):
        super().__init__()
        self.orchestrator = orchestrator
        self.init_ui()
        self.refresh_assessments()
    
    def init_ui(self):
        """Initialize UI"""
        main_layout = QVBoxLayout()
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("Assessment Management")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        header_layout.addWidget(title)
        
        header_layout.addSpacing(20)
        
        # Batch selector
        batch_label = QLabel("Batch:")
        header_layout.addWidget(batch_label)
        
        self.batch_combo = QComboBox()
        self.batch_combo.currentIndexChanged.connect(self.refresh_assessments)
        header_layout.addWidget(self.batch_combo)
        
        create_btn = QPushButton("Create Assessment")
        create_btn.setMaximumWidth(150)
        create_btn.setStyleSheet(f"background-color: {COLORS['success']}; color: white;")
        create_btn.clicked.connect(self._create_assessment)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setMaximumWidth(100)
        refresh_btn.clicked.connect(self.refresh_assessments)
        
        header_layout.addStretch()
        header_layout.addWidget(create_btn)
        header_layout.addWidget(refresh_btn)
        
        main_layout.addLayout(header_layout)
        main_layout.addSpacing(10)
        
        # Statistics
        stats_layout = QHBoxLayout()
        
        self.total_assessments = QLabel("Total: 0")
        self.total_assessments.setStyleSheet(f"font-weight: bold; color: {COLORS['text_primary']};")
        stats_layout.addWidget(self.total_assessments)
        
        self.pending_assessments = QLabel("Pending: 0")
        self.pending_assessments.setStyleSheet(f"font-weight: bold; color: {COLORS['warning']};")
        stats_layout.addWidget(self.pending_assessments)
        
        self.completed_assessments = QLabel("Completed: 0")
        self.completed_assessments.setStyleSheet(f"font-weight: bold; color: {COLORS['success']};")
        stats_layout.addWidget(self.completed_assessments)
        
        self.avg_score = QLabel("Avg Score: 0%")
        self.avg_score.setStyleSheet(f"font-weight: bold; color: {COLORS['primary']};")
        stats_layout.addWidget(self.avg_score)
        
        stats_layout.addStretch()
        main_layout.addLayout(stats_layout)
        main_layout.addSpacing(10)
        
        # Assessment table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Session", "Type", "Questions", "Status", "Actions"
        ])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
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
    
    def refresh_assessments(self):
        """Refresh assessment data"""
        try:
            session = self.orchestrator.db_manager.get_session()
            
            # Load batches
            batches = session.query(TrainingBatch).all()
            current_selection = self.batch_combo.currentText()
            
            self.batch_combo.blockSignals(True)
            self.batch_combo.clear()
            for batch in batches:
                self.batch_combo.addItem(batch.batch_name, batch.id)
            
            index = self.batch_combo.findText(current_selection)
            if index >= 0:
                self.batch_combo.setCurrentIndex(index)
            
            self.batch_combo.blockSignals(False)
            
            # Load assessments
            batch_id = self.batch_combo.currentData()
            if batch_id:
                # Get sessions for batch
                sessions = session.query(TrainingSession).filter_by(batch_id=batch_id).all()
                assessments = session.query(Assessment).filter(
                    Assessment.session_id.in_([s.id for s in sessions])
                ).all()
                
                self.table.setRowCount(len(assessments))
                
                completed = 0
                pending = 0
                total_score = 0
                
                for row, assessment in enumerate(assessments):
                    # ID
                    self.table.setItem(row, 0, QTableWidgetItem(str(assessment.id)))
                    
                    # Session
                    session_title = "N/A"
                    if assessment.session_id:
                        sess = session.query(TrainingSession).filter_by(id=assessment.session_id).first()
                        session_title = sess.topic if sess else "N/A"
                    self.table.setItem(row, 1, QTableWidgetItem(session_title))
                    
                    # Type
                    self.table.setItem(row, 2, QTableWidgetItem("auto"))
                    
                    # Questions
                    try:
                        questions = json.loads(assessment.questions_json) if assessment.questions_json else []
                        num_questions = len(questions)
                    except:
                        num_questions = 0
                    self.table.setItem(row, 3, QTableWidgetItem(str(num_questions)))
                    
                    # Status
                    status_item = QTableWidgetItem(assessment.status or "pending")
                    if assessment.status == "completed":
                        status_item.setBackground(QColor(COLORS['success']))
                        completed += 1
                        if assessment.score:
                            total_score += assessment.score
                    else:
                        status_item.setBackground(QColor(COLORS['warning']))
                        pending += 1
                    self.table.setItem(row, 4, status_item)
                    
                    # Actions
                    actions = self._create_actions_widget(batch_id, assessment.id)
                    self.table.setCellWidget(row, 5, actions)
                
                # Update statistics
                total = len(assessments)
                self.total_assessments.setText(f"Total: {total}")
                self.pending_assessments.setText(f"Pending: {pending}")
                self.completed_assessments.setText(f"Completed: {completed}")
                
                avg = (total_score / completed) if completed > 0 else 0
                self.avg_score.setText(f"Avg Score: {avg:.1f}%")
                
                logger.info(f"Loaded {len(assessments)} assessments")
            
            session.close()
            
        except Exception as e:
            logger.error(f"Error loading assessments: {str(e)}")
    
    def _create_actions_widget(self, batch_id: int, assessment_id: int) -> QWidget:
        """Create actions widget"""
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        
        view_btn = QPushButton("View")
        view_btn.setMaximumWidth(70)
        view_btn.clicked.connect(lambda: self._view_assessment(assessment_id))
        layout.addWidget(view_btn)
        
        score_btn = QPushButton("Score")
        score_btn.setMaximumWidth(70)
        score_btn.clicked.connect(lambda: self._score_assessment(assessment_id))
        layout.addWidget(score_btn)
        
        widget.setLayout(layout)
        return widget
    
    def _create_assessment(self):
        """Create new assessment"""
        batch_id = self.batch_combo.currentData()
        if not batch_id:
            QMessageBox.warning(self, "Warning", "Please select a batch first")
            return
        
        try:
            # Get first session of batch
            session = self.orchestrator.db_manager.get_session()
            sess = session.query(TrainingSession).filter_by(batch_id=batch_id).first()
            
            if sess:
                result = self.orchestrator.generate_session_assessment(batch_id, sess.id)
                self.refresh_assessments()
                QMessageBox.information(self, "Success", "Assessment created successfully!")
            else:
                QMessageBox.warning(self, "Warning", "No sessions found for this batch")
            
            session.close()
            
        except Exception as e:
            logger.error(f"Error creating assessment: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to create assessment:\n{str(e)}")
    
    def _view_assessment(self, assessment_id: int):
        """View assessment details"""
        try:
            session = self.orchestrator.db_manager.get_session()
            assessment = session.query(Assessment).filter_by(id=assessment_id).first()
            
            if assessment:
                details = (
                    f"Assessment ID: {assessment.id}\n"
                    f"Type: {assessment.assessment_type}\n"
                    f"Status: {assessment.status}\n"
                    f"Score: {assessment.score or 'N/A'}\n"
                    f"Questions: {len(assessment.questions) if assessment.questions else 0}"
                )
                QMessageBox.information(self, "Assessment Details", details)
            
            session.close()
        except Exception as e:
            logger.error(f"Error viewing assessment: {str(e)}")
    
    def _score_assessment(self, assessment_id: int):
        """Score an assessment"""
        QMessageBox.information(self, "Scoring", "Assessment scoring feature coming soon!")
