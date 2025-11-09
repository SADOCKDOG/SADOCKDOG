# 🔐 SADOCKDOG Security Policy

## 📢 Reporting Security Vulnerabilities

**DO NOT** create a public GitHub issue for security vulnerabilities.

Instead, please report security issues privately to:
- **GitHub Security Advisories**: https://github.com/SADOCKDOG/SADOCKDOG/security/advisories/new
- **Email**: security@sadockdog.io (if you prefer private email)

We will acknowledge your report within 48 hours and provide a detailed response within 7 days.

## 🛡️ Supported Versions

| Version | Supported          |
|---------|--------------------|
| latest  | ✅ Full support    |
| < 1.0   | ❌ Not supported   |

## 🔍 Security Best Practices

### Environment Variables & Secrets
- ✅ Use `.env` files for local development (never commit)
- ✅ Use GitHub Secrets for CI/CD
- ✅ Rotate secrets regularly (every 90 days minimum)
- ❌ Never hardcode secrets in source code
- ❌ Never use default/demo credentials in production

### Dependencies
- ✅ Dependabot enabled (weekly updates)
- ✅ CodeQL security analysis on every PR
- ✅ Regular `pnpm audit` and `poetry run safety check`

### Network Security
- ✅ Use HTTPS in production
- ✅ Configure CORS for production domains only
- ✅ Enable rate limiting
- ✅ Use secure headers (HSTS, CSP)

## 📚 Resources

- [Full Security Guide](DEPLOYMENT.md#-security-best-practices)
- [Deployment Checklist](DEPLOYMENT.md#-pre-deployment-checklist)
- [Architecture](ARCHITECTURE.md#-security-architecture)

## 🏆 Security Hall of Fame

We recognize and thank security researchers who responsibly disclose vulnerabilities.

<!-- Contributors will be added here -->

---

**Last Updated**: November 2025
