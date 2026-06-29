"""
Attendance Tracker - Tracks trainee attendance and session duration.
"""
from datetime import datetime
from typing import Dict, Any, List, Optional
from config.settings import Settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class AttendanceTracker:
    """Tracks trainee attendance and participation."""
    
    def __init__(self):
        self.min_attendance_percentage = Settings.attendance.MINIMUM_SESSION_DURATION_PERCENTAGE
        self.daily_log_enabled = Settings.attendance.DAILY_LOG_ENABLED
    
    def mark_attendance(
        self,
        session_id: int,
        trainee_id: int,
        joined_time: datetime,
        left_time: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Mark trainee attendance for a session.
        
        Args:
            session_id: Session ID
            trainee_id: Trainee ID
            joined_time: Time when trainee joined
            left_time: Time when trainee left
        
        Returns:
            Attendance record
        """
        try:
            logger.info(f"Marking attendance: Session {session_id}, Trainee {trainee_id}")
            
            attendance = {
                "session_id": session_id,
                "trainee_id": trainee_id,
                "joined_time": joined_time.isoformat() if isinstance(joined_time, datetime) else joined_time,
                "left_time": left_time.isoformat() if isinstance(left_time, datetime) else left_time,
                "status": "present" if left_time else "in-session",
                "marked_at": datetime.utcnow().isoformat()
            }
            
            return attendance
        
        except Exception as e:
            logger.error(f"Error marking attendance: {str(e)}")
            raise
    
    def calculate_session_attendance(
        self,
        session_duration_minutes: int,
        attendance_records: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Calculate attendance percentage for a session.
        
        Args:
            session_duration_minutes: Total session duration
            attendance_records: List of trainee attendance records
        
        Returns:
            Session attendance summary
        """
        try:
            summary = {
                "total_duration_minutes": session_duration_minutes,
                "total_attendees": len(attendance_records),
                "present_count": 0,
                "absent_count": 0,
                "late_count": 0,
                "attendance_details": []
            }
            
            for record in attendance_records:
                if record["status"] == "present":
                    summary["present_count"] += 1
                elif record["status"] == "absent":
                    summary["absent_count"] += 1
                elif record["status"] == "late":
                    summary["late_count"] += 1
                
                summary["attendance_details"].append({
                    "trainee_id": record["trainee_id"],
                    "status": record["status"],
                    "attended_percentage": self._calculate_attendance_percentage(
                        record.get("duration_minutes", 0),
                        session_duration_minutes
                    )
                })
            
            summary["attendance_rate"] = (
                (summary["present_count"] / summary["total_attendees"] * 100)
                if summary["total_attendees"] > 0 else 0
            )
            
            return summary
        
        except Exception as e:
            logger.error(f"Error calculating session attendance: {str(e)}")
            raise
    
    def generate_daily_attendance_log(
        self,
        batch_id: int,
        date: datetime,
        sessions: List[Dict[str, Any]],
        attendance_data: Dict[int, List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
        """
        Generate daily attendance log.
        
        Args:
            batch_id: Batch ID
            date: Date of training
            sessions: List of sessions for the day
            attendance_data: Attendance data keyed by session ID
        
        Returns:
            Daily attendance log
        """
        try:
            logger.info(f"Generating daily attendance log for batch {batch_id} on {date.date()}")
            
            daily_log = {
                "batch_id": batch_id,
                "date": date.date().isoformat(),
                "total_sessions": len(sessions),
                "sessions": []
            }
            
            total_present = 0
            total_absent = 0
            
            for session in sessions:
                session_id = session["session_id"]
                records = attendance_data.get(session_id, [])
                
                session_summary = self.calculate_session_attendance(
                    session["duration_minutes"],
                    records
                )
                
                total_present += session_summary["present_count"]
                total_absent += session_summary["absent_count"]
                
                daily_log["sessions"].append({
                    "session_id": session_id,
                    "topic": session["topic"],
                    "attendance_summary": session_summary
                })
            
            daily_log["daily_summary"] = {
                "total_present": total_present,
                "total_absent": total_absent,
                "generated_at": datetime.utcnow().isoformat()
            }
            
            return daily_log
        
        except Exception as e:
            logger.error(f"Error generating daily attendance log: {str(e)}")
            raise
    
    def get_trainee_attendance_history(
        self,
        trainee_id: int,
        attendance_records: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Get attendance history for a trainee.
        
        Args:
            trainee_id: Trainee ID
            attendance_records: All attendance records
        
        Returns:
            Trainee attendance history
        """
        trainee_records = [
            r for r in attendance_records
            if r["trainee_id"] == trainee_id
        ]
        
        total_sessions = len(trainee_records)
        present_sessions = len([r for r in trainee_records if r["status"] == "present"])
        attendance_percentage = (
            (present_sessions / total_sessions * 100) if total_sessions > 0 else 0
        )
        
        return {
            "trainee_id": trainee_id,
            "total_sessions": total_sessions,
            "sessions_attended": present_sessions,
            "sessions_missed": total_sessions - present_sessions,
            "attendance_percentage": round(attendance_percentage, 2),
            "records": trainee_records
        }
    
    def _calculate_attendance_percentage(
        self,
        attended_minutes: int,
        total_minutes: int
    ) -> float:
        """
        Calculate attendance percentage.
        
        Args:
            attended_minutes: Minutes attended
            total_minutes: Total session minutes
        
        Returns:
            Attendance percentage
        """
        if total_minutes == 0:
            return 0.0
        
        percentage = (attended_minutes / total_minutes) * 100
        return round(min(percentage, 100), 2)  # Cap at 100%
