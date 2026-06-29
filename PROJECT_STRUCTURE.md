# 📊 Project Structure & Quick Reference

## 🎯 Project: AI-Driven Training Orchestration System

### 📁 Directory Tree

```
employment-onboarding-system/
│
├── 📄 main.py                      # Entry point - Interactive CLI
├── 📄 orchestrator.py              # Main orchestrator - Coordinates all components
├── 📄 example_usage.py             # Demo workflow - Run to see full system in action
│
├── 📁 config/                      # Configuration Management
│   ├── __init__.py
│   └── settings.py                 # All system settings and configuration
│
├── 📁 database/                    # Database Layer
│   ├── __init__.py
│   ├── models.py                   # 8 SQLAlchemy models
│   └── db_manager.py               # Database connection & operations
│
├── 📁 engines/                     # Core Training Engines (5)
│   ├── __init__.py
│   ├── training_plan_engine.py     # Generates day-wise training plans
│   ├── content_scheduler.py        # Creates session timing (40min + breaks)
│   ├── content_delivery_engine.py  # Executes sessions & plays videos
│   ├── assessment_engine.py        # Generates assessments & scores
│   └── attendance_tracker.py       # Tracks attendance & generates logs
│
├── 📁 integrations/                # External Integrations
│   ├── __init__.py
│   └── teams_integration.py        # Microsoft Teams API integration
│
├── 📁 utils/                       # Utility Modules
│   ├── __init__.py
│   ├── logger.py                   # Logging setup & utilities
│   └── date_utils.py               # Date/time helper functions
│
├── 📁 content/                     # Content Storage (Auto-created)
│
├── 📁 logs/                        # Log Files (Auto-created)
│   └── YYYYMMDD.log               # Daily log files
│
├── 📄 requirements.txt             # Python dependencies
├── 📄 .env.example                 # Environment variables template
│
├── 📄 README.md                    # Main documentation (START HERE)
├── 📄 GETTING_STARTED.md          # Setup & first run guide
├── 📄 ARCHITECTURE.md             # System design & components
├── 📄 API_REFERENCE.md            # Complete API documentation
├── 📄 PROJECT_CHECKLIST.md        # Implementation checklist
│
└── 📄 __init__.py                 # Root package initialization

```

## 📋 File Summary

### Configuration (2 files)
| File | Purpose |
|------|---------|
| `config/settings.py` | All system configuration and settings |
| `.env.example` | Environment variables template |

### Database (2 files)
| File | Purpose |
|------|---------|
| `database/models.py` | 8 SQLAlchemy models (Batch, Trainee, Session, etc.) |
| `database/db_manager.py` | Database connection and operations |

### Engines (5 files)
| File | Purpose |
|------|---------|
| `engines/training_plan_engine.py` | Generate day-wise training plans |
| `engines/content_scheduler.py` | Create session timing with breaks |
| `engines/content_delivery_engine.py` | Execute sessions and play videos |
| `engines/assessment_engine.py` | Generate assessments and scoring |
| `engines/attendance_tracker.py` | Track attendance and generate reports |

### Integrations (1 file)
| File | Purpose |
|------|---------|
| `integrations/teams_integration.py` | Microsoft Teams API integration |

### Utilities (2 files)
| File | Purpose |
|------|---------|
| `utils/logger.py` | Logging setup and utilities |
| `utils/date_utils.py` | Date and time helper functions |

### Main Application (3 files)
| File | Purpose |
|------|---------|
| `orchestrator.py` | Main orchestrator coordinating all components |
| `main.py` | Interactive CLI entry point |
| `example_usage.py` | Demo workflow and examples |

### Documentation (5 files)
| File | Purpose |
|------|---------|
| `README.md` | Main documentation and overview |
| `GETTING_STARTED.md` | Setup guide and first run instructions |
| `ARCHITECTURE.md` | System design and architecture |
| `API_REFERENCE.md` | Complete API documentation |
| `PROJECT_CHECKLIST.md` | Implementation status checklist |

### Configuration Files (2 files)
| File | Purpose |
|------|---------|
| `requirements.txt` | Python package dependencies |
| `__init__.py` | Root package initialization |

## 🎯 Quick Start Commands

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run interactive system
python main.py

# 3. Run full demo
python example_usage.py

# 4. View logs
tail -f logs/$(date +%Y%m%d).log
```

## 🔗 Key Classes & Methods

### Main Orchestrator
```python
system = TrainingOrchestrationSystem()
system.create_training_batch(...)       # Create batch with plan
system.schedule_batch_with_teams_meetings(...)  # Create Teams meetings
system.execute_scheduled_session(...)   # Run session
system.record_trainee_attendance(...)   # Track attendance
system.generate_session_assessment(...) # Create assessment
system.get_batch_summary(...)           # Get batch info
system.close()                          # Cleanup
```

### Core Engines
```python
# Training Plan Engine
plan = TrainingPlanEngine().create_training_plan(...)

# Content Scheduler
sessions = ContentScheduler().schedule_sessions_from_plan(plan)

# Content Delivery
ContentDeliveryEngine().execute_session(session, meeting_url)

# Assessment
assessment = AssessmentEngine().generate_assessment(topic)

# Attendance
AttendanceTracker().mark_attendance(session_id, trainee_id, ...)

# Teams
TeamsIntegration().create_meeting(session_id, topic, ...)
```

## 📊 Database Models

| Model | Purpose | Key Fields |
|-------|---------|-----------|
| TrainingBatch | Cohort information | batch_name, num_trainees, duration_weeks, skill_area |
| Trainee | Participant details | name, email, batch_id, is_registered |
| TrainingSession | Individual session | session_type, topic, start_time, status |
| TrainingPlan | Schedule plan | batch_id, total_topics, topics_per_day, plan_json |
| Assessment | Assessment data | session_id, trainee_id, score, passed |
| AttendanceLog | Attendance records | session_id, trainee_id, joined_time, attendance_% |
| Meeting | Teams meetings | session_id, meeting_id, meeting_url |
| ContentResource | Content library | skill_area, topic, content_type, duration |

## 🛠️ Key Features

### ✅ Training Planning
- Automatic day-wise plan generation
- Business day calculation
- Content distribution
- Mixed lecture/hands-on sessions

### ✅ Scheduling
- Structured sessions (40 min)
- Automatic breaks (10 min)
- Daily schedule generation
- Rescheduling support

### ✅ Content Delivery
- Video playback (local & URL)
- Teams meeting integration
- Session execution
- Streaming support

### ✅ Assessment
- Auto question generation
- Multiple question types
- Score calculation
- Feedback generation

### ✅ Attendance
- Real-time tracking
- Daily logs
- Per-trainee history
- Attendance percentage

### ✅ Integration
- Teams meetings
- Invite distribution
- Reminders
- Non-email user support

## 📖 Documentation Map

```
Start Here → README.md
         ↓
Setup Guide → GETTING_STARTED.md
         ↓
Understand Design → ARCHITECTURE.md
         ↓
Learn APIs → API_REFERENCE.md
         ↓
See Examples → example_usage.py
         ↓
Review Code → orchestrator.py → engines/
         ↓
Check Status → PROJECT_CHECKLIST.md
```

## 🚀 Running the System

### Method 1: Interactive Mode
```bash
python main.py
# Follow prompts to create training batch
```

### Method 2: Demo Mode
```bash
python example_usage.py
# Shows complete workflow with sample data
```

### Method 3: Programmatic Use
```python
from orchestrator import TrainingOrchestrationSystem
system = TrainingOrchestrationSystem()
# Use API methods directly
```

## 📝 Configuration

All settings in `config/settings.py`:
- Session duration: 40 minutes
- Break duration: 10 minutes
- Hands-on start day: Day 3
- Passing score: 70%
- Min attendance: 80%

Edit `config/settings.py` to customize.

## 🔍 Logging

- **Location**: `logs/` directory
- **Format**: `YYYYMMDD.log`
- **Level**: DEBUG (file) / INFO (console)
- **Rotation**: Daily

View logs:
```bash
tail -f logs/20240115.log
```

## 💾 Database

- **Default**: SQLite (`training_system.db`)
- **Production**: PostgreSQL
- **Connection**: `config/settings.py` → DATABASE_URL

Initialize database:
```bash
python -c "from database.db_manager import DatabaseManager; DatabaseManager()"
```

## 🎓 Learning Path

1. **Start**: Read [README.md](README.md) (5 min)
2. **Setup**: Follow [GETTING_STARTED.md](GETTING_STARTED.md) (10 min)
3. **Understand**: Review [ARCHITECTURE.md](ARCHITECTURE.md) (15 min)
4. **Learn APIs**: Study [API_REFERENCE.md](API_REFERENCE.md) (15 min)
5. **Practice**: Run [example_usage.py](example_usage.py) (5 min)
6. **Explore**: Review source code (30 min)

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| Import error | Activate venv and `pip install -r requirements.txt` |
| Database not found | Ensure project directory permissions |
| No logs | Check `logs/` directory exists |
| Teams errors | Check `.env` credentials (optional for POC) |

## 📊 Statistics

- **Python Files**: 18
- **Total Lines**: 3,500+
- **Functions**: 30+
- **Models**: 8
- **Documentation**: 5 files

## 🎯 Total Files: 33

---

**Version**: 0.1.0 POC  
**Status**: ✅ Complete  
**Last Updated**: 2024
