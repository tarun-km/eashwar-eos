"""
Reports and analytics widget for viewing training insights
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
                             QTableWidgetItem, QLabel, QComboBox, QDateEdit, QTabWidget,
                             QHeaderView, QTextEdit, QMessageBox)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from database.models import TrainingBatch, Trainee, TrainingSession, AttendanceLog, Assessment
from ui.styles import COLORS
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ReportsWidget(QWidget):
    """Widget for reports and analytics"""
    
    def __init__(self, orchestrator):
        super().__init__()
        self.orchestrator = orchestrator
        self.init_ui()
        self.refresh_reports()
    
    def init_ui(self):
        """Initialize UI"""
        main_layout = QVBoxLayout()
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("Reports & Analytics")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        header_layout.addWidget(title)
        
        header_layout.addSpacing(20)
        
        # Batch selector
        batch_label = QLabel("Batch:")
        header_layout.addWidget(batch_label)
        
        self.batch_combo = QComboBox()
        self.batch_combo.currentIndexChanged.connect(self.refresh_reports)
        header_layout.addWidget(self.batch_combo)
        
        export_btn = QPushButton("Export Report")
        export_btn.setMaximumWidth(120)
        export_btn.clicked.connect(self._export_report)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setMaximumWidth(100)
        refresh_btn.clicked.connect(self.refresh_reports)
        
        header_layout.addStretch()
        header_layout.addWidget(export_btn)
        header_layout.addWidget(refresh_btn)
        
        main_layout.addLayout(header_layout)
        main_layout.addSpacing(10)
        
        # Tabs
        self.tabs = QTabWidget()
        
        # Summary tab
        self.summary_tab = QWidget()
        self.summary_layout = QVBoxLayout()
        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)
        self.summary_layout.addWidget(self.summary_text)
        self.summary_tab.setLayout(self.summary_layout)
        self.tabs.addTab(self.summary_tab, "Summary")
        
        # Performance tab
        self.performance_tab = QWidget()
        self.perf_layout = QVBoxLayout()
        self.perf_table = QTableWidget()
        self.perf_table.setColumnCount(5)
        self.perf_table.setHorizontalHeaderLabels([
            "Trainee", "Attendance %", "Avg Score", "Sessions", "Status"
        ])
        self.perf_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.perf_layout.addWidget(self.perf_table)
        self.performance_tab.setLayout(self.perf_layout)
        self.tabs.addTab(self.performance_tab, "Performance")
        
        # Attendance tab
        self.attendance_tab = QWidget()
        self.attend_layout = QVBoxLayout()
        self.attend_table = QTableWidget()
        self.attend_table.setColumnCount(4)
        self.attend_table.setHorizontalHeaderLabels([
            "Trainee", "Present", "Absent", "Rate"
        ])
        self.attend_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.attend_layout.addWidget(self.attend_table)
        self.attendance_tab.setLayout(self.attend_layout)
        self.tabs.addTab(self.attendance_tab, "Attendance")
        
        # Assessment tab
        self.assess_tab = QWidget()
        self.assess_layout = QVBoxLayout()
        self.assess_table = QTableWidget()
        self.assess_table.setColumnCount(4)
        self.assess_table.setHorizontalHeaderLabels([
            "Session", "Count", "Avg Score", "Pass Rate"
        ])
        self.assess_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.assess_layout.addWidget(self.assess_table)
        self.assess_tab.setLayout(self.assess_layout)
        self.tabs.addTab(self.assess_tab, "Assessments")
        
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)
    
    def refresh_reports(self):
        """Refresh all reports"""
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
            
            # Load reports
            batch_id = self.batch_combo.currentData()
            if batch_id:
                self._load_summary(session, batch_id)
                self._load_performance(session, batch_id)
                self._load_attendance(session, batch_id)
                self._load_assessments(session, batch_id)
            
            session.close()
            
        except Exception as e:
            logger.error(f"Error loading reports: {str(e)}")
    
    def _load_summary(self, session, batch_id: int):
        """Load summary report"""
        try:
            batch = session.query(TrainingBatch).filter_by(id=batch_id).first()
            trainees = session.query(Trainee).filter_by(batch_id=batch_id).all()
            sess_obj = session.query(TrainingSession).filter_by(batch_id=batch_id).all()
            
            summary = f"""
BATCH SUMMARY REPORT
{'=' * 60}

Batch Information:
  Name: {batch.batch_name}
  ID: {batch.id}
  Status: {batch.status}
  Skill Area: {batch.skill_area}
  Training Type: {batch.training_type}
  
Overview:
  Total Trainees: {len(trainees)}
  Total Sessions: {len(sess_obj)}
  Start Date: {batch.start_date.strftime('%Y-%m-%d') if batch.start_date else 'N/A'}
  End Date: {batch.end_date.strftime('%Y-%m-%d') if batch.end_date else 'N/A'}
  
Statistics:
  Completed Sessions: {sum(1 for s in sess_obj if s.status == 'completed')}
  Pending Sessions: {sum(1 for s in sess_obj if s.status == 'pending')}
  In-Progress: {sum(1 for s in sess_obj if s.status == 'in-progress')}

{'=' * 60}
Generated: {TrainingBatch.__table__.name}
            """
            
            self.summary_text.setText(summary.strip())
            
        except Exception as e:
            logger.error(f"Error loading summary: {str(e)}")
    
    def _load_performance(self, session, batch_id: int):
        """Load performance report"""
        try:
            trainees = session.query(Trainee).filter_by(batch_id=batch_id).all()
            
            self.perf_table.setRowCount(len(trainees))
            
            for row, trainee in enumerate(trainees):
                # Name
                self.perf_table.setItem(row, 0, QTableWidgetItem(trainee.name))
                
                # Attendance
                attendance = session.query(AttendanceLog).filter_by(trainee_id=trainee.id).all()
                present = sum(1 for a in attendance if a.status == "present")
                total_att = len(attendance)
                att_pct = (present / total_att * 100) if total_att > 0 else 0
                self.perf_table.setItem(row, 1, QTableWidgetItem(f"{att_pct:.1f}%"))
                
                # Avg Score
                assessments = session.query(Assessment).filter_by(trainee_id=trainee.id).all()
                avg_score = sum(a.score for a in assessments if a.score) / len(assessments) if assessments else 0
                self.perf_table.setItem(row, 2, QTableWidgetItem(f"{avg_score:.1f}%"))
                
                # Sessions
                self.perf_table.setItem(row, 3, QTableWidgetItem(str(total_att)))
                
                # Status
                status = "Passed" if att_pct >= 80 and avg_score >= 70 else "In Progress"
                self.perf_table.setItem(row, 4, QTableWidgetItem(status))
            
        except Exception as e:
            logger.error(f"Error loading performance: {str(e)}")
    
    def _load_attendance(self, session, batch_id: int):
        """Load attendance report"""
        try:
            trainees = session.query(Trainee).filter_by(batch_id=batch_id).all()
            
            self.attend_table.setRowCount(len(trainees))
            
            for row, trainee in enumerate(trainees):
                # Name
                self.attend_table.setItem(row, 0, QTableWidgetItem(trainee.name))
                
                # Attendance data
                attendance = session.query(AttendanceLog).filter_by(trainee_id=trainee.id).all()
                present = sum(1 for a in attendance if a.status == "present")
                absent = len(attendance) - present
                
                # Present
                self.attend_table.setItem(row, 1, QTableWidgetItem(str(present)))
                
                # Absent
                self.attend_table.setItem(row, 2, QTableWidgetItem(str(absent)))
                
                # Rate
                rate = (present / len(attendance) * 100) if attendance else 0
                self.attend_table.setItem(row, 3, QTableWidgetItem(f"{rate:.1f}%"))
            
        except Exception as e:
            logger.error(f"Error loading attendance: {str(e)}")
    
    def _load_assessments(self, session, batch_id: int):
        """Load assessment report"""
        try:
            sessions = session.query(TrainingSession).filter_by(batch_id=batch_id).all()
            assessments_by_session = {}
            
            for sess in sessions:
                assessments = session.query(Assessment).filter_by(session_id=sess.id).all()
                if assessments:
                    assessments_by_session[sess.topic or f"Session {sess.id}"] = assessments
            
            self.assess_table.setRowCount(len(assessments_by_session))
            
            for row, (session_name, assessments) in enumerate(assessments_by_session.items()):
                # Session
                self.assess_table.setItem(row, 0, QTableWidgetItem(session_name))
                
                # Count
                self.assess_table.setItem(row, 1, QTableWidgetItem(str(len(assessments))))
                
                # Avg Score
                scores = [a.score for a in assessments if a.score]
                avg = sum(scores) / len(scores) if scores else 0
                self.assess_table.setItem(row, 2, QTableWidgetItem(f"{avg:.1f}%"))
                
                # Pass Rate
                passed = sum(1 for a in assessments if a.score and a.score >= 70)
                pass_rate = (passed / len(assessments) * 100) if assessments else 0
                self.assess_table.setItem(row, 3, QTableWidgetItem(f"{pass_rate:.1f}%"))
            
        except Exception as e:
            logger.error(f"Error loading assessments: {str(e)}")
    
    def _export_report(self):
        """Export report"""
        QMessageBox.information(self, "Export", "Report export feature coming soon!")
