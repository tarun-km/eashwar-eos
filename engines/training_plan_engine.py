"""
Training Planning Engine - Creates day-wise training plans.
"""
import json
from datetime import datetime
from typing import List, Dict, Any
from config.settings import Settings
from utils.logger import setup_logger
from utils.date_utils import get_business_days, calculate_training_dates

logger = setup_logger(__name__)


class TrainingPlanEngine:
    """Engine for creating structured training plans."""
    
    def __init__(self):
        self.session_duration = Settings.training.DEFAULT_SESSION_DURATION
        self.break_duration = Settings.training.DEFAULT_BREAK_DURATION
        self.hands_on_start_day = Settings.training.DEFAULT_HANDS_ON_START_DAY
    
    def create_training_plan(
        self,
        num_trainees: int,
        duration_weeks: int,
        start_date: datetime,
        skill_area: str,
        training_type: str = "full-day",
        predefined_content: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a day-wise training plan based on parameters.
        
        Args:
            num_trainees: Number of trainees
            duration_weeks: Training duration in weeks
            start_date: Training start date
            skill_area: Skill/learning area
            training_type: "full-day" or "half-day"
            predefined_content: List of predefined content items
        
        Returns:
            Training plan dictionary with day-wise schedule
        """
        try:
            # Calculate training dates
            _, end_date = calculate_training_dates(start_date, duration_weeks)
            
            # Get business days
            training_days = get_business_days(start_date, end_date)
            
            logger.info(
                f"Creating training plan for {num_trainees} trainees, "
                f"{len(training_days)} business days, skill: {skill_area}"
            )
            
            # Initialize plan structure
            plan = {
                "skill_area": skill_area,
                "num_trainees": num_trainees,
                "duration_weeks": duration_weeks,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "training_type": training_type,
                "total_business_days": len(training_days),
                "daily_schedule": [],
                "statistics": {}
            }
            
            # Generate day-wise schedule
            if predefined_content is None:
                predefined_content = self._generate_default_content(skill_area)
            
            daily_schedule = self._generate_daily_schedule(
                training_days,
                predefined_content,
                training_type
            )
            
            plan["daily_schedule"] = daily_schedule
            plan["statistics"] = self._calculate_statistics(daily_schedule)
            
            logger.info(f"Training plan created successfully with {len(daily_schedule)} days")
            return plan
        
        except Exception as e:
            logger.error(f"Error creating training plan: {str(e)}")
            raise
    
    def _generate_daily_schedule(
        self,
        training_days: List[datetime],
        content: List[Dict[str, Any]],
        training_type: str
    ) -> List[Dict[str, Any]]:
        """
        Generate daily schedule from training days and content.
        
        Args:
            training_days: List of training days
            content: List of content items
            training_type: "full-day" or "half-day"
        
        Returns:
            List of daily schedules
        """
        daily_schedule = []
        content_index = 0
        session_count = 0
        
        for day_num, day in enumerate(training_days, 1):
            day_schedule = {
                "day": day_num,
                "date": day.isoformat(),
                "training_type": training_type,
                "sessions": []
            }
            
            if training_type == "full-day":
                sessions_per_day = 4  # 3 lectures + 1 hands-on or break
            else:
                sessions_per_day = 2  # 2 lectures or half-day
            
            for session_num in range(sessions_per_day):
                session_count += 1
                
                # Determine session type
                if day_num < self.hands_on_start_day:
                    session_type = "lecture"
                else:
                    session_type = "hands-on" if session_num % 2 == 0 else "lecture"
                
                # Get content
                if content_index < len(content):
                    topic = content[content_index]["topic"]
                    content_url = content[content_index].get("url", "")
                    content_index += 1
                else:
                    topic = f"Advanced {self._extract_skill_from_content(content)} - Session {session_count}"
                    content_url = ""
                
                session = {
                    "session_number": session_count,
                    "session_type": session_type,
                    "topic": topic,
                    "content_url": content_url,
                    "duration_minutes": self.session_duration,
                    "start_hour": 9 + (session_num * 1),  # Starting from 9 AM
                    "break_after": self.break_duration if session_num < sessions_per_day - 1 else 0
                }
                
                day_schedule["sessions"].append(session)
            
            daily_schedule.append(day_schedule)
        
        return daily_schedule
    
    def _generate_default_content(self, skill_area: str) -> List[Dict[str, Any]]:
        """
        Generate default content based on skill area.
        
        Args:
            skill_area: Skill/learning area
        
        Returns:
            List of default content items
        """
        default_topics = {
            "python": [
                {"topic": "Python Basics & Variables", "url": ""},
                {"topic": "Control Flow", "url": ""},
                {"topic": "Functions & Modules", "url": ""},
                {"topic": "OOP Concepts", "url": ""},
                {"topic": "File Handling", "url": ""},
            ],
            "web-development": [
                {"topic": "HTML & CSS Basics", "url": ""},
                {"topic": "JavaScript Fundamentals", "url": ""},
                {"topic": "DOM Manipulation", "url": ""},
                {"topic": "Responsive Design", "url": ""},
                {"topic": "React Basics", "url": ""},
            ],
            "data-science": [
                {"topic": "Data Analysis Basics", "url": ""},
                {"topic": "NumPy & Pandas", "url": ""},
                {"topic": "Data Visualization", "url": ""},
                {"topic": "Statistical Analysis", "url": ""},
                {"topic": "Machine Learning Intro", "url": ""},
            ],
            "default": [
                {"topic": "Introduction to the Course", "url": ""},
                {"topic": "Module 1 - Fundamentals", "url": ""},
                {"topic": "Module 2 - Core Concepts", "url": ""},
                {"topic": "Module 3 - Practical Applications", "url": ""},
                {"topic": "Module 4 - Advanced Topics", "url": ""},
            ]
        }
        
        return default_topics.get(skill_area.lower(), default_topics["default"])
    
    def _extract_skill_from_content(self, content: List[Dict[str, Any]]) -> str:
        """Extract skill name from content."""
        if content and len(content) > 0:
            topic = content[0].get("topic", "Skills")
            return topic.split("-")[0].strip()
        return "Skills"
    
    def _calculate_statistics(self, daily_schedule: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate statistics from daily schedule.
        
        Args:
            daily_schedule: Daily schedule list
        
        Returns:
            Statistics dictionary
        """
        total_sessions = 0
        lecture_sessions = 0
        hands_on_sessions = 0
        total_hours = 0
        
        for day in daily_schedule:
            for session in day["sessions"]:
                total_sessions += 1
                total_hours += session["duration_minutes"] / 60
                
                if session["session_type"] == "lecture":
                    lecture_sessions += 1
                elif session["session_type"] == "hands-on":
                    hands_on_sessions += 1
        
        return {
            "total_days": len(daily_schedule),
            "total_sessions": total_sessions,
            "lecture_sessions": lecture_sessions,
            "hands_on_sessions": hands_on_sessions,
            "total_training_hours": round(total_hours, 2),
            "average_session_duration_minutes": round(total_hours * 60 / total_sessions, 1) if total_sessions > 0 else 0
        }
