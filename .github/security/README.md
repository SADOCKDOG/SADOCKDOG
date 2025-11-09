# Security Documentation

Esta carpeta contiene la documentación relacionada con seguridad del proyecto SADOCKDOG.

## 📚 Contenido

### [GITHUB_SECRETS.md](./GITHUB_SECRETS.md)
Guía completa de configuración de GitHub Secrets para CI/CD. Incluye:
- Lista de secrets requeridos y opcionales
- Comandos para generar valores seguros
- Proceso de rotación de secrets
- Procedimientos en caso de compromiso
- Configuración por ambiente (dev/staging/production)

### Otros Recursos

- **[SECURITY.md](../SECURITY.md)**: Política de seguridad del proyecto
- **[DEPLOYMENT.md](../DEPLOYMENT.md)**: Guía de despliegue con checklist de seguridad
- **[ARCHITECTURE.md](../ARCHITECTURE.md)**: Arquitectura del sistema incluyendo capas de seguridad

## 🔒 Best Practices

### 1. Gestión de Secrets

```bash
# NUNCA hacer commit de archivos .env
git add .env  # ❌ MAL

# Usar .env.example como plantilla
cp .env.example .env  # ✅ BIEN
# Editar .env con valores reales (este archivo está en .gitignore)
```

### 2. Rotación de Secrets

| Tipo de Secret | Frecuencia | Prioridad |
|----------------|------------|-----------|
| Passwords de usuario | 90 días | Alta |
| API Keys de terceros | 90 días | Alta |
| JWT Secrets | 90 días | Alta |
| Encryption Keys | 180 días | Crítica |
| Database Passwords | 90 días | Crítica |

### 3. Detección de Secrets

```bash
# Ejecutar auditoría de seguridad
python security_audit.py

# Pre-commit hooks (detecta secrets antes de commit)
pip install pre-commit
pre-commit install
pre-commit run detect-secrets --all-files
```

### 4. Respuesta a Incidentes

Si se detecta un secret comprometido:

1. **Inmediato** (< 1 hora):
   - Rotar el secret comprometido
   - Revocar acceso del secret anterior
   - Revisar logs de acceso

2. **Corto plazo** (< 24 horas):
   - Desplegar nueva versión con secret rotado
   - Actualizar servicios dependientes
   - Notificar al equipo

3. **Seguimiento** (< 1 semana):
   - Post-mortem del incidente
   - Mejorar procesos de detección
   - Actualizar documentación

Ver detalles completos en [GITHUB_SECRETS.md](./GITHUB_SECRETS.md#-en-caso-de-compromiso).

## 🛡️ Herramientas de Seguridad

### Análisis Estático
- **CodeQL**: Análisis de vulnerabilidades automático (GitHub Actions)
- **Ruff**: Linter de Python con reglas de seguridad
- **ESLint**: Linter de TypeScript con plugins de seguridad

### Dependencias
- **Dependabot**: Actualizaciones automáticas de dependencias (semanal)
- **poetry audit**: Auditoría de dependencias Python
- **pnpm audit**: Auditoría de dependencias Node.js

### Secrets Detection
- **detect-secrets**: Pre-commit hook para detectar secrets
- **security_audit.py**: Script personalizado de auditoría

### Container Security
- **Trivy** (recomendado): Escaneo de vulnerabilidades en imágenes Docker
- **Snyk** (opcional): Análisis continuo de seguridad

## 📋 Checklist de Seguridad

Antes de despliegue a producción:

- [ ] Todos los secrets en GitHub Secrets (no en código)
- [ ] Variables de entorno configuradas correctamente
- [ ] HTTPS habilitado con certificados válidos
- [ ] CORS configurado restrictivamente
- [ ] Rate limiting implementado
- [ ] Logs de seguridad configurados
- [ ] Backups automatizados configurados
- [ ] Monitoreo de seguridad activo (Sentry, CloudWatch, etc.)
- [ ] Dependabot habilitado y monitoreado
- [ ] CodeQL ejecutándose en CI/CD
- [ ] Pre-commit hooks instalados en repositorio
- [ ] Documentación de seguridad actualizada

Ver checklist completo en [DEPLOYMENT.md](../DEPLOYMENT.md#security-checklist).

## 🚨 Reportar Vulnerabilidades

Si encuentras una vulnerabilidad de seguridad:

1. **NO** abras un issue público
2. Usa [GitHub Security Advisories](https://github.com/SADOCKDOG/SADOCKDOG/security/advisories/new)
3. O envía email a: security@sadockdog.io

Responderemos en máximo 48 horas.

Ver política completa en [SECURITY.md](../SECURITY.md).

## 📞 Contacto

- **Equipo de Seguridad**: security@sadockdog.io
- **Issues Generales**: [GitHub Issues](https://github.com/SADOCKDOG/SADOCKDOG/issues)
- **Discussions**: [GitHub Discussions](https://github.com/SADOCKDOG/SADOCKDOG/discussions)

---

**Última actualización**: 2025-01-XX  
**Versión**: 1.0.0
