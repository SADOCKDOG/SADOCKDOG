# 🔒 Security Checklist for Production Deployment

> ⚠️ **CRITICAL**: Never deploy to production without completing this checklist

## Pre-Deployment Security Checklist

### 1. Environment Variables & Secrets

- [ ] **Copy `.env.default` to `.env`** and customize all values
- [ ] **Generate strong passwords** for all services:
  ```bash
  # Generate strong random passwords (minimum 32 characters)
  openssl rand -base64 32
  ```
- [ ] **Change these CRITICAL values in `.env`**:
  - [ ] `POSTGRES_PASSWORD` - Database password
  - [ ] `JWT_SECRET` - JWT signing secret (min 32 chars)
  - [ ] `DASHBOARD_PASSWORD` - Admin dashboard password
  - [ ] `SECRET_KEY_BASE` - Application secret key
  - [ ] `VAULT_ENC_KEY` - Encryption key (min 32 chars)
  - [ ] `RABBITMQ_DEFAULT_PASS` - Message queue password

- [ ] **Generate new Supabase keys** (don't use demo keys):
  ```bash
  # Follow: https://supabase.com/docs/guides/self-hosting
  ```

- [ ] **Verify `.env` is in `.gitignore`**:
  ```bash
  git check-ignore .env
  # Should output: .env
  ```

### 2. API Keys & OAuth Credentials

- [ ] **Obtain production API keys** for services you use:
  - [ ] OpenAI API Key (if using AI features)
  - [ ] GitHub OAuth (client ID & secret)
  - [ ] Google OAuth (client ID & secret)
  - [ ] Other integrations as needed

- [ ] **Configure OAuth callback URLs** for production domain:
  ```
  Production URL: https://your-domain.com/auth/integrations/oauth_callback
  ```

### 3. Database Security

- [ ] **Change PostgreSQL password** from default
- [ ] **Enable SSL/TLS** for database connections
- [ ] **Restrict database access** to application network only
- [ ] **Set up regular backups**:
  ```bash
  # Example backup command
  docker exec db pg_dump -U postgres postgres > backup_$(date +%Y%m%d).sql
  ```
- [ ] **Enable logical replication** if using Supabase features

### 4. Application Security

- [ ] **Update CORS settings** for production domains:
  ```bash
  # In backend/.env
  ALLOWED_ORIGINS=https://your-domain.com
  ```

- [ ] **Disable debug mode**:
  ```bash
  # In backend/.env
  DEBUG=false
  LOG_LEVEL=INFO
  ```

- [ ] **Configure rate limiting** appropriately
- [ ] **Enable HTTPS/TLS** for all services
- [ ] **Set secure cookie flags**:
  ```bash
  COOKIE_SECURE=true
  COOKIE_HTTPONLY=true
  COOKIE_SAMESITE=strict
  ```

### 5. Frontend Security

- [ ] **Update frontend environment** (`frontend/.env`):
  - [ ] `NEXT_PUBLIC_SUPABASE_URL` - Production Supabase URL
  - [ ] `NEXT_PUBLIC_SUPABASE_ANON_KEY` - Production anon key
  - [ ] `NEXT_PUBLIC_AGPT_SERVER_URL` - Production API URL
  - [ ] `NEXT_PUBLIC_FRONTEND_BASE_URL` - Production frontend URL

- [ ] **Set production app environment**:
  ```bash
  NEXT_PUBLIC_APP_ENV=production
  NEXT_PUBLIC_BEHAVE_AS=PRODUCTION
  ```

- [ ] **Configure security headers** in Next.js config
- [ ] **Enable CSP (Content Security Policy)**

### 6. Docker & Infrastructure

- [ ] **Use specific image versions** (not `latest` tags)
- [ ] **Scan images for vulnerabilities**:
  ```bash
  docker scan your-image:tag
  ```

- [ ] **Set resource limits** for containers
- [ ] **Configure health checks** for all services
- [ ] **Set up monitoring and logging**:
  - [ ] Configure Sentry DSN
  - [ ] Set up log aggregation
  - [ ] Configure alerting

### 7. Network Security

- [ ] **Configure firewall rules**:
  - Only expose necessary ports (80, 443)
  - Block direct database access from internet
  - Restrict admin interfaces

- [ ] **Set up reverse proxy** (nginx/traefik) with:
  - [ ] SSL/TLS termination
  - [ ] Rate limiting
  - [ ] Request filtering

- [ ] **Enable DDoS protection**

### 8. Authentication & Authorization

- [ ] **Disable auto-confirm** for email/phone:
  ```bash
  ENABLE_EMAIL_AUTOCONFIRM=false
  ENABLE_PHONE_AUTOCONFIRM=false
  ```

- [ ] **Configure JWT expiry** appropriately:
  ```bash
  JWT_EXPIRY=3600  # 1 hour
  ```

- [ ] **Enable MFA/2FA** if available
- [ ] **Set up user roles and permissions**

### 9. File Upload Security

- [ ] **Configure ClamAV** for virus scanning
- [ ] **Set file size limits**:
  ```bash
  CLAMD_CONF_MaxFileSize=100M
  CLAMD_CONF_MaxScanSize=100M
  ```

- [ ] **Restrict allowed file types**
- [ ] **Use secure storage** (S3, GCS, etc.)

### 10. Email Configuration

- [ ] **Configure production SMTP** settings:
  - [ ] `SMTP_HOST`
  - [ ] `SMTP_PORT`
  - [ ] `SMTP_USER`
  - [ ] `SMTP_PASS`
  - [ ] `SMTP_ADMIN_EMAIL`

- [ ] **Set up SPF, DKIM, DMARC** records

### 11. Monitoring & Logging

- [ ] **Set up error tracking** (Sentry)
- [ ] **Configure log retention** policies
- [ ] **Set up uptime monitoring**
- [ ] **Configure performance monitoring**
- [ ] **Set up security audit logging**

### 12. Compliance & Privacy

- [ ] **Review data retention** policies
- [ ] **Implement GDPR compliance** (if applicable)
- [ ] **Add privacy policy** and terms of service
- [ ] **Set up data backup** and recovery procedures

### 13. Testing

- [ ] **Run security scans**:
  ```bash
  # Example with OWASP ZAP
  docker run -t owasp/zap2docker-stable zap-baseline.py -t https://your-domain.com
  ```

- [ ] **Perform penetration testing**
- [ ] **Test backup and restore** procedures
- [ ] **Test disaster recovery** plan
- [ ] **Load testing** to ensure scalability

### 14. Documentation

- [ ] **Document deployment process**
- [ ] **Create runbook** for common issues
- [ ] **Document disaster recovery** procedures
- [ ] **Create security incident response** plan

## Post-Deployment

- [ ] **Rotate secrets** regularly (every 90 days)
- [ ] **Monitor logs** for suspicious activity
- [ ] **Keep dependencies updated**:
  ```bash
  # Backend
  cd backend && poetry update
  
  # Frontend
  cd frontend && pnpm update
  ```

- [ ] **Review access logs** regularly
- [ ] **Conduct security audits** quarterly

## Quick Security Commands

### Generate Strong Passwords
```bash
# 32-character random password
openssl rand -base64 32

# 64-character random password
openssl rand -base64 48
```

### Generate Encryption Keys
```python
# Fernet encryption key
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
```

### Check for Exposed Secrets
```bash
# Install gitleaks
# https://github.com/gitleaks/gitleaks

# Scan repository
gitleaks detect --source . --verbose
```

## Resources

- [Supabase Self-Hosting Guide](https://supabase.com/docs/guides/self-hosting)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Docker Security Best Practices](https://docs.docker.com/develop/security-best-practices/)
- [Next.js Security Headers](https://nextjs.org/docs/advanced-features/security-headers)

---

**Last Updated**: 2025-11-08

⚠️ **Remember**: Security is an ongoing process, not a one-time task!
