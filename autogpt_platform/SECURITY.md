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

- [ ] **Configure hidden system credentials** (`frontend/.env`):
  
  System credentials are built-in "Use Credits for X" credentials that should be hidden from the UI.
  Configure these via environment variables instead of hardcoding in source code:

  **AI/ML Providers:**
  ```bash
  NEXT_PUBLIC_HIDDEN_CRED_OLLAMA=744fdc56-071a-4761-b5a5-0af0ce10a2b5
  NEXT_PUBLIC_HIDDEN_CRED_OPENAI=53c25cb8-e3ee-465c-a4d1-e75a4c899c2a
  NEXT_PUBLIC_HIDDEN_CRED_ANTHROPIC=24e5d942-d9e3-4798-8151-90143ee55629
  NEXT_PUBLIC_HIDDEN_CRED_GROQ=4ec22295-8f97-4dd1-b42b-2c6957a02545
  NEXT_PUBLIC_HIDDEN_CRED_REPLICATE=6b9fc200-4726-4973-86c9-cd526f5ce5db
  NEXT_PUBLIC_HIDDEN_CRED_AIML=aad82a89-9794-4ebb-977f-d736aa5260a3
  NEXT_PUBLIC_HIDDEN_CRED_OPEN_ROUTER=b5a0e27d-0c98-4df3-a4b9-10193e1f3c40
  NEXT_PUBLIC_HIDDEN_CRED_NVIDIA=96b83908-2789-4dec-9968-18f0ece4ceb3
  NEXT_PUBLIC_HIDDEN_CRED_LLAMA_API=d44045af-1c33-4833-9e19-752313214de2
  ```

  **Media/Content Generation:**
  ```bash
  NEXT_PUBLIC_HIDDEN_CRED_REVID=fdb7f412-f519-48d1-9b5f-d2f73d0e01fe
  NEXT_PUBLIC_HIDDEN_CRED_IDEOGRAM=760f84fc-b270-42de-91f6-08efe1b512d0
  NEXT_PUBLIC_HIDDEN_CRED_DID=7f7b0654-c36b-4565-8fa7-9a52575dfae2
  NEXT_PUBLIC_HIDDEN_CRED_UNREAL_SPEECH=66f20754-1b81-48e4-91d0-f4f0dd82145f
  NEXT_PUBLIC_HIDDEN_CRED_FAL=6c0f5bd0-9008-4638-9d79-4b40b631803e
  ```

  **Data/Search/Tools:**
  ```bash
  NEXT_PUBLIC_HIDDEN_CRED_JINA=7f26de70-ba0d-494e-ba76-238e65e7b45f
  NEXT_PUBLIC_HIDDEN_CRED_EXA=96153e04-9c6c-4486-895f-5bb683b1ecec
  NEXT_PUBLIC_HIDDEN_CRED_E2B=78d19fd7-4d59-4a16-8277-3ce310acf2b7
  NEXT_PUBLIC_HIDDEN_CRED_MEM0=ed55ac19-356e-4243-a6cb-bc599e9b716f
  NEXT_PUBLIC_HIDDEN_CRED_APOLLO=544c62b5-1d0f-4156-8fb4-9525f11656eb
  NEXT_PUBLIC_HIDDEN_CRED_GOOGLE_MAPS=9aa1bde0-4947-4a70-a20c-84daa3850d52
  ```

  **Marketing/Communication:**
  ```bash
  NEXT_PUBLIC_HIDDEN_CRED_SMARTLEAD=3bcdbda3-84a3-46af-8fdb-bfd2472298b8
  NEXT_PUBLIC_HIDDEN_CRED_ZEROBOUNCE=63a6e279-2dc2-448e-bf57-85776f7176dc
  ```

  > **Note:** See `frontend/.env.example` for a complete reference template.
  > These IDs should match your backend credential store. If not configured, fallback values are used.

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

### 10. Email Configuration (SMTP)

Production-grade email delivery is critical for user authentication, notifications, and system alerts. 
Never use local mail services (e.g., `supabase-mail`) in production.

#### Required SMTP Configuration

Configure these environment variables in your `.env` file:

```bash
SMTP_HOST=smtp.your-provider.com
SMTP_PORT=587                      # 587 (STARTTLS) or 465 (SSL/TLS)
SMTP_USER=your-smtp-username
SMTP_PASS=your-smtp-password
SMTP_ADMIN_EMAIL=admin@yourdomain.com
SMTP_SENDER_NAME=AutoGPT Platform
```

#### Recommended SMTP Providers

**1. SendGrid (Recommended for high volume)**
- Best for: Large-scale deployments, marketing emails
- Free tier: 100 emails/day
- Setup:
  ```bash
  SMTP_HOST=smtp.sendgrid.net
  SMTP_PORT=587
  SMTP_USER=apikey
  SMTP_PASS=SG.your-sendgrid-api-key  # Generate in SendGrid dashboard
  ```
- DNS Setup: Configure sender authentication (SPF, DKIM, DMARC)
- Monitoring: Dashboard with analytics, bounce tracking, spam reports

**2. AWS SES (Simple Email Service)**
- Best for: AWS infrastructure, cost-effective at scale
- Free tier: 62,000 emails/month (from EC2)
- Setup:
  ```bash
  SMTP_HOST=email-smtp.us-east-1.amazonaws.com  # Region-specific
  SMTP_PORT=587
  SMTP_USER=your-aws-smtp-username  # From AWS IAM
  SMTP_PASS=your-aws-smtp-password  # From AWS IAM
  ```
- Requirements: Verify domain and email addresses
- Note: Starts in sandbox mode (limited to verified recipients)

**3. Mailgun**
- Best for: Transactional emails, developer-friendly API
- Free tier: 5,000 emails/month (3 months)
- Setup:
  ```bash
  SMTP_HOST=smtp.mailgun.org
  SMTP_PORT=587
  SMTP_USER=postmaster@your-domain.mailgun.org
  SMTP_PASS=your-mailgun-smtp-password
  ```
- Features: Email validation API, detailed logs, webhooks

**4. Office 365 / Outlook (Enterprise)**
- Best for: Organizations already using Microsoft 365
- Setup:
  ```bash
  SMTP_HOST=smtp.office365.com
  SMTP_PORT=587
  SMTP_USER=your-email@yourdomain.com
  SMTP_PASS=your-password  # Or app-specific password
  ```
- Limits: 10,000 recipients/day per mailbox
- Requirement: Microsoft 365 Business subscription

#### Email Deliverability Best Practices

- [ ] **Configure DNS records** for your sending domain:
  - **SPF (Sender Policy Framework)**: Prevents spoofing
    ```
    v=spf1 include:sendgrid.net ~all
    ```
  - **DKIM (DomainKeys Identified Mail)**: Cryptographic authentication
    ```
    Add TXT record provided by your SMTP provider
    ```
  - **DMARC (Domain-based Message Authentication)**: Policy for failed authentication
    ```
    v=DMARC1; p=quarantine; rua=mailto:postmaster@yourdomain.com
    ```

- [ ] **Use a dedicated sending domain** (e.g., `mail.yourdomain.com`)
- [ ] **Warm up your domain** gradually (start with low volume, increase over weeks)
- [ ] **Monitor bounce rates** (keep under 5%)
- [ ] **Monitor spam complaint rates** (keep under 0.1%)
- [ ] **Use double opt-in** for marketing emails
- [ ] **Implement unsubscribe links** in all marketing communications

#### Security Considerations

- [ ] **Never commit SMTP credentials** to version control
- [ ] **Rotate SMTP passwords** every 90 days
- [ ] **Use TLS/SSL encryption** (ports 587 or 465, never 25)
- [ ] **Restrict SMTP access** by IP address if possible
- [ ] **Monitor for unauthorized usage** (unusual send volumes)
- [ ] **Use app-specific passwords** for Gmail/Office 365

#### Testing SMTP Configuration

**Test connection:**
```bash
# Using telnet
telnet smtp.sendgrid.net 587

# Using openssl (with TLS)
openssl s_client -connect smtp.sendgrid.net:587 -starttls smtp
```

**Send test email:**
```bash
# From backend container
docker exec -it autogpt-backend-1 python -c "
from backend.util.email import send_test_email
send_test_email('test@example.com')
"
```

**Check Supabase auth logs:**
```bash
docker logs autogpt-supabase-auth-1 | grep -i smtp
```

#### Troubleshooting Common Issues

| Issue | Possible Cause | Solution |
|-------|----------------|----------|
| "Connection refused" | Wrong port or firewall | Check firewall rules, try port 465 |
| "Authentication failed" | Invalid credentials | Regenerate SMTP password, check username format |
| "TLS handshake failed" | SSL/TLS misconfiguration | Verify port (587 for STARTTLS, 465 for SSL) |
| "Emails in spam" | Missing DNS records | Configure SPF, DKIM, DMARC |
| "Rate limit exceeded" | Too many emails sent | Check provider limits, upgrade plan |
| "Domain not verified" | AWS SES sandbox mode | Verify domain in AWS SES console |

#### Monitoring & Alerts

- [ ] **Set up alerts** for:
  - Failed email deliveries (> 5% bounce rate)
  - Authentication failures
  - Unusual send volumes
  - Spam complaints

- [ ] **Monitor metrics**:
  - Delivery rate (target: > 95%)
  - Open rate (industry average: 15-25%)
  - Click rate (industry average: 2-5%)
  - Bounce rate (target: < 5%)
  - Spam complaint rate (target: < 0.1%)

- [ ] **Log all email events** for audit trail

#### Production Checklist

- [ ] SMTP provider selected and configured
- [ ] Domain verified with SMTP provider
- [ ] SPF record added to DNS
- [ ] DKIM record added to DNS
- [ ] DMARC record added to DNS
- [ ] Test email sent successfully
- [ ] Monitoring and alerts configured
- [ ] SMTP credentials stored in GitHub Secrets (for CI/CD)
- [ ] Email templates reviewed and tested
- [ ] Unsubscribe mechanism implemented (if sending marketing emails)

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
