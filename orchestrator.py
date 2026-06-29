"""
Training Orchestration System - Main orchestrator that coordinates all components.
"""
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from config.settings import Settings
from database.db_manager import DatabaseManager
from database.models import TrainingBatch, Trainee, TrainingSession, AttendanceLog
from engines.training_plan_engine import TrainingPlanEngine
from engines.content_scheduler import ContentScheduler
from engines.content_delivery_engine import ContentDeliveryEngine
from engines.assessment_engine import AssessmentEngine
from engines.attendance_tracker import AttendanceTracker
from integrations.teams_integration import TeamsIntegration
from utils.logger import setup_logger

logger = setup_logger(__name__)


class TrainingOrchestrationSystem:
    """Main orchestration system coordinating all training components."""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.plan_engine = TrainingPlanEngine()
        self.scheduler = ContentScheduler()
        self.delivery_engine = ContentDeliveryEngine()
        self.assessment_engine = AssessmentEngine()
        self.attendance_tracker = AttendanceTracker()
        self.teams_integration = TeamsIntegration()
        
        logger.info("Training Orchestration System initialized")
    
    def create_training_batch(
        self,
        batch_name: str,
        num_trainees: int,
        duration_weeks: int,
        start_date: datetime,
        skill_area: str,
        training_type: str = "full-day",
        trainee_list: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Create and initialize a training batch.
        
        Args:
            batch_name: Name of the batch
            num_trainees: Number of trainees
            duration_weeks: Duration in weeks
            start_date: Start date of training
            skill_area: Skill/learning area
            training_type: "full-day" or "half-day"
            trainee_list: List of trainee details
        
        Returns:
            Created batch with plan and schedule
        """
        try:
            logger.info(f"Creating training batch: {batch_name}")
            
            session = self.db_manager.get_session()
            
            # 1. Create training plan
            plan = self.plan_engine.create_training_plan(
                num_trainees,
                duration_weeks,
                start_date,
                skill_area,
                training_type
            )
            
            # 2. Create schedule from plan
            scheduled_sessions = self.scheduler.schedule_sessions_from_plan(plan)
            
            # 3. Create batch in database
            batch = TrainingBatch(
                batch_name=batch_name,
                num_trainees=num_trainees,
                duration_weeks=duration_weeks,
                start_date=start_date,
                end_date=start_date + timedelta(weeks=duration_weeks),
                skill_area=skill_area,
                training_type=training_type,
                status="planning"
            )
            
            session.add(batch)
            session.commit()
            batch_id = batch.id
            
            # 4. Add trainees if provided
            if trainee_list:
                for trainee_info in trainee_list:
                    trainee = Trainee(
                        batch_id=batch_id,
                        name=trainee_info.get("name"),
                        email=trainee_info.get("email"),
                        is_registered=False
                    )
                    session.add(trainee)
                
                session.commit()
                logger.info(f"Added {len(trainee_list)} trainees to batch")
            
            # 5. Create sessions in database
            for sched_session in scheduled_sessions:
                db_session = TrainingSession(
                    batch_id=batch_id,
                    session_number=sched_session["session_id"],
                    day_number=sched_session["day"],
                    start_time=datetime.fromisoformat(sched_session["start_time"]),
                    end_time=datetime.fromisoformat(sched_session["end_time"]),
                    session_type=sched_session["session_type"],
                    topic=sched_session["topic"],
                    content_url=sched_session["content_url"],
                    status="scheduled"
                )
                session.add(db_session)
            
            session.commit()
            session.close()
            
            result = {
                "batch_id": batch_id,
                "batch_name": batch_name,
                "status": "created",
                "plan": plan,
                "scheduled_sessions": len(scheduled_sessions),
                "num_trainees": num_trainees,
                "created_at": datetime.utcnow().isoformat()
            }
            
            logger.info(f"Training batch created: {batch_name} (ID: {batch_id})")
            return result
        
        except Exception as e:
            logger.error(f"Error creating training batch: {str(e)}")
            raise
    
    def schedule_batch_with_teams_meetings(
        self,
        batch_id: int,
        organizer_email: str
    ) -> Dict[str, Any]:
        """
        Schedule Teams meetings for all sessions in a batch.
        
        Args:
            batch_id: Batch ID
            organizer_email: Organizer email address
        
        Returns:
            Meeting scheduling result
        """
        try:
            logger.info(f"Scheduling Teams meetings for batch {batch_id}")
            
            session = self.db_manager.get_session()
            
            # Get all sessions for the batch
            sessions = session.query(TrainingSession).filter(
                TrainingSession.batch_id == batch_id
            ).all()
            
            # Get all trainees for the batch
            trainees = session.query(Trainee).filter(
                Trainee.batch_id == batch_id
            ).all()
            
            attendee_emails = [t.email for t in trainees if t.email]
            
            meetings_created = 0
            for db_session in sessions:
                meeting = self.teams_integration.create_meeting(
                    db_session.session_number,
                    db_session.topic,
                    db_session.start_time,
                    attendee_emails,
                    organizer_email
                )
                
                # Update session with meeting details
                db_session.teams_meeting_id = meeting["meeting_id"]
                db_session.teams_meeting_url = meeting["meeting_url"]
                session.add(db_session)
                
                # Send invites to all trainees
                for attendee_email in attendee_emails:
                    self.teams_integration.send_meeting_invite(meeting, attendee_email)
                
                meetings_created += 1
            
            session.commit()
            session.close()
            
            logger.info(f"Created {meetings_created} Teams meetings for batch {batch_id}")
            
            return {
                "batch_id": batch_id,
                "meetings_created": meetings_created,
                "created_at": datetime.utcnow().isoformat()
            }
        
        except Exception as e:
            logger.error(f"Error scheduling Teams meetings: {str(e)}")
            raise
    
    def execute_scheduled_session(
        self,
        session_id: int
    ) -> Dict[str, Any]:
        """
        Execute a scheduled training session.
        
        Args:
            session_id: Training session ID
        
        Returns:
            Session execution result
        """
        try:
            logger.info(f"Executing session {session_id}")
            
            session = self.db_manager.get_session()
            
            db_session = session.query(TrainingSession).filter(
                TrainingSession.id == session_id
            ).first()
            
            if not db_session:
                raise ValueError(f"Session {session_id} not found")
            
            # Execute session
            session_data = {
                "session_id": db_session.id,
                "topic": db_session.topic,
                "content_url": db_session.content_url,
                "session_type": db_session.session_type
            }
            
            execution_result = self.delivery_engine.execute_session(
                session_data,
                db_session.teams_meeting_url
            )
            
            # Update session status
            db_session.is_executed = True
            db_session.status = "in-progress"
            session.add(db_session)
            session.commit()
            session.close()
            
            return execution_result
        
        except Exception as e:
            logger.error(f"Error executing session: {str(e)}")
            raise
    
    def generate_session_assessment(
        self,
        session_id: int
    ) -> Dict[str, Any]:
        """
        Generate assessment for a training session.
        
        Args:
            session_id: Training session ID
        
        Returns:
            Assessment object
        """
        try:
            session = self.db_manager.get_session()
            
            db_session = session.query(TrainingSession).filter(
                TrainingSession.id == session_id
            ).first()
            
            if not db_session:
                raise ValueError(f"Session {session_id} not found")
            
            assessment = self.assessment_engine.generate_assessment(
                db_session.topic,
                difficulty="mixed"
            )
            
            session.close()
            
            logger.info(f"Assessment generated for session {session_id}")
            return assessment
        
        except Exception as e:
            logger.error(f"Error generating assessment: {str(e)}")
            raise
    
    def record_trainee_attendance(
        self,
        session_id: int,
        trainee_id: int,
        joined_time: datetime,
        left_time: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Record trainee attendance for a session.
        
        Args:
            session_id: Session ID
            trainee_id: Trainee ID
            joined_time: Time when trainee joined
            left_time: Time when trainee left
        
        Returns:
            Attendance record
        """
        try:
            session = self.db_manager.get_session()
            
            db_session = session.query(TrainingSession).filter(
                TrainingSession.id == session_id
            ).first()
            
            if not db_session:
                raise ValueError(f"Session {session_id} not found")
            
            attendance_record = self.attendance_tracker.mark_attendance(
                session_id,
                trainee_id,
                joined_time,
                left_time
            )
            
            # Calculate attendance percentage
            if left_time:
                duration = (left_time - joined_time).total_seconds() / 60
                attendance_percentage = (
                    duration / db_session.end_time.minute if db_session.end_time.minute > 0 else 0
                ) * 100
            else:
                attendance_percentage = 0
            
            # Create attendance log
            log = AttendanceLog(
                session_id=session_id,
                trainee_id=trainee_id,
                joined_time=joined_time,
                left_time=left_time,
                duration_minutes=int(duration) if left_time else 0,
                attendance_percentage=min(attendance_percentage, 100),
                status=attendance_record["status"]
            )
            
            session.add(log)
            session.commit()
            session.close()
            
            logger.info(f"Attendance recorded: Session {session_id}, Trainee {trainee_id}")
            return attendance_record
        
        except Exception as e:
            logger.error(f"Error recording attendance: {str(e)}")
            raise
    
    def get_batch_summary(self, batch_id: int) -> Dict[str, Any]:
        """
        Get comprehensive batch summary.
        
        Args:
            batch_id: Batch ID
        
        Returns:
            Batch summary with all details
        """
        try:
            session = self.db_manager.get_session()
            
            batch = session.query(TrainingBatch).filter(
                TrainingBatch.id == batch_id
            ).first()
            
            if not batch:
                raise ValueError(f"Batch {batch_id} not found")
            
            trainees = session.query(Trainee).filter(
                Trainee.batch_id == batch_id
            ).all()
            
            sessions = session.query(TrainingSession).filter(
                TrainingSession.batch_id == batch_id
            ).all()
            
            summary = {
                "batch_id": batch.id,
                "batch_name": batch.batch_name,
                "skill_area": batch.skill_area,
                "training_type": batch.training_type,
                "status": batch.status,
                "start_date": batch.start_date.isoformat(),
                "end_date": batch.end_date.isoformat(),
                "num_trainees": len(trainees),
                "total_sessions": len(sessions),
                "completed_sessions": len([s for s in sessions if s.status == "completed"]),
                "trainees": [
                    {
                        "id": t.id,
                        "name": t.name,
                        "email": t.email,
                        "registered": t.is_registered
                    } for t in trainees
                ]
            }
            
            session.close()
            return summary
        
        except Exception as e:
            logger.error(f"Error getting batch summary: {str(e)}")
            raise
    
    def close(self):
        """Close database connection."""
        self.db_manager.close()
