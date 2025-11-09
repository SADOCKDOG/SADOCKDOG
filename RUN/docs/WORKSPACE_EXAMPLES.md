# 🎯 Ejemplos Prácticos de @workspace

Este documento contiene ejemplos reales y prácticos de cómo usar @workspace en el proyecto SADOCKDOG.

---

## 📋 Tabla de Contenidos

1. [Ejemplos Básicos](#ejemplos-básicos)
2. [Debugging](#debugging)
3. [Desarrollo de Features](#desarrollo-de-features)
4. [Testing](#testing)
5. [Optimización](#optimización)
6. [Deployment](#deployment)

---

## 🟢 Ejemplos Básicos

### Ejemplo 1: Estado General del Proyecto
```
Usuario: @workspace Dame un resumen del estado del proyecto

Copilot: El proyecto AutoGPT Platform tiene:
- 13 servicios Docker configurados
- Frontend Next.js en puerto 3000
- Backend FastAPI en puerto 8006
- Base de datos PostgreSQL (db)
- Redis para caché
- RabbitMQ para mensajería
- Servicios activos: 9/13
- Estado: Desarrollo
```

### Ejemplo 2: Verificar Servicios
```
Usuario: @workspace ¿Qué servicios están corriendo?

Copilot: Servicios activos:
✅ frontend (Next.js) - Puerto 3000
✅ rest_server - Puerto 8006
✅ websocket_server - Puerto 8001
✅ db (PostgreSQL) - Puerto 5432
✅ redis - Puerto 6379
❌ executor - No iniciado
❌ scheduler_server - No iniciado
```

### Ejemplo 3: Estructura del Proyecto
```
Usuario: @workspace Explica la arquitectura del proyecto

Copilot: Arquitectura de AutoGPT Platform:

1. FRONTEND (Next.js 15)
   - App Router
   - React Server Components
   - Tailwind CSS + Radix UI
   
2. BACKEND (FastAPI)
   - REST API Server (puerto 8006)
   - WebSocket Server (puerto 8001)
   - Executor para agents
   - Scheduler para tareas
   
3. BASES DE DATOS
   - PostgreSQL (datos principales)
   - Redis (caché y sesiones)
   
4. MESSAGE BROKER
   - RabbitMQ (comunicación async)
```

---

## 🐛 Debugging

### Ejemplo 4: Error en Servicio
```
Usuario: @workspace ¿Por qué falla el servicio rest_server?

Copilot: Analizando logs del rest_server...

Problemas detectados:
1. Error de conexión a PostgreSQL
   - Causa: Variable DATABASE_URL incorrecta
   - Solución: Verificar .env

2. Puerto 8006 en uso
   - Causa: Proceso anterior no terminó
   - Solución: docker compose restart rest_server

3. Dependencias faltantes
   - Causa: requirements.txt no instalado
   - Solución: docker compose build rest_server
```

### Ejemplo 5: Análisis de Logs
```
Usuario: @workspace Analiza los logs y encuentra el error

Copilot: Revisando logs...

ERROR encontrado en rest_server (línea 234):
[ERROR] Connection refused: postgres://localhost:5432
       
Causa raíz:
- El servicio 'db' no está iniciado
- Variable de entorno DATABASE_URL apunta a localhost

Solución:
1. Inicia el servicio: docker compose up db -d
2. O corrige en .env: DATABASE_URL=postgresql://db:5432
```

### Ejemplo 6: Debugging de Timeout
```
Usuario: @workspace ¿Qué servicio está causando timeout?

Copilot: Analizando tiempos de respuesta...

Servicio con timeout: websocket_server

Diagnóstico:
- Tiempo de respuesta: 30+ segundos
- Causa: Conexión bloqueada a RabbitMQ
- RabbitMQ status: No iniciado

Acción recomendada:
docker compose up rabbitmq -d
docker compose restart websocket_server
```

---

## 🚀 Desarrollo de Features

### Ejemplo 7: Nueva Funcionalidad
```
Usuario: @workspace /new endpoint para gestionar notificaciones

Copilot: Creando endpoint de notificaciones...

Archivos a crear/modificar:
1. backend/app/routers/notifications.py
2. backend/app/models/notification.py
3. backend/app/schemas/notification.py
4. frontend/src/app/notifications/page.tsx

[Código generado...]

Test:
curl http://localhost:8006/api/notifications
```

### Ejemplo 8: Integrar Nuevo Servicio
```
Usuario: @workspace Crea un servicio de email notifications

Copilot: Creando servicio de email...

1. Configurar docker-compose.yml:
   [Muestra configuración...]

2. Crear servicio:
   - app/services/email_service.py
   - Configuración SMTP
   - Templates de email

3. Integrar con rest_server:
   - Endpoint POST /api/send-email
   - Validación con Pydantic

4. Variables de entorno necesarias:
   - SMTP_HOST
   - SMTP_PORT
   - SMTP_USER
   - SMTP_PASS
```

### Ejemplo 9: Refactoring
```
Usuario: @workspace Identifica código duplicado

Copilot: Código duplicado detectado:

1. Función check_service_status()
   - Aparece en: sadockdog_manager.py (3 veces)
   - Sugerencia: Extraer a clase ServiceChecker

2. Configuración de colores ANSI
   - Aparece en: 5 archivos diferentes
   - Sugerencia: Crear módulo colors.py

3. Logging setup
   - Repetido en cada servicio
   - Sugerencia: Usar logger.py centralizado
```

---

## 🧪 Testing

### Ejemplo 10: Generar Tests
```
Usuario: @workspace /tests Genera tests para el módulo de autenticación

Copilot: Generando tests para auth...

# tests/test_auth.py
import pytest
from app.auth import AuthService

def test_login_success():
    # Arrange
    auth = AuthService()
    email = "test@example.com"
    password = "secure123"
    
    # Act
    result = auth.login(email, password)
    
    # Assert
    assert result.success is True
    assert result.token is not None

[Más tests generados...]
```

### Ejemplo 11: Ejecutar Tests
```
Usuario: @workspace /tests ¿Qué tests fallan?

Copilot: Ejecutando tests...

Resultados:
✅ test_auth.py::test_login_success - PASSED
✅ test_auth.py::test_login_wrong_password - PASSED
❌ test_users.py::test_create_user - FAILED
   Error: IntegrityError - Email already exists
   
❌ test_notifications.py::test_send_notification - FAILED
   Error: Connection refused to RabbitMQ

Resumen: 8 passed, 2 failed
```

### Ejemplo 12: Cobertura de Tests
```
Usuario: @workspace ¿Cuál es la cobertura de tests actual?

Copilot: Analizando cobertura...

Cobertura por módulo:
- auth: 92% ✅
- users: 87% ✅
- notifications: 45% ⚠️
- agents: 23% ❌
- executor: 15% ❌

Archivos sin tests:
- app/services/cache_service.py
- app/utils/validation.py
- app/routers/monitoring.py

Recomendación: Priorizar executor y agents
```

---

## ⚡ Optimización

### Ejemplo 13: Rendimiento del Backend
```
Usuario: @workspace ¿Cómo puedo optimizar el rendimiento del backend?

Copilot: Análisis de rendimiento:

PROBLEMAS DETECTADOS:
1. N+1 Queries en /api/users
   - Solución: Usar joinedload()
   
2. Cache no configurado
   - Solución: Implementar Redis cache
   
3. Sin compresión de respuestas
   - Solución: Activar gzip middleware

4. Queries lentas (>1s)
   - Tabla 'agents': Sin índices
   - Solución: CREATE INDEX idx_user_id ON agents(user_id)

CÓDIGO MEJORADO:
[Muestra optimizaciones...]
```

### Ejemplo 14: Optimizar Base de Datos
```
Usuario: @workspace Optimiza las consultas a la base de datos

Copilot: Analizando queries...

QUERIES LENTAS:
1. SELECT * FROM agents WHERE user_id = ?
   - Tiempo: 2.3s
   - Filas: 50,000
   - Índice faltante: user_id

2. SELECT * FROM notifications WHERE created_at > ?
   - Tiempo: 1.8s
   - Índice faltante: created_at

MIGRACIONES SUGERIDAS:
CREATE INDEX idx_agents_user_id ON agents(user_id);
CREATE INDEX idx_notifications_created_at ON notifications(created_at);

MEJORA ESTIMADA: 85% más rápido
```

### Ejemplo 15: Bundle Size Frontend
```
Usuario: @workspace Optimiza el bundle size del frontend

Copilot: Análisis de bundle...

BUNDLE SIZE ACTUAL: 2.3 MB

COMPONENTES GRANDES:
- next-auth: 450 KB
- @radix-ui: 380 KB
- moment.js: 230 KB ⚠️ (usar date-fns)
- lodash: 180 KB ⚠️ (importar específico)

OPTIMIZACIONES:
1. Reemplazar moment → date-fns (-150 KB)
2. Import específico lodash (-120 KB)
3. Lazy load modals (-200 KB)
4. Code splitting por ruta (-300 KB)

BUNDLE SIZE OPTIMIZADO: 1.5 MB (-35%)
```

---

## 🚢 Deployment

### Ejemplo 16: Checklist Pre-Producción
```
Usuario: @workspace ¿Qué archivos de configuración debo revisar antes de producción?

Copilot: Checklist de producción:

ARCHIVOS CRÍTICOS:
☐ .env.production
  - DATABASE_URL configurada
  - REDIS_URL configurada
  - SECRET_KEY strong
  - DEBUG=false

☐ docker-compose.prod.yml
  - Recursos limitados
  - Health checks activados
  - Restart policies configuradas

☐ nginx.conf
  - SSL configurado
  - Rate limiting
  - Gzip compression

VALIDACIONES:
☐ Todos los tests pasan
☐ No hay TODOs críticos
☐ Logs configurados
☐ Backup automatizado
☐ Monitoring activo
```

### Ejemplo 17: Variables de Entorno
```
Usuario: @workspace ¿Qué variables de entorno faltan?

Copilot: Variables faltantes:

REQUERIDAS EN PRODUCCIÓN:
❌ SECRET_KEY - No definida
❌ ALLOWED_HOSTS - No definida
❌ SENTRY_DSN - No definida
❌ SMTP_HOST - No definida

OPCIONALES PERO RECOMENDADAS:
⚠️  MAX_WORKERS - Usar default (4)
⚠️  LOG_LEVEL - Usar default (INFO)
⚠️  CACHE_TTL - Usar default (300)

ACCIÓN:
Crear archivo .env.production con estas variables
```

### Ejemplo 18: Plan de Deployment
```
Usuario: @workspace Documenta el proceso de deployment paso a paso

Copilot: PROCESO DE DEPLOYMENT:

PRE-DEPLOYMENT:
1. Ejecutar tests
   $ pytest
   
2. Validar linting
   $ ruff check .
   
3. Build de imágenes
   $ docker compose -f docker-compose.prod.yml build

DEPLOYMENT:
4. Backup de base de datos
   $ pg_dump > backup_$(date +%Y%m%d).sql
   
5. Pull código
   $ git pull origin main
   
6. Aplicar migraciones
   $ alembic upgrade head
   
7. Reiniciar servicios
   $ docker compose -f docker-compose.prod.yml up -d

POST-DEPLOYMENT:
8. Verificar health checks
   $ curl http://localhost:8006/health
   
9. Verificar logs
   $ docker compose logs -f
   
10. Smoke tests
    $ pytest tests/smoke/

ROLLBACK (si falla):
$ git checkout <previous-commit>
$ docker compose -f docker-compose.prod.yml up -d
```

---

## 💡 Tips Avanzados

### Ejemplo 19: Análisis de Seguridad
```
Usuario: @workspace ¿Hay vulnerabilidades en las dependencias?

Copilot: Auditoría de seguridad...

VULNERABILIDADES DETECTADAS:
1. cryptography==3.4.8 → CVE-2024-XXXX
   - Severidad: ALTA
   - Versión segura: 42.0.0+
   
2. Pillow==9.0.0 → CVE-2023-XXXX
   - Severidad: MEDIA
   - Versión segura: 10.0.0+

DEPENDENCIAS DESACTUALIZADAS:
- fastapi: 0.116.1 → 0.121.0 (segura)
- pydantic: 2.5.0 → 2.10.6 (segura)

ACCIÓN RECOMENDADA:
$ pip install --upgrade cryptography Pillow
$ pip list --outdated
```

### Ejemplo 20: Monitoring Setup
```
Usuario: @workspace Crea un dashboard de monitoreo con las métricas clave

Copilot: Configurando monitoring...

MÉTRICAS CLAVE:
1. Servicios
   - Uptime de cada servicio
   - Health checks status
   
2. Performance
   - Response time API (<200ms)
   - Query time DB (<100ms)
   - Cache hit rate (>80%)
   
3. Recursos
   - CPU usage (<70%)
   - Memory usage (<80%)
   - Disk usage (<85%)
   
4. Errores
   - Error rate (<1%)
   - 5xx responses
   - Failed jobs

DASHBOARD:
[Código de dashboard React...]

ALERTAS:
[Configuración de alertas...]
```

---

## 🎓 Casos de Uso por Rol

### DevOps
```
@workspace Estado de infraestructura completa
@workspace Optimiza docker-compose para producción
@workspace Configura monitoring con Prometheus
```

### Backend Developer
```
@workspace Explica la arquitectura del backend
@workspace /new endpoint para analytics
@workspace Optimiza las queries SQL lentas
```

### Frontend Developer
```
@workspace Estructura del proyecto Next.js
@workspace Componentes React disponibles
@workspace Optimiza el bundle size
```

### QA/Testing
```
@workspace /tests ¿Qué módulos no tienen tests?
@workspace Genera plan de testing completo
@workspace Crea tests E2E con Playwright
```

---

**Última actualización:** 2025-11-09  
**Versión:** 1.0  
**Más ejemplos:** Ver WORKSPACE_ADVANCED_GUIDE.md
