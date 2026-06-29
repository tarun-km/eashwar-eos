# Training Orchestration System

An AI-driven training orchestration platform that automatically plans, schedules, executes, and tracks training programs for internship batches.

## 🎯 Core Features (POC)

### 1. **Training Planning Engine**
- Automatic day-wise training plan generation based on:
  - Number of trainees
  - Training duration (weeks)
  - Start date
  - Skill/learning area
- Generates structured content delivery schedule from predefined content

### 2. **Content Scheduling**
- Structured session scheduling (~40 minutes per session)
- Break management (~10 minutes between sessions)
- Support for:
  - Full-day training (4 sessions/day)
  - Half-day training (2 sessions/day)
- Mix of lecture and hands-on sessions (after initial ramp-up days)

### 3. **Automated Calendar & Session Management**
- Automatic Teams meeting creation and scheduling
- Meeting invite distribution to all trainees
- Daily reminder notifications
- Support for users without official email IDs

### 4. **Auto Content Delivery (Execution Layer)**
- Automatic session execution at scheduled times
- Video content playback
- Teams meeting integration
- Session flow management (lectures → hands-on)

### 5. **Assessment Engine**
- Automatic assessment generation based on session topics
- Question generation (multiple choice, true/false, short answer)
- Response collection and scoring
- Performance tracking

### 6. **Attendance & Tracking**
- Real-time attendance tracking
- Session duration monitoring
- Daily attendance logs
- Per-trainee attendance reports

### 7. **Rescheduling Capability** (Future Scope)
- Handle session rescheduling
- Conflict resolution
- Attendee notification

## 📁 Project Structure

```
employment-onboarding-system/
├── config/
│   ├── __init__.py
│   └── settings.py                 # Configuration management
├── database/
│   ├── __init__.py
│   ├── models.py                   # SQLAlchemy models
│   └── db_manager.py               # Database operations
├── engines/
│   ├── __init__.py
│   ├── training_plan_engine.py     # Plan generation
│   ├── content_scheduler.py        # Session scheduling
│   ├── content_delivery_engine.py  # Content execution
│   ├── assessment_engine.py        # Assessment management
│   └── attendance_tracker.py       # Attendance tracking
├── integrations/
│   ├── __init__.py
│   └── teams_integration.py        # Microsoft Teams API
├── utils/
│   ├── __init__.py
│   ├── logger.py                   # Logging utilities
│   └── date_utils.py               # Date/time utilities
├── orchestrator.py                 # Main orchestration system
├── main.py                         # Entry point
├── example_usage.py                # Demo and examples
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
└── README.md                       # This file
```

## 🚀 Quick Start

### Installation

1. **Clone the repository:**
```bash
cd employment-onboarding-system
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/Scripts/activate  # On Windows
# source venv/bin/activate    # On macOS/Linux
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Setup environment variables:**
```bash
cp .env.example .env
# Edit .env with your Teams API credentials
```

5. **Initialize database:**
```bash
python -c "from database.db_manager import DatabaseManager; DatabaseManager()"
```

### Running the System

#### Option 1: Interactive Mode
```bash
python main.py
```

#### Option 2: Run Demo
```bash
python example_usage.py
```

#### Option 3: Use as a Library
```python
from orchestrator import TrainingOrchestrationSystem
from datetime import datetime

system = TrainingOrchestrationSystem()

# Create training batch
batch = system.create_training_batch(
    batch_name="Python Training - Batch 001",
    num_trainees=20,
    duration_weeks=2,
    start_date=datetime.now(),
    skill_area="python",
    training_type="full-day"
)

# Schedule Teams meetings
system.schedule_batch_with_teams_meetings(
    batch_id=batch["batch_id"],
    organizer_email="trainer@example.com"
)

# Execute sessions, record attendance, etc.
system.close()
```

## 📊 Data Models

### Core Entities

- **TrainingBatch**: Represents a training cohort
- **Trainee**: Individual participant in a batch
- **TrainingSession**: Individual training session (lecture/hands-on/assessment)
- **TrainingPlan**: Day-wise training schedule
- **Assessment**: Quiz/assessment for trainees
- **AttendanceLog**: Attendance records per session
- **Meeting**: Teams meeting records
- **ContentResource**: Training content library

## 🔧 Key APIs

### TrainingOrchestrationSystem

```python
# Create batch with training plan
create_training_batch(
    batch_name, num_trainees, duration_weeks, 
    start_date, skill_area, training_type, trainee_list
)

# Schedule Teams meetings
schedule_batch_with_teams_meetings(batch_id, organizer_email)

# Execute session
execute_scheduled_session(session_id)

# Generate assessment
generate_session_assessment(session_id)

# Record attendance
record_trainee_attendance(session_id, trainee_id, joined_time, left_time)

# Get batch summary
get_batch_summary(batch_id)
```

### TrainingPlanEngine

```python
# Create training plan
create_training_plan(
    num_trainees, duration_weeks, start_date, 
    skill_area, training_type, predefined_content
)
```

### ContentScheduler

```python
# Schedule sessions from plan
schedule_sessions_from_plan(plan, start_time_hour)

# Get daily sessions
get_daily_sessions(scheduled_sessions, date)

# Get next session
get_next_session(scheduled_sessions, from_datetime)
```

### AssessmentEngine

```python
# Generate assessment
generate_assessment(session_topic, num_questions, difficulty)

# Submit assessment
submit_assessment(assessment, responses, time_taken_minutes)
```

### AttendanceTracker

```python
# Mark attendance
mark_attendance(session_id, trainee_id, joined_time, left_time)

# Calculate session attendance
calculate_session_attendance(session_duration_minutes, attendance_records)

# Generate daily log
generate_daily_attendance_log(batch_id, date, sessions, attendance_data)
```

## 🔌 Configuration

Edit `.env` file to configure:

```env
# Teams API
TEAMS_TENANT_ID=your-tenant-id
TEAMS_CLIENT_ID=your-client-id
TEAMS_CLIENT_SECRET=your-client-secret

# Database
DATABASE_URL=sqlite:///./training_system.db

# System
DEBUG=False
LOG_LEVEL=INFO
```

## 📝 Example Workflow

1. **Create Training Batch:**
```python
batch = system.create_training_batch(
    batch_name="Python Intensive",
    num_trainees=20,
    duration_weeks=8,
    start_date=datetime(2024, 1, 8),
    skill_area="python"
)
```

2. **Schedule Teams Meetings:**
```python
system.schedule_batch_with_teams_meetings(
    batch_id=1,
    organizer_email="trainer@company.com"
)
```

3. **Execute Session:**
```python
result = system.execute_scheduled_session(session_id=1)
```

4. **Record Attendance:**
```python
system.record_trainee_attendance(
    session_id=1,
    trainee_id=1,
    joined_time=datetime.now(),
    left_time=datetime.now() + timedelta(minutes=40)
)
```

5. **Generate Assessment:**
```python
assessment = system.generate_session_assessment(session_id=1)
```

## 🎓 Pre-configured Content

The system includes default content for skill areas:
- **Python**: Basics, Control Flow, OOP, Functions, File Handling
- **Web Development**: HTML/CSS, JavaScript, DOM, React, Responsive Design
- **Data Science**: Data Analysis, NumPy/Pandas, Visualization, ML Intro

Custom content can be added via the `ContentResource` model.

## 📊 Database

- **SQLite** (default): For development/testing
- **PostgreSQL**: For production (configure in .env)

Database is automatically initialized on first run.

## 🪵 Logging

All operations are logged to `logs/` directory with daily log files:
- Console: INFO level
- File: DEBUG level (detailed)

## 🚀 Future Enhancements

- [ ] Video analytics and engagement tracking
- [ ] Presence validation via webcam
- [ ] Advanced rescheduling with conflict resolution
- [ ] AI-powered Q&A during sessions
- [ ] Certificate generation
- [ ] Mobile app support
- [ ] Advanced reporting and analytics dashboard
- [ ] Real-time chat/Q&A integration
- [ ] Custom content upload
- [ ] Batch comparison analytics

## 🤝 Contributing

This is a POC system. Contributions and improvements are welcome!

## 📄 License

[Your License Here]

## 📧 Support

For issues, questions, or suggestions, please contact the development team.

---

**Version**: 0.1.0  
**Last Updated**: 2024
