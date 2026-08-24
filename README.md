<h1 align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=35&pause=1000&color=2F81F7&width=500&lines=Monastery+Web+API" alt="Typing SVG" />
</h1>

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-API-lightgrey?logo=flask)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange?logo=mysql)
![Docker](https://img.shields.io/badge/Docker-Container-blue?logo=docker)

**Monastery Web API** is a production‑oriented, containerized RESTful web service for managing monastery records. Built with **Flask**, **SQLAlchemy (ORM)** and **MySQL**, the project includes database migrations, unit and integration tests, Swagger documentation, and a Docker Compose setup for reproducible local and CI environments.

---

## Key Features
- **RESTful CRUD endpoints** for monastery resources: GET, POST, PUT, PATCH, DELETE  
- **SQLAlchemy ORM** models with validation and convenience methods (`save`, `update`, `delete`, `to_dict`)  
- **Flask‑Migrate (Alembic)** for versioned database migrations  
- **Swagger / Flasgger** UI at `/apidocs` for interactive API exploration  
- **Consistent JSON error handling** via typed exceptions and structured responses  
- **Unit and integration tests** covering routes and model behavior  
- **Containerized stack** with `Dockerfile` and `docker-compose.yml` and production WSGI via Gunicorn

---

## Architecture and Design
**Application**
- `app.py` — Flask application and route definitions with Swagger annotations  
- `Models/Monastery.py` — SQLAlchemy model encapsulating persistence and validation  
- `exceptions.py` — typed exceptions with logging and consistent JSON payloads

**Persistence**
- **MySQL** as the primary datastore  
- **Migrations** managed by Flask‑Migrate to evolve schema safely  
- **Docker volume** for persistent database storage in local/dev environments

**Deployment**
- **Dockerfile** builds a minimal Python image and runs Gunicorn  
- **docker-compose.yml** orchestrates `monastery_api` and `monastery_db` for local development and CI  
- Designed for portability to cloud/container platforms with minimal changes

---

## Quick Start

## Build and Run

### Clone repository
```bash
git clone https://github.com/MIhajloS07/Monastery-Web-API.git
cd Monastery-Web-API
```
### Build and run (detached)
```
docker compose up -d --build
```
### Verify services
```
docker compose ps
```
### API base URL
```
http://localhost:5000/api/monasteries
```
### Swagger UI
```
http://localhost:5000/apidocs
```
### Stop and remove containers (preserve volumes)
```
docker compose down
```
### Stop and remove containers and volumes (destructive)
```
docker compose down -v
```
---

## Configuration and Migrations

### Primary environment variables
- **SQLALCHEMY_DATABASE_URI** — SQLAlchemy connection string (default provided in `docker-compose.yml`)  
- **MYSQL_DATABASE**, **MYSQL_USER**, **MYSQL_PASSWORD**, **MYSQL_ROOT_PASSWORD** — configured in `docker-compose.yml`

### Local overrides
- Use a **.env** file or CI secrets to override sensitive values.  
- When running via Compose, ensure **SQLALCHEMY_DATABASE_URI** points to the Compose service name, for example:
```
mysql+pymysql://user:password@db:3306/monastery
```

### Database migrations
```bash
# create a migration after model changes
docker compose exec monastery_api flask db migrate -m "describe change"

# apply migrations
docker compose exec monastery_api flask db upgrade
```
---
## Testing and CI

### Run unit and integration tests
```bash
docker compose exec monastery_api python -m unittest discover -s tests
```

### Local test workflow
1. #### build and start services:
   ```bash
   docker compsoe up -d --build
   ```
2. #### Apply migrations:
   ```bash
   docker compose exec monastery_api flask db upgrade
   ```
3. #### Run the test suite:
   ```bash
   docker compose exec monastery_api python -m unittest discover -s tests
   ```
4. #### Tear down test environment (optional ephemeral DB):
   ```bash
   docker compose down -v
   ```
---

## Example API Requests
## Create a monastery
```
curl -X POST http://localhost:5000/api/monasteries \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Studenica",
    "location": "Kraljevo, Serbia",
    "year_of_construction": 1190,
  }'
```
### Expected success (201)
```
{
  "id": 1,
  "name": "Studenica",
  "location": "Kraljevo, Serbia",
  "year_of_construction": 1190,
}
```
## List monasteries
```
curl http://localhost:5000/api/monasteries
```
### Expected success (201)
```
[
  {
    "id": 1,
    "name": "Studenica",
    "location": "Kraljevo, Serbia",
    "year_of_construction": 1190
  },
  {
    "id": 2,
    "name": "Sopoćani",
    "location": "Raška, Serbia",
    "year_of_construction": 1260
  }
]
```
## List monasteries
```
curl http://localhost:5000/api/monasteries
```
### Expected success (200)
```
[
  {
    "id": 1,
    "name": "Studenica",
    "location": "Kraljevo, Serbia",
    "year_of_construction": 1190
  },
  {
    "id": 2,
    "name": "Sopoćani",
    "location": "Raška, Serbia",
    "year_of_construction": 1260
  }
]
```
## Get monastery by ID
```
curl http://localhost:5000/api/monasteries/1
```
### Expected success (200)
```
{
  "id": 1,
  "name": "Studenica",
  "location": "Kraljevo, Serbia",
  "year_of_construction": 1190,
}
```
### not found (404)
```
{ "error": "Monastery not found", "status": 404 }
```
## Update monastery (PUT)
```
curl -X PUT http://localhost:5000/api/monasteries/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Studenica",
    "location": "Kraljevo, Serbia",
    "year_of_construction": 1190,
  }'
```
### Expected success (200)
```
{
  "id": 1,
  "name": "Studenica",
  "location": "Kraljevo, Serbia",
  "year_of_construction": 1190,
}
```
## Partial update (PATCH)
```
curl -X PATCH http://localhost:5000/api/monasteries/1 \
  -H "Content-Type: application/json" \
  -d '{"location":"New Location, Serbia"}'
```
### Expected success (200)
```
{
  "id": 1,
  "name": "Studenica",
  "location": "New Location, Serbia",
  "year_of_construction": 1190
}
```
## Delete monastery
```
curl -X DELETE http://localhost:5000/api/monasteries/1
```
### Expected success (204 No Content)
### Validation error example (400)
```
curl -X POST http://localhost:5000/api/monasteries \
  -H "Content-Type: application/json" \
  -d '{"name": "", "location": "X"}'
```
### Expected error (400)
```
{
  "error": "Validation failed",
  "details": {
    "name": "Name must not be empty",
    "year_of_construction": "Year is required"
  },
  "status": 400
}
```

##  Run requests against Swagger UI
Open the interactive API documentation to try endpoints and view schemas:
```code
http://localhost:5000/apidocs
```
## Architecture Diagram
- **[Presentation Layer](ca://s?q=Presentation_Layer_objasnjenje)** → Client (Web)  
- **[Business Logic Layer](ca://s?q=Business_Logic_Layer_objasnjenje)** → Flask application (`app.py`) + Swagger UI  
- **[Persistence Layer](ca://s?q=Persistence_Layer_objasnjenje)** → Model (Monastery) + MySQL Server  
- **[Docker](ca://s?q=Docker_kontejneri_objasnjenje)** → monastery_api container (Flask + Gunicorn) + monastery_db container (MySQL)

<img width="1081" height="611" alt="image" src="https://github.com/user-attachments/assets/82b2cda7-028a-437a-8d31-a953694b2552" />


## Project Structure
```code
📂 monastery-api/
├── 📂 migrations/                # Alembic migrations (versions, env.py, script templates)
│    ├── versions/                # Database migration history
│    ├── alembic.ini              # Alembic configuration
│    ├── env.py                   # Migration environment setup
│    └── script.py.mako           # Template for generating migrations
│
├── 📂 Models/                    # ORM models
│    ├── init.py                  # Package initializer
│    └── Monastery.py             # Monastery entity model
│
├── 📂 tests/                     # Unit and integration tests
│    ├── test_api.py              # Tests for API routes
│    └── test_monastery_model.py  # Tests for Monastery model
│
├── app.py                        # Main Flask application (Business Logic Layer)
├── exceptions.py                 # Custom exception handling
├── requirements.txt              # Python dependencies
├── docker-compose.yml            # Docker orchestration (API + DB containers)
├── Dockerfile                    # Build definition for monastery_api container
├── .env                          # Environment variables (DB URL, secrets)
├── .dockerignore                 # Files ignored during Docker build
├── .gitignore                    # Files ignored by Git
├── LICENSE                       # Project license
├── README.md                     # Documentation (badges, architecture, setup)
└── errors.log                    # Error log file
```
### 🔹 Layer Explanation
- **[migrations](ca://s?q=Alembic_migrations_explanation)** → Database versioning with Alembic.  
- **[Models](ca://s?q=ORM_models_explanation)** → SQLAlchemy ORM models, e.g. `Monastery.py`.  
- **[tests](ca://s?q=Unit_integration_tests_explanation)** → Unit and integration tests for API and models.  
- **[app.py](ca://s?q=Flask_app_business_logic)** → Main Flask application, routes, Swagger UI.  
- **[exceptions.py](ca://s?q=Python_custom_exceptions_explanation)** → Centralized error handling.  
- **[docker-compose.yml](ca://s?q=Docker_compose_explanation)** + **[Dockerfile](ca://s?q=Dockerfile_explanation)** → Container orchestration and build.  
- **[requirements.txt](ca://s?q=Python_requirements_explanation)** → Project dependencies.  
- **[.env](ca://s?q=Environment_variables_explanation)** → Environment configuration (e.g. DB connection).

### Notes
- Keep .env out of version control; include .env.example with non-sensitive defaults.
- Split tests into unit and integration to separate fast model tests from end‑to‑end API tests.
- Consider adding a top‑level Makefile or scripts/ entries for common tasks (start, test, migrate, seed).


## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

This project is licensed under the **MIT License** — see the `LICENSE` file in the repository for full terms.
