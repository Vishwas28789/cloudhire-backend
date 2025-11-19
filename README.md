# CloudHire Nexus Backend

A production-grade Python FastAPI backend for automated job searching, application management, and follow-up automation.

## Features

### Dual-Mode Operation
- **AI Mode**: Automated resume generation, message crafting, and intelligent matching using OpenAI
- **Manual Mode**: Zero AI dependencies - users provide content directly

### Core Capabilities
- Job source management (manual URL, text paste, CSV import)
- Smart job classification and filtering
- Visa sponsorship detection
- Intelligent job scoring (0-100)
- PDF resume generation with multiple templates
- Email automation with rotating identities
- Application tracking and follow-up management
- Dashboard analytics and metrics

## Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL database

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your database credentials and optional API keys

# Run the application
uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload
```

### Database Setup

The application automatically creates all required tables on startup.

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:5000/docs
- **ReDoc**: http://localhost:5000/redoc

## Project Structure

```
cloudhire-nexus-backend/
├── app/
│   ├── main.py                 # FastAPI application
│   ├── config.py               # Configuration management
│   ├── db.py                   # Database connection
│   ├── models/                 # SQLModel database models
│   ├── schemas/                # Pydantic validation schemas
│   ├── routes/                 # API route handlers
│   └── utils/                  # Utility modules
├── worker/
│   ├── worker_main.py          # Background worker
│   └── utils/                  # Worker utilities
└── requirements.txt
```

## Configuration

### AI Mode (Optional)
Set `OPENAI_API_KEY` in your environment or through the settings API to enable:
- Automated resume bullet generation
- Tailored job summaries
- Recruiter message generation
- Callback/offer predictions

### Manual Mode (Default)
Works without any AI API keys. Users provide:
- Resume content via API
- Message templates
- HR responses

## API Routes

### Jobs
- `GET /api/jobs` - List all jobs
- `POST /api/jobs` - Add new job
- `GET /api/jobs/search` - Search jobs
- `POST /api/jobs/apply/{job_id}` - Apply to job
- `GET /api/jobs/status` - Get application statuses

### Resumes
- `POST /api/resumes/new` - Generate new resume
- `GET /api/resumes/history` - Resume history
- `GET /api/resumes/{resume_id}/download` - Download PDF

### Settings
- `GET /api/settings` - Get user settings
- `PUT /api/settings` - Update settings

### AI
- `POST /api/ai/generate` - Generate AI content
- `POST /api/ai/manual-input` - Submit manual content

### Dashboard
- `GET /api/dashboard/metrics` - Get analytics

### Health
- `GET /api/health` - Health check

## Worker System

Background worker handles:
- Job processing and classification
- Automated applications
- Follow-up scheduling
- Email sending

Start worker:
```bash
python worker/worker_main.py
```

## Deployment

### Railway

```bash
# Install Railway CLI
npm i -g @railway/cli

# Deploy
railway login
railway init
railway up
```

### Docker

```bash
# Build
docker build -t cloudhire-nexus-backend .

# Run
docker run -p 5000:5000 --env-file .env cloudhire-nexus-backend
```

## Security Considerations

**IMPORTANT**: This is a development version. Before deploying to production:

1. **Add Authentication**: All API endpoints are currently unauthenticated. You must add API key authentication or OAuth before exposing to the internet.
2. **Secure Sensitive Endpoints**: The `/api/settings` endpoint returns and accepts sensitive data (API keys, SMTP passwords). Implement proper access controls.
3. **Environment Variables**: Never commit real API keys or passwords to version control.
4. **HTTPS Only**: Always use HTTPS in production to encrypt sensitive data in transit.

Example authentication middleware (add to `app/main.py`):
```python
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

API_KEY_HEADER = APIKeyHeader(name="X-API-Key")

async def verify_api_key(api_key: str = Security(API_KEY_HEADER)):
    if api_key != os.getenv("API_KEY"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key"
        )
    return api_key
```

## License

MIT License
