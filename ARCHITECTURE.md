# 🏗️ SADOCKDOG Platform Architecture

## 📐 System Overview

```
┌─────────────────────────────────────────────────────────┐
│                    SADOCKDOG Platform                    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐         ┌──────────────┐             │
│  │   Frontend   │ ◄─────► │   Backend    │             │
│  │  Next.js 15  │  REST   │   FastAPI    │             │
│  │              │  WebSocket              │             │
│  └──────────────┘         └──────┬───────┘             │
│                                   │                      │
│                          ┌────────┴────────┐            │
│                          │                 │            │
│                   ┌──────▼──────┐   ┌─────▼─────┐     │
│                   │ PostgreSQL  │   │   Redis   │     │
│                   │   (Prisma)  │   │  (Cache)  │     │
│                   └─────────────┘   └───────────┘     │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## 🎯 Tech Stack

### Frontend
**Framework**: Next.js 15.4.7
- **Routing**: App Router
- **Language**: TypeScript 5.9.2 (strict mode)
- **Styling**: TailwindCSS
- **State Management**: React Query
- **API Client**: Orval 7.11.2 (auto-generated)
- **Package Manager**: pnpm 8.15.9

**Key Features**:
- Server-Side Rendering (SSR)
- API Routes
- Real-time WebSocket support
- Responsive UI components

### Backend
**Framework**: FastAPI
- **Language**: Python 3.13
- **ORM**: Prisma 0.15.0
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **Package Manager**: Poetry
- **Validation**: Pydantic

**Key Features**:
- REST API endpoints
- WebSocket connections
- Background task execution
- Agent orchestration
- Graph-based workflows

### Database Layer
**PostgreSQL 15** (via Prisma ORM)
- User management
- Agent configurations
- Execution graphs
- Execution history
- Notifications

**Redis 7**
- Session caching
- Rate limiting
- Real-time data

## 📁 Project Structure

```
SADOCKDOG/
├── autogpt_libs/           # Shared libraries
│   └── autogpt_libs/
│       ├── api_key/        # API key management
│       ├── auth/           # Authentication
│       ├── logging/        # Logging utilities
│       ├── rate_limit/     # Rate limiting
│       └── supabase_integration_credentials_store/
│
├── backend/                # Backend service
│   ├── backend/
│   │   ├── blocks/         # Execution blocks
│   │   ├── data/           # Data models
│   │   ├── executor/       # Execution engine
│   │   ├── integrations/   # Third-party integrations
│   │   ├── notifications/  # Notification system
│   │   ├── sdk/            # SDK utilities
│   │   ├── server/         # Server setup
│   │   ├── usecases/       # Business logic
│   │   └── util/           # Utilities
│   ├── migrations/         # Prisma migrations
│   └── schema.prisma       # Database schema
│
├── frontend/               # Frontend application
│   └── src/
│       ├── app/            # Next.js App Router
│       ├── components/     # React components
│       ├── lib/            # Utilities
│       └── types/          # TypeScript types
│
├── .github/
│   └── workflows/          # CI/CD pipelines
│       ├── ci-backend.yml
│       ├── ci-frontend.yml
│       ├── codeql-analysis.yml
│       └── archive/        # Old workflows
│
└── graph_templates/        # Pre-built agent graphs
```

## 🔄 Data Flow

### 1. User Request Flow
```
User → Frontend → API Client (Orval) → Backend REST API
                                         ↓
                                    Validation (Pydantic)
                                         ↓
                                    Business Logic
                                         ↓
                                    Database (Prisma)
                                         ↓
                                    Response → Frontend
```

### 2. Agent Execution Flow
```
User creates graph → Backend receives → Executor processes
                                         ↓
                                    Block execution
                                         ↓
                                    State management (Redis)
                                         ↓
                                    Result storage (PostgreSQL)
                                         ↓
                                    WebSocket notification → Frontend
```

## 🔌 API Architecture

### REST Endpoints
- `GET /api/v1/agents` - List agents
- `POST /api/v1/agents` - Create agent
- `GET /api/v1/graphs/{id}` - Get execution graph
- `POST /api/v1/execute` - Execute graph
- `GET /api/v1/health` - Health check

### WebSocket
- `/ws` - Real-time execution updates
- Event-driven notifications
- Live agent status

## 🗄️ Database Schema

### Core Tables
- `users` - User accounts
- `agents` - Agent configurations
- `graphs` - Execution graphs
- `executions` - Execution history
- `blocks` - Execution blocks
- `notifications` - User notifications

### Relationships
```
users ←─┬─→ agents
        └─→ graphs ──→ executions ──→ blocks
```

## 🔐 Security Architecture

### Authentication
- JWT tokens
- Session management via Redis
- Secure password hashing

### Authorization
- Role-based access control (RBAC)
- Resource ownership validation
- API rate limiting

### Security Layers
1. **Input Validation**: Pydantic models
2. **SQL Injection Protection**: Prisma ORM
3. **XSS Protection**: Next.js sanitization
4. **CORS**: Configured origins
5. **Secrets**: Environment variables only

## 🚀 CI/CD Pipeline

### GitHub Actions Workflows
1. **Backend CI** (~2-3 min)
   - Ruff linting
   - Black formatting
   - pytest tests
   
2. **Frontend CI** (~5-6 min)
   - ESLint + Prettier
   - TypeScript check
   - Next.js build
   - Orval API generation

3. **CodeQL Security** (~2-12 min)
   - Python analysis
   - JavaScript/TypeScript analysis

### Branch Strategy
```
feature/* → dev (testing) → master (production)
```

### Deployment
- **Automated**: Merge to master triggers deployment
- **Manual**: Tagged releases
- **Rollback**: Git revert + redeploy

## 📊 Performance Considerations

### Frontend
- **Code Splitting**: Automatic (Next.js)
- **Image Optimization**: next/image
- **Static Generation**: Pre-rendered pages
- **Caching**: Browser + CDN

### Backend
- **Database Pooling**: Prisma connection pool
- **Caching**: Redis for frequently accessed data
- **Async Processing**: FastAPI async endpoints
- **Rate Limiting**: Per-user quotas

## 🔧 Development Tools

### Linting & Formatting
- **Python**: Ruff + Black
- **TypeScript**: ESLint + Prettier

### Type Safety
- **Python**: Type hints + Pydantic
- **TypeScript**: Strict mode

### API Documentation
- **OpenAPI/Swagger**: Auto-generated from FastAPI
- **Orval**: TypeScript client generation

## 📈 Scalability

### Horizontal Scaling
- Stateless backend services
- Redis for shared state
- Database read replicas

### Vertical Scaling
- PostgreSQL connection pooling
- Redis memory optimization
- Background task queues

## 🆘 Monitoring & Debugging

### Logs
- Structured logging
- Log levels: DEBUG, INFO, WARNING, ERROR
- Centralized log aggregation

### Metrics
- Response times
- Error rates
- Database query performance
- Cache hit rates

### Debugging
- VS Code launch configurations
- pdb (Python debugger)
- React DevTools
- Network inspection

---

**Architecture Version**: 2.0  
**Last Updated**: November 2025
