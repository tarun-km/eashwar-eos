# 🚀 Deployment & Production Guide

## Quick Deployment Checklist

### Local Development (5 minutes)

```bash
# 1. Install Python packages
pip install -r requirements.txt

# 2. Test system
python main.py

# 3. View example
python example_usage.py

# 4. Check logs
cat logs/$(date +%Y%m%d).log
```

### Pre-Production Setup (15 minutes)

```bash
# 1. Create .env file
cp .env.example .env

# 2. Add Teams credentials (optional)
# Edit .env with TEAMS_TENANT_ID, TEAMS_CLIENT_ID, TEAMS_CLIENT_SECRET

# 3. Change database (optional)
# Edit .env: DATABASE_URL=postgresql://user:pass@host/dbname

# 4. Initialize database
python -c "from database.db_manager import DatabaseManager; DatabaseManager()"

# 5. Verify setup
python -c "from orchestrator import TrainingOrchestrationSystem; print('✓ System ready')"
```

### Production Deployment (30 minutes)

#### Option A: Docker Deployment

1. **Create Dockerfile**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV DATABASE_URL=postgresql://...
ENV TEAMS_CLIENT_ID=...
ENV TEAMS_CLIENT_SECRET=...

EXPOSE 5000

CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:5000"]
```

2. **Build and Run**
```bash
docker build -t training-system .
docker run -d --env-file .env training-system
```

#### Option B: Traditional Deployment

1. **Server Setup**
```bash
# Ubuntu 20.04
sudo apt update
sudo apt install python3.9 python3-pip postgresql

# Create user
useradd -m training-user
```

2. **Clone Project**
```bash
su - training-user
git clone <repo> training-system
cd training-system
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **Setup Database**
```bash
sudo -u postgres createdb training_system
sudo -u postgres createuser training-user
# Grant permissions

# In project:
python -c "from database.db_manager import DatabaseManager; DatabaseManager()"
```

4. **Setup Systemd Service**

Create `/etc/systemd/system/training-system.service`:
```ini
[Unit]
Description=Training Orchestration System
After=network.target postgresql.service

[Service]
Type=simple
User=training-user
WorkingDirectory=/home/training-user/training-system
ExecStart=/home/training-user/training-system/venv/bin/python /home/training-user/training-system/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable training-system
sudo systemctl start training-system
sudo systemctl status training-system
```

5. **Setup Web API (Optional)**

Install Flask/FastAPI:
```bash
pip install flask
```

Create `api.py`:
```python
from flask import Flask, jsonify, request
from orchestrator import TrainingOrchestrationSystem

app = Flask(__name__)
system = TrainingOrchestrationSystem()

@app.route('/api/batches', methods=['POST'])
def create_batch():
    data = request.json
    batch = system.create_training_batch(
        batch_name=data['batch_name'],
        num_trainees=data['num_trainees'],
        duration_weeks=data['duration_weeks'],
        start_date=datetime.fromisoformat(data['start_date']),
        skill_area=data['skill_area']
    )
    return jsonify(batch), 201

@app.route('/api/batches/<int:batch_id>')
def get_batch(batch_id):
    summary = system.get_batch_summary(batch_id)
    return jsonify(summary)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
```

Run with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 api:app
```

6. **Setup Nginx Reverse Proxy**

Create `/etc/nginx/sites-available/training-system`:
```nginx
server {
    listen 80;
    server_name training.example.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable:
```bash
sudo ln -s /etc/nginx/sites-available/training-system /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

7. **Setup SSL/TLS**

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d training.example.com
```

## Scaling Considerations

### Current (POC)
- Single server
- SQLite database
- ~50-100 trainees per batch
- Manual job execution

### Production
```
Load Balancer (Nginx)
        ↓
   [Web API 1]  [Web API 2]  [Web API 3]
        ↓
PostgreSQL (with replication)
        ↓
Redis Cache
        ↓
[Job Worker 1]  [Job Worker 2]  [Job Worker N]
(Celery)
```

### Job Queue Setup (Celery)

1. **Install**
```bash
pip install celery redis
```

2. **Create `celery_config.py`**
```python
from celery import Celery

app = Celery('training')
app.conf.broker_url = 'redis://localhost:6379'
app.conf.result_backend = 'redis://localhost:6379'

@app.task
def execute_session(session_id):
    from orchestrator import TrainingOrchestrationSystem
    system = TrainingOrchestrationSystem()
    result = system.execute_scheduled_session(session_id)
    system.close()
    return result
```

3. **Start workers**
```bash
celery -A celery_config worker --loglevel=info
```

## Monitoring & Maintenance

### Monitoring

```python
# Create `monitor.py`
import logging
import psycopg2

logger = logging.getLogger(__name__)

def check_database():
    try:
        conn = psycopg2.connect("dbname=training_system")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM training_batches")
        count = cursor.fetchone()[0]
        logger.info(f"Database OK: {count} batches")
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Database ERROR: {e}")
        return False

def check_teams_api():
    try:
        from integrations.teams_integration import TeamsIntegration
        teams = TeamsIntegration()
        # Test connection
        return True
    except Exception as e:
        logger.error(f"Teams API ERROR: {e}")
        return False

# Run periodic checks
import schedule
schedule.every(5).minutes.do(check_database)
schedule.every(5).minutes.do(check_teams_api)
```

### Backup Strategy

```bash
# Daily database backup
0 2 * * * pg_dump training_system > /backups/$(date +\%Y\%m\%d).sql

# Upload to S3
0 3 * * * aws s3 cp /backups/ s3://my-backups/training-system/ --recursive
```

### Log Rotation

```bash
# Create `/etc/logrotate.d/training-system`
/home/training-user/training-system/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    create 0644 training-user training-user
}
```

## Security Hardening

1. **Environment Variables**
```bash
# Store secrets in secure vault
export TEAMS_CLIENT_SECRET=$(aws secretsmanager get-secret-value --secret-id training-system-secret)
```

2. **Database Security**
```sql
-- Create limited user
CREATE USER training_app WITH PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE training_system TO training_app;
GRANT USAGE ON SCHEMA public TO training_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO training_app;
```

3. **API Security**
```python
# Add authentication
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    return username == "admin" and password == os.getenv("API_PASSWORD")

@app.route('/api/batches')
@auth.login_required
def get_batches():
    # ...
```

## Performance Tuning

1. **Database Indexing**
```sql
CREATE INDEX idx_batch_start_date ON training_batches(start_date);
CREATE INDEX idx_session_batch_status ON training_sessions(batch_id, status);
CREATE INDEX idx_attendance_trainee ON attendance_logs(trainee_id);
```

2. **Connection Pooling**
```python
# In `database/db_manager.py`
from sqlalchemy.pool import QueuePool

engine = create_engine(
    database_url,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True
)
```

3. **Caching**
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_training_plan(batch_id):
    # Cache training plans
    pass
```

## Disaster Recovery

1. **Database Backup**
```bash
pg_dump training_system | gzip > backup_$(date +%Y%m%d_%H%M%S).sql.gz
```

2. **Restore from Backup**
```bash
gunzip backup_20240115_120000.sql.gz
psql training_system < backup_20240115_120000.sql
```

3. **Replication Setup**
```
Primary PostgreSQL
        ↓ (WAL stream)
Standby PostgreSQL
        ↓ (if primary fails)
Failover to Standby
```

## Compliance & Auditing

1. **Audit Logging**
```python
import logging
audit_logger = logging.getLogger('audit')

def audit_log(action, user, details):
    audit_logger.info(f"[{user}] {action}: {details}")
```

2. **Data Privacy**
- Encrypt PII (Personally Identifiable Information)
- Implement access controls
- Regular security audits

3. **Compliance Checklist**
- [ ] GDPR compliance
- [ ] Data retention policy
- [ ] Security policy
- [ ] Incident response plan

---

**Deployment Status**: Ready for Production ✅

**Last Updated**: 2024
