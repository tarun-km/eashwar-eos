"""
Training Orchestration System - Complete GUI Documentation
PyQt6-Based Desktop Application for Internship Training Management
"""

# QUICK START GUIDE

## Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

This includes all required packages:
- PyQt6, PyQt6-Charts, pyqtgraph (GUI)
- SQLAlchemy, Pydantic (Database & validation)
- Other core dependencies

### 2. Configure Environment (Optional)
```bash
# Copy example config
cp .env.example .env

# Edit .env for Teams integration (optional)
# TEAMS_TENANT_ID=your_tenant_id
# TEAMS_CLIENT_ID=your_client_id
```

### 3. Run the Application

#### Option A: GUI Mode (Recommended)
```bash
python ui_main.py
```
Starts the PyQt6 desktop application with:
- Animated splash screen
- Onboarding wizard
- Professional dashboard interface

#### Option B: CLI Mode (Legacy)
```bash
python main.py
```
Interactive command-line interface for batch creation

#### Option C: Example Script
```bash
python example_usage.py
```
Demonstrates full system workflow

---

# APPLICATION ARCHITECTURE

## Directory Structure
```
employment-onboarding-system/
├── ui/                              # PyQt6 GUI Module
│   ├── __init__.py
│   ├── styles.py                   # Theming & styling
│   ├── worker.py                   # Background workers
│   ├── splash_screen.py            # Loading screen
│   ├── onboarding_wizard.py        # Setup wizard
│   ├── main_window.py              # Main application
│   ├── dashboard.py                # Dashboard tab
│   ├── batch_management.py         # Batch management
│   ├── session_tracking.py         # Session tracking
│   ├── attendance_widget.py        # Attendance tab
│   ├── assessment_widget.py        # Assessment tab
│   └── reports_widget.py           # Reports tab
│
├── engines/                        # Core Processing Engines
│   ├── training_plan_engine.py    # Plan generation
│   ├── content_scheduler.py       # Session scheduling
│   ├── content_delivery_engine.py # Session execution
│   ├── assessment_engine.py       # Assessment generation
│   └── attendance_tracker.py      # Attendance tracking
│
├── database/                       # Data Layer
│   ├── models.py                  # SQLAlchemy models
│   └── db_manager.py              # Database management
│
├── config/                         # Configuration
│   └── settings.py                # Global settings
│
├── integrations/                   # External Integrations
│   └── teams_integration.py       # Microsoft Teams API
│
├── utils/                          # Utilities
│   └── logger.py                  # Logging setup
│
├── ui_main.py                      # GUI Entry Point ⭐
├── main.py                         # CLI Entry Point
├── example_usage.py                # Example Script
├── orchestrator.py                 # Central Orchestrator
├── requirements.txt                # Dependencies
└── training_system.db              # SQLite Database
```

---

# USER INTERFACE GUIDE

## 1. Application Startup

### Splash Screen
- Shows animated loading bar
- Displays initialization steps:
  - "Initializing database..."
  - "Loading orchestrator..."
  - "Configuring engines..."
  - "Preparing UI components..."
  - "Ready!"

### Onboarding Wizard (First Launch)
- **Page 1: Welcome** - Overview of system
- **Page 2: Batch Configuration** - Set batch name, duration, type
- **Page 3: Trainee Configuration** - Number of trainees
- **Page 4: Skill Area Selection** - Choose primary skill (Python, Web Dev, Data Science, etc.)
- **Page 5: Teams Integration** - Optional Azure AD setup
- **Page 6: Summary** - Review and confirm

## 2. Main Window Tabs

### Tab 1: Dashboard
**Overview Statistics**
- Active Batches counter
- Total Trainees counter
- Scheduled Sessions counter
- Completion Rate percentage

**Quick Actions**
- Create New Batch (opens wizard)
- Execute Session
- View Reports

**Recent Activity**
- Latest batch operations
- System events

### Tab 2: Batches
**Batch Table Columns**
- ID: Unique batch identifier
- Batch Name: Display name
- Trainees: Number of trainees
- Status: planning/active/completed
- Start Date: Training start date
- Actions: View/Edit/Delete buttons

**Features**
- [New Batch] button - Opens batch creation dialog
- [Refresh] button - Reload from database
- Double-click row to view details
- Delete with confirmation

**Create Batch Dialog**
- Batch Name (required)
- Number of Trainees (1-500)
- Duration in weeks (1-52)
- Skill Area dropdown (Python, Web Dev, Data Science)
- Training Type (Full-day, Half-day)

### Tab 3: Sessions
**Session Table Columns**
- Session ID: Unique identifier
- Date: YYYY-MM-DD format
- Time: HH:MM format
- Topic: Session topic/title
- Duration: Minutes
- Status: pending/in-progress/completed
- Actions: Execute/Details buttons

**Batch Filter Dropdown**
- Select batch to view its sessions
- Auto-filters session list

**Features**
- [Execute] button - Run session immediately
- [Details] button - View full session information
- Auto-refresh every 30 seconds
- Color-coded status indicators

### Tab 4: Attendance
**Attendance Statistics**
- Total: Total recorded attendance entries
- Present: Count of "present" marks
- Absent: Count of "absent" marks
- Rate: Overall attendance percentage

**Attendance Table Columns**
- Trainee: Name of trainee
- Attendance: Sessions attended
- Sessions: Total sessions
- Percentage: Attendance rate (%)

**Color Coding**
- Green: ≥85% attendance (Good)
- Yellow: ≥70% attendance (Acceptable)
- Red: <70% attendance (Needs Attention)

**Date Filtering**
- Date selector to view attendance for specific date
- Auto-updates statistics

### Tab 5: Assessment
**Assessment Statistics**
- Total: Total assessments created
- Pending: Not yet completed
- Completed: Finished assessments
- Avg Score: Average score percentage

**Assessment Table Columns**
- ID: Assessment identifier
- Session: Associated session
- Type: Assessment type (auto-generated)
- Questions: Number of questions
- Status: pending/in-progress/completed
- Actions: View/Score buttons

**Features**
- [Create Assessment] button - Generate new assessment
- [View] button - See assessment details
- [Score] button - Input/view scores
- Auto-calculates statistics

### Tab 6: Reports
**Tabbed Report Views**

#### Summary Tab
- Batch information (name, ID, status)
- Trainees count
- Sessions breakdown
- Date range
- Key statistics

#### Performance Tab
- Per-trainee performance metrics
- Columns: Name, Attendance %, Avg Score, Sessions, Status
- Identifies top and struggling trainees

#### Attendance Tab
- Detailed attendance breakdown
- Columns: Trainee, Present, Absent, Rate %
- Useful for attendance audits

#### Assessments Tab
- Assessment analysis by session
- Columns: Session, Count, Avg Score, Pass Rate %
- Identifies challenging topics

---

# SYSTEM FEATURES

## Core Capabilities

### 1. Batch Management
- ✅ Create multiple training batches
- ✅ Configure batch parameters (duration, size, skill area)
- ✅ View batch history
- ✅ Edit batch details
- ✅ Delete batches

### 2. Training Planning
- ✅ Auto-generate day-wise training plans
- ✅ Create 40-minute sessions with 10-minute breaks
- ✅ Schedule 44 sessions for 2-week training (example)
- ✅ Support for multiple skill areas

### 3. Session Execution
- ✅ Execute sessions on-demand
- ✅ Track session status (pending/in-progress/completed)
- ✅ Record session duration
- ✅ View session details

### 4. Attendance Tracking
- ✅ Record attendance per session
- ✅ Track attendance percentage by trainee
- ✅ Automatic statistics calculation
- ✅ Color-coded attendance alerts

### 5. Assessment Management
- ✅ Auto-generate assessments from session content
- ✅ Store questions and answers
- ✅ Calculate scores automatically
- ✅ Track assessment completion

### 6. Reporting & Analytics
- ✅ Summary reports with key metrics
- ✅ Performance analysis by trainee
- ✅ Attendance tracking and audits
- ✅ Assessment analytics with pass rates
- ✅ Export functionality (extensible)

### 7. Microsoft Teams Integration (Optional)
- ✅ Create Teams meetings for sessions
- ✅ Send meeting invites to trainees
- ✅ Auto-register non-email users
- ✅ Daily reminders via Teams

---

# DATABASE SCHEMA

## Tables

### training_batches
- id (Primary Key)
- batch_name (Unique)
- num_trainees
- duration_weeks
- start_date, end_date
- skill_area
- training_type
- status

### trainees
- id (Primary Key)
- batch_id (Foreign Key)
- name
- email
- teams_user_id
- is_registered

### training_sessions
- id (Primary Key)
- batch_id (Foreign Key)
- session_number
- day_number
- start_time, end_time
- session_type
- topic
- content_url
- teams_meeting_id
- status

### attendance_logs
- id (Primary Key)
- session_id (Foreign Key)
- trainee_id (Foreign Key)
- joined_time, left_time
- duration_minutes
- status

### assessments
- id (Primary Key)
- session_id (Foreign Key)
- trainee_id (Foreign Key)
- questions_json
- responses_json
- score
- status

### training_plans
- id (Primary Key)
- batch_id (Foreign Key)
- plan_json

---

# CONFIGURATION

## Settings File (config/settings.py)

### Session Configuration
- SESSION_DURATION: 40 minutes
- BREAK_DURATION: 10 minutes
- HANDS_ON_START_DAY: 3

### Database Configuration
- DEFAULT: SQLite (training_system.db)
- PRODUCTION: PostgreSQL support

### Teams Configuration
- TENANT_ID: Azure Active Directory tenant
- CLIENT_ID: Azure application ID
- Requires .env file setup

### Logging Configuration
- Log Level: INFO
- Log Directory: logs/
- Format: timestamp, logger name, level, message

---

# TROUBLESHOOTING

## Common Issues

### Issue: "Database locked" error
**Solution**: Ensure only one instance of the application is running

### Issue: GUI doesn't show on startup
**Solution**: Check logs/training_system.log for errors, ensure PyQt6 is properly installed

### Issue: Sessions not displaying
**Solution**: Verify batch exists, check session creation logs

### Issue: Teams integration errors
**Solution**: Verify Azure credentials in .env file, check network connectivity

---

# COMMAND LINE REFERENCE

## Main Commands

```bash
# GUI Application
python ui_main.py

# CLI Application
python main.py

# Example Usage
python example_usage.py

# Run Tests (if added)
pytest tests/
```

---

# DEVELOPER INFORMATION

## Adding Custom Features

### 1. Add New UI Tab
```python
# In ui/main_window.py
from ui.custom_widget import CustomWidget

self.custom_tab = CustomWidget(self.orchestrator)
self.tabs.addTab(self.custom_tab, "Custom Tab")
```

### 2. Add Background Worker
```python
# In ui/worker.py
class CustomWorker(Worker):
    custom_signal = pyqtSignal(dict)
    
    def run(self):
        # Custom implementation
        pass
```

### 3. Extend Orchestrator
```python
# In orchestrator.py
def custom_operation(self, param):
    # Custom business logic
    pass
```

---

# SYSTEM REQUIREMENTS

## Minimum
- Python 3.8+
- 4GB RAM
- 100MB disk space

## Recommended
- Python 3.10+
- 8GB RAM
- SSD storage
- Windows 10+ / macOS / Linux

## Network
- Optional: Microsoft Azure credentials for Teams integration
- Optional: Internet for Teams meeting creation

---

# FILE LOCATIONS

## Important Paths
- **Database**: `training_system.db` (in project root)
- **Logs**: `logs/training_system.log`
- **Config**: `config/settings.py` and `.env` file
- **UI Assets**: All in `ui/` directory

---

# CONTACT & SUPPORT

For issues or feature requests, check:
- logs/training_system.log for detailed error messages
- Application status bar for real-time feedback
- Database integrity at logs/

---

# VERSION INFORMATION

- **Application**: Training Orchestration System v1.0
- **GUI Framework**: PyQt6 6.5.0+
- **Database**: SQLAlchemy 2.0+
- **Created**: 2024
