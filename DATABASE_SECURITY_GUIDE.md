# 🔒 Database & Credentials Security Guide

## ⚠️ YES - Your Database Can Be Accessed by Anyone with Credentials!

If someone gets your `DATABASE_URL`, they have **FULL ACCESS** to:
- ✅ Read all user data
- ✅ Modify user data
- ✅ Delete tables
- ✅ Steal passwords (hashed, but still dangerous)
- ✅ Access subscription information
- ✅ See all social media data

---

## 🛡️ Security Layers You MUST Implement

### 1. Environment Variables Protection

**✅ GOOD (You're doing this):**
```gitignore
# In .gitignore
.env
.env.local
.env.production
```

**❌ NEVER DO THIS:**
```python
# DON'T hardcode credentials
DATABASE_URL = "postgresql://user:password@localhost/db"
```

**✅ DO THIS:**
```python
# Use environment variables
DATABASE_URL = os.getenv('DATABASE_URL')
```

---

### 2. Database Access Control

#### PostgreSQL User Permissions

Create separate database users with limited permissions:

```sql
-- 1. Create read-only user for analytics
CREATE USER analytics_readonly WITH PASSWORD 'strong_password_here';
GRANT CONNECT ON DATABASE mirai TO analytics_readonly;
GRANT USAGE ON SCHEMA public TO analytics_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO analytics_readonly;

-- 2. Create app user with limited permissions
CREATE USER mirai_app WITH PASSWORD 'strong_password_here';
GRANT CONNECT ON DATABASE mirai TO mirai_app;
GRANT USAGE ON SCHEMA public TO mirai_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO mirai_app;

-- 3. Revoke dangerous permissions
REVOKE DROP, TRUNCATE ON ALL TABLES IN SCHEMA public FROM mirai_app;

-- 4. Don't use superuser/postgres account for app!
```

---

### 3. Network Security

#### Option A: Localhost Only (Development)
```ini
# PostgreSQL config: postgresql.conf
listen_addresses = 'localhost'  # Only accept local connections
```

#### Option B: Specific IP Whitelist (Production)
```ini
# PostgreSQL config: pg_hba.conf
# Allow only your backend server IP
host    mirai    mirai_app    YOUR_BACKEND_IP/32    scram-sha-256
host    mirai    mirai_app    127.0.0.1/32          scram-sha-256
```

#### Option C: Cloud Database with Firewall
If using managed PostgreSQL (AWS RDS, Azure, DigitalOcean):
- ✅ Enable firewall rules
- ✅ Whitelist only your backend server IP
- ✅ Require SSL/TLS connections
- ✅ Use VPC/private network

---

### 4. Connection String Security

#### ❌ EXPOSED CONNECTION STRING
```env
# DON'T expose all details in one string
DATABASE_URL=postgresql://admin:SuperSecret123@db.example.com:5432/mirai
```

**Problems:**
- Username visible
- Password visible
- Host visible
- Everything in one place

#### ✅ SECURE CONNECTION STRING
```env
# Use separate variables
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mirai
DB_USER=mirai_app
DB_PASSWORD=use_secrets_manager_in_production

# Or use connection pooling service
DATABASE_URL=postgresql://user:pass@pgbouncer-internal:6432/mirai?sslmode=require
```

---

### 5. Secrets Management (Production)

**Development:**
```bash
# .env file (not committed to git)
DATABASE_URL=postgresql://localhost/mirai_dev
```

**Production - Option A: Cloud Secrets Manager**
```python
# AWS Secrets Manager
import boto3
import json

def get_db_credentials():
    client = boto3.client('secretsmanager')
    secret = client.get_secret_value(SecretId='mirai/db/credentials')
    return json.loads(secret['SecretString'])

# Use in config
creds = get_db_credentials()
DATABASE_URL = f"postgresql://{creds['username']}:{creds['password']}@{creds['host']}/{creds['database']}"
```

**Production - Option B: Environment Variables (Docker/K8s)**
```yaml
# Kubernetes Secret
apiVersion: v1
kind: Secret
metadata:
  name: mirai-db-secret
type: Opaque
data:
  database-url: <base64-encoded-connection-string>
```

**Production - Option C: Vault**
```python
import hvac

client = hvac.Client(url='https://vault.example.com')
secret = client.secrets.kv.v2.read_secret_version(path='mirai/database')
DATABASE_URL = secret['data']['data']['connection_string']
```

---

### 6. SSL/TLS Encryption

Always use encrypted connections in production:

```python
# In database.py
from sqlalchemy import create_engine

# Force SSL connection
DATABASE_URL = "postgresql://user:pass@host/db?sslmode=require"

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "sslmode": "require",
        "sslrootcert": "/path/to/ca-certificate.crt",
        "sslcert": "/path/to/client-cert.pem",
        "sslkey": "/path/to/client-key.pem"
    }
)
```

---

### 7. Credential Rotation

**Automate password rotation:**

```python
# rotate_db_password.py
import boto3
from datetime import datetime, timedelta

def should_rotate(last_rotation_date):
    """Rotate every 90 days"""
    return datetime.now() - last_rotation_date > timedelta(days=90)

def rotate_database_password():
    # 1. Generate new password
    new_password = generate_secure_password()
    
    # 2. Update database user
    execute_sql(f"ALTER USER mirai_app PASSWORD '{new_password}'")
    
    # 3. Update secrets manager
    update_secret('mirai/db/password', new_password)
    
    # 4. Restart application (rolling restart)
    restart_app_servers()
```

---

### 8. Monitoring & Alerts

**Set up alerts for suspicious activity:**

```sql
-- PostgreSQL audit logging
CREATE EXTENSION IF NOT EXISTS pgaudit;

-- Log all connections
ALTER SYSTEM SET log_connections = 'on';
ALTER SYSTEM SET log_disconnections = 'on';

-- Log failed authentication attempts
ALTER SYSTEM SET log_statement = 'all';
```

**Monitor for:**
- ✅ Failed login attempts (brute force)
- ✅ Connections from unexpected IPs
- ✅ Unusual query patterns (SQL injection attempts)
- ✅ Large data exports
- ✅ Schema modifications (DROP, ALTER)

---

### 9. Backup & Disaster Recovery

```bash
# Automated encrypted backups
pg_dump mirai | gpg --encrypt --recipient admin@mirai.com > backup_$(date +%Y%m%d).sql.gpg

# Store backups in secure location with different credentials
aws s3 cp backup.sql.gpg s3://mirai-backups-encrypted/ --sse AES256
```

---

### 10. Application-Level Security

**In your FastAPI backend:**

```python
# Rate limiting for auth endpoints
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.post("/api/auth/login")
@limiter.limit("5/minute")  # Max 5 login attempts per minute
async def login(credentials: UserLogin):
    # ... login logic
    pass

# IP whitelisting for admin endpoints
from fastapi import Request, HTTPException

ALLOWED_ADMIN_IPS = ["192.168.1.100", "10.0.0.5"]

async def verify_admin_ip(request: Request):
    client_ip = request.client.host
    if client_ip not in ALLOWED_ADMIN_IPS:
        raise HTTPException(status_code=403, detail="Access denied")

@router.get("/admin/users")
async def admin_users(verify: None = Depends(verify_admin_ip)):
    # ... admin logic
    pass
```

---

## 🚨 What To Do If Credentials Are Exposed

### Immediate Actions (within minutes):

1. **Revoke compromised credentials**
   ```sql
   ALTER USER mirai_app WITH PASSWORD 'new_temporary_password';
   ```

2. **Check for unauthorized access**
   ```sql
   SELECT * FROM pg_stat_activity WHERE usename = 'mirai_app';
   ```

3. **Review audit logs**
   ```sql
   SELECT * FROM pg_stat_statements ORDER BY calls DESC;
   ```

4. **Terminate suspicious connections**
   ```sql
   SELECT pg_terminate_backend(pid) 
   FROM pg_stat_activity 
   WHERE usename = 'mirai_app' 
   AND client_addr NOT IN ('your_trusted_ips');
   ```

5. **Update all environment variables**
6. **Restart all application servers**
7. **Notify affected users** (if data breach occurred)
8. **Review security policies**

---

## 🎯 Quick Security Checklist

### Development
- [x] `.env` in `.gitignore`
- [ ] Use localhost-only database
- [ ] Weak passwords OK for dev
- [ ] No SSL required

### Staging
- [ ] Separate database from production
- [ ] Use limited permission user
- [ ] Enable SSL connections
- [ ] IP whitelist enabled
- [ ] Monitor access logs

### Production
- [ ] Strong random passwords (32+ chars)
- [ ] SSL/TLS required
- [ ] Secrets manager (not .env files)
- [ ] IP whitelist strictly enforced
- [ ] Firewall rules configured
- [ ] Audit logging enabled
- [ ] Automated backups
- [ ] Credential rotation (90 days)
- [ ] Monitoring & alerts set up
- [ ] Separate read-only users for analytics
- [ ] VPC/Private network
- [ ] Multi-factor authentication for DB access
- [ ] Regular security audits

---

## 📋 Recommended Production Setup

```
┌─────────────────────────────────────┐
│   User Browser                       │
└──────────────┬──────────────────────┘
               │ HTTPS (TLS 1.3)
               ↓
┌─────────────────────────────────────┐
│   Load Balancer (with WAF)          │
└──────────────┬──────────────────────┘
               │ Private network
               ↓
┌─────────────────────────────────────┐
│   Backend API Servers               │
│   - JWT validation                   │
│   - Rate limiting                    │
│   - IP whitelisting                  │
└──────────────┬──────────────────────┘
               │ SSL connection
               │ Limited DB user
               ↓
┌─────────────────────────────────────┐
│   PostgreSQL (Private subnet)       │
│   - Firewall: only backend IPs      │
│   - Encrypted at rest               │
│   - Automated backups               │
│   - Audit logging                    │
└─────────────────────────────────────┘
```

---

## 🔐 Generate Strong Credentials

```python
# Generate strong database password
import secrets
import string

def generate_db_password(length=32):
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password

print(f"DB_PASSWORD={generate_db_password()}")
# Output: DB_PASSWORD=xK9#mP2@vL8!qR5$nW7&tY3^uH6*aE4
```

---

## 💡 Key Takeaways

1. **Never commit credentials to Git** ✅ You're doing this
2. **Use principle of least privilege** - App user ≠ Admin user
3. **Enable SSL/TLS in production** - Encrypt connections
4. **Whitelist IPs** - Only allow known servers
5. **Use secrets managers** - Not .env files in production
6. **Rotate credentials regularly** - Every 90 days
7. **Monitor & audit** - Detect breaches early
8. **Backup & encrypt** - Disaster recovery plan

---

**Your current risk level:**
- 🟢 **Development**: Low (localhost only)
- 🟡 **Staging**: Medium (needs IP whitelist)
- 🔴 **Production**: HIGH if not following above guidelines

Need help implementing any of these security measures? Let me know!
