# 🏗️ Arquitectura de AutoGPT Platform

Documentación completa de la arquitectura y componentes del sistema.

---

## 📋 Índice

1. [Visión General](#visión-general)
2. [Arquitectura de Servicios](#arquitectura-de-servicios)
3. [Flujo de Datos](#flujo-de-datos)
4. [Componentes Principales](#componentes-principales)
5. [Base de Datos](#base-de-datos)
6. [Seguridad](#seguridad)
7. [Escalabilidad](#escalabilidad)

---

## Visión General

AutoGPT Platform es una arquitectura de microservicios diseñada para ejecutar agentes de IA autónomos y continuos.

### Stack Tecnológico

```
Frontend:     Next.js 15 + React + TypeScript + Tailwind CSS
Backend:      Python 3.11 + FastAPI + Prisma ORM
Database:     PostgreSQL 15 + pgvector
Auth:         Supabase Auth
Message Queue: RabbitMQ 3.x
Cache:        Redis 7.x
Security:     ClamAV
```

### Diagrama de Alto Nivel

```
┌─────────────────────────────────────────────────────────────┐
│                        USUARIOS                              │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   FRONTEND (Next.js)                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │   Home   │  │  Builder │  │   Chat   │  │ Monitor  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP/WS
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  API GATEWAY (Kong)                          │
│                    Port 8000/8443                            │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│ REST API │  │WebSocket │  │  Supabase│
│   8006   │  │   8001   │  │   Auth   │
└────┬─────┘  └────┬─────┘  └──────────┘
     │             │
     └──────┬──────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────┐
│                    MESSAGE QUEUE                             │
│                    RabbitMQ (5672)                           │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┬────────────┐
        ▼            ▼            ▼            ▼
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│ Executor │  │Scheduler │  │DatabaseMgr│ │Notifier │
│   8002   │  │   8003   │  │   8005   │  │   8007  │
└────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘
     │             │              │             │
     └─────────────┴──────────────┴─────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│               POSTGRESQL + REDIS                             │
│          Database (5432) + Cache (6379)                      │
└─────────────────────────────────────────────────────────────┘
```

---

## Arquitectura de Servicios

### 1. Frontend Service (Port 3000)

**Tecnología:** Next.js 15, React, TypeScript

**Responsabilidades:**
- UI/UX para usuarios
- Editor visual de agentes (Builder)
- Chat interface para interacción con agentes
- Dashboard de monitorización
- Gestión de perfil y API Keys

**Rutas Principales:**
```
/                    - Home page
/build               - Visual agent builder
/sadockdog           - Chat con agentes
/monitoring          - Monitor de ejecuciones
/profile             - Perfil de usuario
/library             - Biblioteca de agentes
/marketplace         - Marketplace de bloques
```

**Características:**
- Server-Side Rendering (SSR)
- Real-time updates vía WebSocket
- Optimistic UI updates
- Error boundaries globales
- Sentry integration para monitoreo

### 2. REST API Server (Port 8006)

**Tecnología:** FastAPI, Python 3.11, Prisma ORM

**Responsabilidades:**
- CRUD de agentes y bloques
- Autenticación y autorización
- Gestión de credenciales
- Ejecución de agentes
- API pública documentada

**Endpoints Principales:**
```
GET  /api/v1/health           - Health check
POST /api/v1/graphs           - Crear agente
GET  /api/v1/graphs/:id       - Obtener agente
PUT  /api/v1/graphs/:id       - Actualizar agente
POST /api/v1/graphs/:id/execute - Ejecutar agente
GET  /api/v1/blocks           - Listar bloques
POST /api/v1/credentials      - Crear credenciales
GET  /api/v1/executions       - Listar ejecuciones
```

**Características:**
- OpenAPI/Swagger documentation
- JWT authentication
- Rate limiting
- Request validation con Pydantic
- Cache middleware
- CORS configuration

### 3. WebSocket Server (Port 8001)

**Tecnología:** FastAPI WebSocket, Python

**Responsabilidades:**
- Conexiones persistentes con frontend
- Updates en tiempo real de ejecuciones
- Notificaciones push
- Chat messages streaming

**Eventos:**
```
EXECUTION_STARTED     - Nueva ejecución iniciada
EXECUTION_UPDATED     - Progreso de ejecución
EXECUTION_COMPLETED   - Ejecución completada
EXECUTION_FAILED      - Ejecución falló
NODE_EXECUTED         - Nodo individual ejecutado
```

### 4. Executor (Port 8002)

**Tecnología:** Python 3.11, Async workers

**Responsabilidades:**
- Ejecución de grafos de agentes
- Procesamiento de nodos
- Gestión de estado de ejecución
- Manejo de errores y reintentos
- Timeout management

**Flujo de Ejecución:**
```
1. Recibe mensaje de RabbitMQ
2. Carga definición del agente
3. Resuelve dependencias entre nodos
4. Ejecuta nodos en orden topológico
5. Almacena resultados intermedios
6. Publica updates vía WebSocket
7. Guarda resultado final en BD
8. Envía ACK a RabbitMQ
```

### 5. Scheduler Server (Port 8003)

**Tecnología:** Python 3.11, APScheduler

**Responsabilidades:**
- Programación de ejecuciones recurrentes
- Cron-like scheduling
- Ejecuciones diferidas
- Gestión de timezones
- Persistencia de schedules

**Tipos de Schedule:**
```
ONCE         - Ejecutar una vez en tiempo futuro
INTERVAL     - Ejecutar cada X minutos/horas
CRON         - Ejecutar según expresión cron
DAILY        - Ejecutar diariamente a hora específica
WEEKLY       - Ejecutar semanalmente
```

### 6. Database Manager (Port 8005)

**Tecnología:** Python 3.11, Prisma

**Responsabilidades:**
- Gestión de migraciones
- Optimización de queries
- Backup y restore
- Health checks de BD
- Connection pooling

**Operaciones:**
```
/migrate              - Ejecutar migraciones
/backup               - Crear backup
/restore              - Restaurar backup
/optimize             - Optimizar tablas
/health               - Estado de conexiones
```

### 7. Notification Server (Port 8007)

**Tecnología:** Python 3.11

**Responsabilidades:**
- Envío de notificaciones
- Email delivery
- Webhook calls
- Slack/Discord integration
- SMS (futuro)

**Canales:**
```
EMAIL        - Notificaciones por email
WEBHOOK      - HTTP POST a URL custom
SLACK        - Mensajes a Slack
DISCORD      - Mensajes a Discord
IN_APP       - Notificaciones en UI
```

### 8. PostgreSQL Database (Port 5432)

**Tecnología:** PostgreSQL 15 + pgvector

**Esquema Principal:**
```sql
-- Usuarios y autenticación
users (id, email, created_at, ...)

-- Agentes
AgentGraph (id, user_id, name, description, graph_data, ...)
AgentNode (id, graph_id, block_id, input_data, ...)
AgentNodeLink (id, graph_id, source_id, sink_id, ...)

-- Ejecuciones
AgentGraphExecution (id, graph_id, status, start_time, end_time, ...)
AgentNodeExecution (id, execution_id, node_id, status, output_data, ...)

-- Credenciales
UserCredential (id, user_id, type, encrypted_data, ...)

-- Bloques
AgentBlock (id, name, description, input_schema, output_schema, ...)

-- Schedules
AgentGraphSchedule (id, graph_id, schedule_type, cron_expression, ...)
```

**Extensiones:**
```
pgvector     - Vector similarity search para embeddings
pg_trgm      - Búsqueda de texto fuzzy
uuid-ossp    - Generación de UUIDs
```

### 9. Redis Cache (Port 6379)

**Uso:**
```
Session Storage:      user:session:{token}
Rate Limiting:        ratelimit:{user_id}:{endpoint}
Execution State:      execution:{id}:state
WebSocket Presence:   ws:presence:{user_id}
Block Results Cache:  block:{id}:result
```

### 10. RabbitMQ (Ports 5672, 15672)

**Exchanges:**
```
agent.execution     - Topic exchange para ejecuciones
agent.events        - Fanout exchange para eventos
agent.schedules     - Direct exchange para schedules
```

**Queues:**
```
execution.high      - Prioridad alta (TTL: 1h)
execution.normal    - Prioridad normal (TTL: 24h)
execution.low       - Prioridad baja (TTL: 7d)
execution.dlq       - Dead Letter Queue
```

### 11. Supabase Auth (Port 8000)

**Funcionalidades:**
- Email/Password authentication
- OAuth2 (GitHub, Google)
- JWT token generation
- Password reset
- Email verification

---

## Flujo de Datos

### Flujo de Creación de Agente

```
1. Usuario diseña agente en Builder UI
2. Frontend envía POST /api/v1/graphs
3. Backend valida esquema
4. Backend guarda en PostgreSQL
5. Backend retorna agente creado
6. Frontend actualiza UI
```

### Flujo de Ejecución de Agente

```
1. Usuario trigger ejecución desde Chat
2. Frontend envía POST /api/v1/graphs/:id/execute
3. Backend crea registro en AgentGraphExecution
4. Backend publica mensaje a RabbitMQ exchange
5. Executor consume mensaje de queue
6. Executor ejecuta nodos del grafo
7. Executor publica updates vía WebSocket
8. Frontend recibe updates y actualiza UI
9. Executor guarda resultado final
10. Executor envía ACK a RabbitMQ
```

### Flujo de Schedule

```
1. Usuario configura schedule en UI
2. Frontend envía POST /api/v1/schedules
3. Backend guarda en AgentGraphSchedule
4. Scheduler lee schedules de BD
5. Scheduler agenda ejecuciones futuras
6. Al llegar tiempo, publica a RabbitMQ
7. Continúa con flujo de ejecución normal
```

---

## Componentes Principales

### Agent Block System

Los agentes se construyen conectando **bloques** (blocks):

**Categorías de Bloques:**
```
Input/Output:        Store Value, Output, User Input
AI/LLM:              AI Text Generator, AI Image Generator
GitHub:              Create Repo, Create File, List Branches
Text Processing:     Fill Template, Regex, JSON Parser
Logic:               Conditional, Loop, Switch
Database:            Query, Insert, Update
Web:                 HTTP Request, Web Scraper
Utilities:           Delay, Logger, Math
```

**Estructura de un Bloque:**
```python
class Block:
    id: UUID                    # ID único del bloque
    name: str                   # Nombre display
    description: str            # Descripción
    categories: list[Category]  # Categorías
    input_schema: dict         # Schema de inputs (JSON Schema)
    output_schema: dict        # Schema de outputs (JSON Schema)
    
    async def run(
        self,
        input_data: dict,
        credentials: dict
    ) -> dict:
        # Lógica de ejecución
        pass
```

### Graph Execution Engine

**Algoritmo:**
```
1. Parse graph definition
2. Build dependency graph
3. Topological sort de nodos
4. Para cada nodo en orden:
   a. Resolver inputs desde outputs previos
   b. Ejecutar bloque con inputs
   c. Guardar outputs
   d. Publicar update vía WebSocket
   e. Manejar errores con reintentos
5. Retornar resultado final
```

---

## Base de Datos

### Prisma Schema

```prisma
model AgentGraph {
  id          String   @id @default(uuid())
  userId      String
  name        String
  description String?
  version     Int      @default(1)
  isActive    Boolean  @default(true)
  isTemplate  Boolean  @default(false)
  graphData   Json
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
  
  nodes       AgentNode[]
  links       AgentNodeLink[]
  executions  AgentGraphExecution[]
  schedules   AgentGraphSchedule[]
  
  @@index([userId])
}

model AgentGraphExecution {
  id            String   @id @default(uuid())
  graphId       String
  graphVersion  Int
  status        ExecutionStatus
  inputData     Json?
  outputData    Json?
  startTime     DateTime @default(now())
  endTime       DateTime?
  errorMessage  String?
  
  graph         AgentGraph @relation(fields: [graphId], references: [id])
  nodeExecutions AgentNodeExecution[]
  
  @@index([graphId, status])
  @@index([startTime])
}

enum ExecutionStatus {
  QUEUED
  RUNNING
  COMPLETED
  FAILED
  CANCELLED
}
```

---

## Seguridad

### Autenticación

```
1. Usuario se autentica vía Supabase
2. Supabase genera JWT token
3. Frontend almacena token en cookie httpOnly
4. Cada request incluye token en Authorization header
5. Backend verifica token con Supabase
6. Backend valida permisos de usuario
```

### Autorización

```
- Usuarios solo acceden a sus propios agentes
- API Keys tienen scopes limitados
- Credenciales OAuth son encriptadas
- Rate limiting por usuario
- CORS restrictivo en producción
```

### Cache Control

Middleware de seguridad previene caching de datos sensibles:

```python
Cache-Control: no-store, no-cache, must-revalidate, private
Pragma: no-cache
Expires: 0
```

---

## Escalabilidad

### Horizontal Scaling

```
Frontend:     Multiple replicas detrás de load balancer
Backend:      Stateless, escala horizontalmente
Executor:     Workers pool, auto-scaling basado en queue depth
WebSocket:    Sticky sessions con Redis pub/sub
PostgreSQL:   Read replicas para queries
Redis:        Redis Cluster para high availability
RabbitMQ:     Cluster mode con mirrored queues
```

### Performance Optimizations

```
- Connection pooling en PostgreSQL
- Redis caching de queries frecuentes
- CDN para static assets del frontend
- Gzip compression
- Database indexes optimizados
- Lazy loading de componentes frontend
- Query batching
- Background jobs para tareas pesadas
```

---

## Monitorización

### Métricas

```
Application:
- Request rate y latency
- Error rate por endpoint
- Execution success/failure rate
- Queue depth y processing time

Infrastructure:
- CPU y memoria por servicio
- Network I/O
- Disk usage
- Database connection pool
```

### Logging

```
Formato: JSON structured logs
Niveles: DEBUG, INFO, WARNING, ERROR, CRITICAL
Storage: Archivos locales + agregación futura (ELK stack)
Retention: 30 días
```

### Alerting (futuro)

```
- Execution failures > 10% en 5 min
- API error rate > 5% en 5 min
- Queue depth > 1000 mensajes
- Memory usage > 90%
- Disk usage > 85%
```

---

*Última actualización: 2025-01-06*
