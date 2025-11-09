# 🔧 Referencia Completa de Comandos

Todos los comandos útiles para trabajar con AutoGPT Platform.

---

## 📋 Índice

1. [Docker Compose](#docker-compose)
2. [Docker](#docker)
3. [Backend (Python/Poetry)](#backend-pythonpoetry)
4. [Frontend (Node/pnpm)](#frontend-nodepnpm)
5. [Database (Prisma)](#database-prisma)
6. [Git](#git)
7. [System](#system)

---

## Docker Compose

### Gestión de Servicios

```bash
# Iniciar todos los servicios
docker compose up -d

# Iniciar servicios específicos
docker compose up -d frontend backend

# Detener todos los servicios
docker compose down

# Detener y eliminar volúmenes
docker compose down -v

# Reiniciar todos los servicios
docker compose restart

# Reiniciar servicio específico
docker compose restart frontend

# Pausar servicios (sin detener)
docker compose pause

# Reanudar servicios pausados
docker compose unpause
```

### Estado y Monitorización

```bash
# Ver estado de contenedores
docker compose ps

# Ver estado con formato JSON
docker compose ps --format json

# Ver procesos en contenedores
docker compose top

# Ver configuración actual
docker compose config

# Validar docker-compose.yml
docker compose config --quiet

# Ver eventos en tiempo real
docker compose events
```

### Logs

```bash
# Ver logs de todos los servicios
docker compose logs

# Ver logs de servicio específico
docker compose logs frontend

# Ver últimas N líneas
docker compose logs --tail=100

# Seguir logs en tiempo real
docker compose logs -f

# Ver logs con timestamps
docker compose logs -t

# Ver logs desde tiempo específico
docker compose logs --since 2024-01-06T10:00:00

# Ver logs hasta tiempo específico
docker compose logs --until 2024-01-06T12:00:00
```

### Build

```bash
# Construir todas las imágenes
docker compose build

# Construir sin cache
docker compose build --no-cache

# Construir servicio específico
docker compose build frontend

# Construir en paralelo
docker compose build --parallel

# Construir y iniciar
docker compose up --build -d
```

### Ejecución de Comandos

```bash
# Ejecutar comando en contenedor corriendo
docker compose exec frontend sh

# Ejecutar comando como root
docker compose exec -u root frontend sh

# Ejecutar comando sin TTY (para scripts)
docker compose exec -T frontend npm --version

# Ejecutar comando en nuevo contenedor
docker compose run --rm frontend npm install
```

### Recursos

```bash
# Ver uso de recursos
docker compose stats

# Ver uso sin stream (snapshot)
docker compose stats --no-stream

# Ver imágenes usadas
docker compose images

# Ver volúmenes usados
docker compose volume ls
```

---

## Docker

### Contenedores

```bash
# Listar contenedores corriendo
docker ps

# Listar todos los contenedores
docker ps -a

# Listar últimos N contenedores
docker ps -n 5

# Ver detalles de contenedor
docker inspect <container_id>

# Ver logs de contenedor
docker logs <container_id>

# Entrar en contenedor corriendo
docker exec -it <container_id> sh

# Copiar archivos desde/hacia contenedor
docker cp <container_id>:/path/to/file ./local/path
docker cp ./local/file <container_id>:/path/to/dest

# Detener contenedor
docker stop <container_id>

# Iniciar contenedor detenido
docker start <container_id>

# Reiniciar contenedor
docker restart <container_id>

# Pausar contenedor
docker pause <container_id>

# Reanudar contenedor pausado
docker unpause <container_id>

# Eliminar contenedor
docker rm <container_id>

# Eliminar contenedor forzadamente
docker rm -f <container_id>

# Eliminar todos los contenedores detenidos
docker container prune
```

### Imágenes

```bash
# Listar imágenes
docker images

# Ver detalles de imagen
docker inspect <image_id>

# Construir imagen
docker build -t myimage:tag .

# Construir sin cache
docker build --no-cache -t myimage:tag .

# Eliminar imagen
docker rmi <image_id>

# Eliminar imagen forzadamente
docker rmi -f <image_id>

# Eliminar imágenes no utilizadas
docker image prune

# Eliminar todas las imágenes no usadas
docker image prune -a

# Ver historial de imagen
docker history <image_id>

# Guardar imagen a archivo
docker save -o myimage.tar myimage:tag

# Cargar imagen desde archivo
docker load -i myimage.tar
```

### Redes

```bash
# Listar redes
docker network ls

# Crear red
docker network create mynetwork

# Inspeccionar red
docker network inspect <network_name>

# Conectar contenedor a red
docker network connect <network_name> <container_id>

# Desconectar contenedor de red
docker network disconnect <network_name> <container_id>

# Eliminar red
docker network rm <network_name>

# Eliminar redes no utilizadas
docker network prune
```

### Volúmenes

```bash
# Listar volúmenes
docker volume ls

# Crear volumen
docker volume create myvolume

# Inspeccionar volumen
docker volume inspect myvolume

# Eliminar volumen
docker volume rm myvolume

# Eliminar volúmenes no utilizados
docker volume prune
```

### Sistema

```bash
# Ver información del sistema Docker
docker info

# Ver versión de Docker
docker version

# Ver uso de disco
docker system df

# Ver uso detallado
docker system df -v

# Limpiar sistema completo
docker system prune

# Limpiar incluyendo volúmenes
docker system prune --volumes

# Limpiar TODO (peligroso!)
docker system prune -a --volumes

# Ver eventos del sistema
docker events

# Ver estadísticas de recursos
docker stats

# Ver procesos en contenedor
docker top <container_id>
```

---

## Backend (Python/Poetry)

### Gestión de Entorno

```bash
# Cambiar al directorio backend
cd autogpt_platform/backend

# Instalar dependencias
poetry install

# Instalar con extras
poetry install --extras "dev test"

# Actualizar dependencias
poetry update

# Agregar nueva dependencia
poetry add requests

# Agregar dependencia de desarrollo
poetry add --dev pytest

# Remover dependencia
poetry remove requests

# Mostrar dependencias instaladas
poetry show

# Mostrar dependencias en árbol
poetry show --tree

# Verificar lock file
poetry check
```

### Ejecución

```bash
# Iniciar servidor de desarrollo
poetry run serve

# Iniciar con hot reload
poetry run uvicorn backend.server.server:app --reload --port 8006

# Ejecutar script Python
poetry run python script.py

# Ejecutar comando en entorno virtual
poetry run <command>

# Activar shell del entorno virtual
poetry shell
```

### Testing

```bash
# Ejecutar todos los tests
poetry run test

# Ejecutar tests específicos
poetry run pytest backend/test/test_block.py

# Ejecutar con verbose
poetry run pytest -v

# Ejecutar con coverage
poetry run pytest --cov=backend

# Ejecutar test específico por nombre
poetry run pytest -k "test_github"

# Detener en primer fallo
poetry run pytest -x

# Mostrar print statements
poetry run pytest -s

# Actualizar snapshots
poetry run pytest --snapshot-update

# Ejecutar tests en paralelo
poetry run pytest -n auto
```

### Code Quality

```bash
# Formatear código (Black + isort)
poetry run format

# Solo verificar formato (no cambiar)
poetry run black --check .

# Lint código (ruff)
poetry run lint

# Fix automático de linting
poetry run ruff check --fix .

# Type checking (mypy)
poetry run mypy backend

# Verificar imports
poetry run isort --check-only .
```

### Prisma

```bash
# Generar cliente Prisma
poetry run prisma generate

# Crear migración
poetry run prisma migrate dev --name migration_name

# Aplicar migraciones
poetry run prisma migrate deploy

# Reset database
poetry run prisma migrate reset

# Ver estado de migraciones
poetry run prisma migrate status

# Abrir Prisma Studio
poetry run prisma studio

# Formatear schema.prisma
poetry run prisma format

# Validar schema
poetry run prisma validate
```

---

## Frontend (Node/pnpm)

### Gestión de Dependencias

```bash
# Cambiar al directorio frontend
cd autogpt_platform/frontend

# Instalar dependencias
pnpm install

# Agregar dependencia
pnpm add package-name

# Agregar dev dependency
pnpm add -D package-name

# Remover dependencia
pnpm remove package-name

# Actualizar dependencias
pnpm update

# Actualizar dependencia específica
pnpm update package-name

# Ver dependencias outdated
pnpm outdated

# Listar dependencias instaladas
pnpm list

# Verificar dependencias
pnpm audit
```

### Desarrollo

```bash
# Iniciar servidor de desarrollo
pnpm dev

# Iniciar en puerto específico
pnpm dev -p 3001

# Build para producción
pnpm build

# Iniciar servidor de producción
pnpm start

# Limpiar cache y build
pnpm clean
```

### Testing

```bash
# Ejecutar tests E2E
pnpm test

# Tests con UI de Playwright
pnpm test-ui

# Tests en modo headed
pnpm test --headed

# Tests con debugging
pnpm test --debug

# Generar código de tests
pnpm playwright codegen

# Ver reporte de tests
pnpm playwright show-report
```

### Code Quality

```bash
# Formatear y lint código
pnpm format

# Solo verificar formato
pnpm format:check

# Lint código
pnpm lint

# Fix automático de lint
pnpm lint:fix

# Type checking
pnpm type-check
```

### Storybook

```bash
# Iniciar Storybook
pnpm storybook

# Build Storybook
pnpm build-storybook

# Deploy a Chromatic
pnpm chromatic
```

### API Generation

```bash
# Generar client API desde OpenAPI
pnpm generate:api

# Ver spec OpenAPI
curl http://localhost:8006/openapi.json
```

---

## Database (Prisma)

### Migraciones

```bash
# Crear nueva migración
prisma migrate dev --name add_user_fields

# Aplicar migraciones pendientes
prisma migrate deploy

# Ver estado de migraciones
prisma migrate status

# Resolver migraciones fallidas
prisma migrate resolve --applied "migration_name"
prisma migrate resolve --rolled-back "migration_name"

# Reset completo (PELIGROSO!)
prisma migrate reset

# Crear migración desde cambios en schema
prisma migrate dev

# Aplicar migración específica
prisma migrate deploy --preview-feature
```

### Schema

```bash
# Validar schema.prisma
prisma validate

# Formatear schema.prisma
prisma format

# Generar cliente Prisma
prisma generate

# Pull schema desde database
prisma db pull

# Push schema a database (desarrollo)
prisma db push
```

### Data Management

```bash
# Abrir Prisma Studio
prisma studio

# Seed database
prisma db seed

# Ejecutar query directo
prisma db execute --file query.sql
```

### Debugging

```bash
# Ver queries generadas
DEBUG=prisma:query prisma studio

# Ver todos los logs
DEBUG=* prisma studio

# Ver engine logs
DEBUG=prisma:engine prisma studio
```

---

## Git

### Commits

```bash
# Commit con conventional commit
git commit -m "feat(backend): add new endpoint"
git commit -m "fix(frontend): resolve loading issue"
git commit -m "docs: update README"
git commit -m "refactor(backend): improve query performance"
git commit -m "test(frontend): add E2E tests"
git commit -m "ci: update workflow"

# Ver status
git status

# Add archivos
git add .
git add file.py

# Ver diff
git diff
git diff --staged

# Ver historial
git log
git log --oneline
git log --graph
```

### Branches

```bash
# Crear branch
git checkout -b feature/new-feature

# Cambiar branch
git checkout main

# Listar branches
git branch
git branch -a

# Eliminar branch
git branch -d feature/old-feature
git branch -D feature/force-delete

# Merge branch
git merge feature/new-feature

# Rebase
git rebase main
```

### Remote

```bash
# Ver remotes
git remote -v

# Fetch cambios
git fetch origin

# Pull cambios
git pull origin main

# Push cambios
git push origin main

# Push new branch
git push -u origin feature/new-branch

# Pull con rebase
git pull --rebase origin main
```

### Stash

```bash
# Guardar cambios temporalmente
git stash

# Guardar con mensaje
git stash save "work in progress"

# Listar stashes
git stash list

# Aplicar último stash
git stash pop

# Aplicar stash específico
git stash apply stash@{1}

# Eliminar stash
git stash drop stash@{0}
```

---

## System

### PowerShell

```powershell
# Ver puertos en uso
netstat -ano | findstr :3000

# Matar proceso por PID
taskkill /F /PID 12345

# Ver procesos
Get-Process | Where-Object {$_.Name -like "*docker*"}

# Ver variables de entorno
$env:PATH

# Establecer variable de entorno
$env:MY_VAR = "value"

# Ver versión de PowerShell
$PSVersionTable

# Ejecutar como administrador
Start-Process powershell -Verb RunAs

# Ver uso de disco
Get-PSDrive

# Crear directorio
New-Item -ItemType Directory -Path "C:\path\to\dir"

# Copiar archivos
Copy-Item -Path "source" -Destination "dest" -Recurse

# Eliminar archivos
Remove-Item -Path "file.txt"
Remove-Item -Path "dir" -Recurse -Force
```

### Networking

```powershell
# Test conexión
Test-NetConnection localhost -Port 3000

# Ver configuración de red
ipconfig /all

# Flush DNS
ipconfig /flushdns

# Ping
ping localhost
ping google.com

# Traceroute
tracert google.com

# Ver tabla de routing
route print
```

### Performance

```powershell
# Ver uso de CPU y memoria
Get-Process | Sort-Object CPU -Descending | Select-Object -First 10

# Ver uso de disco
Get-Volume

# Ver servicios corriendo
Get-Service | Where-Object {$_.Status -eq "Running"}

# Task Manager desde CLI
taskmgr

# Resource Monitor
resmon
```

---

## Shortcuts y Aliases

### Crear Aliases en PowerShell

Agregar a `$PROFILE`:

```powershell
# Editar profile
notepad $PROFILE

# Agregar aliases:
function dps { docker compose ps }
function dup { docker compose up -d }
function ddown { docker compose down }
function dlogs { docker compose logs -f $args }
function dexec { docker compose exec $args }

function be { cd C:\Users\yo\SADOCKDOG\autogpt_platform\backend }
function fe { cd C:\Users\yo\SADOCKDOG\autogpt_platform\frontend }
function run { cd C:\Users\yo\SADOCKDOG\RUN }

function gst { git status }
function gco { git checkout $args }
function glog { git log --oneline --graph }
```

### Reload Profile

```powershell
. $PROFILE
```

---

*Última actualización: 2025-01-06*
