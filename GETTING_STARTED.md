# Getting Started Guide

## Installation & Setup

### Step 1: Prerequisites

- Python 3.8 or higher
- Git
- pip (Python package manager)

### Step 2: Clone & Setup

```bash
# Navigate to project directory
cd employment-onboarding-system

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your credentials
# For POC, you can leave Teams credentials empty
```

### Step 4: Initialize Database

```bash
# The database is automatically created on first run
# To manually initialize:
python -c "from database.db_manager import DatabaseManager; db = DatabaseManager(); print('Database initialized!')"
```

## First Run

### Option A: Interactive Mode (Recommended for First Run)

```bash
python main.py
```

Follow the prompts to:
1. Enter batch name
2. Enter number of trainees
3. Enter training duration (weeks)
4. Select skill area (python/web-development/data-science)
5. Select training type (full-day/half-day)

**Output**: 
- Training batch created
- Schedule generated
- Batch saved to database
- Logs saved to `logs/` directory

### Option B: Run Demo

```bash
python example_usage.py
```

This demonstrates:
1. Creating a training batch
2. Viewing batch summary
3. Scheduling Teams meetings
4. Generating assessments
5. Recording attendance
6. Executing sessions

## Common Tasks

### Task 1: Create a Training Batch Programmatically

```python
from orchestrator import TrainingOrchestrationSystem
from datetime import datetime

system = TrainingOrchestrationSystem()

try:
    batch = system.create_training_batch(
        batch_name="Python Training - Q1 2024",
        num_trainees=20,
        duration_weeks=8,
        start_date=datetime(2024, 1, 8),
        skill_area="python",
        training_type="full-day",
        trainee_list=[
            {"name": "John Doe", "email": "john@example.com"},
            {"name": "Jane Smith", "email": "jane@example.com"},
        ]
    )
    
    print(f"Batch created: {batch['batch_id']}")
    print(f"Total sessions: {batch['scheduled_sessions']}")
    
finally:
    system.close()
```

### Task 2: Schedule Teams Meetings

```python
system = TrainingOrchestrationSystem()

try:
    result = system.schedule_batch_with_teams_meetings(
        batch_id=1,
        organizer_email="trainer@company.com"
    )
    
    print(f"Meetings created: {result['meetings_created']}")
    
finally:
    system.close()
```

### Task 3: Execute a Session

```python
system = TrainingOrchestrationSystem()

try:
    result = system.execute_scheduled_session(session_id=1)
    
    print(f"Session started: {result['status']}")
    print(f"Content: {result['content_started']}")
    print(f"Meeting: {result['meeting_started']}")
    
finally:
    system.close()
```

### Task 4: Record Attendance

```python
from datetime import datetime, timedelta

system = TrainingOrchestrationSystem()

try:
    now = datetime.now()
    
    # Mark trainee as present
    attendance = system.record_trainee_attendance(
        session_id=1,
        trainee_id=1,
        joined_time=now,
        left_time=now + timedelta(minutes=38)  # 38 of 40 minutes
    )
    
    print(f"Status: {attendance['status']}")
    
finally:
    system.close()
```

### Task 5: Generate Assessment

```python
system = TrainingOrchestrationSystem()

try:
    assessment = system.generate_session_assessment(session_id=1)
    
    print(f"Questions: {assessment['num_questions']}")
    for q in assessment['questions']:
        print(f"  - {q['question']}")
    
finally:
    system.close()
```

### Task 6: View Batch Summary

```python
system = TrainingOrchestrationSystem()

try:
    summary = system.get_batch_summary(batch_id=1)
    
    print(f"Batch: {summary['batch_name']}")
    print(f"Trainees: {summary['num_trainees']}")
    print(f"Sessions: {summary['total_sessions']}")
    print(f"Completed: {summary['completed_sessions']}")
    
finally:
    system.close()
```

## Understanding the Workflow

### Day 1-2: Lectures Only
- 4 sessions per day (full-day training)
- Each session ~40 minutes
- Focus on foundational concepts
- Assessment at end of day

### Day 3+: Mix of Lectures & Hands-on
- Alternating lecture and hands-on sessions
- Hands-on sessions: practical application
- Daily assessments
- Attendance tracking

### Example Daily Schedule

**Full-Day Training (9 AM - 12:10 PM)**
```
09:00-09:40: Python Basics (Lecture)
09:40-09:50: Break
09:50-10:30: Variables & Data Types (Lecture)
10:30-10:40: Break
10:40-11:20: Hands-on: Write Basic Programs
11:20-11:30: Break
11:30-12:10: Q&A / Assessment
```

## Viewing Logs

Logs are saved in the `logs/` directory with daily files:

```bash
# View today's logs
cat logs/20240115.log

# On Windows:
type logs\20240115.log

# Follow logs in real-time
tail -f logs/20240115.log
```

## Database

### View Database Contents

```python
from database.db_manager import DatabaseManager
from database.models import TrainingBatch, Trainee

db = DatabaseManager()
session = db.get_session()

# View all batches
batches = session.query(TrainingBatch).all()
for batch in batches:
    print(f"{batch.batch_name}: {batch.num_trainees} trainees")

# View trainees in batch 1
trainees = session.query(Trainee).filter(Trainee.batch_id == 1).all()
for trainee in trainees:
    print(f"  - {trainee.name}: {trainee.email}")

session.close()
db.close()
```

### Reset Database

```python
import os
from database.models import Base
from database.db_manager import DatabaseManager

# Remove existing database
if os.path.exists('training_system.db'):
    os.remove('training_system.db')

# Reinitialize
db = DatabaseManager()
print("Database reset!")
db.close()
```

## Teams Integration Setup (Optional)

For full Teams integration:

1. **Register Azure App**:
   - Go to Azure Portal > App registrations
   - Create new app
   - Note: Application (client) ID
   - Create client secret
   - Note: Client secret value

2. **Set Permissions**:
   - Add permissions: `Calendars.ReadWrite`, `OnlineMeetings.ReadWrite`
   - Grant admin consent

3. **Update .env**:
```env
TEAMS_TENANT_ID=your-tenant-id
TEAMS_CLIENT_ID=your-client-id
TEAMS_CLIENT_SECRET=your-client-secret
```

4. **Test Connection**:
```python
from integrations.teams_integration import TeamsIntegration
from datetime import datetime, timedelta

teams = TeamsIntegration()
meeting = teams.create_meeting(
    session_id=1,
    topic="Test Meeting",
    start_time=datetime.now() + timedelta(hours=1),
    attendees=["user@example.com"],
    organizer_email="trainer@example.com"
)
print(f"Meeting URL: {meeting['meeting_url']}")
```

## Troubleshooting

### Issue: Database Not Found
**Solution**: Ensure you're running from the project directory and have write permissions.

### Issue: Import Errors
**Solution**: Ensure virtual environment is activated and dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: No Logs
**Solution**: Check `logs/` directory exists:
```python
import os
os.makedirs('logs', exist_ok=True)
```

### Issue: Teams Integration Fails
**Solution**: 
- Verify .env file has correct credentials
- For POC, Teams integration can be skipped (uses mock API)
- Check `logs/` for error details

## Next Steps

1. ✅ **Understand the architecture** - Read [ARCHITECTURE.md](ARCHITECTURE.md)
2. ✅ **Explore the APIs** - Check [API_REFERENCE.md](API_REFERENCE.md)
3. ✅ **Run examples** - Execute `python example_usage.py`
4. ✅ **Build custom integrations** - Add your own engines
5. ✅ **Deploy to production** - Configure for production database

## Performance Tips

1. **Batch Creation**: Create large batches (100+) in chunks
2. **Database**: Use PostgreSQL for production (SQLite has limitations)
3. **Video Content**: Use CDN for video delivery
4. **Scheduled Jobs**: Use Celery for async session execution
5. **Caching**: Cache training plans for repeated skill areas

## Support Resources

- **Documentation**: See `README.md`, `ARCHITECTURE.md`, `API_REFERENCE.md`
- **Examples**: Check `example_usage.py` for code samples
- **Logs**: Review detailed logs in `logs/` directory
- **Code Comments**: All code is heavily commented

## Learning Path

1. Start with `main.py` - simple entry point
2. Review `example_usage.py` - full workflow
3. Explore `orchestrator.py` - main coordinator
4. Study engines in `engines/` - core logic
5. Review `database/models.py` - data structures
6. Check `integrations/` - external services

## Useful Commands

```bash
# Install requirements
pip install -r requirements.txt

# Run main system
python main.py

# Run demo
python example_usage.py

# Check Python version
python --version

# Activate virtual environment (Windows)
venv\Scripts\activate

# Deactivate virtual environment
deactivate

# View logs
tail -f logs/$(date +%Y%m%d).log
```

---

**Happy Training! 🎓**

If you encounter issues, check the logs and error messages for detailed information.
