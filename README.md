# AI CV Analyzer API

Backend desarrollado con **FastAPI**, **MongoDB**, **Docker** y **Cerebras AI** para analizar automáticamente currículums (CV) mediante Inteligencia Artificial.

El sistema permite analizar un CV en formato texto o PDF, compararlo con una descripción de una vacante y generar una evaluación automática con porcentaje de compatibilidad, tecnologías detectadas, habilidades faltantes y recomendaciones para mejorar el perfil del candidato.

---

# Tecnologías

- Python 3.12
- FastAPI
- Docker
- Docker Compose
- MongoDB
- PyMongo
- Cerebras Cloud SDK
- PyMuPDF
- python-multipart

---

# Arquitectura

```text
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
│   ├── health_routes.py
│   └── user_routes.py
│
├── schemas/
│   └── cv_schema.py
│
└── services/
    ├── ai_service.py
    ├── cv_service.py
    └── pdf_service.py
```

---

# Características

- Arquitectura por capas.
- Integración con Cerebras AI.
- Prompt Engineering desacoplado.
- Persistencia en MongoDB.
- Historial de análisis.
- Consulta de análisis por ID.
- Análisis de CV mediante texto.
- Análisis de CV mediante archivos PDF.
- Extracción automática de texto con PyMuPDF.
- Validación de respuestas del modelo.
- Manejo centralizado de errores.
- Documentación automática con Swagger/OpenAPI.

---

# Instalación

## 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd backend-cv
```

---

## 2. Configurar variables de entorno

El proyecto incluye un archivo **`.env.example`** con la estructura necesaria.

Copiar el archivo:

### Linux / macOS

```bash
cp .env.example .env
```

### Windows

```cmd
copy .env.example .env
```

Editar el archivo `.env` con tus credenciales.

Ejemplo:

```env
MONGO_URI=mongodb://mongo:27017
MONGO_DB_NAME=cvAnalyzer

CEREBRAS_API_KEY=TU_API_KEY
CEREBRAS_MODEL=gpt-oss-120b
```

---

## 3. Ejecutar con Docker

```bash
docker compose up --build
```

La API estará disponible en:

```
http://localhost:8000
```

Documentación Swagger:

```
http://localhost:8000/docs
```

---

# Endpoints

## Health

### Estado del servidor

```http
GET /health
```

Respuesta

```json
{
    "status": "OK"
}
```

---

### Estado de MongoDB

```http
GET /health/db
```

---

### Estado de Cerebras

```http
GET /health/ai
```

---

### Modelos disponibles

```http
GET /health/ai/models
```

---

# CV Analysis

## Analizar CV mediante texto

```http
POST /api/cv/analyze
```

### Request

```json
{
    "cv_text": "Python FastAPI Docker MongoDB",
    "job_description": "Backend Developer con Python y AWS"
}
```

### Response

```json
{
    "score": 87,
    "skills_detectadas": [
        "Python",
        "Docker",
        "FastAPI"
    ],
    "skills_faltantes": [
        "AWS"
    ],
    "recomendaciones": [
        "Agregar experiencia con AWS"
    ]
}
```

---

## Analizar CV mediante PDF

```http
POST /api/cv/analyze-pdf
```

Tipo de contenido:

```
multipart/form-data
```

### Parámetros

| Campo | Tipo | Obligatorio |
|--------|------|-------------|
| cv_file | PDF | Sí |
| job_description | String | Sí |

### Flujo

1. Se valida que el archivo sea un PDF.
2. Se extrae automáticamente el texto del documento.
3. El texto se envía a Cerebras AI.
4. Se genera el análisis del CV.
5. Se almacena el resultado en MongoDB.
6. Se devuelve la respuesta en formato JSON.

---

## Historial de análisis

```http
GET /api/cv/history
```

Obtiene todos los análisis almacenados.

---

## Obtener análisis por ID

```http
GET /api/cv/history/{analysis_id}
```

Obtiene el detalle de un análisis específico.

---

# Flujo del sistema

```text
               PDF / Texto
                    │
                    ▼
            FastAPI Routes
                    │
                    ▼
              CV Service
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
   PDF Service             AI Service
        │                       │
        ▼                       ▼
Extracción de texto       Cerebras AI
        └───────────┬───────────┘
                    ▼
             Repository Pattern
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
- Docker Compose
- Hot Reload

## Sprint 2 ✅

- MongoDB
- Repository Pattern
- Historial de análisis

## Sprint 3 ✅

- Integración con Cerebras AI
- Prompt Engineering
- Análisis inteligente de CV

## Sprint 4 ✅

- Validación de respuestas de IA
- Manejo de errores
- HTTP 502 para errores del proveedor
- Validación de estructura JSON

## Sprint 5 ✅

- Upload de archivos PDF
- Extracción automática de texto
- Integración PDF → IA
- Persistencia del análisis

## Sprint 6 🚧

- Validaciones avanzadas de archivos
- Límite de tamaño de PDF
- Manejo de PDFs protegidos
- Soporte para OCR en PDFs escaneados
- Limpieza y normalización del texto extraído

## Sprint 7

- Frontend con HTML + Tailwind CSS
- Dashboard de resultados
- Historial visual

## Sprint 8

- Autenticación JWT
- Gestión de usuarios
- Dashboard administrativo

---

# Buenas prácticas implementadas

- Arquitectura por capas.
- Repository Pattern.
- Separación entre rutas, servicios y acceso a datos.
- Prompt Engineering desacoplado.
- Variables de entorno mediante `.env`.
- Archivo `.env.example` para facilitar la configuración del proyecto.
- `.dockerignore` para optimizar la construcción de imágenes Docker.
- `.gitignore` para excluir archivos temporales y sensibles.

---

# Autor

**Alan Hernández**
