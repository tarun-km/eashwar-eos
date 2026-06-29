"""
Content Scheduler - Schedules training sessions with structured timing.
"""
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple
from config.settings import Settings
from utils.logger import setup_logger
from utils.date_utils import create_datetime_with_time, get_time_range

logger = setup_logger(__name__)


class ContentScheduler:
    """Scheduler for content delivery sessions."""
    
    def __init__(self):
        self.session_duration = Settings.training.DEFAULT_SESSION_DURATION
        self.break_duration = Settings.training.DEFAULT_BREAK_DURATION
    
    def schedule_sessions_from_plan(
        self,
        plan: Dict[str, Any],
        start_time_hour: int = 9
    ) -> List[Dict[str, Any]]:
        """
        Create detailed session schedule from training plan.
        
        Args:
            plan: Training plan from TrainingPlanEngine
            start_time_hour: Hour to start training (default 9 AM)
        
        Returns:
            List of scheduled sessions
        """
        try:
            scheduled_sessions = []
            session_id = 1
            
            for day_schedule in plan["daily_schedule"]:
                day_date = datetime.fromisoformat(day_schedule["date"])
                
                current_time = create_datetime_with_time(day_date, start_time_hour, 0)
                
                for session_info in day_schedule["sessions"]:
                    session = {
                        "session_id": session_id,
                        "day": day_schedule["day"],
                        "date": day_date.isoformat(),
                        "session_type": session_info["session_type"],
                        "topic": session_info["topic"],
                        "content_url": session_info["content_url"],
                        "start_time": current_time.isoformat(),
                        "end_time": (current_time + timedelta(minutes=self.session_duration)).isoformat(),
                        "duration_minutes": self.session_duration,
                        "break_after_minutes": session_info.get("break_after", 0),
                        "status": "scheduled"
                    }
                    
                    scheduled_sessions.append(session)
                    session_id += 1
                    
                    # Update current_time with session duration + break
                    current_time += timedelta(
                        minutes=self.session_duration + session_info.get("break_after", 0)
                    )
            
            logger.info(f"Scheduled {len(scheduled_sessions)} sessions")
            return scheduled_sessions
        
        except Exception as e:
            logger.error(f"Error scheduling sessions: {str(e)}")
            raise
    
    def get_daily_sessions(
        self,
        scheduled_sessions: List[Dict[str, Any]],
        date: datetime
    ) -> List[Dict[str, Any]]:
        """
        Get all sessions for a specific date.
        
        Args:
            scheduled_sessions: List of all scheduled sessions
            date: Target date
        
        Returns:
            Sessions for the given date
        """
        target_date = date.date().isoformat()
        return [s for s in scheduled_sessions if s["date"] == target_date]
    
    def get_next_session(
        self,
        scheduled_sessions: List[Dict[str, Any]],
        from_datetime: datetime = None
    ) -> Dict[str, Any]:
        """
        Get next upcoming session.
        
        Args:
            scheduled_sessions: List of all scheduled sessions
            from_datetime: Search from this datetime (default: now)
        
        Returns:
            Next session or None
        """
        if from_datetime is None:
            from_datetime = datetime.utcnow()
        
        from_time = from_datetime.isoformat()
        
        pending_sessions = [
            s for s in scheduled_sessions
            if s["status"] == "scheduled" and s["start_time"] >= from_time
        ]
        
        return pending_sessions[0] if pending_sessions else None
    
    def reschedule_session(
        self,
        session: Dict[str, Any],
        new_start_time: datetime
    ) -> Dict[str, Any]:
        """
        Reschedule a session to a new time.
        
        Args:
            session: Session to reschedule
            new_start_time: New start time
        
        Returns:
            Updated session
        """
        try:
            updated_session = session.copy()
            updated_session["start_time"] = new_start_time.isoformat()
            
            new_end_time = new_start_time + timedelta(minutes=self.session_duration)
            updated_session["end_time"] = new_end_time.isoformat()
            updated_session["date"] = new_start_time.date().isoformat()
            
            logger.info(
                f"Session {session['session_id']} rescheduled to {new_start_time.isoformat()}"
            )
            
            return updated_session
        
        except Exception as e:
            logger.error(f"Error rescheduling session: {str(e)}")
            raise
    
    def optimize_schedule(
        self,
        scheduled_sessions: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Optimize schedule for better flow and reduce fatigue.
        
        Args:
            scheduled_sessions: Current scheduled sessions
        
        Returns:
            Optimized schedule
        """
        logger.info("Optimizing schedule...")
        
        # Group by date
        sessions_by_date = {}
        for session in scheduled_sessions:
            date = session["date"]
            if date not in sessions_by_date:
                sessions_by_date[date] = []
            sessions_by_date[date].append(session)
        
        # Optimize each day
        optimized = []
        for date in sorted(sessions_by_date.keys()):
            day_sessions = sessions_by_date[date]
            
            # Reorder: lecture -> break -> hands-on -> break
            lectures = [s for s in day_sessions if s["session_type"] == "lecture"]
            hands_on = [s for s in day_sessions if s["session_type"] == "hands-on"]
            other = [s for s in day_sessions if s["session_type"] not in ["lecture", "hands-on"]]
            
            ordered = lectures + hands_on + other
            optimized.extend(ordered)
        
        logger.info("Schedule optimized")
        return optimized
