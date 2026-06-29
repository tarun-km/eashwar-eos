# Architecture Overview

## System Design

The Training Orchestration System is built as a modular, agent-based architecture where each component handles a specific responsibility in the training pipeline.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                  Orchestration Layer                            │
│            (TrainingOrchestrationSystem)                        │
│  - Coordinates all components                                  │
│  - Manages workflow execution                                  │
│  - Handles cross-component communication                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┼─────────────┐
                │             │             │
        ┌───────▼──────┐  ┌──▼────────┐  ┌─▼────────────┐
        │   Engines    │  │ Database  │  │ Integrations│
        └──────────────┘  └───────────┘  └──────────────┘
                │                │              │
        ┌───────┴────────┐       │         ┌────▼─────┐
        │                │       │         │  Teams   │
    ┌───▼────┐   ┌──────▼───┐   │         │ API      │
    │Training│   │ Content  │   │         └──────────┘
    │ Plan   │   │Scheduler │   │
    │Engine  │   │          │   │
    └────────┘   └──────────┘   │
                                 │
    ┌──────────┐   ┌──────────┐  │
    │Content   │   │Assessment│  │
    │Delivery  │   │Engine    │  │
    │Engine    │   │          │  │
    └──────────┘   └──────────┘  │
                                 │
    ┌────────────────────────────▼────────┐
    │  Database Layer                    │
    │  - Models (SQLAlchemy)            │
    │  - Persistent Storage             │
    │  - Transaction Management         │
    └───────────────────────────────────┘
```

## Component Breakdown

### 1. **Orchestration Layer** (`orchestrator.py`)

**Responsibility**: Central coordinator for all training operations.

**Key Methods**:
- `create_training_batch()` - Initialize batch with plan
- `schedule_batch_with_teams_meetings()` - Create Teams meetings
- `execute_scheduled_session()` - Run session
- `record_trainee_attendance()` - Track attendance
- `generate_session_assessment()` - Create assessment

**Flow**:
```
create_training_batch()
├── TrainingPlanEngine.create_training_plan()
├── ContentScheduler.schedule_sessions_from_plan()
├── DatabaseManager.add_batch()
├── DatabaseManager.add_trainees()
└── DatabaseManager.add_sessions()
```

### 2. **Training Plan Engine** (`engines/training_plan_engine.py`)

**Responsibility**: Generate day-wise training plans.

**Algorithm**:
1. Calculate total business days (excluding weekends)
2. Map content topics to days
3. Distribute sessions across days
4. Determine session types (lecture/hands-on based on day)
5. Calculate statistics

**Inputs**:
- Number of trainees
- Training duration
- Start date
- Skill area
- Predefined content

**Outputs**:
- Daily schedule with sessions
- Statistics (total hours, session count, etc.)

### 3. **Content Scheduler** (`engines/content_scheduler.py`)

**Responsibility**: Create detailed timing schedule for sessions.

**Features**:
- Map scheduled sessions to specific times
- Handle breaks between sessions
- Generate daily time slots
- Optimize schedule for better flow
- Support reschedule scenarios

**Session Structure**:
```
├── 09:00-09:40 AM: Lecture (Session 1)
├── 09:40-09:50 AM: Break
├── 09:50-10:30 AM: Lecture (Session 2)
├── 10:30-10:40 AM: Break
├── 10:40-11:20 AM: Hands-on (Session 3)
├── 11:20-11:30 AM: Break
└── 11:30-12:10 PM: Hands-on (Session 4)
```

### 4. **Content Delivery Engine** (`engines/content_delivery_engine.py`)

**Responsibility**: Execute and deliver content automatically.

**Features**:
- Automatic video playback
- Teams meeting joining
- Content type detection (video, document, etc.)
- Session reminders
- Auto-play capabilities

**Supported Formats**: MP4, MKV, MOV, AVI, URLs

### 5. **Assessment Engine** (`engines/assessment_engine.py`)

**Responsibility**: Generate and manage assessments.

**Features**:
- Auto-generate questions by topic
- Multiple question types (MCQ, T/F, Short Answer)
- Score calculation
- Passing/failing determination
- Feedback generation

**Question Generation**:
```python
Assessment
├── MCQ (Multiple Choice)
├── True/False
└── Short Answer
```

### 6. **Attendance Tracker** (`engines/attendance_tracker.py`)

**Responsibility**: Track and manage attendance.

**Metrics**:
- Join/leave times
- Session duration
- Attendance percentage
- Daily attendance logs
- Per-trainee history

**Status Types**: Present, Absent, Late, Left-Early

### 7. **Teams Integration** (`integrations/teams_integration.py`)

**Responsibility**: Microsoft Teams API integration.

**Features**:
- Meeting creation
- Invite distribution
- Daily reminders
- Non-email user registration
- Mock API for POC

### 8. **Database Layer** (`database/`)

**Models**:
- `TrainingBatch`: Cohort metadata
- `Trainee`: Participant information
- `TrainingSession`: Individual sessions
- `TrainingPlan`: Schedule plan
- `Assessment`: Quiz records
- `AttendanceLog`: Attendance records
- `Meeting`: Teams meeting records
- `ContentResource`: Content library

**Features**:
- SQLAlchemy ORM
- SQLite (default) or PostgreSQL
- Automatic initialization
- Transaction management

## Data Flow

### Training Creation Flow

```
User Input
    │
    ├─→ TrainingPlanEngine
    │   └─→ Generate day-wise plan
    │
    ├─→ ContentScheduler
    │   └─→ Create detailed schedule
    │
    ├─→ Database
    │   ├─→ Save Batch
    │   ├─→ Save Trainees
    │   └─→ Save Sessions
    │
    └─→ TeamsIntegration
        └─→ Create Meetings
```

### Session Execution Flow

```
Scheduled Time
    │
    ├─→ ContentDeliveryEngine
    │   ├─→ Open Teams Meeting
    │   └─→ Play Video Content
    │
    ├─→ AttendanceTracker
    │   └─→ Log attendance
    │
    ├─→ AssessmentEngine
    │   └─→ Post-session assessment
    │
    └─→ Database
        └─→ Update session status
```

## Module Dependencies

```
orchestrator.py
├── TrainingPlanEngine
├── ContentScheduler
├── ContentDeliveryEngine
├── AssessmentEngine
├── AttendanceTracker
├── TeamsIntegration
└── DatabaseManager

DatabaseManager
├── SQLAlchemy Engine
└── Models (database.models)

All Engines
└── Logger (utils.logger)
└── Settings (config.settings)
```

## Configuration Hierarchy

```
Settings (config.settings.py)
├── TrainingConfig
│   ├── Session Duration (40 min)
│   ├── Break Duration (10 min)
│   └── Hands-on Start Day (day 3)
├── DatabaseConfig
├── TeamsConfig
├── ContentConfig
├── AssessmentConfig
└── AttendanceConfig
```

## Extension Points

### 1. Add New Session Type
```python
# In TrainingPlanEngine._generate_daily_schedule()
if day_num < self.hands_on_start_day:
    session_type = "lecture"
elif day_num < self.assessment_start_day:  # NEW
    session_type = "project"
else:
    session_type = "assessment"
```

### 2. Add Email Notifications
```python
# In ContentDeliveryEngine
def send_session_reminder(self, session, recipient_email):
    # Integrate email service
    pass
```

### 3. Add Custom Content Provider
```python
# Create new engine
class CustomContentEngine:
    def get_content_for_topic(self, topic):
        # Fetch from external API
        pass
```

### 4. Add Analytics
```python
# Create new module
class AnalyticsEngine:
    def generate_batch_report(self, batch_id):
        # Analyze all data
        pass
```

## Performance Considerations

1. **Database Indexing**: Sessions indexed by batch_id, date, and status
2. **Lazy Loading**: Relationships use lazy='select' for controlled loading
3. **Batch Operations**: Insert multiple records in single transaction
4. **Caching**: Plan cache can be implemented for repeated queries
5. **Async Operations**: Future enhancement for parallel meeting creation

## Error Handling

- All components use try-except with logging
- Database rollback on transaction failure
- Graceful degradation (e.g., meeting creation failure doesn't block session)
- Error logging to file and console

## Testing Strategy

```
tests/
├── test_training_plan_engine.py
├── test_content_scheduler.py
├── test_assessment_engine.py
├── test_attendance_tracker.py
├── test_orchestrator.py
└── test_integration.py
```

## Deployment Architecture

```
Production Deployment
├── Web Server (Flask/FastAPI)
├── Database (PostgreSQL)
├── Cache (Redis)
├── Job Queue (Celery)
│   ├── Session Execution Jobs
│   ├── Reminder Jobs
│   └── Assessment Jobs
├── Email Service (SendGrid/AWS SES)
└── Teams Integration (OAuth2)
```

## Security Considerations

- Teams API credentials in .env (never in code)
- Database connections use connection pooling
- Input validation for all user inputs
- Trainee data encryption at rest (future)
- Role-based access control (future)

## Scalability

**Current (POC)**:
- Single threaded
- SQLite database
- ~100 trainees per batch
- Manual session execution

**Future (Production)**:
- Multi-threaded session execution
- PostgreSQL with replication
- 1000+ trainees per batch
- Automated scheduler (APScheduler/Celery Beat)
- Load balancer for web API
- CDN for video content

---

**Last Updated**: 2024
