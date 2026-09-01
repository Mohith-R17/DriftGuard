# DriftGuard
> Production-aware API intelligence that detects documentation drift and automatically opens GitHub Pull Requests with updated documentation.

## 🚀 Features

* **Real-time Traffic Capture & Observability**: Non-blocking middleware (`TrafficCaptureMiddleware`) passively captures API requests, responses, latency, headers, and status codes across all production endpoints.
* **AI-Powered Drift Detection**: Powered by LangChain, LangGraph, and Google Gemini / Groq to analyze schema changes, route mutations, and payload structural shifts against your existing API documentation.
* **Automated GitHub Pull Requests**: Automatically generates updated OpenAPI specs or documentation files and submits GitHub PRs directly to your repository when drift is detected.
* **Multi-Tenant API Isolation**: Full user authentication using JWT and Async SQLAlchemy to isolate log telemetry and endpoint discovery per organization.
* **OpenTelemetry Integration**: Out-of-the-box OpenTelemetry tracing and metrics instrumentation for production observability stack integrations.
* **Automated Traffic Simulator**: Built-in background engine to simulate baseline production traffic and test drift detection triggers during staging deployments.

## 📦 Tech Stack

* **Framework & Server**: FastAPI `0.115.0`, Uvicorn `0.30.6`
* **Database & ORM**: PostgreSQL, SQLAlchemy (AsyncIO) `2.0.35`, AsyncPG `0.29.0`, Alembic `1.13.3`
* **Data Validation & Settings**: Pydantic `2.9.2`, Pydantic-Settings `2.5.2`
* **AI & LLM Framework**: LangChain `0.3.1`, LangGraph `0.2.28`, LangChain-Groq `0.2.1`, LangChain-Google-GenAI `2.0.7`, Google Generative AI `0.8.3`
* **Security & Auth**: PyJWT `2.8.0`, Passlib (Bcrypt) `1.7.4`, Bcrypt `4.2.1`
* **HTTP Client & Observability**: HTTPX `0.27.2`, OpenTelemetry API/SDK `1.27.0`

## 📡 API Reference

### Products

#### Fetch Products
```http
GET /api/v1/products
```

**Response (`200 OK`)**
```json
[
  {
    "id": "prod_1001",
    "name": "Standard Subscription",
    "price": 29.99,
    "status": "active"
  }
]
```

### Users

#### Create User
```http
POST /api/v1/users
```

**Request Body**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response (`201 Created`)**
```json
{
  "id": "usr_1001",
  "email": "user@example.com",
  "created_at": "2023-10-27T10:00:00Z"
}
```

#### Update User
```http
PUT /api/v1/users/{user_id}
```

**Response (`200 OK`)**
```json
{
  "id": "usr_1001",
  "email": "updated_user@example.com",
  "updated_at": "2023-10-27T10:15:00Z"
}
```

#### Delete User
```http
DELETE /api/v1/users/{user_id}
```

**Response (`204 No Content`)**

### Telemetry & Intelligence

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/endpoints` | List all discovered API endpoints and their drift status |
| `GET` | `/api/v1/logs` | Query captured API traffic logs |
| `POST` | `/api/v1/github/sync` | Trigger manual sync and GitHub PR generation for documentation drift |

## 🛠️ Getting Started

### Prerequisites

* Python 3.10+
* PostgreSQL database instance
* GitHub Personal Access Token (for PR creation features)
* Google Gemini or Groq API key (for LLM drift analysis)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-org/driftguard.git
   cd driftguard
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables in a `.env` file:
   ```env
   DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/driftguard
   SECRET_KEY=your-super-secret-jwt-key
   GEMINI_API_KEY=your-google-gemini-key
   GROQ_API_KEY=your-groq-api-key
   GITHUB_TOKEN=your-github-token
   ```

### Running the App

1. Run database migrations:
   ```bash
   alembic upgrade head
   ```

2. Start the FastAPI development server:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

3. Access the interactive API documentation at `http://localhost:8000/docs`.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request