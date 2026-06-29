"""
Database Manager - Handles database operations.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from database.models import Base
from config.settings import Settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class DatabaseManager:
    """Manages database connections and operations."""
    
    def __init__(self):
        self.database_url = Settings.database.DATABASE_URL
        self.engine = None
        self.SessionLocal = None
        self._init_database()
    
    def _init_database(self):
        """Initialize database connection."""
        try:
            self.engine = create_engine(
                self.database_url,
                echo=Settings.database.SQLALCHEMY_ECHO,
                connect_args={"check_same_thread": False} if "sqlite" in self.database_url else {}
            )
            
            # Create all tables
            Base.metadata.create_all(bind=self.engine)
            
            # Create session factory
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
            
            logger.info(f"Database initialized: {self.database_url}")
        
        except Exception as e:
            logger.error(f"Error initializing database: {str(e)}")
            raise
    
    def get_session(self) -> Session:
        """Get database session."""
        return self.SessionLocal()
    
    def close(self):
        """Close database connection."""
        if self.engine:
            self.engine.dispose()
            logger.info("Database connection closed")
