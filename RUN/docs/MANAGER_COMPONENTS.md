# 🧩 COMPONENTES GESTIONADOS Y NO GESTIONADOS

**Versión:** 1.0  
**Fecha:** 2025-11-09  
**Documento:** Privado - Solo uso local

---

## 📊 Resumen Ejecutivo

El SADOCKDOG Manager gestiona **20 servicios Docker** y documenta **5 scripts Python standalone** adicionales que forman parte del ecosistema AutoGPT Platform.

### Componentes por Categoría:

| Categoría | Gestionados | No Gestionados | Total |
|-----------|-------------|----------------|-------|
| Servicios Docker | 20 | 0 | 20 |
| Scripts Python | 0 | 5 | 5 |
| Librerías Core | 0 | 1 (autogpt_libs) | 1 |
| **TOTAL** | **20** | **6** | **26** |

---

## ✅ SERVICIOS DOCKER GESTIONADOS (20)

### 1. Frontend (1 servicio)

#### 1.1 Frontend
- **Container:** `autogpt_platform-frontend-1`
- **Puerto:** 3000
- **Tecnología:** Next.js 15 + React + TypeScript
- **Función:** Interfaz de usuario principal
- **Gestión:** Completa via Manager

---

### 2. Backend Services (6 servicios)

#### 2.1 REST API Server
- **Container:** `autogpt_platform-rest_server-1`
- **Puerto:** 8006
- **Tecnología:** FastAPI + Python
- **Función:** API REST principal con Swagger
- **Gestión:** Completa via Manager

#### 2.2 WebSocket Server
- **Container:** `autogpt_platform-websocket_server-1`
- **Puerto:** 8001
- **Tecnología:** FastAPI WebSockets
- **Función:** Comunicación en tiempo real
- **Gestión:** Completa via Manager

#### 2.3 Executor
- **Container:** `autogpt_platform-executor-1`
- **Puerto:** 8002
- **Tecnología:** Python + Pyro
- **Función:** Motor de ejecución de agentes
- **Gestión:** Completa via Manager

#### 2.4 Scheduler Server
- **Container:** `autogpt_platform-scheduler_server-1`
- **Puerto:** 8003
- **Tecnología:** Python + APScheduler
- **Función:** Programación de tareas
- **Gestión:** Completa via Manager

#### 2.5 Database Manager
- **Container:** `autogpt_platform-database_manager-1`
- **Puerto:** 8005
- **Tecnología:** Python + Prisma ORM
- **Función:** Operaciones avanzadas de BD
- **Gestión:** Completa via Manager

#### 2.6 Notification Server
- **Container:** `autogpt_platform-notification_server-1`
- **Puerto:** 8007
- **Tecnología:** Python
- **Función:** Sistema de notificaciones
- **Gestión:** Completa via Manager

---

### 3. Bases de Datos (2 servicios)

#### 3.1 PostgreSQL (Supabase)
- **Container:** `supabase-db`
- **Puerto:** 5432
- **Tecnología:** PostgreSQL 15.8 (Supabase Edition)
- **Función:** Base de datos principal
- **Gestión:** Completa via Manager (backups, restore, health checks)

#### 3.2 Redis
- **Container:** `autogpt_platform-redis-1`
- **Puerto:** 6379
- **Tecnología:** Redis 7.4
- **Función:** Cache y session store
- **Gestión:** Completa via Manager

---

### 4. Message Broker (1 servicio)

#### 4.1 RabbitMQ
- **Container:** `rabbitmq`
- **Puerto:** 5672 (AMQP), 15672 (Management UI)
- **Tecnología:** RabbitMQ 3.13 + Management Plugin
- **Función:** Cola de mensajes asíncrona
- **Gestión:** Completa via Manager

---

### 5. Supabase Services (4 servicios)

#### 5.1 Kong Gateway
- **Container:** `supabase-kong`
- **Puerto:** 8000 (HTTP), 8443 (HTTPS)
- **Tecnología:** Kong 3.9.1
- **Función:** API Gateway para Supabase
- **Gestión:** Completa via Manager

#### 5.2 Supabase Auth
- **Container:** `supabase-auth`
- **Puerto:** 8000 (via Kong)
- **Tecnología:** GoTrue v2.170.0
- **Función:** Autenticación y autorización
- **Gestión:** Completa via Manager

#### 5.3 Supabase Studio (Profile Local)
- **Container:** `supabase-studio`
- **Puerto:** 54323
- **Tecnología:** Supabase Studio 20250224
- **Función:** UI de administración de Supabase
- **Gestión:** Parcial (solo con profile 'local')
- **Nota:** Requiere `docker compose --profile local up`

#### 5.4 Meta Service (Profile Local)
- **Container:** `supabase-meta`
- **Puerto:** 8080
- **Tecnología:** Supabase Meta API
- **Función:** Introspección de metadatos de PostgreSQL
- **Gestión:** Parcial (solo con profile 'local')
- **Nota:** Usado internamente por Supabase Studio

---

### 6. Security (1 servicio)

#### 6.1 ClamAV
- **Container:** `autogpt_platform-clamav-1`
- **Puerto:** 3310
- **Tecnología:** ClamAV Debian
- **Función:** Antivirus para archivos subidos
- **Gestión:** Completa via Manager

---

### 7. Migration (1 servicio)

#### 7.1 Migrate
- **Container:** `autogpt_platform-migrate-1`
- **Puerto:** N/A
- **Tecnología:** Python + Prisma
- **Función:** Migraciones de base de datos
- **Gestión:** Monitoreo de estado via Manager
- **Nota:** Se ejecuta automáticamente al inicio

---

## 📜 SCRIPTS PYTHON STANDALONE (5)

Estos scripts NO son gestionados directamente por el Manager, pero están documentados para referencia:

### 1. create_agent_auto.py
- **Ubicación:** `autogpt_platform/create_agent_auto.py`
- **Función:** Crear agentes automáticamente
- **Categoría:** Agent Creation
- **Uso:** Script independiente para automatización
- **Ejecución:** `python autogpt_platform/create_agent_auto.py`

### 2. create_agent_simple.py
- **Ubicación:** `autogpt_platform/create_agent_simple.py`
- **Función:** Crear agentes de forma simple
- **Categoría:** Agent Creation
- **Uso:** Script independiente para creación manual
- **Ejecución:** `python autogpt_platform/create_agent_simple.py`

### 3. create_android_agent.py
- **Ubicación:** `autogpt_platform/create_android_agent.py`
- **Función:** Crear agentes para plataforma Android
- **Categoría:** Agent Creation (Mobile)
- **Uso:** Creación de agentes móviles
- **Ejecución:** `python autogpt_platform/create_android_agent.py`

### 4. import_android_agent.py
- **Ubicación:** `autogpt_platform/import_android_agent.py`
- **Función:** Importar agentes desde Android
- **Categoría:** Agent Import
- **Uso:** Migración de agentes móviles
- **Ejecución:** `python autogpt_platform/import_android_agent.py`

### 5. fix_json.py
- **Ubicación:** `autogpt_platform/fix_json.py`
- **Función:** Reparar archivos JSON corruptos
- **Categoría:** Utilities
- **Uso:** Mantenimiento de configuraciones
- **Ejecución:** `python autogpt_platform/fix_json.py`

---

## 📚 AUTOGPT LIBS (1 componente)

### autogpt_libs
- **Ubicación:** `autogpt_platform/autogpt_libs/`
- **Tipo:** Librería Python (Poetry package)
- **Función:** Librerías compartidas del core de AutoGPT
- **Contenido:**
  - Utilidades comunes
  - Helpers de integración
  - Funciones compartidas entre servicios
- **Gestión:** No requiere gestión directa
- **Nota:** Componente de bajo nivel, instalado como dependencia

---

## 🔄 GESTIÓN POR EL MANAGER

### ✅ Funciones Completamente Gestionadas:

1. **Inicio/Parada de Servicios**
   - Todos los 20 servicios Docker
   - Inicio selectivo o completo
   - Perfiles Docker (default, local)

2. **Monitoreo**
   - Health checks de todos los servicios
   - Estado de contenedores
   - Uso de recursos (CPU, RAM, Disco)

3. **Logs**
   - Visualización de logs por servicio
   - Logs combinados
   - Filtrado y búsqueda

4. **Backups**
   - PostgreSQL (pg_dump)
   - Configuraciones (.env, docker-compose)
   - Volúmenes Docker
   - Histórico de backups

5. **Restore**
   - Restauración de backups
   - Validación de backups
   - Histórico de restores

6. **Accesos Web**
   - URLs directas a todos los servicios
   - Health checks automáticos
   - Gestión de credenciales

7. **Actualizaciones**
   - Análisis de actualizaciones disponibles
   - Aplicación de actualizaciones
   - Validación de compatibilidad

---

## ❌ Componentes NO Gestionados (Documentados)

### 1. Scripts Python Standalone
- **Razón:** Son herramientas independientes, no servicios
- **Acción:** Documentados en el Manager para referencia
- **Posibilidad futura:** Agregar opción de ejecución desde el Manager

### 2. autogpt_libs
- **Razón:** Es una librería, no un servicio ejecutable
- **Acción:** Documentado para información
- **Gestión:** Via Poetry en el proyecto principal

### 3. Servicios con Profile 'local'
- **Servicios:** Supabase Studio, Meta Service
- **Razón:** Requieren flag especial de Docker
- **Gestión:** Parcial (monitoreo sí, inicio automático no)
- **Acción:** Documentado cómo activarlos manualmente

---

## 🎯 RECOMENDACIONES

### Para el Manager:

1. **Mantener gestión completa de servicios Docker** ✅
2. **Documentar scripts standalone** ✅
3. **Agregar opción para ejecutar scripts** (futuro)
4. **Mejorar gestión de profiles** (futuro)

### Para Seguridad:

1. **NO incluir credenciales en el Manager** ✅
2. **Referenciar archivos .env** ✅
3. **Mantener Manager privado** ✅
4. **Documentar separadamente** ✅

### Para Desarrollo:

1. **Usar Manager para servicios** ✅
2. **Ejecutar scripts manualmente** (por ahora)
3. **Consultar documentación** ✅

---

## 📝 Notas de Versión

**v1.0 (2025-11-09)**
- Documentación completa de 20 servicios gestionados
- Documentación de 5 scripts standalone
- Documentación de autogpt_libs
- Mejoras de seguridad en credenciales
- Actualización de accesos web

---

**Documento Privado** - No compartir públicamente
