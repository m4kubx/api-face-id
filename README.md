# Face ID SaaS API

Sistema de reconocimiento facial para empresas, desplegable en Dokploy.

## Arquitectura

```
┌─────────────────────────────────────────────────┐
│                 DOKPLOY                          │
│  ┌───────────────────────────────────────────┐  │
│  │            TRAEFIK (proxy)                 │  │
│  │         SSL automático + dominio           │  │
│  └─────────────────┬─────────────────────────┘  │
│                    │                             │
│  ┌─────────────────▼─────────────────────────┐  │
│  │         CONTENEDORES                       │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐  │  │
│  │  │  API     │ │PostgreSQL│ │  Redis   │  │  │
│  │  │ FastAPI  │ │          │ │          │  │  │
│  │  │ DeepFace │ │          │ │          │  │  │
│  │  └──────────┘ └──────────┘ └──────────┘  │  │
│  └───────────────────────────────────────────┘  │
│                    │                             │
│  ┌─────────────────▼─────────────────────────┐  │
│  │         FRONTEND (Next.js)                 │  │
│  │      Dashboard para clientes               │  │
│  └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

## Stack Tecnológico

- **Backend:** FastAPI + DeepFace + SQLAlchemy
- **Frontend:** Next.js + Tailwind CSS
- **Base de datos:** PostgreSQL + Redis
- **Deploy:** Docker + Dokploy

## Instalación en Dokploy

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/api-face-id.git
cd api-face-id
```

### 2. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env con tus valores
```

### 3. Crear proyecto en Dokploy

1. Ir al dashboard de Dokploy
2. Crear nuevo proyecto: `face-id-saas`
3. Agregar servicio: Docker Compose
4. Conectar repositorio de Git
5. Configurar dominios:
   - `api.tudominio.com` → Puerto 8000
   - `app.tudominio.com` → Puerto 3000

### 4. Variables de entorno en Dokploy

```
SECRET_KEY=tu-clave-secreta-super-larga
DATABASE_URL=postgresql://faceuser:facepass@postgres:5432/facesaas
REDIS_URL=redis://redis:6379
ALLOWED_ORIGINS=https://tudominio.com,https://app.tudominio.com
NEXT_PUBLIC_API_URL=https://api.tudominio.com
```

### 5. Deploy

Dokploy automáticamente construirá y desplegará los contenedores.

## API Endpoints

### Autenticación

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/auth/register` | Registrar usuario |
| POST | `/api/auth/login` | Iniciar sesión |
| GET | `/api/auth/me` | Obtener usuario actual |

### Rostros

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/faces/register` | Registrar rostro |
| GET | `/api/faces/list` | Listar rostros |
| DELETE | `/api/faces/{id}` | Eliminar rostro |

### Verificación

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/verify/identify` | Identificar rostro |
| POST | `/api/verify/compare` | Comparar dos rostros |
| POST | `/api/verify/analyze` | Analizar atributos faciales |

## Documentación API

Una vez desplegado, accede a la documentación Swagger:
- `https://api.tudominio.com/docs`

## Requisitos del VPS

| Componente | Mínimo | Recomendado |
|------------|--------|-------------|
| CPU | 4 cores | 8 cores |
| RAM | 8 GB | 16 GB |
| Storage | 40 GB SSD | 80 GB SSD |
| OS | Ubuntu 22.04 | Ubuntu 22.04 |

## Costos Estimados

| Servicio | Costo Mensual |
|----------|---------------|
| VPS (Hetzner/DigitalOcean) | $45-80 |
| Dominio | $10-15/año |
| **Total** | **~$50-85/mes** |

## Desarrollo Local

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

## License

MIT
