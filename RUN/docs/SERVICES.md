# 🔧 Detalle de Servicios

Documentación completa de cada servicio en AutoGPT Platform.

---

## 📋 Servicios Disponibles

| Servicio | Puerto | Tecnología | Estado Health | Descripción |
|----------|--------|------------|---------------|-------------|
| Frontend | 3000 | Next.js 15 | ✅ | UI principal |
| Backend | 8006 | FastAPI | ✅ | REST API |
| WebSocket | 8001 | FastAPI WS | ✅ | Real-time updates |
| Executor | 8002 | Python | ✅ | Ejecución de agentes |
| Scheduler | 8003 | Python | ✅ | Programación de tareas |
| Database Manager | 8005 | Python | ✅ | Gestión de BD |
| Notification | 8007 | Python | ✅ | Notificaciones |
| PostgreSQL | 5432 | PostgreSQL 15 | N/A | Base de datos |
| Redis | 6379 | Redis 7 | N/A | Cache |
| RabbitMQ | 5672 | RabbitMQ 3 | N/A | Message broker |
| RabbitMQ UI | 15672 | Web UI | N/A | Management UI |
| Supabase | 8000 | Kong Gateway | N/A | Auth + API Gateway |
| ClamAV | 3310 | ClamAV | N/A | Antivirus |

---

## 1. Frontend Service

### Información General

```yaml
Nombre: frontend
Puerto: 3000
Tecnología: Next.js 15 + React + TypeScript
Dockerfile: autogpt_platform/frontend/Dockerfile
```

### Responsabilidades

- **UI/UX**: Interfaz de usuario completa
- **Builder**: Editor visual de agentes con drag & drop
- **Chat**: Interfaz de chat para interactuar con agentes
- **Monitoring**: Dashboard para ver ejecuciones
- **Profile**: Gestión de perfil, API Keys, credenciales OAuth

### Rutas Principales

```
/                     - Landing page
/build                - Visual agent builder
/sadockdog            - Chat con agentes SADOCKDOG
/monitoring           - Monitor de ejecuciones
/profile              - Perfil de usuario y settings
/library              - Biblioteca de agentes
/library/:id          - Detalle de agente
/marketplace          - Marketplace de bloques
```

### Variables de Entorno

```bash
NEXT_PUBLIC_API_URL=http://localhost:8006      # URL del backend
NEXT_PUBLIC_WS_URL=ws://localhost:8001         # WebSocket URL
NEXT_PUBLIC_SUPABASE_URL=http://localhost:8000 # Supabase URL
NEXT_PUBLIC_SUPABASE_ANON_KEY=...              # Supabase public key
```

### Health Check

```bash
# Test frontend
curl http://localhost:3000

# Ver en navegador
open http://localhost:3000
```

### Logs

```bash
# Ver logs
docker compose logs frontend

# Seguir logs
docker compose logs -f frontend

# Últimas 100 líneas
docker compose logs --tail=100 frontend
```

### Comandos Útiles

```bash
# Entrar al contenedor
docker compose exec frontend sh

# Ver paquetes instalados
docker compose exec frontend pnpm list

# Rebuild
docker compose build frontend
docker compose up -d frontend

# Hot reload (desarrollo local)
cd autogpt_platform/frontend
pnpm dev
```

---

## 2. Backend (REST API) Service

### Información General

```yaml
Nombre: rest_server
Puerto: 8006
Tecnología: FastAPI + Python 3.11 + Prisma ORM
Dockerfile: autogpt_platform/backend/Dockerfile
```

### Responsabilidades

- **API REST**: CRUD de agentes, bloques, credenciales
- **Autenticación**: Validación de JWT tokens
- **Ejecución**: Trigger de ejecuciones de agentes
- **Gestión**: Admin de usuarios, permisos, API Keys
- **Documentación**: OpenAPI/Swagger docs auto-generados

### Endpoints Principales

```
GET  /health                           - Health check
GET  /api/v1/graphs                    - Listar agentes
POST /api/v1/graphs                    - Crear agente
GET  /api/v1/graphs/:id                - Obtener agente
PUT  /api/v1/graphs/:id                - Actualizar agente
DELETE /api/v1/graphs/:id              - Eliminar agente
POST /api/v1/graphs/:id/execute        - Ejecutar agente
GET  /api/v1/blocks                    - Listar bloques
POST /api/v1/credentials               - Crear credenciales
GET  /api/v1/credentials               - Listar credenciales
GET  /api/v1/executions                - Listar ejecuciones
GET  /api/v1/executions/:id            - Detalle de ejecución
```

### Variables de Entorno

```bash
DATABASE_URL=postgresql://postgres:password@db:5432/autogpt
REDIS_URL=redis://redis:6379
RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672
SUPABASE_URL=http://auth:8000
SUPABASE_SERVICE_KEY=...
JWT_SECRET=...
ENCRYPTION_KEY=...
```

### Health Check

```bash
# Test backend
curl http://localhost:8006/health

# Ver API docs
open http://localhost:8006/docs

# Test endpoint específico
curl http://localhost:8006/api/v1/blocks
```

### Logs

```bash
# Ver logs con nivel DEBUG
docker compose logs rest_server | grep DEBUG

# Ver errores
docker compose logs rest_server | grep ERROR

# Ver requests
docker compose logs rest_server | grep "GET\|POST\|PUT\|DELETE"
```

### Comandos Útiles

```bash
# Entrar al contenedor
docker compose exec rest_server bash

# Ejecutar migraciones
docker compose exec rest_server poetry run prisma migrate deploy

# Generar cliente Prisma
docker compose exec rest_server poetry run prisma generate

# Ejecutar tests
docker compose exec rest_server poetry run pytest

# Formatear código
docker compose exec rest_server poetry run format
```

---

## 3. WebSocket Service

### Información General

```yaml
Nombre: websocket_server
Puerto: 8001
Tecnología: FastAPI WebSocket + Python
Dockerfile: autogpt_platform/backend/Dockerfile
```

### Responsabilidades

- **Real-time Updates**: Streaming de ejecuciones en progreso
- **Notificaciones**: Push notifications a frontend
- **Chat Messages**: Streaming de respuestas de agentes
- **Presence**: Tracking de usuarios conectados

### Eventos WebSocket

```javascript
// Eventos que el servidor emite:
EXECUTION_STARTED     // Nueva ejecución iniciada
EXECUTION_UPDATED     // Progreso de ejecución
EXECUTION_COMPLETED   // Ejecución completada
EXECUTION_FAILED      // Ejecución falló
NODE_EXECUTED         // Nodo individual ejecutado
NOTIFICATION          // Notificación general
CHAT_MESSAGE          // Mensaje de chat
```

### Conexión desde Frontend

```typescript
// Ejemplo de conexión
const ws = new WebSocket('ws://localhost:8001/ws');

ws.onopen = () => {
  console.log('Connected to WebSocket');
  
  // Autenticar
  ws.send(JSON.stringify({
    type: 'authenticate',
    token: 'jwt_token_here'
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};

ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};

ws.onclose = () => {
  console.log('Disconnected from WebSocket');
};
```

### Health Check

```bash
# Test WebSocket server (HTTP endpoint)
curl http://localhost:8001/health

# Test WebSocket connection (desde navegador DevTools)
const ws = new WebSocket('ws://localhost:8001/ws');
ws.onopen = () => console.log('Connected!');
```

---

## 4. Executor Service

### Información General

```yaml
Nombre: executor
Puerto: 8002
Tecnología: Python 3.11 + Async Workers
Dockerfile: autogpt_platform/backend/Dockerfile
```

### Responsabilidades

- **Ejecución de Grafos**: Procesa grafos de agentes
- **Resolución de Dependencias**: Ordena nodos topológicamente
- **Gestión de Estado**: Mantiene estado de ejecución
- **Error Handling**: Reintentos y manejo de fallos
- **Timeout Management**: Cancela ejecuciones largas

### Flujo de Trabajo

```
1. Consume mensaje de RabbitMQ queue
2. Carga definición del agente desde BD
3. Valida esquema del grafo
4. Construye grafo de dependencias
5. Ejecuta nodos en orden topológico:
   - Resuelve inputs desde outputs previos
   - Ejecuta bloque con credenciales
   - Guarda outputs
   - Publica update vía WebSocket
6. Guarda resultado final en BD
7. Envía notificaciones si configuradas
8. Envía ACK a RabbitMQ
```

### Variables de Entorno

```bash
RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672
DATABASE_URL=postgresql://postgres:password@db:5432/autogpt
REDIS_URL=redis://redis:6379
EXECUTION_TIMEOUT=3600        # 1 hora max por ejecución
MAX_RETRIES=3                 # Reintentos por nodo
WEBSOCKET_URL=http://websocket_server:8001
```

### Monitoring

```bash
# Ver ejecuciones activas
docker compose logs executor | grep "Executing graph"

# Ver errores
docker compose logs executor | grep "ERROR\|Exception"

# Ver performance
docker compose logs executor | grep "Execution time"

# Ver queue depth
docker compose exec rabbitmq rabbitmqctl list_queues
```

---

## 5. Scheduler Service

### Información General

```yaml
Nombre: scheduler_server
Puerto: 8003
Tecnología: Python 3.11 + APScheduler
Dockerfile: autogpt_platform/backend/Dockerfile
```

### Responsabilidades

- **Scheduling**: Programación de ejecuciones recurrentes
- **Cron Jobs**: Expresiones cron para schedules complejos
- **Timezones**: Manejo de diferentes zonas horarias
- **Persistencia**: Guarda schedules en BD
- **Recovery**: Recupera schedules después de restart

### Tipos de Schedule

```python
# Una vez en el futuro
{
  "type": "ONCE",
  "run_at": "2024-12-25T00:00:00Z"
}

# Cada X minutos
{
  "type": "INTERVAL",
  "interval_minutes": 30
}

# Expresión cron
{
  "type": "CRON",
  "cron_expression": "0 9 * * 1-5"  # 9am weekdays
}

# Diariamente
{
  "type": "DAILY",
  "time": "09:00",
  "timezone": "America/New_York"
}

# Semanalmente
{
  "type": "WEEKLY",
  "day_of_week": "monday",
  "time": "09:00"
}
```

### Comandos Útiles

```bash
# Ver schedules activos
docker compose logs scheduler_server | grep "Scheduled"

# Ver próximas ejecuciones
docker compose exec scheduler_server poetry run python -c "
from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()
print(scheduler.get_jobs())
"
```

---

## 6. Database Manager Service

### Información General

```yaml
Nombre: database_manager
Puerto: 8005
Tecnología: Python 3.11 + Prisma
Dockerfile: autogpt_platform/backend/Dockerfile
```

### Responsabilidades

- **Migraciones**: Aplica migraciones de schema
- **Backups**: Crea backups de base de datos
- **Restore**: Restaura desde backups
- **Optimization**: Optimiza queries y tablas
- **Health Checks**: Monitorea conexiones

### Endpoints

```
GET  /health              - Estado de conexión a BD
POST /migrate             - Ejecutar migraciones
POST /backup              - Crear backup
POST /restore             - Restaurar backup
POST /optimize            - Optimizar tablas
GET  /stats               - Estadísticas de BD
```

### Comandos de Backup

```bash
# Crear backup manual
docker compose exec database_manager curl -X POST http://localhost:8005/backup

# Restaurar backup
docker compose exec database_manager curl -X POST http://localhost:8005/restore \
  -H "Content-Type: application/json" \
  -d '{"backup_file": "backup_20240106.sql"}'

# Listar backups
docker compose exec db ls -lh /backups
```

---

## 7. Notification Service

### Información General

```yaml
Nombre: notification_server
Puerto: 8007
Tecnología: Python 3.11
Dockerfile: autogpt_platform/backend/Dockerfile
```

### Responsabilidades

- **Email**: Envío de emails transaccionales
- **Webhooks**: HTTP POST a URLs configuradas
- **Slack**: Mensajes a canales de Slack
- **Discord**: Mensajes a servidores Discord
- **In-App**: Notificaciones en la UI

### Canales Disponibles

```python
# Email
{
  "type": "EMAIL",
  "to": "user@example.com",
  "subject": "Agent Execution Completed",
  "body": "Your agent finished successfully"
}

# Webhook
{
  "type": "WEBHOOK",
  "url": "https://example.com/webhook",
  "method": "POST",
  "payload": {"status": "completed"}
}

# Slack
{
  "type": "SLACK",
  "webhook_url": "https://hooks.slack.com/...",
  "message": "Agent completed!"
}

# Discord
{
  "type": "DISCORD",
  "webhook_url": "https://discord.com/api/webhooks/...",
  "message": "Agent completed!"
}
```

---

## 8. PostgreSQL Database

### Información General

```yaml
Nombre: db
Puerto: 5432
Tecnología: PostgreSQL 15 + pgvector
Image: postgres:15-alpine
```

### Extensiones Instaladas

```sql
-- Vectores para embeddings
CREATE EXTENSION IF NOT EXISTS vector;

-- Búsqueda fuzzy
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- UUIDs
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

### Tablas Principales

```sql
-- Usuarios
users

-- Agentes
AgentGraph
AgentNode
AgentNodeLink

-- Ejecuciones
AgentGraphExecution
AgentNodeExecution

-- Credenciales
UserCredential

-- Bloques
AgentBlock

-- Schedules
AgentGraphSchedule

-- API Keys
APIKey
```

### Comandos Útiles

```bash
# Conectar a PostgreSQL
docker compose exec db psql -U postgres -d autogpt

# Ver tablas
docker compose exec db psql -U postgres -d autogpt -c "\dt"

# Ver tamaño de BD
docker compose exec db psql -U postgres -c "SELECT pg_size_pretty(pg_database_size('autogpt'));"

# Backup completo
docker compose exec db pg_dump -U postgres autogpt > backup.sql

# Restore
docker compose exec -T db psql -U postgres autogpt < backup.sql

# Ver conexiones activas
docker compose exec db psql -U postgres -c "SELECT count(*) FROM pg_stat_activity;"
```

---

## 9. Redis Cache

### Información General

```yaml
Nombre: redis
Puerto: 6379
Tecnología: Redis 7
Image: redis:7-alpine
```

### Uso en la Plataforma

```
Session Storage:       user:session:{token}
Rate Limiting:         ratelimit:{user_id}:{endpoint}
Execution State:       execution:{id}:state
WebSocket Presence:    ws:presence:{user_id}
Block Results Cache:   block:{id}:result
API Response Cache:    api:cache:{endpoint}:{params}
```

### Comandos Útiles

```bash
# Conectar a Redis CLI
docker compose exec redis redis-cli

# Ver todas las keys
docker compose exec redis redis-cli KEYS "*"

# Ver valor de key
docker compose exec redis redis-cli GET "key_name"

# Eliminar key
docker compose exec redis redis-cli DEL "key_name"

# Limpiar toda la BD (CUIDADO!)
docker compose exec redis redis-cli FLUSHALL

# Ver info
docker compose exec redis redis-cli INFO

# Ver memoria usada
docker compose exec redis redis-cli INFO memory
```

---

## 10. RabbitMQ Message Broker

### Información General

```yaml
Nombre: rabbitmq
Puerto AMQP: 5672
Puerto UI: 15672
Tecnología: RabbitMQ 3
Credenciales: guest / guest
```

### Exchanges

```
agent.execution     - Topic exchange para ejecuciones
agent.events        - Fanout exchange para eventos
agent.schedules     - Direct exchange para schedules
```

### Queues

```
execution.high      - Prioridad alta (TTL: 1h)
execution.normal    - Prioridad normal (TTL: 24h)
execution.low       - Prioridad baja (TTL: 7d)
execution.dlq       - Dead Letter Queue
```

### Management UI

```bash
# Abrir en navegador
open http://localhost:15672

# Credenciales por defecto
Username: guest
Password: guest
```

### Comandos Útiles

```bash
# Ver queues
docker compose exec rabbitmq rabbitmqctl list_queues

# Ver exchanges
docker compose exec rabbitmq rabbitmqctl list_exchanges

# Ver bindings
docker compose exec rabbitmq rabbitmqctl list_bindings

# Ver consumers
docker compose exec rabbitmq rabbitmqctl list_consumers

# Purge queue
docker compose exec rabbitmq rabbitmqctl purge_queue execution.normal

# Ver status
docker compose exec rabbitmq rabbitmqctl status
```

---

## 11. Supabase Auth

### Información General

```yaml
Nombre: auth
Puerto: 8000 (Kong Gateway)
Tecnología: Supabase + Kong
```

### Endpoints

```
POST /auth/v1/signup          - Registro de usuario
POST /auth/v1/token           - Login (obtener JWT)
POST /auth/v1/logout          - Logout
POST /auth/v1/recover         - Password recovery
POST /auth/v1/verify          - Email verification
GET  /auth/v1/user            - Obtener usuario actual
```

### OAuth Providers

```
GitHub
Google (futuro)
Microsoft (futuro)
```

---

## Diagrama de Comunicación

```
┌──────────┐
│ Frontend │
│  :3000   │
└────┬─────┘
     │
     │ HTTP/WS
     ▼
┌──────────────┐
│   Supabase   │
│   Auth:8000  │
└──────┬───────┘
       │
       │ JWT Validation
       ▼
┌────────────────────┬──────────────────┐
│   Backend :8006    │ WebSocket :8001  │
└─────────┬──────────┴──────┬───────────┘
          │                  │
          │ Publish          │ Push
          ▼                  ▼
    ┌──────────┐       ┌──────────┐
    │ RabbitMQ │       │  Redis   │
    │  :5672   │       │  :6379   │
    └────┬─────┘       └──────────┘
         │
         │ Consume
         ▼
┌────────────────────┬──────────────┬─────────────┐
│  Executor :8002    │Scheduler:8003│Database:8005│
└─────────┬──────────┴──────┬───────┴──────┬──────┘
          │                  │              │
          └──────────────────┴──────────────┘
                     │
                     ▼
              ┌─────────────┐
              │ PostgreSQL  │
              │    :5432    │
              └─────────────┘
```

---

*Última actualización: 2025-01-06*
