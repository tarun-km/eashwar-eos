"""
Configuration settings for the training orchestration system.
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class TrainingConfig:
    """Training system configuration."""
    
    # Default session configuration
    DEFAULT_SESSION_DURATION = 40  # minutes
    DEFAULT_BREAK_DURATION = 10    # minutes
    DEFAULT_HANDS_ON_START_DAY = 3  # Start hands-on after day 3
    
    # Training types
    TRAINING_TYPES = ["full-day", "half-day"]
    
    # Session types
    SESSION_TYPES = ["lecture", "hands-on", "assessment"]


class DatabaseConfig:
    """Database configuration."""
    
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./training_system.db")
    SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO", False)


class TeamsConfig:
    """Microsoft Teams integration configuration."""
    
    # OAuth configuration
    TENANT_ID = os.getenv("TEAMS_TENANT_ID", "")
    CLIENT_ID = os.getenv("TEAMS_CLIENT_ID", "")
    CLIENT_SECRET = os.getenv("TEAMS_CLIENT_SECRET", "")
    
    # Meeting configuration
    MEETING_DURATION_MINUTES = 50
    REMINDER_MINUTES_BEFORE = 15
    
    # Graph API endpoint
    GRAPH_API_ENDPOINT = "https://graph.microsoft.com/v1.0"


class ContentConfig:
    """Content configuration."""
    
    # Content storage
    CONTENT_DIRECTORY = os.path.join(os.path.dirname(__file__), "..", "content")
    SUPPORTED_VIDEO_FORMATS = [".mp4", ".mkv", ".mov", ".avi"]
    
    # Auto-play configuration
    AUTO_PLAY_ENABLED = True
    AUTO_PLAY_DELAY_SECONDS = 30


class AssessmentConfig:
    """Assessment configuration."""
    
    QUESTIONS_PER_SESSION = 5
    PASSING_SCORE = 70  # percentage
    ASSESSMENT_TIME_MINUTES = 15


class AttendanceConfig:
    """Attendance tracking configuration."""
    
    MINIMUM_SESSION_DURATION_PERCENTAGE = 80  # Mark present if attended 80% of session
    DAILY_LOG_ENABLED = True


class Settings:
    """Main settings class."""
    
    # Service configuration
    SERVICE_NAME = "Training Orchestration System"
    VERSION = "0.1.0"
    DEBUG = os.getenv("DEBUG", False)
    
    # Paths
    LOG_DIRECTORY = os.path.join(os.path.dirname(__file__), "..", "logs")
    
    # Sub-configurations
    training = TrainingConfig()
    database = DatabaseConfig()
    teams = TeamsConfig()
    content = ContentConfig()
    assessment = AssessmentConfig()
    attendance = AttendanceConfig()


# Create logs directory if it doesn't exist
os.makedirs(Settings.LOG_DIRECTORY, exist_ok=True)
os.makedirs(ContentConfig.CONTENT_DIRECTORY, exist_ok=True)
