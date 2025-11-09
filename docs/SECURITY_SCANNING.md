# Seguridad: Escaneo de secretos

Este documento describe el escaneo de secretos con **Gitleaks** en modo bloqueante.

## Estado actual (PR 2)

- ✅ Workflow activo en push, PR y semanalmente
- ✅ Generación de reportes SARIF en Security > Code Scanning
- ✅ **Modo fail activo**: PRs con secretos detectados NO se pueden mergear
- ✅ Allowlist ajustada para `.env.example`, docs y snapshots de tests
- ✅ Script local para Windows (`scripts/run_gitleaks.ps1`)

## Archivos de configuración

- `.github/workflows/security-gitleaks.yml` – Workflow con fail mode
- `.gitleaks.toml` – Configuración endurecida con allowlist específica
- `scripts/run_gitleaks.ps1` – Ejecución local (auto-instalación binario)
- `docs/SECURITY_SCANNING.md` – Este documento

## Cómo funciona

1. **Detección**: Gitleaks escanea commits buscando patrones de secretos (API keys, tokens, passwords)
2. **Allowlist**: Excepciones explícitas para plantillas (`.env.example`) y docs
3. **Fallo**: Si detecta secreto real → workflow falla → bloquea merge
4. **SARIF**: Genera reporte visible en Security > Code scanning alerts

## Próximas mejoras previstas

1. ✅ ~~Endurecer reglas~~ (Completado en PR 2)
2. ✅ ~~Activar fail mode~~ (Completado en PR 2)
3. ✅ ~~Hook pre-push local~~ (Completado en PR 3) - Ver `docs/PRECOMMIT_HOOKS.md`
4. Baseline formal si aparecen falsos positivos inevitables
5. Notificaciones automáticas (comentario en PR con resumen de hallazgos)

## Uso local

Escanear el árbol de trabajo:

```powershell
pwsh ./scripts/run_gitleaks.ps1
```

Solo cambios staged (antes de commit):

```powershell
pwsh ./scripts/run_gitleaks.ps1 -Staged
```

Historial completo (más lento):

```powershell
pwsh ./scripts/run_gitleaks.ps1 -History -Format json
```

## Gestión de hallazgos

### Si Gitleaks detecta un secreto

1. **Ver reporte**: Security > Code scanning alerts > categoría `gitleaks`
2. **Confirmar naturaleza**:
   - ¿Es un secreto real? → Rotar inmediatamente
   - ¿Es falso positivo? → Ver sección "Falsos positivos"

3. **Si es secreto real**:
   - **Paso 1**: Rotar la credencial en su sistema origen (OpenAI, GitHub, AWS, etc.)
   - **Paso 2**: Invalidar la clave expuesta (revocar en dashboard del proveedor)
   - **Paso 3**: Actualizar `.env` local y variables de CI/CD
   - **Paso 4**: Forzar nuevo commit sin el secreto
   - **Opcional**: Reescribir historial (`git filter-repo`) solo si política interna lo exige

4. **Si es falso positivo**:
   - Ver sección "Falsos positivos" abajo

### Falsos positivos

**Criterios para allowlist**:
- ✅ Placeholder explícito (`REPLACE_ME`, `your-api-key`, etc.)
- ✅ Valor de ejemplo en documentación
- ✅ Demo key pública (Supabase self-hosted, etc.)
- ❌ Secreto real aunque esté en archivo de test

**Opciones en orden de preferencia**:

1. **Inline exception** (preferido para casos puntuales):
   ```bash
   API_KEY=demo-key-for-testing # gitleaks:allow
   ```

2. **Mejorar placeholder**:
   ```bash
   # ❌ Antes (puede alertar)
   API_KEY=abc123def456
   
   # ✅ Después (más claro)
   API_KEY=REPLACE_WITH_YOUR_REAL_API_KEY
   ```

3. **Añadir a allowlist** (último recurso, requiere justificación):
   - Editar `.gitleaks.toml`
   - Añadir regex específico (no demasiado amplio)
   - Comentar por qué es necesario
   - Abrir PR separado para revisión

## Buenas prácticas preventivas

- Usar variables de entorno y gestores de secretos (no hardcode).
- Evitar pegar outputs de herramientas que contengan tokens.
- Sustituir claves reales en ejemplos por patrones tipo `sk-example...`.
- Revisar diff antes de commit buscando `sk-`, `AKIA`, `-----BEGIN`.

## Indicadores de éxito (fase inicial)

- 0 secretos válidos comprometidos tras habilitar reporte.
- Reducción de falsos positivos < 5 en 2 semanas.
- Tiempo de revisión de alertas < 2 minutos por hallazgo.

## FAQ breve

**¿Por qué modo bloqueante ahora?**  
Fase inicial (PR 1) estableció baseline y ajustó allowlist. PR 2 activa fail para prevenir fugas reales.

**¿Qué pasa si mi PR es bloqueado?**  
1. Revisa el reporte en Security > Code scanning alerts
2. Si es secreto real: rótalo y haz nuevo commit sin él
3. Si es falso positivo: usa inline exception `# gitleaks:allow` con justificación

**¿Puedo hacer merge igualmente?**  
No. El workflow falla intencionalmente. Debes resolver el hallazgo primero.

**¿Cómo evitar que esto pase?**  
- Usa `.env` (gitignored) para secretos locales
- Escanea localmente antes de push: `pwsh ./scripts/run_gitleaks.ps1 -Staged`
- Nunca hagas hardcode de API keys en código

**¿Necesito baseline?**  
Solo si hay secretos históricos ya rotados que no puedes eliminar del historial. Documenta por qué cada uno está permitido.

## Indicadores de éxito

- ✅ 0 secretos válidos comprometidos desde activación
- ✅ < 3 falsos positivos por semana
- ✅ Tiempo de resolución de alertas < 10 minutos
- ✅ 100% de PRs bloqueados por secretos reales resueltos antes de merge

---

## Siguientes capas de seguridad (roadmap)

**PR 3**: Hook pre-commit local
- Gitleaks pre-push automático en `.pre-commit-config.yaml`
- Valida antes de enviar a remoto

**PR 4**: Escaneo de dependencias
- `pip-audit` para backend (detecta CVEs en paquetes Python)
- `osv-scanner` para frontend (pnpm lockfile)
- Reportes SARIF en Code Scanning

**PR 5**: Escaneo de contenedores
- `Trivy` para imágenes Docker (OS + app vulnerabilities)
- `Syft` para generar SBOM (Software Bill of Materials)
- Integración con GitHub Container Registry

Ver `AGENTS.md` y `.github/copilot-instructions.md` para convenciones de commit y PR.
