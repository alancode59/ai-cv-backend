# AI CV Analyzer API

Backend desarrollado con **FastAPI**, **MongoDB**, **Docker** y **Cerebras AI** para analizar automáticamente currículums (CV) mediante Inteligencia Artificial.

El sistema permite analizar un CV en formato texto o PDF, compararlo con una descripción de una vacante y generar una evaluación automática con porcentaje de compatibilidad, tecnologías detectadas, habilidades faltantes y recomendaciones para mejorar el perfil del candidato.

---

# Tecnologías

* Python 3.12
* FastAPI
* Jinja2 Templates
* Docker
* Docker Compose
* MongoDB
* PyMongo
* Cerebras Cloud SDK
* PyMuPDF
* python-multipart
* HTML5
* CSS3
* JavaScript
* Tailwind CSS (CDN)

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
├── services/
│   ├── ai_service.py
│   ├── cv_service.py
│   └── pdf_service.py
│
├── templates/
│   └── index.html
│
└── static/
    ├── css/
    │   └── styles.css
    ├── js/
    │   └── app.js
    └── uploads/
```

---

# Características

* Arquitectura por capas.
* Integración con Cerebras AI.
* Prompt Engineering desacoplado.
* Persistencia en MongoDB.
* Historial de análisis.
* Consulta de análisis por ID.
* Análisis de CV mediante texto.
* Análisis de CV mediante archivos PDF.
* Validación avanzada de archivos PDF.
* Extracción automática de texto con PyMuPDF.
* Limpieza y normalización del texto extraído.
* Validación de respuestas del modelo.
* Manejo centralizado de errores.
* Interfaz web integrada mediante Jinja2 Templates.
* Recursos estáticos organizados (HTML, CSS y JavaScript).
* Documentación automática mediante Swagger/OpenAPI.

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

### Linux / macOS

```bash
cp .env.example .env
```

### Windows

```cmd
copy .env.example .env
```

Editar el archivo `.env`:

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

La aplicación estará disponible en:

```
http://localhost:8000
```

Interfaz web:

```
http://localhost:8000/
```

Swagger:

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

### Estado de MongoDB

```http
GET /health/db
```

### Estado de Cerebras

```http
GET /health/ai
```

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

---

## Analizar CV mediante PDF

```http
POST /api/cv/analyze-pdf
```

**Content-Type**

```
multipart/form-data
```

### Parámetros

| Campo           | Tipo   | Obligatorio |
| --------------- | ------ | ----------- |
| cv_file         | PDF    | Sí          |
| job_description | String | Sí          |

### Flujo

1. Validación del archivo.
2. Verificación del tipo MIME.
3. Validación del tamaño máximo permitido.
4. Detección de PDFs protegidos.
5. Extracción automática del texto.
6. Limpieza y normalización del contenido.
7. Análisis mediante Cerebras AI.
8. Persistencia en MongoDB.
9. Respuesta en formato JSON.

---

## Historial de análisis

```http
GET /api/cv/history
```

---

## Obtener análisis por ID

```http
GET /api/cv/history/{analysis_id}
```

---

# Flujo del sistema

```text
             Usuario
                 │
                 ▼
        Interfaz Web (Jinja2)
                 │
                 ▼
         FastAPI Routes
                 │
                 ▼
           CV Service
                 │
      ┌──────────┴──────────┐
      ▼                     ▼
 PDF Service          AI Service
      │                     │
      ▼                     ▼
Extracción           Cerebras AI
de texto                  │
      └──────────┬─────────┘
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

* FastAPI
* Docker
* Docker Compose
* Hot Reload

## Sprint 2 ✅

* MongoDB
* Repository Pattern
* Historial de análisis

## Sprint 3 ✅

* Integración con Cerebras AI
* Prompt Engineering
* Análisis inteligente de CV

## Sprint 4 ✅

* Validación de respuestas de IA
* Manejo de errores
* HTTP 502 para errores del proveedor
* Validación de estructura JSON

## Sprint 5 ✅

* Upload de archivos PDF
* Extracción automática de texto
* Integración PDF → IA
* Persistencia del análisis

## Sprint 6 ✅

* Validaciones avanzadas de archivos PDF
* Límite de tamaño
* Verificación del tipo MIME
* Manejo de PDFs protegidos
* Limpieza y normalización del texto
* Manejo de errores de extracción

## Sprint 7 🚧

* Interfaz web con Jinja2 Templates
* Diseño moderno y profesional
* Visualización del resultado del análisis
* Historial visual de análisis

## Sprint 8

* Autenticación JWT
* Gestión de usuarios
* Dashboard administrativo

---

# Buenas prácticas implementadas

* Arquitectura por capas.
* Repository Pattern.
* Separación entre rutas, servicios y acceso a datos.
* Prompt Engineering desacoplado.
* Variables de entorno mediante `.env`.
* Archivo `.env.example` para facilitar la configuración.
* Organización de recursos estáticos (`templates`, `css`, `js`).
* `.dockerignore` para optimizar la construcción de imágenes.
* `.gitignore` para excluir archivos temporales y sensibles.

---

# Autor

**Alan Hernández**
