"""
Worker threads for background task execution without blocking UI
"""

from PyQt6.QtCore import QThread, pyqtSignal, QObject
from typing import Any, Callable, Optional
from utils.logger import setup_logger

logger = setup_logger(__name__)


class Worker(QObject):
    """Generic worker for executing background tasks"""
    
    # Signals
    started = pyqtSignal()
    finished = pyqtSignal()
    error = pyqtSignal(str)
    progress = pyqtSignal(int)
    result = pyqtSignal(object)
    
    def __init__(self, func: Callable, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self._is_running = True
    
    def run(self):
        """Execute the task"""
        try:
            self.started.emit()
            logger.info(f"Worker starting: {self.func.__name__}")
            
            result = self.func(*self.args, **self.kwargs)
            
            if self._is_running:
                self.result.emit(result)
                self.finished.emit()
            
            logger.info(f"Worker completed: {self.func.__name__}")
            
        except Exception as e:
            logger.error(f"Worker error in {self.func.__name__}: {str(e)}")
            self.error.emit(str(e))
            self.finished.emit()
    
    def stop(self):
        """Stop the worker"""
        self._is_running = False


class WorkerThread(QThread):
    """Thread wrapper for Worker"""
    
    def __init__(self, func: Callable, *args, **kwargs):
        super().__init__()
        self.worker = Worker(func, *args, **kwargs)
        self.worker.moveToThread(self)
        
        # Connect signals
        self.started.connect(self.worker.run)
        self.worker.finished.connect(self.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.finished.connect(self.deleteLater)
    
    def get_worker(self) -> Worker:
        """Get the worker object"""
        return self.worker


class BatchCreationWorker(Worker):
    """Worker for batch creation tasks"""
    
    batch_created = pyqtSignal(dict)
    
    def __init__(self, orchestrator, batch_name: str, num_trainees: int, 
                 duration_weeks: int, start_date, skill_area: str, training_type: str):
        super().__init__(self._create_batch, orchestrator, batch_name, num_trainees, 
                        duration_weeks, start_date, skill_area, training_type)
    
    @staticmethod
    def _create_batch(orchestrator, batch_name: str, num_trainees: int, 
                     duration_weeks: int, start_date, skill_area: str, training_type: str):
        """Create batch in background"""
        return orchestrator.create_training_batch(
            batch_name=batch_name,
            num_trainees=num_trainees,
            duration_weeks=duration_weeks,
            start_date=start_date,
            skill_area=skill_area,
            training_type=training_type
        )
    
    def run(self):
        """Execute batch creation"""
        try:
            self.started.emit()
            logger.info("Starting batch creation")
            
            result = self.func(*self.args, **self.kwargs)
            
            if self._is_running:
                self.batch_created.emit(result)
                self.result.emit(result)
                self.finished.emit()
            
            logger.info("Batch creation completed")
            
        except Exception as e:
            logger.error(f"Batch creation error: {str(e)}")
            self.error.emit(str(e))
            self.finished.emit()


class SessionExecutionWorker(Worker):
    """Worker for session execution tasks"""
    
    session_started = pyqtSignal(dict)
    session_completed = pyqtSignal(dict)
    
    def __init__(self, orchestrator, batch_id: int, session_id: int):
        super().__init__(self._execute_session, orchestrator, batch_id, session_id)
    
    @staticmethod
    def _execute_session(orchestrator, batch_id: int, session_id: int):
        """Execute session in background"""
        return orchestrator.execute_scheduled_session(batch_id, session_id)
    
    def run(self):
        """Execute session"""
        try:
            self.started.emit()
            logger.info(f"Starting session execution: batch={self.args[1]}, session={self.args[2]}")
            
            result = self.func(*self.args, **self.kwargs)
            
            if self._is_running:
                self.session_completed.emit(result)
                self.result.emit(result)
                self.finished.emit()
            
            logger.info("Session execution completed")
            
        except Exception as e:
            logger.error(f"Session execution error: {str(e)}")
            self.error.emit(str(e))
            self.finished.emit()


class AssessmentWorker(Worker):
    """Worker for assessment generation and submission"""
    
    assessment_generated = pyqtSignal(dict)
    assessment_submitted = pyqtSignal(dict)
    
    def __init__(self, orchestrator, batch_id: int, session_id: int):
        super().__init__(self._generate_assessment, orchestrator, batch_id, session_id)
    
    @staticmethod
    def _generate_assessment(orchestrator, batch_id: int, session_id: int):
        """Generate assessment in background"""
        return orchestrator.generate_session_assessment(batch_id, session_id)
    
    def run(self):
        """Generate assessment"""
        try:
            self.started.emit()
            logger.info(f"Starting assessment generation: batch={self.args[1]}, session={self.args[2]}")
            
            result = self.func(*self.args, **self.kwargs)
            
            if self._is_running:
                self.assessment_generated.emit(result)
                self.result.emit(result)
                self.finished.emit()
            
            logger.info("Assessment generation completed")
            
        except Exception as e:
            logger.error(f"Assessment generation error: {str(e)}")
            self.error.emit(str(e))
            self.finished.emit()
