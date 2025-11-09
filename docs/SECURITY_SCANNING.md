# Seguridad: Escaneos de secretos con Gitleaks

Este repositorio incluye un flujo de trabajo de GitHub Actions para ejecutar **Gitleaks** en modo de reporte (no falla el build) sobre `push` y `pull_request`.

## ¿Qué hace?
- Detecta posibles secretos expuestos en el código o en la historia git.
- Genera un reporte en formato **SARIF** y lo sube a GitHub Security.
- Publica artefactos con los reportes para su descarga.

## Archivos relevantes
- `.github/workflows/security-gitleaks.yml`: workflow CI que ejecuta Gitleaks.
- `.gitleaks.toml`: configuración base con una allowlist para claves de demo/local.
- `scripts/run_gitleaks.ps1`: script opcional para ejecución local (modo reporte).

## Ejecución local (Windows PowerShell)

```pwsh
# Desde la raíz del repo
pwsh ./scripts/run_gitleaks.ps1 -Config .gitleaks.toml
```

> Nota: El script descarga la última versión de Gitleaks y deja los reportes en `gitleaks.sarif`.

## Buenas prácticas
- Nunca subas claves reales. Usa variables de entorno y `.env` en local.
- Si un secreto real se filtra, **revoca y rota** ese secreto inmediatamente.
- Usa la allowlist con cuidado; manténla al mínimo para evitar ocultar issues reales.
