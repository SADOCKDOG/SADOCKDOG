# 🔧 Solución de Problemas del Frontend (Builder)

## 🐛 Problema Identificado

**Error**: "Excepción del lado del cliente al cargar localhost" al acceder a http://localhost:3000/build

**Causas Principales**:
1. ❌ Falta archivo `.env` en el frontend
2. ⚠️ Next.js 15 tiene errores de hidratación React
3. ⚠️ Imágenes faltantes (avatar-placeholder.png)
4. ⚠️ Configuración deprecada de images.domains

---

## ✅ Soluciones Aplicadas

### 1. **Archivo .env Creado**
```bash
Ubicación: C:\Users\yo\SADOCKDOG\autogpt_platform\frontend\.env
```

El archivo `.env` es **CRÍTICO** para que Next.js funcione correctamente. Contiene:
- URLs de Supabase
- URLs de backend (API REST y WebSocket)
- Configuración de entorno local
- Feature flags

**Estado**: ✅ Archivo creado automáticamente

---

### 2. **Rebuild Completo del Frontend**

**Comando ejecutado**:
```bash
docker compose -f C:\Users\yo\SADOCKDOG\autogpt_platform\docker-compose.yml build --no-cache frontend
```

**Por qué es necesario**:
- Limpia caché de compilación de Next.js
- Reinstala dependencias npm
- Regenera API endpoints desde OpenAPI spec
- Recompila componentes React

**Tiempo estimado**: 5-10 minutos

**Estado**: 🔄 En progreso...

---

### 3. **Nuevas Funciones en SADOCKDOG Manager**

Agregadas en `sadockdog_manager.py` → **Opción 8: Acciones Rápidas**:

#### **Opción 1**: 🔧 Fix Frontend (Rápido - 10 segundos)
- Verifica/crea archivo `.env`
- Reinicia servicio frontend
- Verifica conectividad HTTP
- **Usar cuando**: El frontend da errores pero no quieres esperar rebuild

#### **Opción 2**: 🔨 Rebuild Frontend (Completo - 5-10 minutos)
- Rebuild completo sin cache
- Reinstala todas las dependencias
- Recompila todo el código
- **Usar cuando**: Problemas persistentes o después de actualizar código

---

## 📋 Cómo Usar las Soluciones

### **Método 1: Desde SADOCKDOG Manager** (RECOMENDADO)

```bash
cd C:\Users\yo\SADOCKDOG\RUN
python sadockdog_manager.py
```

**Pasos**:
1. Menú principal → Opción `8` (Acciones Rápidas)
2. Seleccionar:
   - `1` para Fix Rápido (prueba esto primero)
   - `2` para Rebuild Completo (si el rápido no funciona)

---

### **Método 2: Script Dedicado fix_frontend.py**

```bash
cd C:\Users\yo\SADOCKDOG\RUN
python fix_frontend.py
```

**Opciones del script**:
1. **Reiniciar frontend** (rápido, ~10 segundos)
2. **Reconstruir frontend** completamente (lento, ~5-10 minutos)
3. **Solo ver logs**

---

### **Método 3: Comandos Manuales**

#### **Fix Rápido**:
```powershell
cd C:\Users\yo\SADOCKDOG\autogpt_platform

# Verificar .env existe
if (-Not (Test-Path "frontend\.env")) {
    Copy-Item "frontend\.env.default" "frontend\.env"
}

# Reiniciar frontend
docker compose restart frontend

# Esperar 5 segundos
Start-Sleep -Seconds 5

# Verificar salud
curl http://localhost:3000
```

#### **Rebuild Completo**:
```powershell
cd C:\Users\yo\SADOCKDOG\autogpt_platform

# Detener frontend
docker compose stop frontend

# Rebuild sin cache
docker compose build --no-cache frontend

# Iniciar frontend
docker compose up -d frontend

# Esperar 10 segundos
Start-Sleep -Seconds 10

# Ver logs
docker compose logs frontend --tail=50
```

---

## 🎯 Verificación Post-Solución

### **1. Verificar que frontend esté corriendo**:
```powershell
docker compose ps frontend
```

**Esperado**: Status = "Up X minutes"

---

### **2. Verificar conectividad HTTP**:
```powershell
curl http://localhost:3000
```

**Esperado**: Respuesta 200 OK

---

### **3. Probar Builder**:
```
http://localhost:3000/build
```

**Esperado**: 
- ✅ Página carga sin errores
- ✅ No hay "excepción del lado del cliente"
- ✅ Canvas del builder visible
- ✅ Bloques disponibles en sidebar

---

### **4. Ver logs en tiempo real**:
```powershell
docker compose logs frontend -f
```

**Buscar**:
- ✅ "Ready in XXXms" (significa que compiló correctamente)
- ❌ NO debe aparecer "Error" o "Failed"

---

## 🔍 Troubleshooting Adicional

### **Problema**: Frontend no responde después de rebuild

**Solución**:
```powershell
# Ver recursos del contenedor
docker stats autogpt_platform-frontend-1 --no-stream

# Si memoria o CPU están al 100%, reiniciar Docker Desktop
Restart-Service docker

# Luego reiniciar frontend
docker compose restart frontend
```

---

### **Problema**: Error "ECONNREFUSED" en el navegador

**Causas**:
1. Backend no está corriendo
2. WebSocket server caído
3. Puerto 3000 bloqueado

**Solución**:
```powershell
# Verificar todos los servicios
docker compose ps

# Si hay alguno "Exited", reiniciar todos
docker compose up -d
```

---

### **Problema**: Error en consola del navegador "Failed to load resource"

**Solución**:
```powershell
# Limpiar cache del navegador:
# Chrome: Ctrl+Shift+Del → Borrar cache
# Firefox: Ctrl+Shift+Del → Borrar cache

# O usar modo incógnito:
# Chrome: Ctrl+Shift+N
# Firefox: Ctrl+Shift+P
```

---

## 📊 Logs Útiles para Diagnóstico

### **Ver logs del frontend**:
```powershell
docker compose logs frontend --tail=100
```

### **Ver logs de backend**:
```powershell
docker compose logs rest_server --tail=50
```

### **Ver logs de WebSocket**:
```powershell
docker compose logs websocket_server --tail=50
```

### **Ver logs de todos los servicios**:
```powershell
docker compose logs --tail=20
```

---

## 🎉 Resultado Esperado

Después de aplicar las soluciones:

✅ **Frontend funcionando**:
- http://localhost:3000 → Home page carga correctamente
- http://localhost:3000/build → Builder sin errores
- Canvas del builder interactivo
- Bloques disponibles y dragueables

✅ **Sin errores en consola del navegador**:
- No hay "Client Exception"
- No hay "Failed to fetch"
- No hay errores de hidratación React

✅ **Servicios sincronizados**:
- Frontend conectado a backend (API REST)
- WebSocket conectado para actualizaciones en tiempo real
- Supabase auth funcionando

---

## 🆘 Si Nada Funciona

### **Último Recurso: Reset Completo**

```powershell
cd C:\Users\yo\SADOCKDOG\autogpt_platform

# 1. Detener todo
docker compose down

# 2. Limpiar volúmenes (⚠️ CUIDADO: Borra datos)
docker compose down -v

# 3. Rebuild todo sin cache
docker compose build --no-cache

# 4. Iniciar todo
docker compose up -d

# 5. Esperar 2 minutos
Start-Sleep -Seconds 120

# 6. Verificar
docker compose ps
```

**⚠️ ADVERTENCIA**: Esto borrará:
- Datos de base de datos local
- Sesiones de usuario
- Agentes creados localmente

---

## 📞 Contacto

Si los problemas persisten:
1. Generar reporte completo: `python generate_report.py`
2. Revisar `TROUBLESHOOTING.md` en docs/
3. Verificar logs completos en logs/

---

**Última actualización**: 2025-11-06
**Versión**: 1.0
**Autor**: SADOCKDOG Manager
