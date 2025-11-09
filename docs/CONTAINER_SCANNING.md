# Escaneo de Contenedores (Trivy + Syft)

## Objetivo
Detectar vulnerabilidades (CVEs) y generar inventario (SBOM) de las imágenes Docker del monorepo:
- Backend (`autogpt_platform/backend/Dockerfile`)
- Frontend (`autogpt_platform/frontend/Dockerfile`)
- Classic (`classic/Dockerfile.autogpt`)

## Herramientas

### Trivy
- Escanea paquetes del sistema (APK/apt), dependencias de aplicación y configuración (exposed secrets, permisos, etc.)
- Soporta salida SARIF (integración con GitHub Code Scanning)
- Filtrado de severidad configurado: HIGH, CRITICAL (baseline inicial)

### Syft
- Genera SBOM (Software Bill of Materials) en formato CycloneDX JSON
- Inventario completo de componentes para auditoría y cumplimiento

## Workflow
Archivo: `.github/workflows/security-containers.yml`

Acciones:
1. Construye cada imagen con `docker build`
2. Ejecuta Trivy → SARIF + reporte tabla
3. Ejecuta Syft → SBOM CycloneDX JSON
4. Sube SARIF a Code Scanning y artefactos a Actions
5. Resume resultados en GitHub Step Summary

## Uso local

### Requisitos
- Docker instalado
- Trivy y Syft (instalación rápida abajo)

### Instalar Trivy
```bash
# Linux
sudo apt-get update -y
sudo apt-get install -y wget
wget -qO - https://aquasecurity.github.io/trivy-repo/debian/public.key | sudo apt-key add -
echo deb https://aquasecurity.github.io/trivy-repo/debian stable main | sudo tee -a /etc/apt/sources.list.d/trivy.list
sudo apt-get update -y
sudo apt-get install -y trivy

# macOS (Homebrew)
brew install trivy
```

### Instalar Syft
```bash
curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin
```

### Escanear backend
```bash
docker build -f autogpt_platform/backend/Dockerfile autogpt_platform/backend -t autogpt-backend:local
trivy image --severity HIGH,CRITICAL autogpt-backend:local
syft autogpt-backend:local -o cyclonedx-json > sbom-backend.json
```

### Escanear frontend
```bash
docker build -f autogpt_platform/frontend/Dockerfile autogpt_platform/frontend -t autogpt-frontend:local
trivy image --severity HIGH,CRITICAL autogpt-frontend:local
syft autogpt-frontend:local -o cyclonedx-json > sbom-frontend.json
```

### Escanear classic
```bash
docker build -f classic/Dockerfile.autogpt classic -t autogpt-classic:local
trivy image --severity HIGH,CRITICAL autogpt-classic:local
syft autogpt-classic:local -o cyclonedx-json > sbom-classic.json
```

## Interpretar resultados

### Trivy
- CRITICAL: Vulnerabilidades explotables de impacto mayor (RCE, escalada de privilegios)
- HIGH: Serias, deben planificarse correcciones pronto
- MEDIUM/LOW: No incluidas en baseline, se pueden habilitar más adelante

### Syft (SBOM)
- Útil para: Cumplimiento, comparación entre versiones, auditorías post-incidente
- Se recomienda almacenar SBOM de releases en artefactos o bucket seguro

## Remediación

1. Actualizar paquetes base (apt/apk) → reconstruir imagen
2. Ajustar versión de dependencias en `poetry.lock` / `pnpm-lock.yaml`
3. Usar imágenes base más recientes (ej: `python:3.11-slim` en lugar de `python:3.11`)
4. Multi-stage build para reducir superficie
5. Quitar herramientas innecesarias (curl, wget) tras instalación

## Ejemplo de mejora
```dockerfile
# ❌ Imagen base grande
FROM python:3.11

# ✅ Imagen base reducida
FROM python:3.11-slim
```

## Roadmap de endurecimiento
- Fase 1 (actual): Escaneo HIGH/CRITICAL diario
- Fase 2: Añadir configuración (misconfig) + SECRET scan en imágenes
- Fase 3: Firmado de imágenes (cosign) + verificación en deploy
- Fase 4: Política de SBOM (rechazar componentes sin licencia válida)

## Integración futura
- Combine con dependencia scanning para correlación (paquete vulnerable → imagen afectada)
- Integración con alerta Slack cuando CRITICAL > 0

## Indicadores de éxito
- 0 vulnerabilidades CRITICAL abiertas > 48h
- Tiempo medio de parche HIGH < 7 días
- SBOM generado para cada release tag

## FAQ
**¿Por qué solo HIGH y CRITICAL ahora?** Para reducir ruido inicial y enfocar remediación prioritaria.

**¿Qué pasa con vulnerabilidades LOW?** Se incluirán tras estabilizar pipeline.

**¿Necesito Syft siempre?** Sí para releases; en desarrollo puede ejecutarse bajo demanda.

**¿Esto reemplaza escaneo de dependencias?** No; lo complementa con capa OS + empaquetado.

**¿Podemos fallar el build si hay CRITICAL?** Se puede activar quitando `|| true` y agregando política tras baseline estable.
