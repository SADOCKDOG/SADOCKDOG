# Hooks Pre-commit para Gitleaks

## Instalación rápida

1. **Instalar pre-commit** (una vez por sistema):
   ```bash
   pip install pre-commit
   ```

2. **Instalar Gitleaks binary** (si no está instalado):
   - **Windows**: Usar `scripts/run_gitleaks.ps1` (auto-instala)
   - **Linux/Mac**: 
     ```bash
     # Linux
     wget https://github.com/gitleaks/gitleaks/releases/download/v8.19.3/gitleaks_8.19.3_linux_x64.tar.gz
     tar -xzf gitleaks_8.19.3_linux_x64.tar.gz
     sudo mv gitleaks /usr/local/bin/
     
     # macOS
     brew install gitleaks
     ```

3. **Activar hooks en el repo**:
   ```bash
   cd /path/to/SADOCKDOG
   pre-commit install           # Hook pre-commit
   pre-commit install --hook-type pre-push  # Hook pre-push
   ```

4. **Verificar instalación**:
   ```bash
   pre-commit run --all-files
   ```

## Uso diario

### Automático (recomendado)
Los hooks se ejecutan automáticamente:
- **Pre-commit**: Escanea archivos staged antes de cada commit
- **Pre-push**: Escanea historial completo antes de cada push

### Manual
```bash
# Ejecutar todos los hooks manualmente
pre-commit run --all-files

# Solo Gitleaks
pre-commit run gitleaks --all-files

# Solo en archivos staged
pre-commit run gitleaks

# Saltarse hooks (¡usar con precaución!)
SKIP=gitleaks git commit -m "WIP: temp code"
```

## Qué hace cada hook

### Hook pre-commit (rápido)
- Escanea **solo archivos staged** (`git add`)
- Detecta secretos antes de crear el commit
- Bloquea commit si encuentra secretos reales
- ~1-3 segundos en commits normales

### Hook pre-push (completo)
- Escanea **todo el historial local**
- Última línea de defensa antes de enviar a remoto
- Más lento pero más exhaustivo (~10-30 segundos)

## Resolución de problemas

### "gitleaks: command not found"
```bash
# Verificar instalación
which gitleaks  # Linux/Mac
where.exe gitleaks  # Windows

# Reinstalar si es necesario (ver paso 2 arriba)
```

### Hook bloqueó commit con falso positivo
```bash
# Opción 1: Añadir inline exception
echo 'API_KEY="demo-key"  # gitleaks:allow' > file.py

# Opción 2: Mejorar placeholder
# Cambiar: API_KEY="abc123"
# Por:     API_KEY="REPLACE_WITH_YOUR_KEY"

# Opción 3: Saltarse solo este commit (NO recomendado)
SKIP=gitleaks git commit -m "fix: update config"
```

### Desactivar hooks temporalmente
```bash
# Desinstalar (reversible)
pre-commit uninstall
pre-commit uninstall --hook-type pre-push

# Reinstalar después
pre-commit install
pre-commit install --hook-type pre-push
```

### Actualizar hooks a última versión
```bash
pre-commit autoupdate
pre-commit run --all-files  # Verificar que funciona
```

## Integración con CI/CD

El workflow `.github/workflows/security-precommit-hooks.yml` valida:
- Sintaxis de `.pre-commit-config.yaml`
- Instalación correcta de hooks
- Detección funcional de secretos

Si el CI falla pero los hooks locales pasan, ejecutar:
```bash
pre-commit clean
pre-commit install --install-hooks
pre-commit run --all-files
```

## FAQ

**¿Debo instalar esto?**  
Sí, especialmente si trabajas con secrets o API keys. Es la mejor defensa local.

**¿Ralentiza mucho el desarrollo?**  
No. Pre-commit hook < 3s. Pre-push ~10-30s (solo en push).

**¿Qué pasa si no tengo hooks y hago push con secreto?**  
El workflow de GitHub Actions lo detectará y bloqueará el PR (pero ya está en historial remoto).

**¿Puedo usar otros hooks además de Gitleaks?**  
Sí. Ver `.pre-commit-config.yaml` para hooks de linting, formateo, etc.

**¿Funciona en Windows?**  
Sí, pero necesitas instalar Gitleaks binary primero (usar `scripts/run_gitleaks.ps1`).

## Próximos pasos

Tras instalar hooks locales:
1. Ejecutar `pre-commit run --all-files` para verificar estado actual
2. Resolver hallazgos existentes (si hay)
3. Configurar editores para auto-formateo (opcional)
4. Compartir esta guía con el equipo

Ver `docs/SECURITY_SCANNING.md` para más información sobre Gitleaks y gestión de hallazgos.
