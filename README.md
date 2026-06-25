# AI CV Analyzer API

Backend desarrollado con **FastAPI**, **MongoDB**, **Docker** y **Cerebras AI** para analizar automáticamente currículums (CV) utilizando modelos de Inteligencia Artificial.

El sistema compara un CV con una descripción de puesto, calcula un porcentaje de compatibilidad y genera recomendaciones para mejorar el perfil del candidato.

---

# Tecnologías

- FastAPI
- Docker
- Docker Compose
- MongoDB
- PyMongo
- Cerebras Cloud SDK
- Python 3.12

---

# Arquitectura

```
app/
│
├── main.py
│
├── models/
│   └── mongo.py
│
├── prompts/
│   └── cv_prompt.py
│
├── repositories/
│   └── cv_repository.py
│
├── routes/
│   ├── cv_routes.py
│   └── health_routes.py
│
├── schemas/
│   └── cv_schema.py
│
└── services/
    ├── ai_service.py
    └── cv_service.py
```

---

# Características

- Arquitectura por capas.
- Integración con Cerebras AI.
- Prompt Engineering desacoplado.
- Persistencia en MongoDB.
- Historial de análisis.
- Consulta de análisis por ID.
- Validación de respuestas de IA.
- Manejo de errores.
- API documentada automáticamente con Swagger.

---

# Instalación

## Clonar el proyecto

```bash
git clone <url-del-repositorio>
cd backend-cv
```

---

## Variables de entorno

Crear un archivo `.env`

```env
MONGO_URI=mongodb://mongo:27017
MONGO_DB_NAME=cvAnalyzer

CEREBRAS_API_KEY=TU_API_KEY
CEREBRAS_MODEL=gpt-oss-120b
```

---

## Ejecutar con Docker

```bash
docker compose up --build
```

La API estará disponible en

```
http://localhost:8000
```

Swagger

```
http://localhost:8000/docs
```

---

# Endpoints

## Health

### Estado del servidor

```
GET /health
```

Respuesta

```json
{
    "status":"OK"
}
```

---

### Estado de MongoDB

```
GET /health/db
```

---

### Estado de Cerebras

```
GET /health/ai
```

---

### Modelos disponibles

```
GET /health/ai/models
```

---

## CV Analysis

### Analizar CV

```
POST /api/cv/analyze
```

Request

```json
{
    "cv_text":"Python FastAPI Docker MongoDB",
    "job_description":"Backend Developer con Python y AWS"
}
```

Respuesta

```json
{
    "score":87,
    "skills_detectadas":[
        "Python",
        "Docker"
    ],
    "skills_faltantes":[
        "AWS"
    ],
    "recomendaciones":[
        "Agregar experiencia con AWS"
    ]
}
```

---

### Historial

```
GET /api/cv/history
```

---

### Detalle de un análisis

```
GET /api/cv/history/{analysis_id}
```

---

# Flujo del sistema

```
Cliente
    │
    ▼
FastAPI
    │
    ▼
cv_service
    │
    ▼
ai_service
    │
    ▼
Cerebras AI
    │
    ▼
MongoDB
    │
    ▼
Respuesta JSON
```

---

# Roadmap

## Sprint 1 ✅

- FastAPI
- Docker
- Hot Reload

## Sprint 2 ✅

- MongoDB
- Repository Pattern
- Historial de análisis

## Sprint 3 ✅

- Cerebras AI
- Prompt Engineering
- Análisis inteligente de CV

## Sprint 4 ✅

- Validación de respuestas IA
- Manejo de errores
- HTTP 502 para errores del proveedor
- Validación de estructura JSON

## Sprint 5 🚧

- Upload de PDF
- Extracción de texto
- Análisis automático desde archivos

## Sprint 6

- Frontend Vue 3

## Sprint 7

- Autenticación JWT

## Sprint 8

- Dashboard de análisis

---

# Autor

**Alan Hernández**