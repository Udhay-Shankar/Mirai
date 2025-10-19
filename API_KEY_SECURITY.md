# 🔐 API Key Security Guide

## ⚠️ CRITICAL: Your API Key Was Exposed!

You shared this key publicly:
```
sk_1330845c413fba4ccde270c9adc94ff01e0710eb54f24b4c43ab9c6e622ad8a9
```

**This key is now compromised and MUST be revoked immediately!**

---

## 🚨 Immediate Actions Required

### 1. Revoke the Exposed Key
1. Log into your API provider dashboard
2. Find the key: `sk_1330845c413fba4ccde270c9adc94ff01e0710eb54f24b4c43ab9c6e622ad8a9`
3. Click "Revoke" or "Delete"
4. Generate a new key

### 2. Update Your Application Securely

**DO NOT paste the new key in chat or anywhere public!**

Instead, follow these steps:

```powershell
# Navigate to backend directory
cd c:\Users\udhay\OneDrive\Desktop\Mirai\backend

# Run the secure setup script
python setup_env.py
```

The script will:
- ✅ Create a `.env` file (protected by .gitignore)
- ✅ Prompt for your API keys securely
- ✅ Generate JWT secret automatically
- ✅ Verify security settings

### 3. Verify Security

```powershell
# Check that .env is NOT tracked by Git
git status

# You should NOT see .env in the list
# If you do see it, run:
git rm --cached .env
```

---

## 🔒 How to Store API Keys Securely

### ✅ CORRECT Way (Use .env file)

**1. Create `.env` file in backend directory:**
```bash
# backend/.env
SOCIAL_MEDIA_API_KEY=sk_your_new_api_key_here
AWARIO_API_KEY=your_awario_key_here
JWT_SECRET_KEY=generated_secret_key_here
```

**2. Load in your application:**
```python
# backend/app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    social_media_api_key: str
    
    class Config:
        env_file = ".env"

settings = Settings()
# Access: settings.social_media_api_key
```

**3. Use in your code:**
```python
# backend/app/analytics/social_media_api.py
from app.config import settings

api_key = settings.social_media_api_key  # Loaded from .env
```

---

### ❌ WRONG Ways (NEVER DO THIS!)

**DON'T hardcode in code:**
```python
# ❌ WRONG - visible in Git
API_KEY = "sk_1330845c413fba4ccde270c9adc94ff01e0710eb54f24b4c"
```

**DON'T share in chat:**
```
❌ "Hey, use this key: sk_abc123..."
```

**DON'T commit to Git:**
```bash
# ❌ WRONG
git add .env
git commit -m "Add API keys"  # Keys now public!
```

**DON'T put in frontend code:**
```javascript
// ❌ WRONG - exposed to browser
const API_KEY = "sk_abc123...";
```

**DON'T share in screenshots:**
```
❌ Including .env file contents in screenshots
```

---

## 🛡️ Security Best Practices

### 1. Use Environment Variables

**Development:**
```bash
# .env (local, not committed)
SOCIAL_MEDIA_API_KEY=sk_dev_key_here
```

**Production:**
```bash
# Set in hosting platform (Heroku, AWS, etc.)
heroku config:set SOCIAL_MEDIA_API_KEY=sk_prod_key_here
```

### 2. Different Keys for Different Environments

```
Development:  sk_dev_abc123...
Staging:      sk_staging_def456...
Production:   sk_prod_ghi789...
```

### 3. Rotate Keys Regularly

- Change keys every 90 days
- Immediately after team member leaves
- After any suspected breach

### 4. Use Key Restrictions

Configure in your API provider dashboard:
- ✅ IP whitelist (only your server IPs)
- ✅ Rate limits
- ✅ Usage alerts
- ✅ Expiration dates

### 5. Monitor Usage

Set up alerts for:
- Unusual request patterns
- High usage spikes
- Failed authentication attempts
- Requests from unexpected IPs

---

## 📋 .gitignore Verification

**Ensure these files are in `.gitignore`:**

```gitignore
# Environment variables
.env
.env.local
.env.*.local
.env.development
.env.production

# API keys
**/api_keys.txt
**/secrets.json
**/*secret*
**/*key*.txt

# Firebase
firebase-credentials.json
serviceAccountKey.json

# Database
*.db
*.sqlite
*.sqlite3
```

**Verify:**
```powershell
# Check if .env is ignored
git check-ignore .env
# Should output: .env

# Check Git status
git status
# Should NOT show .env
```

---

## 🔧 Using API Keys in Code

### Backend (Python/FastAPI)

**1. Configuration:**
```python
# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    social_media_api_key: str
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
```

**2. Usage:**
```python
# app/services/social_media_service.py
import requests
from app.config import settings

class SocialMediaAPI:
    def __init__(self):
        self.api_key = settings.social_media_api_key
        self.base_url = "https://api.socialmedia.com/v1"
    
    def analyze_sentiment(self, text: str):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            f"{self.base_url}/analyze",
            headers=headers,
            json={"text": text}
        )
        
        return response.json()
```

### Frontend (NEVER store API keys!)

**❌ WRONG:**
```javascript
// DON'T do this - exposed in browser
const API_KEY = "sk_abc123";
```

**✅ CORRECT:**
```javascript
// Call your backend API instead
const response = await fetch('/api/analyze', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${userToken}`,  // User's JWT token
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ text: "analyze this" })
});

// Backend uses the API key securely
```

---

## 🐳 Docker/Container Deployment

### Option 1: Environment Variables

**docker-compose.yml:**
```yaml
services:
  backend:
    build: ./backend
    environment:
      - SOCIAL_MEDIA_API_KEY=${SOCIAL_MEDIA_API_KEY}
    # Or from .env file:
    env_file:
      - .env
```

### Option 2: Docker Secrets

```yaml
services:
  backend:
    secrets:
      - social_media_api_key

secrets:
  social_media_api_key:
    file: ./secrets/api_key.txt
```

### Option 3: Kubernetes Secrets

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: api-keys
type: Opaque
stringData:
  social-media-api-key: sk_your_key_here
```

---

## ☁️ Cloud Deployment

### AWS

```bash
# Use AWS Secrets Manager
aws secretsmanager create-secret \
  --name mirai/social-media-api-key \
  --secret-string "sk_your_key_here"

# Load in application
import boto3

client = boto3.client('secretsmanager')
secret = client.get_secret_value(SecretId='mirai/social-media-api-key')
api_key = secret['SecretString']
```

### Heroku

```bash
# Set config vars
heroku config:set SOCIAL_MEDIA_API_KEY=sk_your_key_here

# View (masked)
heroku config
```

### Azure

```bash
# Use Azure Key Vault
az keyvault secret set \
  --vault-name mirai-vault \
  --name social-media-api-key \
  --value "sk_your_key_here"
```

### DigitalOcean

```bash
# Use environment variables in App Platform
doctl apps create-deployment \
  --env SOCIAL_MEDIA_API_KEY=sk_your_key_here
```

---

## 🔍 Checking for Exposed Keys

### 1. Check Git History

```bash
# Search for API keys in Git history
git log -p | grep -i "api.key\|secret\|sk_"

# If found, you MUST:
# 1. Revoke the key
# 2. Remove from Git history (advanced)
git filter-branch --tree-filter 'rm -f .env' HEAD
```

### 2. Use Secret Scanning Tools

```bash
# Install truffleHog
pip install truffleHog

# Scan repository
trufflehog --regex --entropy=False .

# Install gitleaks
brew install gitleaks  # Mac
choco install gitleaks  # Windows

# Scan
gitleaks detect --source . --verbose
```

### 3. GitHub Secret Scanning

GitHub automatically scans for leaked secrets and alerts you.

Enable: Settings → Security → Secret scanning

---

## 📞 What to Do If Key Is Leaked

### Immediate (Within 5 minutes):

1. **Revoke the key** - Make it unusable
2. **Generate new key** - Get a replacement
3. **Update .env** - Use new key locally
4. **Deploy new key** - Update production

### Short-term (Within 1 hour):

5. **Check logs** - Look for unauthorized usage
6. **Review bills** - Check for unusual charges
7. **Notify team** - Alert relevant people
8. **Update docs** - Document the incident

### Long-term:

9. **Implement monitoring** - Set up alerts
10. **Review processes** - Prevent future leaks
11. **Security audit** - Check other keys
12. **Training** - Educate team on security

---

## 🎯 Quick Setup Checklist

- [ ] Run `python setup_env.py` in backend directory
- [ ] Enter your NEW API key (after revoking old one)
- [ ] Verify `.env` file is created
- [ ] Check `.env` is in `.gitignore`
- [ ] Test application loads key correctly
- [ ] Never commit `.env` to Git
- [ ] Use different keys for dev/prod
- [ ] Set up key rotation schedule
- [ ] Configure usage alerts
- [ ] Document key management process

---

## 📚 Additional Resources

- **OWASP API Security**: https://owasp.org/www-project-api-security/
- **12-Factor App**: https://12factor.net/config
- **GitHub Secret Scanning**: https://docs.github.com/en/code-security/secret-scanning
- **AWS Secrets Manager**: https://aws.amazon.com/secrets-manager/
- **Hashicorp Vault**: https://www.vaultproject.io/

---

## 🆘 Need Help?

If you:
- Can't revoke the exposed key
- Need help securing your application
- Found keys in Git history
- Have questions about deployment

**DO NOT share keys in messages!**

Instead:
1. Revoke the key first
2. Ask general security questions
3. Get help with setup process
4. Review security best practices

---

**Remember: Treat API keys like passwords - NEVER share them publicly!** 🔐
