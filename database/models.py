"""
Database models for the training orchestration system.
"""
from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Text, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()


class TrainingBatch(Base):
    """Training batch model."""
    
    __tablename__ = "training_batches"
    
    id = Column(Integer, primary_key=True, index=True)
    batch_name = Column(String(255), unique=True, index=True)
    num_trainees = Column(Integer)
    duration_weeks = Column(Integer)
    start_date = Column(DateTime, index=True)
    end_date = Column(DateTime)
    skill_area = Column(String(255))
    training_type = Column(String(50))  # full-day or half-day
    status = Column(String(50))  # planning, scheduled, in-progress, completed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    sessions = relationship("TrainingSession", back_populates="batch", cascade="all, delete-orphan")
    trainees = relationship("Trainee", back_populates="batch", cascade="all, delete-orphan")
    plan = relationship("TrainingPlan", back_populates="batch", uselist=False, cascade="all, delete-orphan")


class Trainee(Base):
    """Trainee model."""
    
    __tablename__ = "trainees"
    
    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("training_batches.id"), index=True)
    name = Column(String(255))
    email = Column(String(255), index=True)
    teams_user_id = Column(String(255), nullable=True)
    is_registered = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    batch = relationship("TrainingBatch", back_populates="trainees")
    attendance_logs = relationship("AttendanceLog", back_populates="trainee", cascade="all, delete-orphan")
    assessments = relationship("Assessment", back_populates="trainee", cascade="all, delete-orphan")


class TrainingPlan(Base):
    """Training plan model."""
    
    __tablename__ = "training_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("training_batches.id"), unique=True, index=True)
    total_topics = Column(Integer)
    topics_per_day = Column(Integer)
    days_scheduled = Column(Integer)
    plan_json = Column(Text)  # Store day-wise plan as JSON
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    batch = relationship("TrainingBatch", back_populates="plan")


class TrainingSession(Base):
    """Training session model."""
    
    __tablename__ = "training_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("training_batches.id"), index=True)
    session_number = Column(Integer)
    day_number = Column(Integer)
    start_time = Column(DateTime, index=True)
    end_time = Column(DateTime)
    session_type = Column(String(50))  # lecture, hands-on, assessment
    topic = Column(String(255))
    content_url = Column(String(500), nullable=True)
    teams_meeting_id = Column(String(255), nullable=True)
    teams_meeting_url = Column(String(500), nullable=True)
    status = Column(String(50))  # scheduled, in-progress, completed, cancelled
    is_executed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    batch = relationship("TrainingBatch", back_populates="sessions")
    attendance_logs = relationship("AttendanceLog", back_populates="session", cascade="all, delete-orphan")


class AttendanceLog(Base):
    """Attendance logging model."""
    
    __tablename__ = "attendance_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("training_sessions.id"), index=True)
    trainee_id = Column(Integer, ForeignKey("trainees.id"), index=True)
    joined_time = Column(DateTime, nullable=True)
    left_time = Column(DateTime, nullable=True)
    duration_minutes = Column(Integer, default=0)
    attendance_percentage = Column(Float, default=0.0)
    status = Column(String(50))  # present, absent, late, left-early
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    session = relationship("TrainingSession", back_populates="attendance_logs")
    trainee = relationship("Trainee", back_populates="attendance_logs")


class Assessment(Base):
    """Assessment model."""
    
    __tablename__ = "assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("training_sessions.id"), index=True, nullable=True)
    trainee_id = Column(Integer, ForeignKey("trainees.id"), index=True)
    questions_json = Column(Text)  # Store questions as JSON
    responses_json = Column(Text, nullable=True)  # Store responses as JSON
    score = Column(Float, nullable=True)
    passed = Column(Boolean, nullable=True)
    time_taken_minutes = Column(Integer, nullable=True)
    status = Column(String(50))  # pending, in-progress, completed
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    trainee = relationship("Trainee", back_populates="assessments")


class ContentResource(Base):
    """Content resource model."""
    
    __tablename__ = "content_resources"
    
    id = Column(Integer, primary_key=True, index=True)
    skill_area = Column(String(255), index=True)
    topic = Column(String(255))
    content_type = Column(String(50))  # video, document, link
    content_url = Column(String(500))
    duration_minutes = Column(Integer, nullable=True)
    difficulty_level = Column(String(50))  # beginner, intermediate, advanced
    created_at = Column(DateTime, default=datetime.utcnow)


class Meeting(Base):
    """Teams meeting records model."""
    
    __tablename__ = "meetings"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("training_sessions.id"), index=True)
    meeting_id = Column(String(255), unique=True)
    meeting_url = Column(String(500))
    organizer_email = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
