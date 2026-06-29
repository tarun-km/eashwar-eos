"""
Onboarding wizard for initial system setup and configuration
"""

from PyQt6.QtWidgets import (QWizard, QWizardPage, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QSpinBox, QComboBox, QTextEdit,
                             QPushButton, QGroupBox, QCheckBox, QFileDialog)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap
from datetime import datetime
from ui.styles import COLORS, SIZES, button_primary, card_style
from utils.logger import setup_logger

logger = setup_logger(__name__)


class OnboardingWizard(QWizard):
    """Wizard for initial system setup"""
    
    completed = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Training System Setup Wizard")
        self.setGeometry(200, 100, 700, 600)
        
        # Store configuration data
        self.config_data = {}
        
        # Setup wizard pages
        self.addPage(WelcomePage(self))
        self.addPage(BatchConfigPage(self))
        self.addPage(TraineeConfigPage(self))
        self.addPage(SkillAreaPage(self))
        self.addPage(TeamsConfigPage(self))
        self.addPage(SummaryPage(self))
        
        # Connect finish signal
        self.finished.connect(self._on_completed)
        
        # Apply stylesheet
        self._apply_styles()
    
    def _apply_styles(self):
        """Apply custom styling"""
        self.setStyleSheet(f"""
            QWizard {{
                background-color: {COLORS['background']};
            }}
            QWizard > QAbstractButton {{
                min-width: 80px;
                min-height: 30px;
            }}
            QPushButton {{
                background-color: {COLORS['primary']};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 15px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #2472A4;
            }}
            QPushButton:pressed {{
                background-color: #1E5A8E;
            }}
        """)
    
    def _on_completed(self):
        """Handle wizard completion"""
        try:
            self.config_data = self._collect_config()
            self.completed.emit(self.config_data)
            logger.info(f"Onboarding completed with config: {self.config_data}")
        except Exception as e:
            logger.error(f"Error completing onboarding: {str(e)}")
    
    def _collect_config(self) -> dict:
        """Collect configuration from all pages"""
        batch_page = self.page(1)
        trainee_page = self.page(2)
        skill_page = self.page(3)
        teams_page = self.page(4)
        
        return {
            'batch_name': batch_page.batch_name_input.text(),
            'duration_weeks': batch_page.duration_spin.value(),
            'training_type': batch_page.training_type_combo.currentText().lower().replace(" ", "-"),
            'num_trainees': trainee_page.num_trainees_spin.value(),
            'skill_area': skill_page.skill_area_combo.currentText().lower().replace(" ", "-"),
            'enable_teams': teams_page.enable_teams_check.isChecked(),
            'teams_tenant_id': teams_page.tenant_id_input.text(),
            'teams_client_id': teams_page.client_id_input.text(),
        }


class WelcomePage(QWizardPage):
    """Welcome page for onboarding wizard"""
    
    def __init__(self, wizard):
        super().__init__()
        self.wizard = wizard
        self.setTitle("Welcome")
        self.setSubTitle("Let's set up your Training Orchestration System")
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Welcome to Training Orchestration System")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Description
        description = QLabel(
            "This wizard will help you:\n"
            "• Create a new training batch\n"
            "• Configure trainees and skill areas\n"
            "• Set up Teams integration\n"
            "• Schedule training sessions\n\n"
            "Click 'Next' to begin configuration."
        )
        description.setFont(QFont("Segoe UI", 11))
        description.setStyleSheet(f"color: {COLORS['text_secondary']};")
        layout.addWidget(description)
        
        layout.addStretch()
        
        self.setLayout(layout)


class BatchConfigPage(QWizardPage):
    """Page for batch configuration"""
    
    def __init__(self, wizard):
        super().__init__()
        self.wizard = wizard
        self.setTitle("Batch Configuration")
        self.setSubTitle("Configure your training batch details")
        
        layout = QVBoxLayout()
        
        # Batch name
        batch_name_label = QLabel("Batch Name:")
        batch_name_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        layout.addWidget(batch_name_label)
        
        self.batch_name_input = QLineEdit()
        self.batch_name_input.setPlaceholderText("e.g., Python Internship Batch 2024")
        layout.addWidget(self.batch_name_input)
        
        layout.addSpacing(10)
        
        # Duration
        duration_label = QLabel("Training Duration (weeks):")
        duration_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        layout.addWidget(duration_label)
        
        self.duration_spin = QSpinBox()
        self.duration_spin.setMinimum(1)
        self.duration_spin.setMaximum(52)
        self.duration_spin.setValue(4)
        layout.addWidget(self.duration_spin)
        
        layout.addSpacing(10)
        
        # Training type
        type_label = QLabel("Training Type:")
        type_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        layout.addWidget(type_label)
        
        self.training_type_combo = QComboBox()
        self.training_type_combo.addItems(["Full-day", "Half-day"])
        layout.addWidget(self.training_type_combo)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def validatePage(self) -> bool:
        """Validate page before next"""
        if not self.batch_name_input.text().strip():
            self._show_error("Please enter a batch name")
            return False
        return True
    
    def _show_error(self, message: str):
        """Show error message"""
        logger.warning(f"Validation error: {message}")


class TraineeConfigPage(QWizardPage):
    """Page for trainee configuration"""
    
    def __init__(self, wizard):
        super().__init__()
        self.wizard = wizard
        self.setTitle("Trainee Configuration")
        self.setSubTitle("Configure trainee details")
        
        layout = QVBoxLayout()
        
        # Number of trainees
        num_label = QLabel("Number of Trainees:")
        num_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        layout.addWidget(num_label)
        
        self.num_trainees_spin = QSpinBox()
        self.num_trainees_spin.setMinimum(1)
        self.num_trainees_spin.setMaximum(500)
        self.num_trainees_spin.setValue(10)
        layout.addWidget(self.num_trainees_spin)
        
        layout.addSpacing(10)
        
        # Notes
        notes_label = QLabel("Notes:")
        notes_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        layout.addWidget(notes_label)
        
        self.notes_text = QTextEdit()
        self.notes_text.setPlaceholderText("Add any notes about this batch (optional)")
        self.notes_text.setMaximumHeight(100)
        layout.addWidget(self.notes_text)
        
        layout.addStretch()
        self.setLayout(layout)


class SkillAreaPage(QWizardPage):
    """Page for skill area configuration"""
    
    def __init__(self, wizard):
        super().__init__()
        self.wizard = wizard
        self.setTitle("Skill Area Selection")
        self.setSubTitle("Choose the primary skill area for training")
        
        layout = QVBoxLayout()
        
        # Skill area
        skill_label = QLabel("Primary Skill Area:")
        skill_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        layout.addWidget(skill_label)
        
        self.skill_area_combo = QComboBox()
        self.skill_area_combo.addItems([
            "Python Programming",
            "Web Development",
            "Data Science",
            "Machine Learning",
            "Cloud Computing",
            "DevOps",
            "Mobile Development",
            "Other"
        ])
        layout.addWidget(self.skill_area_combo)
        
        layout.addSpacing(10)
        
        # Description
        description = QLabel(
            "The selected skill area will determine:\n"
            "• Training content and modules\n"
            "• Assessment criteria\n"
            "• Hands-on projects and exercises"
        )
        description.setFont(QFont("Segoe UI", 9))
        description.setStyleSheet(f"color: {COLORS['text_secondary']};")
        layout.addWidget(description)
        
        layout.addStretch()
        self.setLayout(layout)


class TeamsConfigPage(QWizardPage):
    """Page for Microsoft Teams configuration"""
    
    def __init__(self, wizard):
        super().__init__()
        self.wizard = wizard
        self.setTitle("Teams Integration")
        self.setSubTitle("Configure Microsoft Teams integration (optional)")
        
        layout = QVBoxLayout()
        
        # Enable Teams checkbox
        self.enable_teams_check = QCheckBox("Enable Microsoft Teams Integration")
        self.enable_teams_check.setChecked(False)
        self.enable_teams_check.stateChanged.connect(self._toggle_teams_fields)
        layout.addWidget(self.enable_teams_check)
        
        layout.addSpacing(10)
        
        # Teams configuration group
        self.teams_group = QGroupBox("Teams Configuration")
        teams_layout = QVBoxLayout()
        
        # Tenant ID
        tenant_label = QLabel("Tenant ID:")
        tenant_label.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        teams_layout.addWidget(tenant_label)
        
        self.tenant_id_input = QLineEdit()
        self.tenant_id_input.setPlaceholderText("Enter your Azure Tenant ID")
        self.tenant_id_input.setEnabled(False)
        teams_layout.addWidget(self.tenant_id_input)
        
        teams_layout.addSpacing(10)
        
        # Client ID
        client_label = QLabel("Client ID:")
        client_label.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        teams_layout.addWidget(client_label)
        
        self.client_id_input = QLineEdit()
        self.client_id_input.setPlaceholderText("Enter your Azure Client ID")
        self.client_id_input.setEnabled(False)
        teams_layout.addWidget(self.client_id_input)
        
        self.teams_group.setLayout(teams_layout)
        self.teams_group.setEnabled(False)
        layout.addWidget(self.teams_group)
        
        # Note
        note = QLabel(
            "Note: You can configure Teams integration later in the settings.\n"
            "Leave this blank to skip for now."
        )
        note.setFont(QFont("Segoe UI", 9))
        note.setStyleSheet(f"color: {COLORS['text_secondary']};")
        layout.addWidget(note)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def _toggle_teams_fields(self, state):
        """Toggle Teams fields based on checkbox"""
        enabled = self.enable_teams_check.isChecked()
        self.teams_group.setEnabled(enabled)
        self.tenant_id_input.setEnabled(enabled)
        self.client_id_input.setEnabled(enabled)


class SummaryPage(QWizardPage):
    """Summary page showing configuration"""
    
    def __init__(self, wizard):
        super().__init__()
        self.wizard = wizard
        self.setTitle("Configuration Summary")
        self.setSubTitle("Review and confirm your configuration")
        self.setCommitPage(True)
        self.setButtonText(QWizard.WizardButton.FinishButton, "Create Batch")
        
        layout = QVBoxLayout()
        
        title = QLabel("Configuration Summary")
        title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        layout.addWidget(title)
        
        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)
        layout.addWidget(self.summary_text)
        
        self.setLayout(layout)
    
    def initializePage(self):
        """Initialize page and show summary"""
        self._generate_summary()
    
    def _generate_summary(self):
        """Generate summary from collected data"""
        batch_page = self.wizard.page(1)
        trainee_page = self.wizard.page(2)
        skill_page = self.wizard.page(3)
        teams_page = self.wizard.page(4)
        
        summary = f"""
CONFIGURATION SUMMARY
{'=' * 50}

Batch Information:
  • Batch Name: {batch_page.batch_name_input.text()}
  • Duration: {batch_page.duration_spin.value()} weeks
  • Type: {batch_page.training_type_combo.currentText()}

Trainee Information:
  • Number of Trainees: {trainee_page.num_trainees_spin.value()}

Skill Area:
  • Primary Skill: {skill_page.skill_area_combo.currentText()}

Teams Integration:
  • Enabled: {'Yes' if teams_page.enable_teams_check.isChecked() else 'No'}

Start Date: {datetime.now().strftime('%Y-%m-%d')}

{'=' * 50}
Click 'Create Batch' to initialize the training system.
        """
        
        self.summary_text.setText(summary.strip())
