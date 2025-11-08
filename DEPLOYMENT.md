# 🚀 SADOCKDOG Deployment Guide

## 📋 Pre-Deployment Checklist

### Environment Requirements
- ✅ Python 3.13+
- ✅ Node.js 20+
- ✅ PostgreSQL 15+
- ✅ Redis 7+
- ✅ Docker & Docker Compose (recommended)

### Security
- ✅ All secrets in environment variables
- ✅ API keys configured
- ✅ Database credentials secured
- ✅ CORS configured for production domains

### CI/CD
- ✅ All tests passing
- ✅ CodeQL security scan passed
- ✅ No high/critical vulnerabilities (Dependabot)
- ✅ Branch protection rules enforced

## 🐳 Docker Deployment (Recommended)

### Production Setup
```bash
# Clone repository
git clone https://github.com/SADOCKDOG/SADOCKDOG.git
cd SADOCKDOG/autogpt_platform

# Configure environment
cp .env.default .env
nano .env  # Set production values (or use your editor)

# Build and start services
docker-compose -f docker-compose.yml up -d

# Check status
docker-compose ps
```

### Environment Variables
```bash
# Database
DATABASE_URL="postgresql://user:pass@db:5432/sadockdog"
DIRECT_URL="postgresql://user:pass@db:5432/sadockdog"

# Redis
REDIS_URL="redis://redis:6379"

# API Keys
OPENAI_API_KEY="sk-..."
ANTHROPIC_API_KEY="sk-ant-..."

# Frontend
NEXT_PUBLIC_API_URL="https://api.yourdomain.com"

# Security
JWT_SECRET="your-secret-key"
ALLOWED_ORIGINS="https://yourdomain.com"
```

## 🔧 Manual Deployment

### Backend

```bash
cd autogpt_platform/backend

# Install dependencies
poetry install --no-dev

# Run database migrations
poetry run prisma migrate deploy

# Start server
poetry run uvicorn backend.app:app --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd autogpt_platform/frontend

# Install dependencies
pnpm install --prod

# Build
pnpm build

# Start server
pnpm start
```

## 🌐 Cloud Platforms

### Vercel (Frontend)
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd autogpt_platform/frontend
vercel --prod
```

### Railway (Backend + Database)
1. Connect GitHub repository
2. Configure environment variables
3. Deploy backend service
4. Provision PostgreSQL + Redis

### AWS / GCP / Azure
See `docker-compose.yml` for service requirements.

## 📊 Health Checks

### Backend
```bash
curl https://api.yourdomain.com/health
# Expected: {"status": "ok"}
```

### Frontend
```bash
curl https://yourdomain.com
# Expected: 200 OK
```

### Database
```bash
# Check Prisma connection (PowerShell)
cd autogpt_platform/backend
poetry run python -c "from prisma import Prisma; import asyncio; asyncio.run(Prisma().connect())"
```

## 🔄 Update Procedure

```bash
# 1. Pull latest changes
git pull origin master

# 2. Backend updates
cd autogpt_platform/backend
poetry install
poetry run prisma migrate deploy

# 3. Frontend updates
cd ../frontend
pnpm install
pnpm build

# 4. Restart services
docker-compose restart
```

## 📈 Monitoring

### Logs
```bash
# Backend
docker-compose logs -f backend

# Frontend
docker-compose logs -f frontend

# All services
docker-compose logs -f
```

### Metrics
- Response times
- Error rates
- Database connections
- Memory usage

## 🆘 Rollback

```bash
# 1. Stop services
docker-compose down

# 2. Checkout previous version
git checkout <previous-commit>

# 3. Rebuild and restart
docker-compose up -d --build
```

## 🔐 Security Best Practices

1. **SSL/TLS**: Use HTTPS only
2. **Secrets**: Never commit to repository
3. **Firewall**: Restrict database/Redis access
4. **Updates**: Regular dependency updates
5. **Backups**: Daily database backups
6. **Monitoring**: Set up alerts

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/SADOCKDOG/SADOCKDOG/issues)
- **Security**: Report privately

---

**Last Updated**: November 2025
