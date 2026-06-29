"""
Batch management widget for creating and managing training batches
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
                             QTableWidgetItem, QLineEdit, QLabel, QSpinBox, QComboBox,
                             QDialog, QMessageBox, QHeaderView, QGroupBox, QDateEdit)
from PyQt6.QtCore import Qt, pyqtSignal, QDate, QThread
from PyQt6.QtGui import QFont, QColor
from datetime import datetime, timedelta
from database.models import TrainingBatch, Trainee
from ui.worker import BatchCreationWorker, WorkerThread
from ui.styles import COLORS
from utils.logger import setup_logger

logger = setup_logger(__name__)


class BatchManagementWidget(QWidget):
    """Widget for batch management"""
    
    batch_created = pyqtSignal(int)
    
    def __init__(self, orchestrator):
        super().__init__()
        self.orchestrator = orchestrator
        self.batch_threads = []
        self.init_ui()
        self.refresh_batches()
    
    def init_ui(self):
        """Initialize UI"""
        main_layout = QVBoxLayout()
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("Batch Management")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        header_layout.addWidget(title)
        
        new_btn = QPushButton("New Batch")
        new_btn.setMaximumWidth(120)
        new_btn.setStyleSheet(f"background-color: {COLORS['success']}; color: white; font-weight: bold;")
        new_btn.clicked.connect(self._show_create_batch)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setMaximumWidth(100)
        refresh_btn.clicked.connect(self.refresh_batches)
        
        header_layout.addStretch()
        header_layout.addWidget(new_btn)
        header_layout.addWidget(refresh_btn)
        
        main_layout.addLayout(header_layout)
        main_layout.addSpacing(10)
        
        # Batches table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Batch Name", "Trainees", "Status", "Start Date", "Actions"
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
    
    def refresh_batches(self):
        """Refresh batch list"""
        try:
            logger.info("Refreshing batches")
            
            session = self.orchestrator.db_manager.get_session()
            batches = session.query(TrainingBatch).all()
            
            self.table.setRowCount(len(batches))
            
            for row, batch in enumerate(batches):
                # ID
                self.table.setItem(row, 0, QTableWidgetItem(str(batch.id)))
                
                # Name
                self.table.setItem(row, 1, QTableWidgetItem(batch.batch_name))
                
                # Trainees count
                trainee_count = session.query(Trainee).filter_by(batch_id=batch.id).count()
                self.table.setItem(row, 2, QTableWidgetItem(str(trainee_count)))
                
                # Status
                status_item = QTableWidgetItem(batch.status)
                if batch.status == "active":
                    status_item.setBackground(QColor(COLORS['success']))
                elif batch.status == "planning":
                    status_item.setBackground(QColor(COLORS['warning']))
                else:
                    status_item.setBackground(QColor(COLORS['border']))
                self.table.setItem(row, 3, status_item)
                
                # Start date
                start_date = batch.start_date.strftime("%Y-%m-%d") if batch.start_date else "N/A"
                self.table.setItem(row, 4, QTableWidgetItem(start_date))
                
                # Actions
                actions_widget = self._create_actions_widget(batch.id)
                self.table.setCellWidget(row, 5, actions_widget)
            
            session.close()
            logger.info(f"Loaded {len(batches)} batches")
            
        except Exception as e:
            logger.error(f"Error loading batches: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to load batches:\n{str(e)}")
    
    def _create_actions_widget(self, batch_id: int) -> QWidget:
        """Create actions widget for batch"""
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        
        view_btn = QPushButton("View")
        view_btn.setMaximumWidth(70)
        view_btn.clicked.connect(lambda: self._view_batch(batch_id))
        layout.addWidget(view_btn)
        
        edit_btn = QPushButton("Edit")
        edit_btn.setMaximumWidth(70)
        edit_btn.clicked.connect(lambda: self._edit_batch(batch_id))
        layout.addWidget(edit_btn)
        
        delete_btn = QPushButton("Delete")
        delete_btn.setMaximumWidth(70)
        delete_btn.setStyleSheet(f"background-color: {COLORS['danger']}; color: white;")
        delete_btn.clicked.connect(lambda: self._delete_batch(batch_id))
        layout.addWidget(delete_btn)
        
        widget.setLayout(layout)
        return widget
    
    def _show_create_batch(self):
        """Show batch creation dialog"""
        dialog = CreateBatchDialog(self.orchestrator, self)
        dialog.batch_created.connect(self._on_batch_created)
        dialog.exec()
    
    def _on_batch_created(self, batch_data: dict):
        """Handle batch creation"""
        try:
            logger.info(f"Creating batch: {batch_data['batch_name']}")
            
            # Create worker thread
            worker = BatchCreationWorker(
                self.orchestrator,
                batch_data['batch_name'],
                batch_data['num_trainees'],
                batch_data['duration_weeks'],
                datetime.now(),
                batch_data['skill_area'],
                batch_data['training_type']
            )
            
            thread = WorkerThread(worker.func, *worker.args, **worker.kwargs)
            
            worker.error.connect(lambda msg: self._on_creation_error(msg))
            worker.result.connect(lambda result: self._on_batch_created_result(result))
            
            # Move worker to thread
            worker.moveToThread(thread)
            thread.started.connect(worker.run)
            
            thread.start()
            self.batch_threads.append(thread)
            
        except Exception as e:
            logger.error(f"Error creating batch: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to create batch:\n{str(e)}")
    
    def _on_batch_created_result(self, result: dict):
        """Handle batch creation result"""
        batch_id = result['batch_id']
        self.batch_created.emit(batch_id)
        self.refresh_batches()
        QMessageBox.information(self, "Success", f"Batch created successfully (ID: {batch_id})")
        logger.info(f"Batch created: {batch_id}")
    
    def _on_creation_error(self, error: str):
        """Handle creation error"""
        logger.error(f"Batch creation error: {error}")
        QMessageBox.critical(self, "Error", f"Failed to create batch:\n{error}")
    
    def _view_batch(self, batch_id: int):
        """View batch details"""
        try:
            session = self.orchestrator.db_manager.get_session()
            batch = session.query(TrainingBatch).filter_by(id=batch_id).first()
            
            if batch:
                summary = self.orchestrator.get_batch_summary(batch_id)
                QMessageBox.information(self, "Batch Details", 
                    f"Batch: {batch.batch_name}\n"
                    f"Trainees: {summary.get('num_trainees', 'N/A')}\n"
                    f"Status: {summary.get('status', 'N/A')}\n"
                    f"Skill Area: {summary.get('skill_area', 'N/A')}")
            
            session.close()
        except Exception as e:
            logger.error(f"Error viewing batch: {str(e)}")
    
    def _edit_batch(self, batch_id: int):
        """Edit batch"""
        QMessageBox.information(self, "Edit", "Edit functionality coming soon!")
    
    def _delete_batch(self, batch_id: int):
        """Delete batch"""
        reply = QMessageBox.question(self, "Confirm Delete",
            "Are you sure you want to delete this batch?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                session = self.orchestrator.db_manager.get_session()
                batch = session.query(TrainingBatch).filter_by(id=batch_id).first()
                if batch:
                    session.delete(batch)
                    session.commit()
                session.close()
                
                self.refresh_batches()
                QMessageBox.information(self, "Success", "Batch deleted")
                logger.info(f"Batch deleted: {batch_id}")
                
            except Exception as e:
                logger.error(f"Error deleting batch: {str(e)}")
                QMessageBox.critical(self, "Error", f"Failed to delete batch:\n{str(e)}")


class CreateBatchDialog(QDialog):
    """Dialog for creating a new batch"""
    
    batch_created = pyqtSignal(dict)
    
    def __init__(self, orchestrator, parent=None):
        super().__init__(parent)
        self.orchestrator = orchestrator
        self.setWindowTitle("Create New Batch")
        self.setGeometry(200, 200, 400, 300)
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        
        # Batch name
        layout.addWidget(QLabel("Batch Name:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter batch name")
        layout.addWidget(self.name_input)
        
        layout.addSpacing(10)
        
        # Number of trainees
        layout.addWidget(QLabel("Number of Trainees:"))
        self.trainees_spin = QSpinBox()
        self.trainees_spin.setMinimum(1)
        self.trainees_spin.setMaximum(500)
        self.trainees_spin.setValue(10)
        layout.addWidget(self.trainees_spin)
        
        layout.addSpacing(10)
        
        # Duration
        layout.addWidget(QLabel("Duration (weeks):"))
        self.duration_spin = QSpinBox()
        self.duration_spin.setMinimum(1)
        self.duration_spin.setMaximum(52)
        self.duration_spin.setValue(4)
        layout.addWidget(self.duration_spin)
        
        layout.addSpacing(10)
        
        # Skill area
        layout.addWidget(QLabel("Skill Area:"))
        self.skill_combo = QComboBox()
        self.skill_combo.addItems(["python", "web-development", "data-science"])
        layout.addWidget(self.skill_combo)
        
        layout.addSpacing(10)
        
        # Training type
        layout.addWidget(QLabel("Training Type:"))
        self.type_combo = QComboBox()
        self.type_combo.addItems(["full-day", "half-day"])
        layout.addWidget(self.type_combo)
        
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        
        create_btn = QPushButton("Create")
        create_btn.setStyleSheet(f"background-color: {COLORS['success']}; color: white;")
        create_btn.clicked.connect(self._create_batch)
        button_layout.addWidget(create_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def _create_batch(self):
        """Create batch"""
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Validation", "Please enter a batch name")
            return
        
        training_type = self.type_combo.currentText().lower().replace(" ", "-")
        
        self.batch_created.emit({
            'batch_name': self.name_input.text(),
            'num_trainees': self.trainees_spin.value(),
            'duration_weeks': self.duration_spin.value(),
            'skill_area': self.skill_combo.currentText().lower().replace(" ", "-"),
            'training_type': training_type
        })
        
        self.accept()
