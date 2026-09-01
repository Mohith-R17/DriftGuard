# DriftGuard
> Production-aware API intelligence that detects documentation drift and automatically opens GitHub Pull Requests with updated documentation.

---

## 🚀 Features

- **Real-Time Traffic Capture Middleware**: Intercepts, inspects, and logs live API requests, responses, status codes, and latencies without introducing measurable overhead.
- **Automated Schema Drift Detection**: Continuously compares real-world payload structures against stored API documentation to detect undocumented or modified attributes instantly.
- **AI-Powered Doc Synthesis**: Leverages LLM pipelines powered by **LangGraph**, **LangChain**, and **Google Gemini / Groq** to regenerate accurate OpenAPI/Markdown documentation based on observed execution state.
- **Automated GitHub Pull Requests**: Opens pull requests directly against project repositories with auto-generated documentation updates whenever schema drift is confirmed.
- **Full Observability & Analytics**: Provides isolated multi-tenant endpoint performance tracking, raw request/response log inspection, and native **OpenTelemetry** instrumentation.

---

## 📦 Tech Stack

- **Core Framework**: [FastAPI](https://fastapi.tiangolo.com/) (v0.115.0) & [Uvicorn](https://www.uvicorn.org/) (v0.30.6)
- **Database & ORM**: PostgreSQL via [AsyncPG](https://github.com/MagicStack/asyncpg) (v0.29.0), [SQLAlchemy AsyncIO](https://www.sqlalchemy.org/) (v2.0.35), [Alembic](https://alembic.sqlalchemy.org/) (v1.13.3)
- **AI & Workflow Orchestration**: [LangGraph](https://github.com/langchain-ai/langgraph) (v0.2.28), [LangChain](https://github.com/langchain-ai/langchain) (v0.3.1), `langchain-groq`, `langchain-google-genai`
- **Data Validation & Settings**: [Pydantic v2](https://docs.pydantic.dev/) (v2.9.2) & `pydantic-settings` (v2.5.2)
- **Authentication & Security**: PyJWT (v2.8.0), Passlib with Bcrypt (v4.2.1)
- **Observability**: OpenTelemetry API & SDK (v1.27.0)

---

## 📡 API Reference

### Health Check & System Status

#### `GET /`
Check API availability and server state.

**Response (`200 OK`)**:
```json
{
  "status": "online",
  "service": "DriftGuard API Engine",
  "version": "1.0.0"
}
```

---

### Endpoints Management

#### `GET /api/v1/products`
Fetch product resources (monitored endpoint).

**Response (`200 OK`)**:
```json
[
  {
    "id": "prod_1001",
    "name": "API Intelligence Suite",
    "status": "active"
  }
]
```

#### `GET /api/v1/products/{product_id}`
Fetch detailed metadata for a specific product.

**Response (`404 Not Found`)**:
```json
{
  "detail": "Product prod_not_found not found"
}
```

---

### User Operations

#### `POST /api/v1/users`
Create a new user within the system.

**Request Body**:
```json
{
  "email": "developer@example.com",
  "password": "SecurePassword123!"
}
```

**Response (`201 Created`)**:
```json
{
  "id": "usr_1001",
  "email": "developer@example.com",
  "created_at": "2023-10-27T10:00:00Z"
}
```

#### `PUT /api/v1/users/{user_id}`
Update existing user attributes.

**Request Body**:
```json
{
  "email": "updated_developer@example.com"
}
```

**Response (`200 OK`)**:
```json
{
  "id": "usr_1001",
  "email": "updated_developer@example.com",
  "updated_at": "2023-10-27T10:05:00Z"
}
```

#### `DELETE /api/v1/users/{user_id}`
Remove a user by ID.

**Response (`204 No Content`)**

---

### Drift & Observability Routers

#### `GET /api/v1/endpoints`
Retrieve monitored API endpoints, observed drift status, and usage metrics.

**Response (`200 OK`)**:
```json
[
  {
    "endpoint_id": "ep_99",
    "path": "/api/v1/users",
    "method": "POST",
    "drift_detected": true,
    "last_synced": "2023-10-26T12:00:00Z"
  }
]
```

#### `GET /api/v1/logs`
Retrieve captured API execution logs.

**Response (`200 OK`)**:
```json
[
  {
    "id": "c1f72d5b-8012-4211-9e20-7f240989f665",
    "method": "POST",
    "path": "/api/v1/users",
    "status_code": 201,
    "latency_ms": 1.25,
    "client_ip": "127.0.0.1",
    "created_at": "2023-10-27T10:00:00Z"
  }
]
```

#### `POST /api/v1/github/sync`
Trigger automated drift analysis and generate a GitHub Pull Request with updated specs.

**Response (`200 OK`)**:
```json
{
  "status": "success",
  "pull_request_url": "https://github.com/organization/repo/pull/42",
  "changes_detected": 1
}
```

---

## 🛠️ Getting Started

### Prerequisites

Ensure you have the following installed on your local environment:
- **Python 3.11+**
- **PostgreSQL** database instance
- **GitHub Personal Access Token** (for automated PR creation)
- **Groq / Google Gemini API Key** (for LLM documentation synthesis)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-org/driftguard.git
   cd driftguard
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install fastapi==0.115.0 "uvicorn[standard]==0.30.6" "sqlalchemy[asyncio]==2.0.35" \
               asyncpg==0.29.0 alembic==1.13.3 pydantic==2.9.2 pydantic-settings==2.5.2 \
               python-dotenv==1.0.1 PyJWT==2.8.0 "passlib[bcrypt]==1.7.4" bcrypt==4.2.1 \
               httpx==0.27.2 langchain==0.3.1 langchain-groq==0.2.1 langchain-google-genai==2.0.7 \
               langgraph==0.2.28 langchain-core==0.3.15 google-generativeai==0.8.3 \
               opentelemetry-api==1.27.0 opentelemetry-sdk==1.27.0
   ```

4. **Environment Configuration**:
   Create a `.env` file in the root directory:
   ```env
   PORT=8000
   DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/driftguard
   SECRET_KEY=your_jwt_secret_key
   GROQ_API_KEY=your_groq_api_key
   GEMINI_API_KEY=your_gemini_api_key
   GITHUB_TOKEN=your_github_token
   ```

5. **Run Database Migrations**:
   ```bash
   alembic upgrade head
   ```

### Running the App

Start the Uvicorn ASGI server with automatic reload enabled:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Access the interactive API documentation at `http://localhost:8000/docs`.

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
---

## ⚠️ Documentation Drift Detected

> The README updates the default `GEMINI_MODEL` to `gemini-3.6-flash`, which does not match the model default configured in the application code.

*This documentation was auto-regenerated by DriftGuard to reflect the latest code changes.*

---