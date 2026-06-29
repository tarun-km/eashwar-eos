"""
Attendance tracking widget for monitoring trainee attendance
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
                             QTableWidgetItem, QLabel, QComboBox, QMessageBox, QHeaderView,
                             QDateEdit, QSpinBox)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QColor
from database.models import AttendanceLog, TrainingBatch, Trainee, TrainingSession
from ui.styles import COLORS
from utils.logger import setup_logger

logger = setup_logger(__name__)


class AttendanceWidget(QWidget):
    """Widget for attendance tracking"""
    
    def __init__(self, orchestrator):
        super().__init__()
        self.orchestrator = orchestrator
        self.init_ui()
        self.refresh_attendance()
    
    def init_ui(self):
        """Initialize UI"""
        main_layout = QVBoxLayout()
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("Attendance Tracking")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        header_layout.addWidget(title)
        
        header_layout.addSpacing(20)
        
        # Batch selector
        batch_label = QLabel("Batch:")
        header_layout.addWidget(batch_label)
        
        self.batch_combo = QComboBox()
        self.batch_combo.currentIndexChanged.connect(self.refresh_attendance)
        header_layout.addWidget(self.batch_combo)
        
        # Date selector
        date_label = QLabel("Date:")
        header_layout.addWidget(date_label)
        
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.dateChanged.connect(self.refresh_attendance)
        header_layout.addWidget(self.date_edit)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setMaximumWidth(100)
        refresh_btn.clicked.connect(self.refresh_attendance)
        
        header_layout.addStretch()
        header_layout.addWidget(refresh_btn)
        
        main_layout.addLayout(header_layout)
        main_layout.addSpacing(10)
        
        # Statistics
        stats_layout = QHBoxLayout()
        
        self.total_label = QLabel("Total: 0")
        self.total_label.setStyleSheet(f"font-weight: bold; color: {COLORS['text_primary']};")
        stats_layout.addWidget(self.total_label)
        
        self.present_label = QLabel("Present: 0")
        self.present_label.setStyleSheet(f"font-weight: bold; color: {COLORS['success']};")
        stats_layout.addWidget(self.present_label)
        
        self.absent_label = QLabel("Absent: 0")
        self.absent_label.setStyleSheet(f"font-weight: bold; color: {COLORS['danger']};")
        stats_layout.addWidget(self.absent_label)
        
        self.percentage_label = QLabel("Rate: 0%")
        self.percentage_label.setStyleSheet(f"font-weight: bold; color: {COLORS['primary']};")
        stats_layout.addWidget(self.percentage_label)
        
        stats_layout.addStretch()
        
        main_layout.addLayout(stats_layout)
        main_layout.addSpacing(10)
        
        # Attendance table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "Trainee", "Attendance", "Sessions", "Percentage"
        ])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
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
    
    def refresh_attendance(self):
        """Refresh attendance data"""
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
            
            # Load attendance
            batch_id = self.batch_combo.currentData()
            if batch_id:
                trainees = session.query(Trainee).filter_by(batch_id=batch_id).all()
                
                self.table.setRowCount(len(trainees))
                
                total_present = 0
                total_absent = 0
                
                for row, trainee in enumerate(trainees):
                    # Trainee name
                    self.table.setItem(row, 0, QTableWidgetItem(trainee.name))
                    
                    # Get attendance
                    attendance = session.query(AttendanceLog).filter_by(trainee_id=trainee.id).all()
                    present_count = sum(1 for a in attendance if a.status == "present")
                    total_attendance = len(attendance)
                    
                    total_present += present_count
                    total_absent += (total_attendance - present_count)
                    
                    # Attendance count
                    self.table.setItem(row, 1, QTableWidgetItem(str(present_count)))
                    
                    # Total sessions
                    self.table.setItem(row, 2, QTableWidgetItem(str(total_attendance)))
                    
                    # Percentage
                    percentage = (present_count / total_attendance * 100) if total_attendance > 0 else 0
                    pct_item = QTableWidgetItem(f"{percentage:.1f}%")
                    
                    if percentage >= 85:
                        pct_item.setBackground(QColor(COLORS['success']))
                    elif percentage >= 70:
                        pct_item.setBackground(QColor(COLORS['warning']))
                    else:
                        pct_item.setBackground(QColor(COLORS['danger']))
                    
                    self.table.setItem(row, 3, pct_item)
                
                # Update statistics
                total = total_present + total_absent
                self.total_label.setText(f"Total: {total}")
                self.present_label.setText(f"Present: {total_present}")
                self.absent_label.setText(f"Absent: {total_absent}")
                
                percentage = (total_present / total * 100) if total > 0 else 0
                self.percentage_label.setText(f"Rate: {percentage:.1f}%")
                
                logger.info(f"Loaded attendance for {len(trainees)} trainees")
            
            session.close()
            
        except Exception as e:
            logger.error(f"Error loading attendance: {str(e)}")
