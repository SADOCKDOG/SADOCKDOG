# 🔍 Guía de Troubleshooting

Soluciones a problemas comunes en AutoGPT Platform.

---

## 📋 Índice

1. [Docker Issues](#docker-issues)
2. [Database Issues](#database-issues)
3. [Backend Issues](#backend-issues)
4. [Frontend Issues](#frontend-issues)
5. [Network Issues](#network-issues)
6. [Performance Issues](#performance-issues)
7. [Authentication Issues](#authentication-issues)
8. [Deployment Issues](#deployment-issues)

---

## Docker Issues

### ❌ Docker no está corriendo

**Síntomas:**
```
Cannot connect to the Docker daemon
Error response from daemon
```

**Diagnóstico:**
```powershell
# Verificar si Docker está corriendo
docker ps
docker --version

# Ver servicios de Docker
Get-Service -Name "*docker*"
```

**Soluciones:**

1. **Iniciar Docker Desktop:**
   - Abrir Docker Desktop desde el menú de inicio
   - Esperar a que el icono cambie a verde
   - Reintentar comando

2. **Reiniciar Docker Service:**
   ```powershell
   # Como administrador
   Restart-Service -Name "Docker Desktop Service"
   ```

3. **Reinstalar Docker:**
   - Desinstalar Docker Desktop
   - Reiniciar Windows
   - Descargar última versión de [docker.com](https://www.docker.com/products/docker-desktop/)
   - Instalar con permisos de administrador

---

### ❌ Port already allocated

**Síntomas:**
```
Error starting userland proxy: listen tcp 0.0.0.0:3000: bind: address already in use
```

**Diagnóstico:**
```powershell
# Ver qué proceso usa el puerto
netstat -ano | findstr :3000

# Identificar proceso
Get-Process -Id [PID]
```

**Soluciones:**

1. **Matar proceso que usa el puerto:**
   ```powershell
   # Reemplazar [PID] con el número del proceso
   taskkill /F /PID [PID]
   ```

2. **Cambiar puerto en docker-compose.yml:**
   ```yaml
   services:
     frontend:
       ports:
         - "3001:3000"  # Cambiar 3000 a 3001
   ```

3. **Detener todos los contenedores:**
   ```bash
   docker compose down
   # Esperar 5 segundos
   docker compose up -d
   ```

---

### ❌ Container keeps restarting

**Síntomas:**
```
Restarting (1) X seconds ago
Status: unhealthy
```

**Diagnóstico:**
```bash
# Ver logs del contenedor
docker compose logs [service_name]

# Ver últimas 50 líneas
docker compose logs --tail=50 [service_name]

# Seguir logs en tiempo real
docker compose logs -f [service_name]

# Inspeccionar contenedor
docker inspect [container_id]
```

**Soluciones:**

1. **Revisar logs para error específico:**
   ```bash
   docker compose logs frontend | grep -i error
   docker compose logs frontend | grep -i exception
   ```

2. **Verificar health check:**
   ```bash
   # Ver health status
   docker inspect [container_id] | grep -i health

   # Ejecutar health check manualmente
   docker compose exec frontend curl http://localhost:3000/api/health
   ```

3. **Rebuild contenedor:**
   ```bash
   docker compose build [service_name]
   docker compose up -d [service_name]
   ```

4. **Reset completo:**
   ```bash
   docker compose down
   docker compose build --no-cache
   docker compose up -d
   ```

---

### ❌ Out of memory

**Síntomas:**
```
OOMKilled
Container killed due to memory limit
```

**Diagnóstico:**
```bash
# Ver uso de memoria
docker stats

# Ver límites de memoria
docker inspect [container_id] | grep Memory
```

**Soluciones:**

1. **Aumentar memoria en Docker Desktop:**
   - Docker Desktop → Settings → Resources
   - Memory: Aumentar a mínimo 8 GB
   - Apply & Restart

2. **Aumentar límite en docker-compose.yml:**
   ```yaml
   services:
     frontend:
       mem_limit: 4g
       mem_reservation: 2g
   ```

3. **Liberar memoria:**
   ```bash
   # Limpiar containers detenidos
   docker container prune

   # Limpiar imágenes no usadas
   docker image prune -a

   # Limpiar todo
   docker system prune -a --volumes
   ```

---

### ❌ No space left on device

**Síntomas:**
```
Error response from daemon: no space left on device
```

**Diagnóstico:**
```bash
# Ver uso de disco por Docker
docker system df

# Ver detallado
docker system df -v
```

**Soluciones:**

1. **Limpiar recursos Docker:**
   ```bash
   # Limpiar todo excepto volúmenes
   docker system prune -a

   # Limpiar incluyendo volúmenes
   docker system prune -a --volumes

   # Limpiar específicamente
   docker image prune -a
   docker container prune
   docker volume prune
   docker network prune
   ```

2. **Aumentar espacio en disco virtual (Docker Desktop):**
   - Docker Desktop → Settings → Resources → Disk image size
   - Aumentar tamaño
   - Apply & Restart

---

## Database Issues

### ❌ Can't reach database server

**Síntomas:**
```
Error: Can't reach database server at `localhost:5432`
Connection refused
```

**Diagnóstico:**
```bash
# Verificar estado de PostgreSQL
docker compose ps db

# Ver logs de PostgreSQL
docker compose logs db

# Test conexión
docker compose exec db pg_isready -U postgres
```

**Soluciones:**

1. **Reiniciar PostgreSQL:**
   ```bash
   docker compose restart db
   
   # Esperar 10 segundos
   sleep 10
   
   # Verificar estado
   docker compose ps db
   ```

2. **Verificar variables de entorno:**
   ```bash
   # Ver configuración
   docker compose config | grep -A 10 "db:"
   
   # Verificar .env
   cat autogpt_platform/.env | grep DATABASE
   ```

3. **Reset completo de base de datos:**
   ```bash
   # CUIDADO: Esto borra todos los datos!
   docker compose down -v
   docker compose up -d db
   
   # Esperar inicialización
   sleep 15
   
   # Ejecutar migraciones
   cd autogpt_platform/backend
   poetry run prisma migrate deploy
   ```

---

### ❌ Migration failed

**Síntomas:**
```
Error: Migration failed
P3009: Migration failed to apply
```

**Diagnóstico:**
```bash
# Ver estado de migraciones
cd autogpt_platform/backend
poetry run prisma migrate status

# Ver logs de migración
docker compose logs rest_server | grep migration
```

**Soluciones:**

1. **Resolver migración manualmente:**
   ```bash
   # Marcar migración como aplicada
   poetry run prisma migrate resolve --applied [migration_name]
   
   # O marcar como rolled back
   poetry run prisma migrate resolve --rolled-back [migration_name]
   
   # Reintentar
   poetry run prisma migrate deploy
   ```

2. **Reset de migraciones (desarrollo):**
   ```bash
   # CUIDADO: Borra todos los datos!
   poetry run prisma migrate reset
   
   # Confirmar con 'y'
   
   # Regenerar cliente
   poetry run prisma generate
   ```

3. **Crear nueva migración desde schema:**
   ```bash
   # Push schema directamente (desarrollo)
   poetry run prisma db push
   
   # O crear migración
   poetry run prisma migrate dev --name fix_schema
   ```

---

### ❌ Connection pool exhausted

**Síntomas:**
```
Error: Can't find an available connection
Connection pool timeout
```

**Diagnóstico:**
```bash
# Ver conexiones activas
docker compose exec db psql -U postgres -c "SELECT count(*) FROM pg_stat_activity;"

# Ver conexiones por estado
docker compose exec db psql -U postgres -c "SELECT state, count(*) FROM pg_stat_activity GROUP BY state;"
```

**Soluciones:**

1. **Aumentar connection pool:**
   ```prisma
   // En schema.prisma
   datasource db {
     provider = "postgresql"
     url      = env("DATABASE_URL")
     connection_limit = 20  // Aumentar de 10 a 20
   }
   ```

2. **Reiniciar servicios:**
   ```bash
   docker compose restart rest_server executor
   ```

3. **Cerrar conexiones idle:**
   ```bash
   docker compose exec db psql -U postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE state = 'idle' AND pid != pg_backend_pid();"
   ```

---

## Backend Issues

### ❌ Module not found

**Síntomas:**
```
ModuleNotFoundError: No module named 'xxx'
ImportError: cannot import name 'xxx'
```

**Diagnóstico:**
```bash
# Ver dependencias instaladas
cd autogpt_platform/backend
poetry show

# Verificar lock file
poetry check

# Ver entorno Python
poetry env info
```

**Soluciones:**

1. **Reinstalar dependencias:**
   ```bash
   poetry install
   
   # O forzar reinstalación
   poetry install --no-cache
   ```

2. **Agregar dependencia faltante:**
   ```bash
   poetry add [package_name]
   ```

3. **Reset del entorno virtual:**
   ```bash
   # Eliminar entorno
   poetry env remove python
   
   # Recrear e instalar
   poetry install
   ```

---

### ❌ Prisma client not generated

**Síntomas:**
```
ImportError: cannot import name 'PrismaClient' from 'prisma'
```

**Diagnóstico:**
```bash
# Ver cliente Prisma
poetry show prisma

# Ver archivos generados
ls -la node_modules/@prisma/client 2>/dev/null || echo "Not found"
```

**Soluciones:**

1. **Generar cliente Prisma:**
   ```bash
   poetry run prisma generate
   ```

2. **Reset completo:**
   ```bash
   poetry run prisma migrate reset
   poetry run prisma generate
   ```

3. **Verificar schema.prisma:**
   ```bash
   poetry run prisma validate
   poetry run prisma format
   ```

---

### ❌ Test failures

**Síntomas:**
```
FAILED tests/test_block.py::test_github_create_repo
AssertionError: ...
```

**Diagnóstico:**
```bash
# Ejecutar test con verbose
poetry run pytest tests/test_block.py::test_github_create_repo -vvs

# Ver traceback completo
poetry run pytest --tb=long

# Ver logs de test
poetry run pytest --log-cli-level=DEBUG
```

**Soluciones:**

1. **Actualizar snapshots:**
   ```bash
   poetry run pytest --snapshot-update
   
   # Revisar cambios
   git diff snapshots/
   ```

2. **Limpiar cache de pytest:**
   ```bash
   rm -rf .pytest_cache
   poetry run pytest
   ```

3. **Ejecutar tests aislados:**
   ```bash
   poetry run pytest -x  # Detener en primer fallo
   poetry run pytest --lf  # Solo último fallido
   poetry run pytest --ff  # Primero fallidos, luego resto
   ```

---

## Frontend Issues

### ❌ Build failed

**Síntomas:**
```
Error: Build failed
Type error: ...
Module not found: ...
```

**Diagnóstico:**
```bash
# Ver logs completos
cd autogpt_platform/frontend
pnpm build 2>&1 | tee build.log

# Type check
pnpm type-check
```

**Soluciones:**

1. **Limpiar y rebuil:**
   ```bash
   # Limpiar cache
   rm -rf .next
   rm -rf node_modules/.cache
   
   # Reinstalar dependencias
   rm -rf node_modules
   pnpm install
   
   # Rebuil
   pnpm build
   ```

2. **Fix de types:**
   ```bash
   # Regenerar types desde backend
   pnpm generate:api
   
   # Verificar types
   pnpm type-check
   ```

3. **Update de dependencias:**
   ```bash
   # Ver outdated
   pnpm outdated
   
   # Update selectivo
   pnpm update [package]
   
   # O update todo
   pnpm update
   ```

---

### ❌ Tests failing

**Síntomas:**
```
Error: Test failed
Playwright test failed
```

**Diagnóstico:**
```bash
# Ejecutar con UI
pnpm test-ui

# Ejecutar con headed
pnpm test --headed

# Ver trace
pnpm playwright show-trace trace.zip
```

**Soluciones:**

1. **Regenerar snapshots:**
   ```bash
   pnpm test --update-snapshots
   ```

2. **Limpiar estado:**
   ```bash
   # Limpiar storage de tests
   rm -rf test-results
   rm -rf playwright-report
   
   # Reintentar
   pnpm test
   ```

3. **Debug interactivo:**
   ```bash
   # Abrir inspector
   pnpm test --debug
   
   # Generar código de test
   pnpm playwright codegen http://localhost:3000
   ```

---

### ❌ Hot reload no funciona

**Síntomas:**
```
Cambios en código no se reflejan en el navegador
```

**Diagnóstico:**
```bash
# Ver logs de Next.js
pnpm dev

# Verificar file watchers
echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf
```

**Soluciones:**

1. **Reiniciar dev server:**
   ```bash
   # Ctrl+C para detener
   pnpm dev
   ```

2. **Limpiar cache:**
   ```bash
   rm -rf .next
   pnpm dev
   ```

3. **Aumentar file watchers (Linux/WSL):**
   ```bash
   echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf
   sudo sysctl -p
   ```

---

## Network Issues

### ❌ Cannot connect to backend

**Síntomas:**
```
Failed to fetch
Network error
CORS error
```

**Diagnóstico:**
```bash
# Test conexión desde frontend
docker compose exec frontend curl http://rest_server:8006/health

# Test desde host
curl http://localhost:8006/health

# Ver configuración de red
docker network inspect autogpt_platform_default
```

**Soluciones:**

1. **Verificar que backend esté corriendo:**
   ```bash
   docker compose ps rest_server
   docker compose logs rest_server | tail -20
   ```

2. **Verificar URL en frontend:**
   ```typescript
   // Verificar en .env o código
   NEXT_PUBLIC_API_URL=http://localhost:8006
   ```

3. **Reiniciar servicios:**
   ```bash
   docker compose restart rest_server frontend
   ```

---

### ❌ WebSocket connection failed

**Síntomas:**
```
WebSocket connection failed
ws://localhost:8001 failed
```

**Diagnóstico:**
```bash
# Verificar WebSocket server
docker compose ps websocket_server
docker compose logs websocket_server

# Test conexión
curl http://localhost:8001/health
```

**Soluciones:**

1. **Reiniciar WebSocket server:**
   ```bash
   docker compose restart websocket_server
   ```

2. **Verificar configuración:**
   ```bash
   # Ver variables de entorno
   docker compose config | grep -A 5 websocket
   ```

3. **Verificar desde navegador:**
   ```javascript
   // En DevTools Console
   const ws = new WebSocket('ws://localhost:8001');
   ws.onopen = () => console.log('Connected');
   ws.onerror = (e) => console.error('Error:', e);
   ```

---

## Performance Issues

### ❌ Slow response times

**Síntomas:**
```
Requests taking > 5 seconds
UI sluggish
```

**Diagnóstico:**
```bash
# Ver uso de recursos
docker stats

# Ver queries lentas
docker compose exec db psql -U postgres -c "SELECT pid, query, state, query_start FROM pg_stat_activity WHERE state != 'idle' ORDER BY query_start;"

# Ver logs de backend
docker compose logs rest_server | grep "ms"
```

**Soluciones:**

1. **Agregar indexes a base de datos:**
   ```sql
   -- Ejemplo
   CREATE INDEX idx_user_id ON agent_graph(user_id);
   CREATE INDEX idx_status_created ON agent_graph_execution(status, created_at);
   ```

2. **Aumentar recursos:**
   ```yaml
   # docker-compose.yml
   services:
     rest_server:
       cpus: '2.0'
       mem_limit: 4g
   ```

3. **Optimizar queries:**
   ```python
   # Usar select_related / prefetch_related
   # Agregar límites a queries
   # Usar paginación
   ```

---

### ❌ High memory usage

**Síntomas:**
```
Container using > 2GB RAM
System becoming slow
```

**Diagnóstico:**
```bash
# Ver uso por contenedor
docker stats --no-stream

# Ver procesos dentro del contenedor
docker compose exec rest_server ps aux

# Memory profiling (Python)
docker compose exec rest_server python -m memory_profiler script.py
```

**Soluciones:**

1. **Agregar límites de memoria:**
   ```yaml
   services:
     rest_server:
       mem_limit: 2g
       mem_reservation: 1g
   ```

2. **Optimizar código:**
   - Cerrar conexiones
   - Liberar objetos grandes
   - Usar generadores en vez de listas
   - Agregar garbage collection manual

3. **Reiniciar servicios periódicamente:**
   ```bash
   # Cada 24 horas
   docker compose restart rest_server executor
   ```

---

## Authentication Issues

### ❌ Invalid token

**Síntomas:**
```
401 Unauthorized
Invalid token
Token expired
```

**Diagnóstico:**
```bash
# Ver logs de autenticación
docker compose logs auth | grep -i token
docker compose logs rest_server | grep -i auth

# Verificar Supabase
curl http://localhost:8000/auth/v1/health
```

**Soluciones:**

1. **Logout y login nuevamente:**
   - Ir a http://localhost:3000/profile
   - Logout
   - Login nuevamente

2. **Limpiar cookies:**
   ```javascript
   // En DevTools Console
   document.cookie.split(";").forEach(c => {
     document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/");
   });
   ```

3. **Verificar configuración de Supabase:**
   ```bash
   # Ver variables de entorno
   docker compose config | grep -i supabase
   ```

---

## Deployment Issues

### ❌ Production build fails

**Síntomas:**
```
Error building for production
Deployment failed
```

**Diagnóstico:**
```bash
# Build local
pnpm build

# Ver errores específicos
pnpm build 2>&1 | grep -i error
```

**Soluciones:**

1. **Verificar variables de entorno:**
   ```bash
   # Asegurar que existen en producción
   NEXT_PUBLIC_API_URL
   DATABASE_URL
   SUPABASE_URL
   SUPABASE_KEY
   ```

2. **Test build localmente:**
   ```bash
   # Simular producción
   NODE_ENV=production pnpm build
   pnpm start
   ```

3. **Verificar dependencias:**
   ```bash
   # Verificar que no hay dev dependencies en runtime
   pnpm install --production
   ```

---

## Diagnostic Commands

### Quick Health Check

```bash
#!/bin/bash
# health_check.sh

echo "=== Docker ==="
docker --version
docker compose ps

echo -e "\n=== Services Health ==="
curl -f http://localhost:3000 || echo "Frontend: DOWN"
curl -f http://localhost:8006/health || echo "Backend: DOWN"
curl -f http://localhost:8001/health || echo "WebSocket: DOWN"

echo -e "\n=== Database ==="
docker compose exec db pg_isready -U postgres

echo -e "\n=== Resources ==="
docker stats --no-stream
```

### Full System Report

```bash
#!/bin/bash
# system_report.sh

OUTPUT="system_report_$(date +%Y%m%d_%H%M%S).txt"

{
  echo "=== SYSTEM REPORT ==="
  echo "Generated: $(date)"
  echo ""
  
  echo "=== Docker Version ==="
  docker --version
  docker compose version
  echo ""
  
  echo "=== Container Status ==="
  docker compose ps
  echo ""
  
  echo "=== Resource Usage ==="
  docker stats --no-stream
  echo ""
  
  echo "=== Disk Usage ==="
  docker system df
  echo ""
  
  echo "=== Recent Logs (Last 50 lines per service) ==="
  for service in frontend rest_server executor websocket_server; do
    echo "--- $service ---"
    docker compose logs --tail=50 $service
    echo ""
  done
  
} > "$OUTPUT"

echo "Report saved to: $OUTPUT"
```

---

*Última actualización: 2025-01-06*
