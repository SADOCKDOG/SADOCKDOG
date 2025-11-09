# 🚀 Guía Avanzada de @workspace en GitHub Copilot

## 📋 Índice

1. [Comandos Básicos](#comandos-básicos)
2. [Comandos Slash](#comandos-slash)
3. [Participantes](#participantes)
4. [Consultas Avanzadas](#consultas-avanzadas)
5. [Casos de Uso Específicos](#casos-de-uso-específicos)
6. [Atajos de Teclado](#atajos-de-teclado)
7. [Tips y Trucos](#tips-y-trucos)

---

## 🎯 Comandos Básicos

### Análisis General
```
@workspace Dame un resumen del estado del proyecto
@workspace ¿Cuál es la estructura del proyecto?
@workspace Explica la arquitectura general
```

### Estado de la Infraestructura
```
@workspace ¿Qué servicios están corriendo?
@workspace Verifica el estado de los contenedores Docker
@workspace ¿Cuál es el estado de las bases de datos?
```

### Análisis de Código
```
@workspace ¿Hay errores o warnings en el código?
@workspace ¿Qué tareas están pendientes? (TODOs y FIXMEs)
@workspace ¿Qué archivos han cambiado recientemente?
```

---

## ⚡ Comandos Slash

### `/tests` - Testing
```
/tests ¿Qué tests fallan?
/tests Ejecuta los tests del backend
/tests Genera tests para el módulo de autenticación
/tests ¿Cuál es la cobertura de tests actual?
```

### `/fix` - Corrección Automática
```
/fix el error en rest_server.py
/fix los problemas de importación
/fix las vulnerabilidades detectadas
/fix el rendimiento de la base de datos
```

### `/explain` - Explicaciones
```
/explain cómo funciona el executor
/explain el flujo de autenticación
/explain la arquitectura del backend
/explain #SADOCKDOGManager.check_service_status
```

### `/new` - Crear Componentes
```
/new endpoint para notificaciones
/new servicio de análisis de logs
/new componente React para dashboard
/new migración de base de datos
```

### `/doc` - Documentación
```
/doc para la API de usuarios
/doc el proceso de deployment
/doc las variables de entorno necesarias
/doc el flujo de trabajo de desarrollo
```

---

## 🎯 Participantes

### `@workspace` - Contexto Completo
```
@workspace ¿Dónde está implementada la lógica de auth?
@workspace Encuentra todos los endpoints relacionados con usuarios
@workspace ¿Qué servicios dependen de RabbitMQ?
```

### `#symbol` - Referencias a Símbolos
```
Explica #SADOCKDOGManager
Refactoriza #check_service_status
¿Dónde se usa #Colors?
Optimiza #project_integration_status
```

### `@filename` - Referencias a Archivos
```
Revisa @docker-compose.yml
Explica @sadockdog_manager.py
¿Qué hace @fix_frontend.py?
Analiza @.env.example
```

### `/terminal` - Comandos de Terminal
```
/terminal docker ps
/terminal docker stats --no-stream
/terminal git status
/terminal npm run build
```

### `@vscode` - Comandos de VS Code
```
@vscode settings para Python
@vscode configuración de ESLint
@vscode extensiones recomendadas
```

---

## 🔥 Consultas Avanzadas

### Optimización y Rendimiento
```
@workspace Analiza el uso de memoria y propón optimizaciones
@workspace ¿Cómo puedo mejorar el rendimiento del backend?
@workspace Identifica cuellos de botella en la aplicación
@workspace Optimiza las consultas a la base de datos
```

### Seguridad
```
@workspace ¿Hay vulnerabilidades en las dependencias?
@workspace Analiza la seguridad del flujo de autenticación
@workspace ¿Qué endpoints no están protegidos?
@workspace Verifica que las contraseñas estén encriptadas
```

### Arquitectura y Diseño
```
@workspace Explica el patrón de arquitectura usado
@workspace ¿Cómo se comunican los microservicios?
@workspace Diagrama de flujo del proceso de login
@workspace ¿Qué servicios son críticos para producción?
```

### DevOps y CI/CD
```
@workspace Crea un script de deployment automatizado
@workspace ¿Qué checks debo hacer antes de producción?
@workspace Genera un Dockerfile optimizado para el backend
@workspace Configura health checks para todos los servicios
```

### Debugging
```
@workspace ¿Por qué falla el servicio rest_server?
@workspace Analiza los logs y encuentra el error
@workspace ¿Qué servicio está causando timeout?
@workspace Debuggea el problema de conexión a la BD
```

### Refactoring
```
@workspace Identifica código duplicado
@workspace Refactoriza el módulo de notificaciones
@workspace Mejora la estructura de carpetas del proyecto
@workspace Aplica principios SOLID al código actual
```

---

## 💼 Casos de Uso Específicos

### 1. Preparación para Producción
```
@workspace Checklist completo para deployment a producción:
1. Verificar todas las variables de entorno
2. Validar configuración de seguridad
3. Revisar logs y errores
4. Confirmar backups configurados
5. Testing completo de endpoints
6. Documentación actualizada
```

### 2. Onboarding de Nuevo Desarrollador
```
@workspace Genera una guía de onboarding para nuevo desarrollador:
1. Requisitos del sistema
2. Pasos de instalación
3. Arquitectura del proyecto
4. Flujo de trabajo de desarrollo
5. Convenciones de código
6. Testing y deployment
```

### 3. Análisis de Impacto
```
@workspace Si modifico el servicio de autenticación:
1. ¿Qué otros servicios se verán afectados?
2. ¿Qué tests debo actualizar?
3. ¿Qué documentación debo modificar?
4. ¿Hay riesgos de compatibilidad?
```

### 4. Migración de Versiones
```
@workspace Plan de migración de Python 3.10 a 3.13:
1. Compatibilidad de dependencias
2. Cambios necesarios en el código
3. Tests de regresión
4. Rollback plan
5. Timeline estimado
```

### 5. Monitoreo y Alertas
```
@workspace Crea un sistema de monitoreo que incluya:
1. Health checks de todos los servicios
2. Métricas de rendimiento (CPU, RAM, Disco)
3. Alertas para errores críticos
4. Dashboard de visualización
5. Logs centralizados
```

### 6. Análisis de Dependencias
```
@workspace Analiza las dependencias del proyecto:
1. Lista todas las dependencias
2. Identifica versiones desactualizadas
3. Detecta vulnerabilidades conocidas
4. Propón actualizaciones compatibles
5. Genera reporte de riesgos
```

---

## ⌨️ Atajos de Teclado

| Atajo | Función | Uso |
|-------|---------|-----|
| `Ctrl+Shift+I` | Abrir/Cerrar Copilot Chat | Principal |
| `Ctrl+I` | Inline Chat (editar código) | Edición rápida |
| `Alt+\` | Activar sugerencias Copilot | Autocompletado |
| `Alt+]` | Siguiente sugerencia | Navegación |
| `Alt+[` | Sugerencia anterior | Navegación |
| `Ctrl+Enter` | Aceptar sugerencia | Aplicar |
| `Tab` | Aceptar palabra por palabra | Precisión |
| `Esc` | Cerrar sugerencias | Cancelar |
| `Ctrl+Shift+P` | Command Palette | Comandos |

---

## 💡 Tips y Trucos

### 1. Contexto Específico
Usa referencias múltiples para mejor contexto:
```
@workspace Basándote en @docker-compose.yml y @.env.example,
verifica si todos los servicios tienen sus variables configuradas
```

### 2. Preguntas Encadenadas
Haz seguimiento a respuestas previas:
```
# Primera pregunta
@workspace ¿Qué servicios usan PostgreSQL?

# Seguimiento
¿Cuáles de esos servicios tienen índices optimizados?

# Profundización
Genera índices para mejorar el rendimiento
```

### 3. Combinación de Comandos
```
@workspace /new test para verificar la integración entre
rest_server y database_manager usando #check_service_status
```

### 4. Exportar Resultados
```
@workspace Genera un reporte completo del estado del proyecto
y guárdalo en RUN/reports/project_status_YYYYMMDD.md
```

### 5. Análisis Comparativo
```
@workspace Compara las configuraciones de desarrollo vs producción
en @docker-compose.yml y @docker-compose.prod.yml
```

### 6. Validaciones Pre-commit
```
@workspace Antes de hacer commit, verifica:
1. Todos los tests pasan
2. No hay errores de linting
3. Documentación actualizada
4. No hay TODOs críticos pendientes
```

### 7. Búsqueda Semántica
```
@workspace Encuentra todos los lugares donde se maneja
autenticación de usuarios, incluyendo middlewares y decoradores
```

### 8. Generación de Código
```
@workspace Genera un endpoint FastAPI completo para gestionar
notificaciones, incluyendo:
- CRUD operations
- Validación con Pydantic
- Documentación OpenAPI
- Tests unitarios
```

---

## 🎓 Comandos por Rol

### Para DevOps
```
@workspace Estado de infraestructura completa
@workspace Optimiza docker-compose para producción
@workspace Crea script de backup automatizado
@workspace Configura monitoring con Prometheus
```

### Para Backend Developers
```
@workspace Explica la arquitectura del backend
@workspace Optimiza las queries SQL lentas
@workspace Implementa cache con Redis
@workspace Refactoriza el módulo de autenticación
```

### Para Frontend Developers
```
@workspace Estructura del proyecto Next.js
@workspace Componentes React disponibles
@workspace Integración con la API del backend
@workspace Optimiza el bundle size
```

### Para QA/Testing
```
@workspace Genera plan de testing completo
@workspace ¿Qué módulos no tienen tests?
@workspace Ejecuta todos los tests y reporta fallos
@workspace Crea tests E2E con Playwright
```

### Para Project Managers
```
@workspace Resumen ejecutivo del proyecto
@workspace Estado de todas las funcionalidades
@workspace Estimación de tiempo para [feature]
@workspace Riesgos técnicos identificados
```

---

## 📚 Recursos Adicionales

### Documentación Oficial
- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [VS Code Copilot Guide](https://code.visualstudio.com/docs/copilot/overview)

### Mejores Prácticas
- Sé específico en tus preguntas
- Proporciona contexto cuando sea necesario
- Usa referencias a archivos y símbolos
- Divide tareas grandes en pasos pequeños
- Verifica las sugerencias antes de aplicarlas

### Limitaciones
- No puede ejecutar código directamente (usa `/terminal` para eso)
- No tiene acceso a internet en tiempo real
- Conocimiento limitado a su fecha de entrenamiento
- Puede requerir múltiples iteraciones para tareas complejas

---

## 🔄 Actualizaciones

**Última actualización:** 2025-11-09

Para más información o sugerencias, consulta la documentación del proyecto.

---

**🎯 Recuerda:** @workspace es tu asistente inteligente. Cuanto más específico seas en tus preguntas, mejores respuestas obtendrás.
