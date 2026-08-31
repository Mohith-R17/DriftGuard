# DriftGuard

### Autonomous API Drift Detection & Documentation

<div align="center">

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688.svg?style=flat-square&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.2.28-FF6F00.svg?style=flat-square&logo=langchain&logoColor=white)](https://langchain-ai.github.io/langgraph/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-asyncpg-4169E1.svg?style=flat-square&logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)

**Production-aware API intelligence that detects documentation drift and automatically opens GitHub Pull Requests with updated documentation.**

</div>

---

> **DriftGuard** is a production-aware API intelligence platform that analyzes live HTTP traffic, source-code changes, and Git history to detect documentation drift. It uses an AI-powered LangGraph pipeline to analyze API behavior, generate updated technical documentation, and automatically open GitHub Pull Requests for developer review.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [How It Works](#-how-it-works)
- [LangGraph AI Pipeline](#-langgraph-ai-pipeline)
- [GitHub Automation](#-github-automation)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Environment Variables](#-environment-variables)
- [Current Capabilities vs. Future Scope](#-current-capabilities-vs-future-scope)
- [Security Notes](#-security-notes)
- [Demo Workflow](#-demo-workflow)
- [License](#-license)

---

## 🎯 Overview

### The Problem: Documentation Drift

In modern software development, APIs evolve at a rapid pace. Developers add endpoints, adjust schemas, alter status codes, and introduce new business logic. Unfortunately, API documentation often lags behind:

- **Static Docs Stagnate:** Manually maintained READMEs, Wiki pages, and OpenAPI specs quickly become outdated.
- **Code vs. Reality Disconnect:** Code annotations describe intended behavior, while observability metrics describe raw telemetry without explaining functionality.
- **Silent Failures:** Consumers build integrations against outdated documentation, leading to integration bugs and support overhead.

### The Solution: DriftGuard

DriftGuard bridges the gap between **runtime observability**, **source code analysis**, and **developer workflows**:

```
Live API Behavior + Source Code + Git History
                     ↓
              AI Analysis (LangGraph)
                     ↓
               Drift Detection
                     ↓
          Documentation Generation
                     ↓
      Automated GitHub Pull Request
```

---

## ✨ Key Features

### 📡 Live API Traffic Intelligence
- Intercepts incoming requests and responses non-intrusively via FastAPI middleware.
- Captures HTTP methods, endpoint paths, status codes, query parameters, request/response bodies, client IP, user agent, and latency down to the millisecond.
- Provides per-user data isolation and high-performance asynchronous logging to PostgreSQL.

### 🔍 Dynamic Endpoint Discovery & Normalization
- Automatically clusters observed traffic into parameterized endpoints (e.g. `/api/v1/users/1001` → `/api/v1/users/{id}`).
- Aggregates call counts, error rates, average latency, and drift status across the entire API surface.

### 🧠 AI-Powered Behavioral Analysis
- Evaluates real HTTP payloads, response patterns, and edge cases to construct behavioral summaries of what endpoints actually do in production.
- Detects error spikes, latency anomalies, and schema discrepancies.

### 🔄 Git-Aware Drift Detection
- Fetches repository file trees, source files, dependencies, and commit history via the GitHub REST API.
- Compares commit diffs against existing README and markdown documentation to identify behavioral and architectural drift.

### 📝 Autonomous Documentation Generation
- Produces clean, publication-ready API references, comprehensive READMEs, usage guides, and full **OpenAPI 3.0 JSON specifications**.
- Automatically captures edge cases and request/response examples derived from real execution logs.

### 🚀 Automated GitHub Pull Requests
- Creates a dedicated branch (`driftguard/update-docs`), commits updated documentation files (`README.md`, `DOCUMENTATION.md`, or custom paths), and opens a Pull Request with an AI-generated drift summary and review checklist.

### 🔌 Multi-LLM Provider Architecture
- Prioritized LLM fallback system:
  1. **OpenRouter** (Claude 3.5 Sonnet / GPT-4o)
  2. **Groq** (Llama 3.3 70B Versatile — high-throughput, low-latency)
  3. **Google Gemini** (Gemini 2.5 Flash / Gemini 2.0 Flash)

---

## 🏗️ How It Works

DriftGuard captures runtime HTTP telemetry, correlates it with source code extracted from Git repositories, and runs structured AI graph workflows to detect discrepancies:

```mermaid
flowchart LR
    A[Live API Traffic] --> B[Traffic Capture Middleware]
    B --> C[(PostgreSQL)]
    C --> D[Endpoint Intelligence]

    E[GitHub Repository] --> F[Source Code + Git Diffs]

    D --> G[LangGraph AI Pipeline]
    F --> G

    G --> H[Behavior Analysis]
    H --> I[Drift Detection]
    I --> J[Documentation Generation]

    J --> K[GitHub Branch]
    K --> L[Documentation Commit]
    L --> M[Pull Request]
```

---

## 🤖 LangGraph AI Pipeline

DriftGuard leverages **LangGraph** to model the AI analysis workflow as a typed, deterministic state machine:

```
[analyze_behavior] ──► [detect_drift] ──► [generate_docs] ──► END
```

### Pipeline Nodes

1. **`analyze_behavior`**:
   - Ingests recent API execution logs (methods, paths, status codes, latencies).
   - Generates a concise summary of the endpoint's functional behavior, normal operation patterns, and edge cases.

2. **`detect_drift`**:
   - Calculates error rates, latency spikes, and payload changes.
   - Evaluates sample response bodies against expected behavior to flag anomalies and provide a drift reason.

3. **`generate_docs`**:
   - Synthesizes the behavioral analysis into markdown documentation, edge case catalogs, and structured request/response examples.

```python
# Shared LangGraph State
class AnalysisState(TypedDict):
    endpoint_method:   str
    endpoint_path:     str
    logs:              List[Dict[str, Any]]
    behavior_summary:  str
    drift_detected:    bool
    drift_description: Optional[str]
    documentation:     str
    edge_cases:        List[str]
    examples:          List[Dict[str, Any]]
    error:             Optional[str]
```

---

## 🐙 GitHub Automation Workflow

When documentation drift is detected or documentation is regenerated, DriftGuard executes an autonomous GitHub workflow:

```
1. Repository Analysis
   └── Inspects repository tree, source code files, and dependency manifests.

2. Commit Diff Analysis
   └── Compares recent commits to detect code changes since last documentation update.

3. Documentation Drift Detection
   └── LLM compares code changes against existing docs to confirm if docs are outdated.

4. Documentation Generation
   └── Writes a complete, production-grade documentation file with API references.

5. Branch Creation
   └── Creates an isolated branch (e.g. driftguard/update-docs) from default branch.

6. File Commit
   └── Commits the updated documentation to the target path.

7. Pull Request Submission
   └── Opens a Pull Request with drift summary, changed files list, and merge checklist.
```

> **Why Pull Requests?** DriftGuard enforces a human-in-the-loop workflow. Automated changes are proposed as reviewable pull requests rather than silently overwriting the primary branch.

---

## 💻 Technology Stack

| Layer | Technology | Description |
|---|---|---|
| **Frontend** | HTML5, TailwindCSS, Alpine.js, Chart.js | Responsive, accessible developer console with dark/light mode parity |
| **Backend** | Python 3.11+, FastAPI, Uvicorn, Starlette | High-performance asynchronous REST API and traffic capture middleware |
| **Database** | PostgreSQL, Neon Serverless | Relational database for logs, endpoints, user accounts, and doc history |
| **ORM & Driver** | SQLAlchemy 2.0 (Async), asyncpg | Fully asynchronous database queries and connection pooling |
| **AI Orchestration** | LangGraph, LangChain Core | Deterministic multi-step state graph execution |
| **LLM Integrations** | OpenRouter, Groq, Google Gemini | Flexible multi-provider support (Claude 3.5 Sonnet, Llama 3.3 70B, Gemini 2.5 Flash) |
| **Authentication** | JWT (PyJWT), GitHub OAuth 2.0 | Secure session tokens and OAuth repository integration |
| **Git Automation** | GitHub REST API (httpx) | Branch creation, tree analysis, file commits, and PR management |
| **Observability** | OpenTelemetry | Distributed tracing and telemetry instrumentation |
| **Deployment** | Docker | Portable containerization ready for cloud deployments |

---

## 📁 Project Structure

```text
DriftGuard/
├── app/
│   ├── __init__.py
│   ├── config.py                  # Pydantic Settings & environment loader
│   ├── database.py                # SQLAlchemy async engine & session management
│   ├── deps.py                    # FastAPI authentication dependencies
│   ├── main.py                    # Application entry point & demo endpoints
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── traffic_capture.py     # Non-blocking HTTP request/response interceptor
│   ├── models/
│   │   ├── __init__.py
│   │   ├── api_log.py             # Log entry SQLAlchemy model
│   │   ├── doc_history.py         # PR & documentation history model
│   │   ├── documentation.py       # Versioned documentation model
│   │   └── endpoint.py            # Discovered endpoint model
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py                # JWT auth & GitHub OAuth endpoints
│   │   ├── dashboard.py           # Metrics, stats, and analytics router
│   │   ├── docs_router.py         # Documentation & OpenAPI export router
│   │   ├── endpoints.py           # Endpoint discovery & drift re-analysis
│   │   ├── github.py              # GitHub connection, analysis & PR router
│   │   └── logs.py                # Traffic logs query router
│   ├── schemas/
│   │   └── __init__.py            # Pydantic request/response schemas
│   └── services/
│       ├── __init__.py
│       ├── ai_service.py          # LangGraph state graph & LLM provider logic
│       ├── background_tasks.py    # Background stats refresh & maintenance
│       ├── endpoint_service.py    # Endpoint aggregation & drift tracking
│       └── log_service.py         # Log retrieval & filtering service
├── frontend/
│   └── index.html                 # Complete single-page Alpine.js console
├── Dockerfile                     # Docker container configuration
├── LICENSE                        # MIT License
├── migration_user_isolation.py    # Database migration helper
├── README.md                      # Project documentation
└── requirements.txt               # Python package dependencies
```

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.11+** installed
- **PostgreSQL database** (local PostgreSQL or cloud instance like Neon)
- **Git** installed
- API key for at least one supported LLM provider:
  - OpenRouter (`OPENROUTER_API_KEY`)
  - Groq (`GROK_API_KEY`)
  - Google Gemini (`GEMINI_API_KEY`)
- GitHub Personal Access Token (PAT) with `repo` scope or GitHub OAuth App credentials.

---

### Step-by-Step Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/Mohith-R17/DriftGuard.git
cd DriftGuard
```

#### 2. Create and Activate Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Configure Environment Variables
Create a `.env` file in the project root:

```env
# Application
APP_NAME=DriftGuard
APP_VERSION=1.0.0
DEBUG=False
SECRET_KEY=generate_a_secure_random_string_here

# Database (PostgreSQL / Neon)
DATABASE_URL=postgresql+asyncpg://username:password@hostname:5432/database_name

# AI Providers (configure at least one)
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet

GROK_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile

GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash

# GitHub Integration
GITHUB_TOKEN=your_github_personal_access_token
GITHUB_CLIENT_ID=your_github_oauth_client_id
GITHUB_CLIENT_SECRET=your_github_oauth_client_secret
GITHUB_OAUTH_REDIRECT=http://localhost:8000/api/auth/github/callback

# Frontend & CORS
FRONTEND_URL=http://localhost:5500
CORS_ORIGINS=http://localhost:5500,http://127.0.0.1:5500,http://localhost:3000
```

#### 5. Run Database Migrations
```bash
python migration_user_isolation.py
```

#### 6. Start the Backend Server
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
The FastAPI backend will start at `http://127.0.0.1:8000`. Interactive API docs are available at `http://127.0.0.1:8000/docs`.

#### 7. Start the Frontend Server
In a new terminal window:
```bash
python -m http.server 5500 --directory frontend
```

#### 8. Open the Application
Navigate to `http://localhost:5500` in your web browser.

---

## ⚙️ Environment Variables

| Variable | Required | Description |
|---|---|---|
| `DATABASE_URL` | **Yes** | PostgreSQL connection URL using `postgresql+asyncpg://` protocol |
| `SECRET_KEY` | **Yes** | Secret key for JWT signing and session validation |
| `OPENROUTER_API_KEY` | Optional | OpenRouter API key for Claude 3.5 Sonnet / GPT-4o inference |
| `OPENROUTER_MODEL` | Optional | Model identifier for OpenRouter (default: `anthropic/claude-3.5-sonnet`) |
| `GROK_API_KEY` | Optional | Groq API key for Llama 3.3 70B high-throughput inference |
| `GROQ_MODEL` | Optional | Model identifier for Groq (default: `llama-3.3-70b-versatile`) |
| `GEMINI_API_KEY` | Optional | Google Gemini API key for fallback inference |
| `GEMINI_MODEL` | Optional | Model identifier for Gemini (default: `gemini-2.5-flash`) |
| `GITHUB_TOKEN` | Optional | GitHub PAT for server-level fallback on Git write operations |
| `GITHUB_CLIENT_ID` | Optional | GitHub OAuth App Client ID for user sign-in |
| `GITHUB_CLIENT_SECRET` | Optional | GitHub OAuth App Client Secret |
| `GITHUB_OAUTH_REDIRECT` | Optional | OAuth callback URL (default: `http://localhost:8000/api/auth/github/callback`) |
| `FRONTEND_URL` | Optional | URL of the frontend application (default: `http://localhost:5500`) |
| `CORS_ORIGINS` | Optional | Comma-separated list of allowed CORS origins |

---

## 📊 Current Capabilities vs. Future Scope

### ✅ Currently Implemented & Working
- [x] Non-intrusive FastAPI traffic capture middleware with latency and payload logging.
- [x] Dynamic endpoint path discovery and parameter normalization.
- [x] Multi-provider LLM integration with automatic priority fallbacks.
- [x] LangGraph 3-node state machine (`analyze_behavior` → `detect_drift` → `generate_docs`).
- [x] Full OpenAPI 3.0 specification export based on observed traffic.
- [x] GitHub REST API integration for tree inspection, commit comparisons, and source file retrieval.
- [x] Autonomous Git branch creation, documentation commits, and Pull Request submission.
- [x] Multi-tier token resolution (Request Payload → User OAuth Database Record → Environment Fallback).
- [x] Modern, accessible developer console with dark/light mode support.

### 🔮 Future Roadmap
- [ ] Automated GitHub webhook listener for real-time push event drift checking.
- [ ] Bidirectional OpenAPI specification synchronization via Pull Requests.
- [ ] Multi-repository organization workspace management.
- [ ] Webhook alerts for Slack, Discord, and Microsoft Teams on drift detection.
- [ ] Framework middleware adapters for Express.js, Spring Boot, and Go Gin.

---

## 🔒 Security Notes

- **Never Commit Secrets:** The `.gitignore` file is pre-configured to ignore `.env`, virtual environments, and local logs. Never push secrets or API keys to version control.
- **Least Privilege Access:** When using Personal Access Tokens (PATs), grant only the minimum required permissions (`repo` scope for read/write repository access).
- **Human-in-the-Loop:** DriftGuard creates Pull Requests instead of committing directly to `main`, ensuring all automated documentation changes are verified by a developer.
- **Token Protection:** Tokens and secrets are masked in logs and never returned in public API responses.

---

## 🎮 Demo Workflow

1. **Sign In**: Open `http://localhost:5500` and sign in or create an account.
2. **View Traffic Logs**: Inspect the live HTTP traffic captured by the middleware.
3. **Explore Endpoints**: View discovered endpoints and aggregated latency metrics in the *Overview* tab.
4. **Inspect API Intelligence**: View AI-generated summaries, edge cases, and request/response examples.
5. **Re-Analyze Endpoint**: Trigger the LangGraph pipeline to re-evaluate endpoint behavior against recent traffic.
6. **Connect GitHub Repository**: Navigate to *GitHub Integration* and enter a repository URL (e.g. `https://github.com/Mohith-R17/tracestory`).
7. **Analyze Repository**: DriftGuard scans the repository files, inspects recent commits, and compares them with documentation.
8. **Select Destination**: Choose whether to update `README.md`, create `DOCUMENTATION.md`, or write to a custom path.
9. **Generate Docs & Open PR**: Click **Generate Documentation & Open PR**.
10. **Review on GitHub**: Click the generated Pull Request link on GitHub, inspect the automated diff, and merge!

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

*Built with ❤️ for developers who believe documentation should always reflect reality.*

</div>
