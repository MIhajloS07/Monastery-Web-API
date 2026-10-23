<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,14,18&height=220&section=header&text=Monastery%20Web%20API&fontSize=58&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=Production-oriented%20REST%20API%20%E2%80%A2%20Flask%20%C2%B7%20MySQL%20%C2%B7%20Docker&descAlignY=60&descSize=18" alt="Monastery Web API banner" width="100%"/>

<a href="https://github.com/MIhajloS07/Monastery-Web-API">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=24&duration=3000&pause=1000&color=2F81F7&center=true&vCenter=true&width=760&lines=Containerized+RESTful+web+service;Flask+%2B+SQLAlchemy+%2B+MySQL;Versioned+migrations+with+Alembic;Interactive+Swagger+documentation;Unit+%26+integration+tested;One+command+to+run%3A+docker+compose+up" alt="Typing SVG" />
</a>

<br/>

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-REST_API-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-Database-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Swagger](https://img.shields.io/badge/Swagger-OpenAPI_UI-85EA2D?style=for-the-badge&logo=swagger&logoColor=black)
![Gunicorn](https://img.shields.io/badge/Gunicorn-WSGI-499848?style=for-the-badge&logo=gunicorn&logoColor=white)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](./LICENSE)
[![Repo size](https://img.shields.io/github/repo-size/MIhajloS07/Monastery-Web-API?style=flat-square&color=2F81F7)](https://github.com/MIhajloS07/Monastery-Web-API)
[![Last commit](https://img.shields.io/github/last-commit/MIhajloS07/Monastery-Web-API?style=flat-square&color=2F81F7)](https://github.com/MIhajloS07/Monastery-Web-API/commits/main)
[![Stars](https://img.shields.io/github/stars/MIhajloS07/Monastery-Web-API?style=flat-square&color=2F81F7)](https://github.com/MIhajloS07/Monastery-Web-API/stargazers)
[![Issues](https://img.shields.io/github/issues/MIhajloS07/Monastery-Web-API?style=flat-square&color=2F81F7)](https://github.com/MIhajloS07/Monastery-Web-API/issues)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square)](#-contributing)

<br/>

<img src="https://skillicons.dev/icons?i=python,flask,mysql,docker,git,linux,vscode&theme=dark" alt="Tech stack icons"/>

<br/><br/>

**[Quick Start](#-quick-start)** &nbsp;•&nbsp;
**[API Reference](#-api-reference)** &nbsp;•&nbsp;
**[Architecture](#-architecture)** &nbsp;•&nbsp;
**[Testing](#-testing)** &nbsp;•&nbsp;
**[Roadmap](#-roadmap)**

</div>

---

## 📖 Overview

**Monastery Web API** is a production‑oriented, containerized RESTful web service for managing monastery records. It is built with **Flask**, **SQLAlchemy (ORM)** and **MySQL**, and ships with versioned database migrations, unit and integration tests, interactive Swagger documentation, and a Docker Compose setup that makes local development and CI fully reproducible.

The project is intentionally small in domain but complete in engineering: layered structure, typed error handling, schema migrations, automated tests, and a one‑command deployment.

> **TL;DR** — `docker compose up -d --build` and open **http://localhost:5000/apidocs**.

---

## 📑 Table of Contents

- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Configuration](#%EF%B8%8F-configuration)
- [Database & Migrations](#%EF%B8%8F-database--migrations)
- [API Reference](#-api-reference)
- [Example Requests](#-example-requests)
- [Error Handling](#-error-handling)
- [Testing](#-testing)
- [Project Structure](#-project-structure)
- [Docker Deep Dive](#-docker-deep-dive)
- [Troubleshooting](#-troubleshooting)
- [Security Notes](#-security-notes)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Key Features

| | Feature | Details |
|---|---|---|
| 🔌 | **RESTful CRUD** | Full resource lifecycle: `GET`, `POST`, `PUT`, `PATCH`, `DELETE` |
| 🧱 | **ORM Model Layer** | SQLAlchemy model with validation and helpers: `save`, `update`, `delete`, `to_dict` |
| 🧬 | **Versioned Migrations** | Flask‑Migrate (Alembic) for safe, reviewable schema evolution |
| 📚 | **Interactive Docs** | Swagger UI via Flasgger at `/apidocs` |
| 🚨 | **Consistent Errors** | Typed exceptions mapped to structured JSON responses, with logging |
| 🧪 | **Automated Tests** | Unit tests (model) and integration tests (API routes) with `unittest` |
| 🐳 | **Containerized** | `Dockerfile` + `docker-compose.yml`, served by Gunicorn |
| 💾 | **Persistent Storage** | Named Docker volume keeps MySQL data across restarts |

---

## 🧰 Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Language | **Python 3.11** | Application runtime |
| Web framework | **Flask** | HTTP routing and request handling |
| ORM | **SQLAlchemy** | Object‑relational mapping |
| Database | **MySQL** (`pymysql` driver) | Primary datastore |
| Migrations | **Flask‑Migrate / Alembic** | Versioned schema changes |
| API docs | **Flasgger (Swagger UI)** | Interactive documentation |
| WSGI server | **Gunicorn** | Production‑grade serving |
| Containers | **Docker & Docker Compose** | Reproducible environments |
| Testing | **unittest** | Unit + integration test suites |

---

## 🏛 Architecture

### Layered overview

```mermaid
flowchart LR
    subgraph Client["🖥️ Presentation Layer"]
        C1["Browser / Swagger UI"]
        C2["curl / Postman / Services"]
    end

    subgraph API["⚙️ Business Logic Layer — container: monastery_api"]
        G["Gunicorn (WSGI)"]
        F["Flask app (app.py)"]
        E["exceptions.py<br/>typed errors → JSON"]
        G --> F
        F --> E
    end

    subgraph DATA["🗄️ Persistence Layer"]
        M["Models/Monastery.py<br/>SQLAlchemy ORM"]
        DB[("MySQL<br/>container: monastery_db")]
        V[("Docker volume")]
        M --> DB
        DB --- V
    end

    C1 -->|HTTP/JSON| G
    C2 -->|HTTP/JSON| G
    F --> M

    style Client fill:#0d1117,stroke:#2F81F7,color:#fff
    style API fill:#0d1117,stroke:#3FB950,color:#fff
    style DATA fill:#0d1117,stroke:#F0883E,color:#fff
```

### Request lifecycle

```mermaid
sequenceDiagram
    autonumber
    actor Client
    participant G as Gunicorn
    participant F as Flask (app.py)
    participant M as Monastery model
    participant DB as MySQL

    Client->>G: POST /api/monasteries (JSON)
    G->>F: WSGI request
    F->>M: validate payload
    alt valid
        M->>DB: INSERT
        DB-->>M: row + id
        M-->>F: to_dict()
        F-->>Client: 201 Created + JSON
    else invalid
        M-->>F: ValidationError(details)
        F-->>Client: 400 Bad Request + structured error
    end
```

### Data model

```mermaid
erDiagram
    MONASTERY {
        int id PK "auto-increment"
        string name "required, non-empty"
        string location "required"
        int year_of_construction "required"
    }
```

<details>
<summary><b>🖼️ Original architecture diagram</b></summary>
<br/>

<img width="1081" height="611" alt="Monastery Web API architecture diagram" src="https://github.com/user-attachments/assets/82b2cda7-028a-437a-8d31-a953694b2552" />

</details>

### Design principles

- **Separation of concerns** — routing (`app.py`), persistence (`Models/`) and error semantics (`exceptions.py`) live in separate modules.
- **Fail loudly, respond consistently** — every error path produces the same JSON envelope and is logged to `errors.log`.
- **Reproducibility first** — the whole stack (API + database) is defined declaratively in Compose.
- **Schema as code** — database changes are tracked as Alembic migrations, never applied by hand.
- **Portable by default** — configuration through environment variables keeps the service cloud‑ready.

---

## 🚀 Quick Start

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) 20.10+
- [Docker Compose](https://docs.docker.com/compose/) v2 (`docker compose`)
- `git`

### 1. Clone

```bash
git clone https://github.com/MIhajloS07/Monastery-Web-API.git
cd Monastery-Web-API
```

### 2. Build and run (detached)

```bash
docker compose up -d --build
```

### 3. Verify services

```bash
docker compose ps
```

You should see both `monastery_api` and `monastery_db` in the `running` state.

### 4. Apply database migrations

```bash
docker compose exec monastery_api flask db upgrade
```

### 5. Open the API

| Resource | URL |
|---|---|
| **API base URL** | http://localhost:5000/api/monasteries |
| **Swagger UI** | http://localhost:5000/apidocs |

### 6. Smoke test

```bash
curl http://localhost:5000/api/monasteries
```

### Stop the stack

```bash
# stop and remove containers, keep database data
docker compose down

# stop and remove containers AND volumes (destructive — deletes all data)
docker compose down -v
```

---

## ⚙️ Configuration

Configuration is supplied through environment variables.

| Variable | Description | Where defined |
|---|---|---|
| `SQLALCHEMY_DATABASE_URI` | SQLAlchemy connection string | `docker-compose.yml` / `.env` |
| `MYSQL_DATABASE` | Database name | `docker-compose.yml` / `.env` |
| `MYSQL_USER` | Application DB user | `docker-compose.yml` / `.env` |
| `MYSQL_PASSWORD` | Application DB password | `docker-compose.yml` / `.env` |
| `MYSQL_ROOT_PASSWORD` | MySQL root password | `docker-compose.yml` / `.env` |

### Connection string

When running under Compose, the **host in the URI must be the Compose service name of the database container** (not `localhost`):

```text
mysql+pymysql://<user>:<password>@<db-service-name>:3306/<database>
```

### Local overrides

- Use a `.env` file or CI secrets to override sensitive values.
- Never commit real credentials. Commit a `.env.example` with safe placeholders instead:

```dotenv
# .env.example
MYSQL_DATABASE=monastery
MYSQL_USER=monastery_user
MYSQL_PASSWORD=change_me
MYSQL_ROOT_PASSWORD=change_me_too
SQLALCHEMY_DATABASE_URI=mysql+pymysql://monastery_user:change_me@monastery_db:3306/monastery
```

---

## 🗄️ Database & Migrations

Schema changes are managed with **Flask‑Migrate (Alembic)**.

```mermaid
flowchart LR
    A["Edit model<br/>Models/Monastery.py"] --> B["flask db migrate -m '...'"]
    B --> C["Review generated<br/>migrations/versions/*.py"]
    C --> D["flask db upgrade"]
    D --> E[("MySQL schema updated")]
    style A fill:#161b22,stroke:#2F81F7,color:#fff
    style B fill:#161b22,stroke:#2F81F7,color:#fff
    style C fill:#161b22,stroke:#F0883E,color:#fff
    style D fill:#161b22,stroke:#3FB950,color:#fff
    style E fill:#161b22,stroke:#3FB950,color:#fff
```

```bash
# 1) generate a migration after changing a model
docker compose exec monastery_api flask db migrate -m "describe change"

# 2) ALWAYS review the generated file in migrations/versions/

# 3) apply migrations
docker compose exec monastery_api flask db upgrade

# roll back one revision
docker compose exec monastery_api flask db downgrade

# inspect history / current revision
docker compose exec monastery_api flask db history
docker compose exec monastery_api flask db current
```

---

## 📡 API Reference

**Base URL:** `http://localhost:5000/api/monasteries`
**Content type:** `application/json`

### Endpoints

| Method | Endpoint | Description | Success | Errors |
|:---:|---|---|:---:|:---:|
| `GET` | `/api/monasteries` | List all monasteries | `200` | — |
| `GET` | `/api/monasteries/{id}` | Get a monastery by ID | `200` | `404` |
| `POST` | `/api/monasteries` | Create a monastery | `201` | `400` |
| `PUT` | `/api/monasteries/{id}` | Replace a monastery (full update) | `200` | `400`, `404` |
| `PATCH` | `/api/monasteries/{id}` | Partially update a monastery | `200` | `400`, `404` |
| `DELETE` | `/api/monasteries/{id}` | Delete a monastery | `204` | `404` |

### Resource schema

| Field | Type | Required | Description |
|---|---|:---:|---|
| `id` | integer | — (read‑only) | Auto‑generated primary key |
| `name` | string | ✅ | Monastery name, must not be empty |
| `location` | string | ✅ | Place / region, e.g. `"Kraljevo, Serbia"` |
| `year_of_construction` | integer | ✅ | Year the monastery was built |

### HTTP status codes

| Code | Meaning | When |
|:---:|---|---|
| `200` | OK | Successful read or update |
| `201` | Created | Resource successfully created |
| `204` | No Content | Resource successfully deleted |
| `400` | Bad Request | Validation failed |
| `404` | Not Found | Resource does not exist |
| `500` | Internal Server Error | Unexpected failure (logged to `errors.log`) |

> 🧪 Prefer clicking over typing? Open **[Swagger UI](http://localhost:5000/apidocs)** to explore schemas and execute requests directly from the browser.

---

## 🧾 Example Requests

<details open>
<summary><b>➕ Create a monastery — <code>POST</code></b></summary>

```bash
curl -X POST http://localhost:5000/api/monasteries \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Studenica",
    "location": "Kraljevo, Serbia",
    "year_of_construction": 1190
  }'
```

**Response `201 Created`**

```json
{
  "id": 1,
  "name": "Studenica",
  "location": "Kraljevo, Serbia",
  "year_of_construction": 1190
}
```

</details>

<details>
<summary><b>📋 List monasteries — <code>GET</code></b></summary>

```bash
curl http://localhost:5000/api/monasteries
```

**Response `200 OK`**

```json
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

</details>

<details>
<summary><b>🔍 Get by ID — <code>GET</code></b></summary>

```bash
curl http://localhost:5000/api/monasteries/1
```

**Response `200 OK`**

```json
{
  "id": 1,
  "name": "Studenica",
  "location": "Kraljevo, Serbia",
  "year_of_construction": 1190
}
```

**Response `404 Not Found`**

```json
{ "error": "Monastery not found", "status": 404 }
```

</details>

<details>
<summary><b>✏️ Full update — <code>PUT</code></b></summary>

```bash
curl -X PUT http://localhost:5000/api/monasteries/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Studenica",
    "location": "Kraljevo, Serbia",
    "year_of_construction": 1190
  }'
```

**Response `200 OK`**

```json
{
  "id": 1,
  "name": "Studenica",
  "location": "Kraljevo, Serbia",
  "year_of_construction": 1190
}
```

</details>

<details>
<summary><b>🩹 Partial update — <code>PATCH</code></b></summary>

```bash
curl -X PATCH http://localhost:5000/api/monasteries/1 \
  -H "Content-Type: application/json" \
  -d '{"location": "New Location, Serbia"}'
```

**Response `200 OK`**

```json
{
  "id": 1,
  "name": "Studenica",
  "location": "New Location, Serbia",
  "year_of_construction": 1190
}
```

</details>

<details>
<summary><b>🗑️ Delete — <code>DELETE</code></b></summary>

```bash
curl -X DELETE http://localhost:5000/api/monasteries/1
```

**Response `204 No Content`** (empty body)

</details>

<details>
<summary><b>⚠️ Validation error — <code>400</code></b></summary>

```bash
curl -X POST http://localhost:5000/api/monasteries \
  -H "Content-Type: application/json" \
  -d '{"name": "", "location": "X"}'
```

**Response `400 Bad Request`**

```json
{
  "error": "Validation failed",
  "details": {
    "name": "Name must not be empty",
    "year_of_construction": "Year is required"
  },
  "status": 400
}
```

</details>

---

## 🚨 Error Handling

All errors share one predictable envelope, produced by the typed exceptions in `exceptions.py`:

```json
{
  "error": "Human-readable message",
  "details": { "field": "optional per-field explanation" },
  "status": 400
}
```

| Field | Type | Always present | Description |
|---|---|:---:|---|
| `error` | string | ✅ | Short description of what went wrong |
| `status` | integer | ✅ | HTTP status code mirrored in the body |
| `details` | object | ❌ | Per‑field validation messages (validation errors only) |

Errors are also written to **`errors.log`** for post‑mortem analysis.

---

## 🧪 Testing

The suite is split by scope:

| File | Scope | Covers |
|---|---|---|
| `tests/test_monastery_model.py` | Unit | Model validation and helper methods |
| `tests/test_api.py` | Integration | Routes, status codes, payloads, error responses |

### Run the full suite

```bash
docker compose exec monastery_api python -m unittest discover -s tests
```

### Recommended local workflow

```mermaid
flowchart LR
    A["1. Build & start<br/>docker compose up -d --build"] --> B["2. Apply migrations<br/>flask db upgrade"]
    B --> C["3. Run tests<br/>python -m unittest discover -s tests"]
    C --> D["4. Tear down (optional)<br/>docker compose down -v"]
    style A fill:#161b22,stroke:#2F81F7,color:#fff
    style B fill:#161b22,stroke:#F0883E,color:#fff
    style C fill:#161b22,stroke:#3FB950,color:#fff
    style D fill:#161b22,stroke:#F85149,color:#fff
```

```bash
docker compose up -d --build
docker compose exec monastery_api flask db upgrade
docker compose exec monastery_api python -m unittest discover -s tests
docker compose down -v   # optional: wipe the ephemeral test database
```

### Run a single test module

```bash
docker compose exec monastery_api python -m unittest tests.test_api -v
```

---

## 🗂 Project Structure

```text
📂 Monastery-Web-API/
├── 📂 migrations/                # Alembic migrations
│   ├── 📂 versions/              # Database migration history
│   ├── alembic.ini               # Alembic configuration
│   ├── env.py                    # Migration environment setup
│   └── script.py.mako            # Template for generated migrations
│
├── 📂 Models/                    # Persistence layer (ORM)
│   ├── __init__.py               # Package initializer
│   └── Monastery.py              # Monastery entity model
│
├── 📂 tests/                     # Unit and integration tests
│   ├── test_api.py               # API route tests
│   └── test_monastery_model.py   # Model tests
│
├── app.py                        # Flask app, routes, Swagger annotations
├── exceptions.py                 # Typed exceptions and JSON error handling
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Image build for monastery_api
├── docker-compose.yml            # Orchestration: API + MySQL
├── .env                          # Environment variables (keep out of VCS)
├── .dockerignore                 # Files excluded from the Docker build context
├── .gitignore                    # Files excluded from Git
├── errors.log                    # Runtime error log
├── LICENSE                       # MIT license
└── README.md                     # You are here
```

### Responsibility map

| Component | Layer | Responsibility |
|---|---|---|
| `app.py` | Business logic | Routes, request parsing, Swagger docs |
| `Models/Monastery.py` | Persistence | Schema, validation, `save` / `update` / `delete` / `to_dict` |
| `exceptions.py` | Cross‑cutting | Typed errors, logging, uniform JSON payloads |
| `migrations/` | Persistence | Versioned schema history |
| `tests/` | Quality | Automated verification |
| `Dockerfile`, `docker-compose.yml` | Infrastructure | Build, run and wire the services |

---

## 🐳 Docker Deep Dive

```mermaid
flowchart TB
    subgraph Host["💻 Host machine"]
        P["localhost:5000"]
    end

    subgraph Net["🔗 Compose network"]
        subgraph API["monastery_api"]
            GU["Gunicorn → Flask"]
        end
        subgraph DBC["monastery_db"]
            MY["MySQL :3306"]
        end
        GU -->|"pymysql"| MY
    end

    VOL[("📦 Named volume<br/>MySQL data")]
    P -->|"port 5000"| GU
    MY --- VOL

    style Host fill:#0d1117,stroke:#8b949e,color:#fff
    style Net fill:#0d1117,stroke:#2F81F7,color:#fff
    style API fill:#161b22,stroke:#3FB950,color:#fff
    style DBC fill:#161b22,stroke:#F0883E,color:#fff
```

| Service | Role | Notes |
|---|---|---|
| `monastery_api` | Flask app served by Gunicorn | Exposed on host port `5000` |
| `monastery_db` | MySQL database | Data persisted in a named Docker volume |

### Useful commands

```bash
docker compose logs -f monastery_api       # follow API logs
docker compose logs -f monastery_db        # follow DB logs
docker compose exec monastery_api bash     # shell into the API container
docker compose restart monastery_api       # restart only the API
docker compose build --no-cache            # force a clean rebuild
```

---

## 🩺 Troubleshooting

<details>
<summary><b>API cannot connect to the database</b></summary>

- Make sure `SQLALCHEMY_DATABASE_URI` uses the **Compose service name** of the database container as host, not `localhost`.
- The database may still be initializing on first start. Wait a few seconds and check `docker compose logs monastery_db`.

</details>

<details>
<summary><b>Table <code>monasteries</code> doesn't exist / 500 on first request</b></summary>

Migrations have not been applied yet:

```bash
docker compose exec monastery_api flask db upgrade
```

</details>

<details>
<summary><b>Port 5000 is already in use</b></summary>

Change the host‑side port mapping in `docker-compose.yml` (for example `"5001:5000"`) and use `http://localhost:5001` instead. On macOS, AirPlay Receiver commonly occupies port 5000.

</details>

<details>
<summary><b>I want a completely clean slate</b></summary>

```bash
docker compose down -v
docker compose up -d --build
docker compose exec monastery_api flask db upgrade
```

⚠️ This deletes all stored data.

</details>

---

## 🔐 Security Notes

- Keep `.env` **out of version control**; ship a `.env.example` with placeholders only.
- Replace every default password before any non‑local deployment.
- Do not expose the MySQL port publicly; keep it reachable only on the internal Compose network.
- Run behind a reverse proxy (e.g. Nginx / Traefik) with TLS in production.
- Consider adding authentication, rate limiting and CORS policy before exposing the API publicly (see [Roadmap](#-roadmap)).

---

## 🛣 Roadmap

- [ ] Pagination, filtering and sorting on `GET /api/monasteries`
- [ ] CI pipeline (GitHub Actions): build image, run migrations, run tests on every push
- [ ] Test coverage reporting with a coverage badge
- [ ] `.env.example` and a `Makefile` for common tasks (`make up`, `make test`, `make migrate`, `make seed`)
- [ ] Seed script with real Serbian monastery data
- [ ] Authentication (JWT) and role‑based write access
- [ ] Container health checks and `depends_on: condition: service_healthy`
- [ ] Request validation with schemas (e.g. Marshmallow / Pydantic)
- [ ] Structured JSON logging and request IDs
- [ ] Linting and formatting (Ruff / Black) with pre‑commit hooks

---

## 🤝 Contributing

Contributions, issues and feature requests are welcome.

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m "feat: add amazing feature"`
4. **Run the tests** and make sure they pass
5. **Push** the branch: `git push origin feature/amazing-feature`
6. **Open a Pull Request**

Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `chore:`).

---

## 📄 License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](./LICENSE)

Distributed under the **MIT License**. See the [`LICENSE`](./LICENSE) file for full terms.

---

<div align="center">

### 👤 Author

**[MIhajloS07](https://github.com/MIhajloS07)**

⭐ If you find this project useful, consider giving it a star — it helps a lot!

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,14,18&height=120&section=footer" alt="footer wave" width="100%"/>

</div>
