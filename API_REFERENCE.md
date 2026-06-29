# API Reference

## TrainingOrchestrationSystem

Main orchestrator class that coordinates all training operations.

### Initialization

```python
from orchestrator import TrainingOrchestrationSystem

system = TrainingOrchestrationSystem()
```

### Methods

#### `create_training_batch()`

Create a new training batch with automatic plan generation.

**Signature:**
```python
def create_training_batch(
    batch_name: str,
    num_trainees: int,
    duration_weeks: int,
    start_date: datetime,
    skill_area: str,
    training_type: str = "full-day",
    trainee_list: List[Dict[str, str]] = None
) -> Dict[str, Any]
```

**Parameters:**
- `batch_name` (str): Unique name for the batch
- `num_trainees` (int): Number of trainees in batch
- `duration_weeks` (int): Training duration in weeks
- `start_date` (datetime): Training start date
- `skill_area` (str): Skill area ('python', 'web-development', 'data-science')
- `training_type` (str): 'full-day' or 'half-day'
- `trainee_list` (List): Optional list of trainee dicts with 'name' and 'email'

**Returns:**
```python
{
    "batch_id": 1,
    "batch_name": "Python Training",
    "status": "created",
    "plan": {...},
    "scheduled_sessions": 40,
    "num_trainees": 20,
    "created_at": "2024-01-15T10:30:00"
}
```

**Example:**
```python
batch = system.create_training_batch(
    batch_name="Python Q1 2024",
    num_trainees=20,
    duration_weeks=8,
    start_date=datetime(2024, 1, 8),
    skill_area="python",
    trainee_list=[
        {"name": "John Doe", "email": "john@example.com"},
        {"name": "Jane Smith", "email": "jane@example.com"},
    ]
)
```

---

#### `schedule_batch_with_teams_meetings()`

Create Teams meetings for all sessions in a batch.

**Signature:**
```python
def schedule_batch_with_teams_meetings(
    batch_id: int,
    organizer_email: str
) -> Dict[str, Any]
```

**Parameters:**
- `batch_id` (int): ID of the batch
- `organizer_email` (str): Email of meeting organizer

**Returns:**
```python
{
    "batch_id": 1,
    "meetings_created": 40,
    "created_at": "2024-01-15T10:35:00"
}
```

**Example:**
```python
result = system.schedule_batch_with_teams_meetings(
    batch_id=1,
    organizer_email="trainer@company.com"
)
```

---

#### `execute_scheduled_session()`

Execute a scheduled training session.

**Signature:**
```python
def execute_scheduled_session(session_id: int) -> Dict[str, Any]
```

**Parameters:**
- `session_id` (int): ID of the session to execute

**Returns:**
```python
{
    "session_id": 1,
    "executed_at": "2024-01-15T10:40:00",
    "status": "started",
    "content_started": True,
    "meeting_started": True
}
```

**Example:**
```python
result = system.execute_scheduled_session(session_id=1)
```

---

#### `generate_session_assessment()`

Generate assessment for a training session.

**Signature:**
```python
def generate_session_assessment(session_id: int) -> Dict[str, Any]
```

**Parameters:**
- `session_id` (int): ID of the session

**Returns:**
```python
{
    "assessment_id": "ASSESS_1705315234000",
    "topic": "Python Basics",
    "num_questions": 5,
    "questions": [
        {
            "id": 1,
            "type": "multiple-choice",
            "question": "What is a variable?",
            "options": [...],
            "difficulty": "mixed"
        },
        ...
    ],
    "time_limit_minutes": 15,
    "passing_score": 70,
    "created_at": "2024-01-15T10:45:00",
    "status": "created"
}
```

**Example:**
```python
assessment = system.generate_session_assessment(session_id=1)
```

---

#### `record_trainee_attendance()`

Record trainee attendance for a session.

**Signature:**
```python
def record_trainee_attendance(
    session_id: int,
    trainee_id: int,
    joined_time: datetime,
    left_time: Optional[datetime] = None
) -> Dict[str, Any]
```

**Parameters:**
- `session_id` (int): Session ID
- `trainee_id` (int): Trainee ID
- `joined_time` (datetime): Time when trainee joined
- `left_time` (datetime, optional): Time when trainee left

**Returns:**
```python
{
    "session_id": 1,
    "trainee_id": 1,
    "joined_time": "2024-01-15T09:00:00",
    "left_time": "2024-01-15T09:38:00",
    "status": "present",
    "marked_at": "2024-01-15T09:40:00"
}
```

**Example:**
```python
from datetime import datetime, timedelta

now = datetime.now()
attendance = system.record_trainee_attendance(
    session_id=1,
    trainee_id=1,
    joined_time=now,
    left_time=now + timedelta(minutes=38)
)
```

---

#### `get_batch_summary()`

Get comprehensive batch summary.

**Signature:**
```python
def get_batch_summary(batch_id: int) -> Dict[str, Any]
```

**Parameters:**
- `batch_id` (int): Batch ID

**Returns:**
```python
{
    "batch_id": 1,
    "batch_name": "Python Training",
    "skill_area": "python",
    "training_type": "full-day",
    "status": "created",
    "start_date": "2024-01-08T00:00:00",
    "end_date": "2024-02-19T00:00:00",
    "num_trainees": 20,
    "total_sessions": 40,
    "completed_sessions": 0,
    "trainees": [
        {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com",
            "registered": False
        },
        ...
    ]
}
```

**Example:**
```python
summary = system.get_batch_summary(batch_id=1)
```

---

#### `close()`

Close database connection and cleanup resources.

**Signature:**
```python
def close() -> None
```

**Example:**
```python
system.close()
```

---

## TrainingPlanEngine

Engine for creating structured training plans.

### Initialization

```python
from engines.training_plan_engine import TrainingPlanEngine

engine = TrainingPlanEngine()
```

### Methods

#### `create_training_plan()`

Create day-wise training plan.

**Signature:**
```python
def create_training_plan(
    num_trainees: int,
    duration_weeks: int,
    start_date: datetime,
    skill_area: str,
    training_type: str = "full-day",
    predefined_content: List[Dict[str, Any]] = None
) -> Dict[str, Any]
```

**Returns:**
```python
{
    "skill_area": "python",
    "num_trainees": 20,
    "duration_weeks": 8,
    "start_date": "2024-01-08T00:00:00",
    "end_date": "2024-02-29T00:00:00",
    "training_type": "full-day",
    "total_business_days": 40,
    "daily_schedule": [
        {
            "day": 1,
            "date": "2024-01-08T00:00:00",
            "training_type": "full-day",
            "sessions": [
                {
                    "session_number": 1,
                    "session_type": "lecture",
                    "topic": "Python Basics",
                    "content_url": "",
                    "duration_minutes": 40,
                    "start_hour": 9,
                    "break_after": 10
                },
                ...
            ]
        },
        ...
    ],
    "statistics": {
        "total_days": 40,
        "total_sessions": 160,
        "lecture_sessions": 80,
        "hands_on_sessions": 80,
        "total_training_hours": 106.67,
        "average_session_duration_minutes": 40.0
    }
}
```

---

## ContentScheduler

Scheduler for content delivery sessions.

### Initialization

```python
from engines.content_scheduler import ContentScheduler

scheduler = ContentScheduler()
```

### Methods

#### `schedule_sessions_from_plan()`

Create detailed session schedule from training plan.

**Signature:**
```python
def schedule_sessions_from_plan(
    plan: Dict[str, Any],
    start_time_hour: int = 9
) -> List[Dict[str, Any]]
```

**Returns:**
```python
[
    {
        "session_id": 1,
        "day": 1,
        "date": "2024-01-08",
        "session_type": "lecture",
        "topic": "Python Basics",
        "content_url": "",
        "start_time": "2024-01-08T09:00:00",
        "end_time": "2024-01-08T09:40:00",
        "duration_minutes": 40,
        "break_after_minutes": 10,
        "status": "scheduled"
    },
    ...
]
```

---

#### `get_daily_sessions()`

Get all sessions for a specific date.

**Signature:**
```python
def get_daily_sessions(
    scheduled_sessions: List[Dict[str, Any]],
    date: datetime
) -> List[Dict[str, Any]]
```

---

#### `get_next_session()`

Get next upcoming session.

**Signature:**
```python
def get_next_session(
    scheduled_sessions: List[Dict[str, Any]],
    from_datetime: datetime = None
) -> Dict[str, Any]
```

---

## ContentDeliveryEngine

Engine for automatic content execution and delivery.

### Initialization

```python
from engines.content_delivery_engine import ContentDeliveryEngine

engine = ContentDeliveryEngine()
```

### Methods

#### `execute_session()`

Execute a training session.

**Signature:**
```python
def execute_session(
    session: Dict[str, Any],
    meeting_url: Optional[str] = None
) -> Dict[str, Any]
```

**Returns:**
```python
{
    "session_id": 1,
    "executed_at": "2024-01-15T09:00:00",
    "status": "started",
    "content_started": True,
    "meeting_started": True
}
```

---

#### `play_video_content()`

Play video content.

**Signature:**
```python
def play_video_content(
    content_url: str,
    auto_play: bool = None
) -> bool
```

---

## AssessmentEngine

Engine for generating and managing assessments.

### Initialization

```python
from engines.assessment_engine import AssessmentEngine

engine = AssessmentEngine()
```

### Methods

#### `generate_assessment()`

Generate assessment questions for a session.

**Signature:**
```python
def generate_assessment(
    session_topic: str,
    num_questions: int = None,
    difficulty: str = "mixed"
) -> Dict[str, Any]
```

---

#### `submit_assessment()`

Submit and score assessment.

**Signature:**
```python
def submit_assessment(
    assessment: Dict[str, Any],
    responses: List[Dict[str, Any]],
    time_taken_minutes: int
) -> Dict[str, Any]
```

**Returns:**
```python
{
    "assessment_id": "ASSESS_1705315234000",
    "responses": [...],
    "score": 85.5,
    "passed": True,
    "time_taken_minutes": 12,
    "feedback": "Good job! You have strong understanding...",
    "submitted_at": "2024-01-15T10:00:00",
    "status": "completed"
}
```

---

## AttendanceTracker

Tracker for trainee attendance and participation.

### Initialization

```python
from engines.attendance_tracker import AttendanceTracker

tracker = AttendanceTracker()
```

### Methods

#### `mark_attendance()`

Mark trainee attendance for a session.

**Signature:**
```python
def mark_attendance(
    session_id: int,
    trainee_id: int,
    joined_time: datetime,
    left_time: Optional[datetime] = None
) -> Dict[str, Any]
```

---

#### `calculate_session_attendance()`

Calculate attendance percentage for a session.

**Signature:**
```python
def calculate_session_attendance(
    session_duration_minutes: int,
    attendance_records: List[Dict[str, Any]]
) -> Dict[str, Any]
```

---

## TeamsIntegration

Integration with Microsoft Teams API.

### Initialization

```python
from integrations.teams_integration import TeamsIntegration

teams = TeamsIntegration()
```

### Methods

#### `create_meeting()`

Create Teams meeting for a session.

**Signature:**
```python
def create_meeting(
    session_id: int,
    topic: str,
    start_time: datetime,
    attendees: List[str],
    organizer_email: str
) -> Dict[str, Any]
```

---

#### `send_meeting_invite()`

Send meeting invite to attendee.

**Signature:**
```python
def send_meeting_invite(
    meeting: Dict[str, Any],
    attendee_email: str
) -> bool
```

---

## Database Models

### TrainingBatch

```python
class TrainingBatch(Base):
    __tablename__ = "training_batches"
    
    id: int                    # Primary key
    batch_name: str            # Unique batch name
    num_trainees: int          # Number of trainees
    duration_weeks: int        # Duration in weeks
    start_date: datetime       # Start date
    end_date: datetime         # End date
    skill_area: str            # Skill area
    training_type: str         # "full-day" or "half-day"
    status: str                # Status
    created_at: datetime       # Creation timestamp
    updated_at: datetime       # Last update timestamp
```

### Trainee

```python
class Trainee(Base):
    __tablename__ = "trainees"
    
    id: int                    # Primary key
    batch_id: int              # Foreign key to TrainingBatch
    name: str                  # Trainee name
    email: str                 # Email address
    teams_user_id: str         # Teams user ID
    is_registered: bool        # Registration status
    created_at: datetime       # Creation timestamp
```

### TrainingSession

```python
class TrainingSession(Base):
    __tablename__ = "training_sessions"
    
    id: int                    # Primary key
    batch_id: int              # Foreign key to TrainingBatch
    session_number: int        # Session number
    day_number: int            # Day number
    start_time: datetime       # Session start time
    end_time: datetime         # Session end time
    session_type: str          # Type of session
    topic: str                 # Session topic
    content_url: str           # Content URL
    teams_meeting_id: str      # Teams meeting ID
    teams_meeting_url: str     # Teams meeting URL
    status: str                # Session status
    is_executed: bool          # Whether executed
    created_at: datetime       # Creation timestamp
    updated_at: datetime       # Last update timestamp
```

### AttendanceLog

```python
class AttendanceLog(Base):
    __tablename__ = "attendance_logs"
    
    id: int                    # Primary key
    session_id: int            # Foreign key to TrainingSession
    trainee_id: int            # Foreign key to Trainee
    joined_time: datetime      # Join time
    left_time: datetime        # Leave time
    duration_minutes: int      # Duration attended
    attendance_percentage: float   # Attendance %
    status: str                # Attendance status
    created_at: datetime       # Log creation time
```

### Assessment

```python
class Assessment(Base):
    __tablename__ = "assessments"
    
    id: int                    # Primary key
    session_id: int            # Foreign key to TrainingSession
    trainee_id: int            # Foreign key to Trainee
    questions_json: str        # Questions as JSON
    responses_json: str        # Responses as JSON
    score: float               # Score
    passed: bool               # Passed/Failed
    time_taken_minutes: int    # Time taken
    status: str                # Assessment status
    created_at: datetime       # Creation time
    completed_at: datetime     # Completion time
```

---

**Last Updated**: 2024
