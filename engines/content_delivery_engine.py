"""
Content Delivery Engine - Manages automatic content execution and delivery.
"""
import subprocess
import webbrowser
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path
from config.settings import Settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ContentDeliveryEngine:
    """Engine for automatic content delivery and execution."""
    
    def __init__(self):
        self.auto_play_enabled = Settings.content.AUTO_PLAY_ENABLED
        self.auto_play_delay = Settings.content.AUTO_PLAY_DELAY_SECONDS
        self.supported_formats = Settings.content.SUPPORTED_VIDEO_FORMATS
    
    def execute_session(
        self,
        session: Dict[str, Any],
        meeting_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute a training session.
        
        Args:
            session: Session to execute
            meeting_url: Teams meeting URL if available
        
        Returns:
            Session execution result
        """
        try:
            logger.info(f"Executing session {session['session_id']}: {session['topic']}")
            
            result = {
                "session_id": session["session_id"],
                "executed_at": datetime.utcnow().isoformat(),
                "status": "started",
                "content_started": False,
                "meeting_started": False
            }
            
            # Start Teams meeting if URL provided
            if meeting_url:
                self._open_teams_meeting(meeting_url)
                result["meeting_started"] = True
            
            # Deliver content based on type
            if session.get("content_url"):
                self._deliver_content(session["content_url"], session.get("session_type"))
                result["content_started"] = True
            
            logger.info(f"Session {session['session_id']} execution started")
            return result
        
        except Exception as e:
            logger.error(f"Error executing session: {str(e)}")
            raise
    
    def play_video_content(
        self,
        content_url: str,
        auto_play: bool = None
    ) -> bool:
        """
        Play video content.
        
        Args:
            content_url: URL or local path to video
            auto_play: Whether to auto-play (default from config)
        
        Returns:
            True if playback started successfully
        """
        try:
            if auto_play is None:
                auto_play = self.auto_play_enabled
            
            # Check if local file
            if content_url.startswith(("http://", "https://")):
                # Open in browser
                webbrowser.open(content_url)
                logger.info(f"Opening video in browser: {content_url}")
            else:
                # Local file
                file_path = Path(content_url)
                if file_path.exists():
                    self._play_local_video(str(file_path))
                    logger.info(f"Playing local video: {content_url}")
                else:
                    logger.warning(f"Video file not found: {content_url}")
                    return False
            
            return True
        
        except Exception as e:
            logger.error(f"Error playing video: {str(e)}")
            return False
    
    def _open_teams_meeting(self, meeting_url: str) -> bool:
        """
        Open Teams meeting.
        
        Args:
            meeting_url: Teams meeting URL
        
        Returns:
            True if meeting opened successfully
        """
        try:
            webbrowser.open(meeting_url)
            logger.info(f"Teams meeting opened: {meeting_url}")
            return True
        except Exception as e:
            logger.error(f"Error opening Teams meeting: {str(e)}")
            return False
    
    def _deliver_content(self, content_url: str, session_type: str = "lecture") -> bool:
        """
        Deliver content based on type.
        
        Args:
            content_url: Content URL or path
            session_type: Type of session (lecture, hands-on, etc.)
        
        Returns:
            True if content delivery started
        """
        if session_type == "lecture":
            return self.play_video_content(content_url)
        elif session_type == "hands-on":
            # For hands-on, might need to open a document or environment
            return self.play_video_content(content_url)
        else:
            return self.play_video_content(content_url)
    
    def _play_local_video(self, file_path: str) -> bool:
        """
        Play local video file using system default player.
        
        Args:
            file_path: Path to video file
        
        Returns:
            True if playback started
        """
        try:
            import os
            import platform
            
            if platform.system() == "Windows":
                os.startfile(file_path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.Popen(["open", file_path])
            else:  # Linux
                subprocess.Popen(["xdg-open", file_path])
            
            return True
        except Exception as e:
            logger.error(f"Error playing local video: {str(e)}")
            return False
    
    def send_session_reminder(
        self,
        session: Dict[str, Any],
        recipient_email: str
    ) -> bool:
        """
        Send session reminder to trainee.
        
        Args:
            session: Session details
            recipient_email: Recipient email address
        
        Returns:
            True if reminder sent
        """
        try:
            logger.info(f"Sending reminder for session {session['session_id']} to {recipient_email}")
            # TODO: Integrate with email service
            return True
        except Exception as e:
            logger.error(f"Error sending reminder: {str(e)}")
            return False
    
    def stream_content(
        self,
        content_url: str,
        session_duration_minutes: int
    ) -> Dict[str, Any]:
        """
        Stream content for specified duration.
        
        Args:
            content_url: Content URL
            session_duration_minutes: Duration of session
        
        Returns:
            Streaming metadata
        """
        return {
            "content_url": content_url,
            "duration_minutes": session_duration_minutes,
            "started_at": datetime.utcnow().isoformat(),
            "streaming": True
        }
