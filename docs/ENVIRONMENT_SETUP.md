# Configuración de entorno (local)

Esta guía explica cómo configurar variables de entorno para el stack de AutoGPT Platform en local.

## 1) Archivos de entorno

- `autogpt_platform/.env.example` → copia a `autogpt_platform/.env` y rellena placeholders.
- `autogpt_platform/backend/.env.example` → copia a `autogpt_platform/backend/.env`.
- `autogpt_platform/frontend/.env.example` → copia a `autogpt_platform/frontend/.env`.

Si usas Docker Compose local, los `.env.default` ya traen valores de demo. Aun así, personaliza secretos básicos.

## 2) Secretos mínimos a ajustar

- Base de datos: `POSTGRES_PASSWORD`
- JWT: `JWT_SECRET` (y `JWT_VERIFY_KEY` en backend)
- Claves Fernet: `ENCRYPTION_KEY`
- GitHub OAuth: `GITHUB_CLIENT_ID`, `GITHUB_CLIENT_SECRET` y URLs (127.0.0.1)

## 3) Generar claves

- Fernet (Python 3):
```python
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
```

- JWT (32+ chars):
```
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

## 4) URLs recomendadas (local)

- Frontend: `http://127.0.0.1:3000`
- Supabase/Kong: `http://127.0.0.1:8000`
- Backend API: `http://127.0.0.1:8006/api`
- Websocket: `ws://127.0.0.1:8001/ws`

## 5) GitHub OAuth (GoTrue y backend)

- App OAuth (GitHub): Homepage `http://127.0.0.1:3000`, Callback `http://127.0.0.1:3000/auth/callback`.
- GoTrue redirect: `http://127.0.0.1:8000/auth/v1/callback`.
- Allow list: `GOTRUE_URI_ALLOW_LIST=http://127.0.0.1:3000/*,http://127.0.0.1:8000/*`.

## 6) Puesta en marcha (resumen)

1. Inicia dependencias:
```
docker compose -f autogpt_platform/docker-compose.yml --profile local up deps -d
```
2. Backend (poetry):
```
cd autogpt_platform/backend
poetry install
poetry run prisma migrate dev
poetry run prisma generate
poetry run serve
```
3. Frontend (pnpm):
```
cd autogpt_platform/frontend
pnpm install
pnpm dev
```

## 7) Seguridad y escaneo

- Este repo incluye Gitleaks en modo reporte.
- No subas secretos reales; usa `.env` locales (ignorados por git) y revisa los reportes en Security > Code scanning.
