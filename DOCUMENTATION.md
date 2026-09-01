# DriftGuard
> Production-aware API intelligence that detects documentation drift and automatically opens GitHub Pull Requests with updated documentation.

## 🚀 Features

* **Real-Time Traffic Capture Middleware**: Intercepts incoming HTTP requests and responses to monitor payloads, headers, status codes, and latency with minimal overhead.
* **AI-Driven Schema Drift Detection**: Integrates LangChain, LangGraph, and LLM models (Google Gemini / Groq) to analyze actual runtime payloads against static API documentation.
* **Automated Pull Request Generation**: Automatically opens GitHub Pull Requests with updated OpenAPI specifications and documentation whenever drift is identified.
* **Multi-Tenant Endpoint Observability**: Groups logs by user, path, and method to track API metrics, latency trends, and usage velocity.
* **Autonomous Demo Traffic Simulator**: Includes an optional background traffic generation task for continuous pipeline testing and integration validation.

## 📦 Tech Stack

| Category | Technology |
| :--- | :--- |
| **Framework & Server** | FastAPI (`0.115.0`), Uvicorn (`0.30.6`), Pydantic (`2.9.2`) |
| **Database & ORM** | PostgreSQL, SQLAlchemy AsyncIO (`2.0.35`), Asyncpg (`0.29.0`), Alembic (`1.13.3`) |
| **AI Agent & LLM** | LangChain (`0.3.1`), LangGraph (`0.2.28`), LangChain-Groq (`0.2.1`), LangChain-Google-GenAI (`2.0.7`) |
| **Security & Auth** | PyJWT (`2.8.0`), Passlib (`1.7.4`), Bcrypt (`4.2.1`) |
| **Observability & HTTP** | OpenTelemetry SDK (`1.27.0`), HTTPX (`0.27.2`) |

## 📡 API Reference

### Products

#### List Products
```http
GET /api/v1/products
```
Retrieves a paginated list of available products.

##### Response Example (200 OK)
```json
{
  "total": 2,
  "items": [
    {
      "id": "prod_1001",
      "name": "Cloud Observability Agent",
      "price": 199.99,
      "status": "active"
    },
    {
      "id": "prod_1002",
      "name": "API Intelligence Engine",
      "price": 499.00,
      "status": "active"
    }
  ]
}
```

#### Get Product Details
```http
GET /api/v1/products/{product_id}
```
Fetches details for a given product by ID.

##### Response Example (404 Not Found)
```json
{
  "error": "PRODUCT_NOT_FOUND",
  "message": "Product with ID 'prod_not_found' was not found.",
  "status_code": 404
}
```

---

### User Management

#### Create User
```http
POST /api/v1/users
```
Registers a new user inside the system.

##### Request Body
```json
{
  "email": "developer@example.com",
  "name": "Jane Doe",
  "role": "engineer"
}
```

##### Response Example (201 Created)
```json
{
  "id": "usr_1001",
  "email": "developer@example.com",
  "name": "Jane Doe",
  "role": "engineer",
  "created_at": "2026-03-31T12:00:00Z"
}
```

#### Update User
```http
PUT /api/v1/users/{user_id}
```
Updates an existing user record.

##### Request Body
```json
{
  "name": "Jane Smith",
  "role": "lead_engineer"
}
```

##### Response Example (200 OK)
```json
{
  "id": "usr_1001",
  "email": "developer@example.com",
  "name": "Jane Smith",
  "role": "lead_engineer",
  "updated_at": "2026-03-31T12:30:00Z"
}
```

#### Delete User
```http
DELETE /api/v1/users/{user_id}
```
Deletes a user account.

##### Response Example (200 OK)
```json
{
  "success": true,
  "message": "User usr_9999 successfully deleted."
}
```

## 🛠️ Getting Started

### Prerequisites

* **Python**: `v3.10` or higher
* **PostgreSQL**: Running instance or local database
* **API Keys**: Groq API Key or Google Gemini API Key (for LLM analysis) and GitHub Personal Access Token (for PR generation)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-org/driftguard.git
   cd driftguard
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install requirements:
   ```bash
   pip install fastapi uvicorn "sqlalchemy[asyncio]" asyncpg alembic pydantic pydantic-settings python-dotenv PyJWT "passlib[bcrypt]" bcrypt httpx langchain langchain-groq langchain-google-genai langgraph langchain-core google-generativeai opentelemetry-api opentelemetry-sdk
   ```

4. Configure environment variables:
   Create a `.env` file in the root directory:
   ```env
   DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/driftguard
   SECRET_KEY=your_jwt_secret_key
   GROQ_API_KEY=your_groq_api_key
   GEMINI_API_KEY=your_gemini_api_key
   GITHUB_TOKEN=your_github_token
   PORT=8000
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

3. Access the API and interactive documentation:
   * **Swagger UI**: `http://localhost:8000/docs`
   * **ReDoc**: `http://localhost:8000/redoc`

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request