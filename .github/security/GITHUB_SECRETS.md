# 🔐 GitHub Secrets Configuration Guide

## Overview

This guide documents all GitHub Secrets needed for SADOCKDOG CI/CD pipelines and deployments.

## 📋 Required Secrets

### Backend Secrets

Configure these in `Settings` → `Secrets and variables` → `Actions`:

| Secret Name | Description | How to Generate | Example |
|------------|-------------|-----------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | From your database provider | `postgresql://user:pass@host:5432/db` |
| `DIRECT_URL` | Direct database URL (same as DATABASE_URL for most cases) | Same as DATABASE_URL | `postgresql://user:pass@host:5432/db` |
| `REDIS_URL` | Redis connection string | From Redis provider | `redis://default:pass@host:6379` |
| `ENCRYPTION_KEY` | Data encryption key | `openssl rand -base64 32` | `abc123...` (32+ chars) |
| `JWT_SECRET` | JWT signing secret | `openssl rand -base64 32` | `xyz789...` (32+ chars) |
| `POSTGRES_PASSWORD` | PostgreSQL password | `openssl rand -base64 32` | Strong random password |

### Optional Backend Secrets (if using these services)

| Secret Name | Description | Where to Get |
|------------|-------------|--------------|
| `OPENAI_API_KEY` | OpenAI API key | https://platform.openai.com/api-keys |
| `ANTHROPIC_API_KEY` | Anthropic API key | https://console.anthropic.com/settings/keys |
| `SENTRY_DSN` | Sentry error tracking DSN | https://sentry.io/settings/projects/ |
| `STRIPE_SECRET_KEY` | Stripe payment key | https://dashboard.stripe.com/apikeys |

### Frontend Secrets

| Secret Name | Description | Notes |
|------------|-------------|-------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | Public (visible in browser), but environment-specific |
| `SUPABASE_URL` | Supabase project URL | From Supabase dashboard |
| `SUPABASE_ANON_KEY` | Supabase anonymous key | From Supabase dashboard (public key, safe for client) |
| `NEXT_PUBLIC_SUPABASE_URL` | Same as SUPABASE_URL | For Next.js client-side access |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Same as SUPABASE_ANON_KEY | For Next.js client-side access |

## 🛠️ How to Add Secrets

### Via GitHub UI:

1. Navigate to your repository on GitHub
2. Click `Settings` → `Secrets and variables` → `Actions`
3. Click `New repository secret`
4. Enter the **Name** and **Value**
5. Click `Add secret`

### Via GitHub CLI:

```bash
# Install GitHub CLI
# https://cli.github.com/

# Login
gh auth login

# Add a secret
gh secret set DATABASE_URL --body "postgresql://user:pass@host:5432/db"

# Add secret from file
gh secret set PRIVATE_KEY < private_key.pem

# List all secrets
gh secret list
```

## 🔒 Generating Secure Values

### Random Passwords (32+ characters):
```bash
openssl rand -base64 32
```

### Encryption Keys (Fernet):
```python
# Python
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
```

### UUID-based Secrets:
```bash
python -c "import uuid; print(str(uuid.uuid4()))"
```

### JWT Secret (256-bit):
```bash
openssl rand -hex 32
```

## 📝 Environment-Specific Secrets

### Development (Local)

Store in `.env` (never commit):
```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/sadockdog_dev
REDIS_URL=redis://localhost:6379
ENCRYPTION_KEY=dev_key_only_for_local_testing
JWT_SECRET=dev_jwt_secret_only_for_local_testing
```

### Staging

GitHub Secrets for staging environment:
```
DATABASE_URL → staging database
NEXT_PUBLIC_API_URL → https://api-staging.sadockdog.com
```

### Production

GitHub Secrets for production environment:
```
DATABASE_URL → production database (strong password!)
NEXT_PUBLIC_API_URL → https://api.sadockdog.com
ENCRYPTION_KEY → Strong random key (rotate every 90 days)
JWT_SECRET → Strong random key (rotate every 90 days)
```

## 🔄 Secret Rotation Schedule

| Secret Type | Rotation Frequency | Impact |
|------------|-------------------|--------|
| Database passwords | Every 90 days | High - requires app restart |
| API keys (external) | When compromised | Medium - depends on service |
| JWT secrets | Every 90 days | High - invalidates all sessions |
| Encryption keys | Every 180 days | Critical - requires data re-encryption |

### Rotation Process:

1. Generate new secret
2. Add new secret to GitHub Secrets (keep old one temporarily)
3. Deploy with dual-secret support (accept both old and new)
4. Update all services to use new secret
5. Remove old secret after 24 hours

## ✅ Security Checklist

Before going to production:

- [ ] All secrets use strong random values (not defaults)
- [ ] No secrets committed to version control
- [ ] `.env` file in `.gitignore`
- [ ] GitHub Secrets configured for production
- [ ] Secrets rotation schedule documented
- [ ] Team members know how to access secrets securely
- [ ] Backup of critical secrets stored securely (encrypted vault)

## 🚨 What to Do if Secrets are Compromised

### Immediate Actions (within 1 hour):

1. **Rotate compromised secret immediately**
   ```bash
   gh secret set COMPROMISED_KEY --body "new_secure_value"
   ```

2. **Revoke old credentials** (database, API keys, etc.)

3. **Deploy updated secrets**
   ```bash
   # Trigger deployment with new secrets
   git commit --allow-empty -m "chore: rotate compromised secrets"
   git push origin master
   ```

4. **Monitor for unauthorized access**
   - Check logs for suspicious activity
   - Review recent database queries
   - Check API usage patterns

### Follow-up Actions (within 24 hours):

1. Conduct post-mortem analysis
2. Update security procedures
3. Notify affected users if necessary
4. Document incident in security log

## 📚 Resources

- [GitHub Encrypted Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [SADOCKDOG Deployment Guide](../DEPLOYMENT.md)
- [SADOCKDOG Security Policy](../SECURITY.md)

## 🔧 Troubleshooting

### Secret not available in workflow

**Problem**: Workflow fails with "secret not found"

**Solution**:
```yaml
# Ensure secret name matches exactly (case-sensitive)
env:
  DATABASE_URL: ${{ secrets.DATABASE_URL }}  # Correct
  # database_url: ${{ secrets.database_url }}  # Wrong (case mismatch)
```

### Secret value contains special characters

**Problem**: Secret breaks when it contains `$`, `` ` ``, or newlines

**Solution**:
```bash
# Base64 encode the secret
echo -n "my$secret`value" | base64
# Add the base64 value to GitHub Secrets

# Decode in workflow
echo "${{ secrets.MY_SECRET }}" | base64 -d
```

### Need to use secret in multiple workflows

**Solution**: Secrets are repository-wide, accessible to all workflows automatically.

---

**Last Updated**: November 2025  
**Maintained by**: SADOCKDOG DevOps Team
