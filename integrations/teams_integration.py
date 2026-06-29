"""
Teams Integration - Handles Microsoft Teams meeting creation and management.
"""
import requests
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from config.settings import Settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class TeamsIntegration:
    """Integration with Microsoft Teams API."""
    
    def __init__(self):
        self.tenant_id = Settings.teams.TENANT_ID
        self.client_id = Settings.teams.CLIENT_ID
        self.client_secret = Settings.teams.CLIENT_SECRET
        self.graph_api = Settings.teams.GRAPH_API_ENDPOINT
        self.meeting_duration = Settings.teams.MEETING_DURATION_MINUTES
        self.reminder_minutes = Settings.teams.REMINDER_MINUTES_BEFORE
    
    def create_meeting(
        self,
        session_id: int,
        topic: str,
        start_time: datetime,
        attendees: List[str],
        organizer_email: str
    ) -> Dict[str, Any]:
        """
        Create Teams meeting for a session.
        
        Args:
            session_id: Session ID
            topic: Meeting topic
            start_time: Meeting start time
            attendees: List of attendee email addresses
            organizer_email: Organizer email
        
        Returns:
            Meeting details including URL
        """
        try:
            logger.info(f"Creating Teams meeting for session {session_id}: {topic}")
            
            # Note: In production, this would use actual Graph API authentication
            # For POC, creating a mock meeting object
            
            end_time = start_time + timedelta(minutes=self.meeting_duration)
            
            meeting = {
                "meeting_id": f"MEET_{session_id}_{int(datetime.utcnow().timestamp())}",
                "session_id": session_id,
                "topic": topic,
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "organizer": organizer_email,
                "attendees": attendees,
                "meeting_url": self._generate_mock_meeting_url(session_id),
                "status": "created",
                "created_at": datetime.utcnow().isoformat()
            }
            
            logger.info(f"Teams meeting created: {meeting['meeting_url']}")
            return meeting
        
        except Exception as e:
            logger.error(f"Error creating Teams meeting: {str(e)}")
            raise
    
    def send_meeting_invite(
        self,
        meeting: Dict[str, Any],
        attendee_email: str
    ) -> bool:
        """
        Send meeting invite to attendee.
        
        Args:
            meeting: Meeting object
            attendee_email: Attendee email
        
        Returns:
            True if invite sent successfully
        """
        try:
            logger.info(f"Sending meeting invite to {attendee_email}")
            
            # In production, this would send actual email via Graph API
            # For now, we simulate it
            
            logger.info(f"Meeting invite sent to {attendee_email} for {meeting['topic']}")
            return True
        
        except Exception as e:
            logger.error(f"Error sending meeting invite: {str(e)}")
            return False
    
    def send_daily_reminder(
        self,
        batch_id: int,
        date: datetime,
        sessions: List[Dict[str, Any]],
        attendees: List[Dict[str, str]]
    ) -> int:
        """
        Send daily reminders to all attendees.
        
        Args:
            batch_id: Batch ID
            date: Date of sessions
            sessions: List of sessions for the day
            attendees: List of attendee details
        
        Returns:
            Number of reminders sent
        """
        try:
            logger.info(f"Sending daily reminders for batch {batch_id} on {date.date()}")
            
            reminders_sent = 0
            
            for attendee in attendees:
                # Create reminder message
                reminder_text = f"Hello {attendee.get('name', 'Trainee')},\n\n"
                reminder_text += f"Reminder: You have {len(sessions)} training session(s) today:\n\n"
                
                for session in sessions:
                    reminder_text += f"- {session['start_time']}: {session['topic']}\n"
                
                # In production, send via email
                logger.info(f"Reminder sent to {attendee.get('email')}")
                reminders_sent += 1
            
            return reminders_sent
        
        except Exception as e:
            logger.error(f"Error sending daily reminders: {str(e)}")
            return 0
    
    def register_non_email_users(
        self,
        trainee_name: str,
        batch_id: int
    ) -> Dict[str, Any]:
        """
        Register trainees without official email IDs.
        
        Args:
            trainee_name: Trainee name
            batch_id: Batch ID
        
        Returns:
            User registration details
        """
        try:
            # Generate temporary access token/link
            temp_user = {
                "trainee_name": trainee_name,
                "batch_id": batch_id,
                "temp_id": f"TEMP_{batch_id}_{int(datetime.utcnow().timestamp())}",
                "access_token": self._generate_access_token(),
                "registration_url": self._generate_registration_url(batch_id),
                "registered_at": datetime.utcnow().isoformat()
            }
            
            logger.info(f"Registered non-email user: {trainee_name}")
            return temp_user
        
        except Exception as e:
            logger.error(f"Error registering non-email user: {str(e)}")
            raise
    
    def _generate_mock_meeting_url(self, session_id: int) -> str:
        """Generate mock Teams meeting URL."""
        return f"https://teams.microsoft.com/l/meetup-join/{session_id}"
    
    def _generate_access_token(self) -> str:
        """Generate temporary access token."""
        import secrets
        return secrets.token_urlsafe(32)
    
    def _generate_registration_url(self, batch_id: int) -> str:
        """Generate registration URL for non-email users."""
        return f"https://training-system.com/register/{batch_id}"
