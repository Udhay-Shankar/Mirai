# 📊 Database Monitoring Guide

## Overview
This guide shows you how to monitor your PostgreSQL database in real-time for performance, security, and health.

---

## 🚀 Quick Start

### 1. Enable PostgreSQL Extensions

```sql
-- Connect to your database
psql -U your_user -d mirai

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
CREATE EXTENSION IF NOT EXISTS pgaudit;  -- Optional: for security auditing

-- Reload PostgreSQL to activate
SELECT pg_reload_conf();
```

### 2. Configure PostgreSQL for Monitoring

Edit `postgresql.conf`:

```ini
# Enable query statistics
shared_preload_libraries = 'pg_stat_statements'
pg_stat_statements.track = all
pg_stat_statements.max = 10000

# Connection logging
log_connections = on
log_disconnections = on
log_duration = on
log_statement = 'all'  # Or 'ddl' for production

# Slow query logging
log_min_duration_statement = 1000  # Log queries slower than 1s

# Connection limits
max_connections = 100
```

Restart PostgreSQL:
```powershell
# Windows
Restart-Service postgresql-x64-14

# Linux
sudo systemctl restart postgresql
```

### 3. Add Monitoring Router to Backend

In `backend/app/main.py`:

```python
from app.routers import monitoring

app.include_router(monitoring.router)
```

### 4. Start Backend

```powershell
cd backend
uvicorn app.main:app --reload
```

---

## 📊 Available Monitoring Endpoints

### Health Check (Public)
```bash
GET /api/monitor/health
```
Returns: Database connection status

### Connection Stats (Admin)
```bash
GET /api/monitor/db/connections
Authorization: Bearer <token>
```
Returns: Active, idle, waiting connections

### Performance Metrics (Admin)
```bash
GET /api/monitor/db/performance
Authorization: Bearer <token>
```
Returns: Slow queries, cache hit ratio, long-running queries

### Database Size (Admin)
```bash
GET /api/monitor/db/size
Authorization: Bearer <token>
```
Returns: Database and table sizes

### Index Stats (Admin)
```bash
GET /api/monitor/db/indexes
Authorization: Bearer <token>
```
Returns: Index usage and unused indexes

### Blocking Queries (Admin)
```bash
GET /api/monitor/db/blocking
Authorization: Bearer <token>
```
Returns: Queries blocking other queries

### Vacuum Stats (Admin)
```bash
GET /api/monitor/db/vacuum
Authorization: Bearer <token>
```
Returns: Table bloat and vacuum statistics

### Full Health Report (Admin)
```bash
GET /api/monitor/db/full-report
Authorization: Bearer <token>
```
Returns: Comprehensive health report

### Active Sessions (Admin)
```bash
GET /api/monitor/security/sessions
Authorization: Bearer <token>
```
Returns: All active database sessions

### Suspicious Activity (Admin)
```bash
GET /api/monitor/security/suspicious
Authorization: Bearer <token>
```
Returns: Potentially malicious queries

### Kill Query (Admin)
```bash
POST /api/monitor/db/kill-query/{pid}
Authorization: Bearer <token>
```
Terminates a specific database connection

---

## 🖥️ Using the Dashboard

### 1. Add Route to Frontend

In `frontend/src/App.jsx`:

```jsx
import DatabaseMonitor from './components/DatabaseMonitor';

// Add route
<Route path="/admin/monitor" element={<DatabaseMonitor />} />
```

### 2. Access Dashboard

Navigate to: `http://localhost:5173/admin/monitor`

### Features:
- ✅ Real-time connection stats
- ✅ Cache hit ratio visualization
- ✅ Long-running query alerts
- ✅ Slow query analysis
- ✅ Auto-refresh every 5 seconds
- ✅ Manual refresh button

---

## 📈 What to Monitor

### 1. Connection Count
**Normal:** 5-20 connections  
**Warning:** 50+ connections  
**Critical:** Near max_connections (100)

**Action if high:**
```sql
-- Find idle connections
SELECT * FROM pg_stat_activity WHERE state = 'idle';

-- Kill idle connections older than 5 minutes
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'idle'
AND state_change < now() - interval '5 minutes';
```

### 2. Cache Hit Ratio
**Good:** > 99%  
**Warning:** 90-99%  
**Critical:** < 90%

**Action if low:**
- Increase `shared_buffers` in postgresql.conf
- Check if working set fits in memory
- Review query patterns

### 3. Long Running Queries
**Normal:** < 5 seconds  
**Warning:** 5-30 seconds  
**Critical:** > 30 seconds

**Action:**
```sql
-- Find long-running queries
SELECT pid, now() - query_start as duration, query
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY duration DESC;

-- Kill specific query
SELECT pg_terminate_backend(12345);  -- Replace with actual PID
```

### 4. Table Bloat
**Good:** < 10% dead tuples  
**Warning:** 10-20% dead tuples  
**Critical:** > 20% dead tuples

**Action:**
```sql
-- Vacuum specific table
VACUUM ANALYZE users;

-- Aggressive vacuum (locks table)
VACUUM FULL users;
```

### 5. Unused Indexes
**Action:** Drop indexes never used
```sql
-- Drop unused index
DROP INDEX IF EXISTS idx_never_used;
```

### 6. Blocking Queries
**Critical:** Any blocking > 5 seconds

**Action:**
```sql
-- Find blocking queries
SELECT * FROM pg_stat_activity WHERE wait_event IS NOT NULL;

-- Kill blocking query
SELECT pg_terminate_backend(blocking_pid);
```

---

## 🔔 Setting Up Alerts

### Option 1: Email Alerts (Python Script)

```python
# monitor_alerts.py
import asyncio
import smtplib
from email.mime.text import MIMEText
from app.monitoring.db_monitor import DatabaseMonitor

async def check_and_alert():
    monitor = DatabaseMonitor(db_session)
    
    # Check connections
    stats = await monitor.get_connection_stats()
    if stats['total_connections'] > 80:
        send_alert(
            "High Connection Count",
            f"Current connections: {stats['total_connections']}"
        )
    
    # Check cache hit ratio
    cache = await monitor.get_cache_hit_ratio()
    if cache['cache_hit_ratio_percent'] < 90:
        send_alert(
            "Low Cache Hit Ratio",
            f"Cache hit: {cache['cache_hit_ratio_percent']}%"
        )
    
    # Check long-running queries
    queries = await monitor.get_long_running_queries(30)
    if queries:
        send_alert(
            "Long Running Queries Detected",
            f"Found {len(queries)} queries running > 30s"
        )

def send_alert(subject, message):
    msg = MIMEText(message)
    msg['Subject'] = f"DB Alert: {subject}"
    msg['From'] = 'alerts@mirai.com'
    msg['To'] = 'admin@mirai.com'
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login('your_email', 'your_password')
        server.send_message(msg)

# Run every 1 minute
asyncio.run(check_and_alert())
```

### Option 2: Slack Alerts

```python
# slack_alerts.py
import requests

def send_slack_alert(message):
    webhook_url = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
    
    payload = {
        "text": f"🚨 Database Alert",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": message
                }
            }
        ]
    }
    
    requests.post(webhook_url, json=payload)

# Usage
send_slack_alert("⚠️ Connection count: 95/100")
```

### Option 3: Discord Webhook

```python
# discord_alerts.py
import requests

def send_discord_alert(title, message, color=0xFF0000):
    webhook_url = "YOUR_DISCORD_WEBHOOK_URL"
    
    payload = {
        "embeds": [{
            "title": f"🔔 {title}",
            "description": message,
            "color": color
        }]
    }
    
    requests.post(webhook_url, json=payload)
```

---

## 🐳 Docker Monitoring Setup

### docker-compose.yml

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:14
    environment:
      POSTGRES_DB: mirai
      POSTGRES_USER: mirai_user
      POSTGRES_PASSWORD: secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./postgresql.conf:/etc/postgresql/postgresql.conf
    command: postgres -c config_file=/etc/postgresql/postgresql.conf
    ports:
      - "5432:5432"

  # Prometheus for metrics
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"

  # Grafana for dashboards
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      GF_SECURITY_ADMIN_PASSWORD: admin
    depends_on:
      - prometheus

  # PostgreSQL Exporter
  postgres_exporter:
    image: prometheuscommunity/postgres-exporter
    environment:
      DATA_SOURCE_NAME: "postgresql://mirai_user:secure_password@postgres:5432/mirai?sslmode=disable"
    ports:
      - "9187:9187"
    depends_on:
      - postgres

volumes:
  postgres_data:
```

---

## 📊 Grafana Dashboard Setup

### 1. Access Grafana
Navigate to: `http://localhost:3000`  
Login: admin / admin

### 2. Add PostgreSQL Data Source
1. Configuration → Data Sources → Add data source
2. Select "PostgreSQL"
3. Configure:
   - Host: `postgres:5432`
   - Database: `mirai`
   - User: `mirai_user`
   - Password: `secure_password`
   - SSL Mode: disable (for development)

### 3. Import Dashboard
1. Dashboards → Import
2. Use Dashboard ID: `9628` (PostgreSQL Database)
3. Select PostgreSQL data source
4. Import

### Key Metrics to Watch:
- Connections (current/max)
- Transactions per second
- Cache hit ratio
- Query duration
- Table sizes
- Index usage
- Replication lag (if applicable)

---

## 🔍 Manual Monitoring Queries

### Check Current Connections
```sql
SELECT count(*), state
FROM pg_stat_activity
WHERE datname = 'mirai'
GROUP BY state;
```

### Find Slow Queries
```sql
SELECT query, calls, mean_exec_time, max_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;
```

### Check Table Sizes
```sql
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

### Check Index Usage
```sql
SELECT 
    indexrelname as index_name,
    idx_scan as times_used,
    idx_tup_read as tuples_read
FROM pg_stat_user_indexes
ORDER BY idx_scan ASC;
```

### Find Blocking Locks
```sql
SELECT 
    blocked.pid AS blocked_pid,
    blocking.pid AS blocking_pid,
    blocked.query AS blocked_query,
    blocking.query AS blocking_query
FROM pg_stat_activity blocked
JOIN pg_locks blocked_locks ON blocked.pid = blocked_locks.pid
JOIN pg_locks blocking_locks ON blocked_locks.locktype = blocking_locks.locktype
JOIN pg_stat_activity blocking ON blocking.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted
AND blocked.pid != blocking.pid;
```

### Check Replication Status
```sql
SELECT * FROM pg_stat_replication;
```

### Database Size
```sql
SELECT 
    pg_database.datname,
    pg_size_pretty(pg_database_size(pg_database.datname)) AS size
FROM pg_database
ORDER BY pg_database_size(pg_database.datname) DESC;
```

---

## 🎯 Performance Tuning Tips

### 1. Optimize Queries
```sql
-- Use EXPLAIN ANALYZE to understand query performance
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';

-- Look for:
-- - Seq Scan (bad) → should be Index Scan
-- - High cost values
-- - Long execution time
```

### 2. Add Indexes
```sql
-- Create index on frequently queried columns
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_provider ON users(provider, provider_user_id);

-- Composite indexes for multi-column queries
CREATE INDEX idx_users_active_tier ON users(is_active, subscription_tier);
```

### 3. Configure Connection Pooling
```python
# Use PgBouncer or SQLAlchemy pooling
from sqlalchemy import create_engine

engine = create_engine(
    DATABASE_URL,
    pool_size=20,  # Max connections in pool
    max_overflow=10,  # Additional connections if needed
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=3600  # Recycle connections after 1 hour
)
```

### 4. Optimize PostgreSQL Config
```ini
# postgresql.conf

# Memory
shared_buffers = 256MB  # 25% of RAM
effective_cache_size = 1GB  # 50-75% of RAM
work_mem = 4MB
maintenance_work_mem = 64MB

# Connections
max_connections = 100
```

---

## 🚨 Troubleshooting

### Issue: Too Many Connections
```sql
-- Find idle connections
SELECT pid, usename, application_name, state, state_change
FROM pg_stat_activity
WHERE state = 'idle'
ORDER BY state_change;

-- Kill idle connections
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'idle'
AND state_change < now() - interval '10 minutes';
```

### Issue: Slow Queries
```sql
-- Reset pg_stat_statements
SELECT pg_stat_statements_reset();

-- Monitor after reset
SELECT query, calls, mean_exec_time
FROM pg_stat_statements
WHERE mean_exec_time > 100  -- queries > 100ms
ORDER BY mean_exec_time DESC;
```

### Issue: High CPU Usage
```sql
-- Find CPU-intensive queries
SELECT pid, query_start, state, query
FROM pg_stat_activity
WHERE state = 'active'
ORDER BY query_start;
```

### Issue: Disk Space Full
```bash
# Check disk usage
df -h

# Find large tables
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename))
FROM pg_tables
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
LIMIT 10;

# Vacuum to reclaim space
VACUUM FULL;
```

---

## 📋 Monitoring Checklist

### Daily
- [ ] Check connection count
- [ ] Review long-running queries
- [ ] Check cache hit ratio
- [ ] Review error logs

### Weekly
- [ ] Analyze slow query trends
- [ ] Check table bloat
- [ ] Review index usage
- [ ] Check disk space usage

### Monthly
- [ ] Vacuum full database
- [ ] Reindex tables
- [ ] Review and optimize queries
- [ ] Update PostgreSQL statistics
- [ ] Review security logs

---

## 🔗 Useful Tools

1. **pgAdmin** - GUI for PostgreSQL  
   Download: https://www.pgadmin.org/

2. **DBeaver** - Universal database tool  
   Download: https://dbeaver.io/

3. **pg_stat_statements** - Query performance tracking  
   Docs: https://www.postgresql.org/docs/current/pgstatstatements.html

4. **Grafana** - Monitoring dashboards  
   https://grafana.com/

5. **Prometheus** - Time-series metrics  
   https://prometheus.io/

6. **Datadog** - Full monitoring platform (paid)  
   https://www.datadoghq.com/

---

## 🎓 Next Steps

1. ✅ Enable pg_stat_statements extension
2. ✅ Configure PostgreSQL for monitoring
3. ✅ Add monitoring router to backend
4. ✅ Test monitoring endpoints
5. ✅ Set up Grafana dashboard
6. ✅ Configure alerts (email/Slack)
7. ✅ Schedule regular health checks
8. ✅ Document baseline metrics

---

**Need help?** Check the logs at `/var/log/postgresql/` or run:
```sql
SELECT * FROM pg_stat_activity WHERE state != 'idle';
```
