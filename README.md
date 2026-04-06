# GitHub Cloud Connector

A clean, production-ready FastAPI backend that connects to the GitHub REST API.

---

## Project Structure

```
github-connector/
├── main.py                  # App entry point & router registration
├── requirements.txt
├── .env.example             # Token config template
├── config/
│   ├── __init__.py
│   └── settings.py          # Pydantic settings (reads .env)
├── services/
│   ├── __init__.py
│   └── github.py            # Reusable async GitHub API client
└── routes/
    ├── __init__.py
  ├── repos.py             # GET /repos | GET /commits
    └── issues.py            # GET /issues | POST /create-issue
```

---

## Setup

### 1. Clone / enter the project directory
```bash
cd github-connector
```

### 2. Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure your GitHub PAT
```bash
cp .env.example .env
```
Edit `.env` and replace `your_personal_access_token_here` with a real token.

Generate one at → https://github.com/settings/tokens  
Required scopes: **`repo`**, **`read:user`**

### 5. Run the server
```bash
uvicorn main:app --reload
```

Server starts at: `http://127.0.0.1:8000`  
Interactive docs: `http://127.0.0.1:8000/docs`

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/repos` | List repos of the authenticated user |
| GET | `/commits?owner=&repo=&per_page=&sha=` | Fetch commits for a repository |
| GET | `/issues?owner=&repo=` | List issues for a repository |
| POST | `/create-issue` | Create a new issue |

---

## Sample curl Commands

### Health check
```bash
curl http://localhost:8000/health
```

### Fetch authenticated user's repos
```bash
curl http://localhost:8000/repos
```

### List issues for a repo
```bash
curl "http://localhost:8000/issues?owner=octocat&repo=Hello-World"
```

### Fetch commits for a repo
```bash
curl "http://localhost:8000/commits?owner=octocat&repo=Hello-World&per_page=10"
```

### Create an issue
```bash
curl -X POST http://localhost:8000/create-issue \
  -H "Content-Type: application/json" \
  -d '{
    "owner": "your-username",
    "repo": "your-repo",
    "title": "Bug: something is broken",
    "body": "Steps to reproduce...\n1. Do this\n2. See error"
  }'
```

---

## Error Handling

| Scenario | HTTP Status |
|---|---|
| Invalid / expired token | 401 |
| Repo or resource not found | 404 |
| Validation error (bad input) | 422 |
| GitHub API unreachable | 503 |