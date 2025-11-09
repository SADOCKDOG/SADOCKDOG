# Escaneo de Dependencias - CVE Detection

## Resumen

Workflow automatizado que escanea dependencias en busca de vulnerabilidades conocidas (CVEs):
- **Backend**: `pip-audit` para paquetes Python
- **Frontend**: `osv-scanner` para dependencias npm/pnpm
- **Frecuencia**: Diariamente + cada push a lockfiles

## Herramientas utilizadas

### pip-audit (Python)
- Mantiene by PyPA (Python Packaging Authority)
- Base de datos: PyPI Advisory Database + OSV
- Detecta: CVEs en paquetes Python instalados
- Formato: JSON, CycloneDX SBOM

### osv-scanner (npm/pnpm)
- Mantenido por Google (Open Source Vulnerabilities)
- Base de datos: OSV.dev (agregador multi-ecosistema)
- Detecta: CVEs en npm/yarn/pnpm lockfiles
- Formato: SARIF (integración nativa con GitHub Code Scanning)

## Qué se escanea

```
autogpt_platform/
├── backend/poetry.lock          → pip-audit
├── autogpt_libs/poetry.lock     → pip-audit
└── frontend/pnpm-lock.yaml      → osv-scanner

classic/
├── original_autogpt/poetry.lock → (futuro)
├── forge/poetry.lock            → (futuro)
└── benchmark/poetry.lock        → (futuro)
```

## Cómo revisar vulnerabilidades

### En GitHub
1. Ir a **Security > Code scanning alerts**
2. Filtrar por categoría `osv-scanner-frontend` o buscar por `pip-audit`
3. Cada alerta muestra:
   - Paquete afectado
   - Versión vulnerable
   - CVE ID y severidad (CRITICAL, HIGH, MEDIUM, LOW)
   - Versión segura recomendada
   - Descripción del problema

### En workflow artifacts
1. Ir a **Actions > Security - Dependency Scanning**
2. Última ejecución > **Artifacts**
3. Descargar:
   - `pip-audit-backend-results` (JSON)
   - `pip-audit-libs-results` (JSON)
   - `osv-scanner-frontend-results` (JSON)

### Localmente

**Backend (pip-audit)**:
```bash
cd autogpt_platform/backend
poetry run pip install pip-audit
poetry run pip-audit --desc
```

**Frontend (osv-scanner)**:
```bash
cd autogpt_platform/frontend

# Instalar osv-scanner
curl -sSL https://github.com/google/osv-scanner/releases/download/v1.8.5/osv-scanner_1.8.5_linux_amd64 -o osv-scanner
chmod +x osv-scanner

# Escanear
./osv-scanner scan --lockfile pnpm-lock.yaml
```

**Windows (osv-scanner)**:
```powershell
# Descargar desde GitHub Releases
Invoke-WebRequest -Uri "https://github.com/google/osv-scanner/releases/download/v1.8.5/osv-scanner_1.8.5_windows_amd64.exe" -OutFile "osv-scanner.exe"

# Escanear
.\osv-scanner.exe scan --lockfile pnpm-lock.yaml
```

## Resolución de vulnerabilidades

### Priorización
1. **CRITICAL**: Reparar inmediatamente (RCE, inyección SQL, etc.)
2. **HIGH**: Reparar en < 7 días (XSS, autenticación, etc.)
3. **MEDIUM**: Reparar en sprint actual/siguiente
4. **LOW**: Evaluar si afecta a funcionalidad usada

### Proceso de actualización

**Backend (Poetry)**:
```bash
cd autogpt_platform/backend

# Ver paquetes desactualizados
poetry show --outdated

# Actualizar paquete específico
poetry update <package-name>

# O actualizar todo (con cuidado)
poetry update

# Re-escanear
poetry run pip-audit
```

**Frontend (pnpm)**:
```bash
cd autogpt_platform/frontend

# Ver paquetes desactualizados
pnpm outdated

# Actualizar paquete específico
pnpm update <package-name>

# O actualizar todo interactivo
pnpm update -i

# Re-escanear
osv-scanner scan --lockfile pnpm-lock.yaml
```

### Si no hay parche disponible

1. **Verificar explotabilidad**: ¿Afecta a código que usamos?
2. **Mitigación temporal**:
   - Desactivar funcionalidad afectada si es posible
   - Restricciones a nivel de red (firewall, WAF)
   - Monitoreo intensivo de intentos de explotación
3. **Alternativas**:
   - Buscar fork mantenido del paquete
   - Reemplazar con biblioteca alternativa
   - Vendor el paquete y patchear localmente (último recurso)
4. **Documentar decisión** en `SECURITY.md` o issue tracker

### Dependencias transitivas

Si la vulnerabilidad está en dependencia transitiva (no directa):

```bash
# Backend: ver árbol de dependencias
poetry show --tree <vulnerable-package>

# Forzar versión segura en pyproject.toml
[tool.poetry.dependencies]
vulnerable-package = ">=1.2.3"  # versión segura

# Frontend: ver árbol
pnpm why <vulnerable-package>

# Forzar versión en package.json
{
  "pnpm": {
    "overrides": {
      "vulnerable-package": ">=1.2.3"
    }
  }
}
```

## Falsos positivos

### Criterios para ignorar
- ✅ CVE afecta a funcionalidad que NO usamos (ej: plugin de Django que no habilitamos)
- ✅ CVE ya mitigado por otra capa (ej: XSS en backend API-only)
- ✅ CVE en dependencia de desarrollo (pytest, storybook) sin impacto en producción
- ❌ "No tenemos tiempo para arreglarlo" (NO es válido para CRITICAL/HIGH)

### Documentar excepciones

Crear issue explicando:
- CVE ID y severidad
- Por qué no aplica (análisis técnico)
- Fecha de revisión
- Cuándo re-evaluar (ej: próximo sprint, próximo release)

## Integración con CI/CD

### Bloqueo de merge

Actualmente el workflow **NO bloquea** PRs automáticamente. Para activar fail mode:

```yaml
# En .github/workflows/security-dependencies.yml
jobs:
  scan-python-backend:
    steps:
      - name: Run pip-audit on backend
        run: |
          poetry run pip-audit --desc  # Sin || true
```

**Recomendación**: Esperar 2-4 semanas con modo report-only para establecer baseline antes de activar bloqueo.

### Scheduled scans

Workflow ejecuta diariamente (6 AM UTC) para detectar:
- CVEs nuevos publicados
- Actualizaciones de bases de datos de vulnerabilidades
- Dependencias que pasaron de LOW a HIGH severidad

## Indicadores de éxito

- **CVE discovery time**: < 24 horas desde publicación
- **CRITICAL CVE resolution**: < 48 horas
- **HIGH CVE resolution**: < 7 días
- **False positive rate**: < 10% de alertas
- **Dependency freshness**: Paquetes desactualizados < 6 meses

## Roadmap

- [ ] **Fase 1** (actual): Escaneo diario, modo report-only
- [ ] **Fase 2**: Activar fail mode para CRITICAL vulnerabilities
- [ ] **Fase 3**: Integrar con Dependabot para auto-PRs
- [ ] **Fase 4**: SBOM completo con Syft (PR 5)
- [ ] **Fase 5**: Policy-as-code con OPA (rechazar paquetes sin licencia OSS aprobada)

## FAQ

**¿Por qué pip-audit y no Safety/Snyk?**  
pip-audit es oficial de PyPA, gratuito, y tiene buena cobertura. Safety es de pago para CI. Snyk puede añadirse más adelante.

**¿osv-scanner vs npm audit?**  
OSV agrega múltiples fuentes (npm, GitHub, NVD) y genera SARIF nativo. npm audit solo ve npm registry.

**¿Escanean código propio o solo dependencias?**  
Solo dependencias (third-party). Para código propio ver CodeQL/Semgrep (futura PR).

**¿Qué pasa con Classic AutoGPT?**  
Por ahora solo autogpt_platform. Classic puede añadirse extendiendo el workflow.

**¿Hay alertas de severidad UNKNOWN?**  
Sí, osv-scanner reporta UNKNOWN cuando no puede determinar severidad. Tratar como MEDIUM hasta investigar.

## Referencias

- [pip-audit docs](https://github.com/pypa/pip-audit)
- [OSV.dev database](https://osv.dev/)
- [osv-scanner GitHub](https://github.com/google/osv-scanner)
- [GitHub Code Scanning](https://docs.github.com/en/code-security/code-scanning)
