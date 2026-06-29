"""
GUI Entry Point for Training Orchestration System
Starts the PyQt6 application with splash screen and onboarding
"""

import sys
import logging
from datetime import datetime
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

from ui.main_window import MainWindow
from ui.splash_screen import AnimatedSplashScreen
from ui.styles import GLOBAL_STYLESHEET, SIZES, COLORS
from utils.logger import setup_logger

logger = setup_logger(__name__)


class TrainingOrchestrationApp:
    """Main application class"""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.splash = None
        self.main_window = None
        self.initialize_app()
    
    def initialize_app(self):
        """Initialize the application"""
        # Apply global stylesheet
        self.app.setStyle('Fusion')
        self.app.setStyleSheet(GLOBAL_STYLESHEET)
        
        # Show splash screen
        self.splash = AnimatedSplashScreen()
        self.splash.show()
        self.app.processEvents()
        
        # Setup initialization steps
        self.splash.start_loading([
            "Initializing database...",
            "Loading orchestrator...",
            "Configuring engines...",
            "Preparing UI components...",
            "Ready!"
        ])
        
        # Use timer to transition from splash to main window
        QTimer.singleShot(3000, self._load_main_window)
    
    def _load_main_window(self):
        """Load main window"""
        try:
            logger.info("Loading main application window")
            self.splash.update_status("Loading main window...", 90)
            
            # Create main window
            self.main_window = MainWindow()
            
            logger.info("Main window created successfully")
            self.splash.update_status("Done!", 100)
            
            # Show main window
            self.splash.finish(self.main_window)
            self.main_window.show()
            
            # Set window properties
            self.main_window.setMinimumSize(SIZES['window_width'], SIZES['window_height'])
            
            logger.info("Application started successfully")
            
        except Exception as e:
            logger.error(f"Error loading main window: {str(e)}")
            self.splash.close()
            QMessageBox.critical(None, "Error", 
                f"Failed to load application:\n{str(e)}\n\n"
                f"Please check the logs for more details.")
            sys.exit(1)
    
    def run(self):
        """Run the application"""
        try:
            logger.info("=" * 80)
            logger.info("Training Orchestration System - GUI Version")
            logger.info("=" * 80)
            logger.info(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            exit_code = self.app.exec()
            
            logger.info(f"Application closed with exit code: {exit_code}")
            return exit_code
            
        except Exception as e:
            logger.error(f"Error running application: {str(e)}")
            import traceback
            traceback.print_exc()
            return 1


def main():
    """Main entry point"""
    try:
        app = TrainingOrchestrationApp()
        sys.exit(app.run())
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
