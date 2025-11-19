# CloudHire Nexus Backend

## Project Overview
CloudHire Nexus is a production-grade Python FastAPI backend for automated job searching, application management, and follow-up automation. The system is designed to help job seekers streamline their job application process with intelligent automation and tracking.

## Current State
- **Status**: Fully functional backend API running on port 5000
- **Database**: PostgreSQL with all tables created and relationships established
- **API Documentation**: Available at `/docs` (Swagger UI) and `/redoc` (ReDoc)
- **Health Status**: API is healthy and responding to requests

## Architecture

### Dual-Mode Operation
The system supports two distinct operation modes:

1. **AI Mode (Optional)**
   - Requires OpenAI API key
   - Automatically generates resume bullets, summaries, and recruiter messages
   - Provides intelligent content tailored to each job
   - Can be toggled on/off via settings API

2. **Manual Mode (Default - FREE)**
   - Zero AI dependencies
   - Users provide all content through API endpoints
   - Full automation still available for email sending, follow-ups, and tracking
   - No external API costs

### Core Components

#### Database Models (`app/models/`)
- **User**: Profile information, preferences, salary expectations, visa requirements
- **Job**: Job listings with classification, scoring, and application tracking
- **Resume**: Generated resumes with version tracking and performance metrics
- **EmailLog**: Email delivery tracking with status and error handling
- **Followup**: Scheduled follow-up management
- **Settings**: User preferences and API key management

#### API Routes (`app/routes/`)
- **/api/health**: System health check
- **/api/jobs**: Job CRUD operations, search, import (CSV/text/URL), status tracking
- **/api/resumes**: Resume generation, history, download
- **/api/apply**: Application submission with email automation
- **/api/followups**: Follow-up scheduling and sending
- **/api/settings**: User settings management (AI mode, email identities, preferences)
- **/api/ai**: AI content generation and manual input submission
- **/api/dashboard**: Analytics and metrics (callback rates, success by country/role/template)

#### Utilities (`app/utils/`)
- **classification.py**: Job role classification (Cloud Engineer, DevOps, Support, etc.)
- **visa_detector.py**: Visa sponsorship keyword detection
- **scoring.py**: Job scoring algorithm (0-100) based on user preferences
- **parser.py**: CSV and text parsing for job imports
- **scraper.py**: Basic web scraping for job URLs
- **ai_engine.py**: OpenAI integration with fallback to manual mode
- **pdf_resume.py**: PDF generation with ReportLab (multiple templates)
- **email_sender.py**: SMTP email sending with rotating identities
- **message_builder.py**: Message generation for recruiters and follow-ups
- **logger.py**: Centralized logging configuration

#### Background Worker (`worker/`)
- **worker_main.py**: APScheduler-based background worker
- **scheduler.py**: Automatic follow-up scheduling
- **utils/notifier.py**: Webhook notifications

### Key Features Implemented

1. **Job Management**
   - Manual job entry, CSV import, text paste, URL scraping
   - Automatic classification (filters out coding-heavy roles)
   - Visa sponsorship detection
   - Intelligent scoring based on user preferences
   - Application status tracking

2. **Resume Generation**
   - PDF generation with clean 1-page templates
   - Multiple template types: Architect, Support, DevOps
   - AI-powered content generation (when enabled)
   - Resume versioning and performance tracking
   - Download functionality

3. **Application Automation**
   - Email sending with SMTP support
   - Rotating email identities for rate limiting
   - Resume attachment
   - Custom or AI-generated messages
   - Delivery status tracking

4. **Follow-up System**
   - Automatic follow-up scheduling (configurable delay)
   - Email-based follow-ups
   - Status tracking (scheduled, sent, failed)

5. **Analytics Dashboard**
   - Callback rate and offer rate tracking
   - Success metrics by country
   - Success metrics by role
   - Resume template effectiveness
   - Application timeline graphs

### Technology Stack
- **Framework**: FastAPI 0.104.1
- **Database**: PostgreSQL with SQLModel ORM
- **PDF Generation**: ReportLab
- **Email**: smtplib with SMTP support
- **Scheduling**: APScheduler for background tasks
- **AI**: OpenAI (optional)
- **Deployment**: Uvicorn ASGI server

## API Usage

### Quick Start
```bash
# Get API health
curl http://localhost:5000/api/health

# View interactive docs
http://localhost:5000/docs
```

### Common Workflows

#### 1. Add a Job
```bash
POST /api/jobs
{
  "title": "Cloud Engineer",
  "company": "Tech Corp",
  "location": "Remote",
  "description": "Looking for an experienced cloud engineer...",
  "country": "USA"
}
```

#### 2. Generate a Resume
```bash
POST /api/resumes/new
{
  "template_type": "architect",
  "use_ai": false,
  "bullets": [
    "Designed and deployed AWS infrastructure",
    "Managed Kubernetes clusters"
  ],
  "summary": "Cloud professional with 5 years experience"
}
```

#### 3. Apply to a Job
```bash
POST /api/apply/{job_id}
{
  "resume_id": 1,
  "recipient_email": "hr@company.com",
  "use_ai_message": false
}
```

#### 4. Configure Settings
```bash
PUT /api/settings
{
  "ai_mode_enabled": true,
  "openai_api_key": "sk-...",
  "followup_delay_days": 7,
  "message_tone": "professional"
}
```

### Dashboard Metrics
```bash
GET /api/dashboard/metrics
```
Returns comprehensive analytics including callback rates, offer rates, and success metrics by country/role/template.

## Environment Configuration

### Required Variables
- `DATABASE_URL`: PostgreSQL connection string (auto-configured in Replit)

### Optional Variables
- `OPENAI_API_KEY`: For AI mode (can also be set via API)
- `SMTP_SERVER`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD`: Email configuration

### Worker Configuration
The background worker can be started separately:
```bash
python worker/worker_main.py
```

It handles:
- Pending follow-up processing (every 30 minutes)
- Auto-apply workflow (every 6 hours, requires auto_apply_enabled in settings)
- Log cleanup (daily)

## Recent Changes
- 2025-11-19: Initial project creation
  - Complete backend implementation with all core features
  - Database schema with 6 tables and proper relationships
  - All API routes implemented and tested
  - Worker system with APScheduler
  - Dual AI/Manual mode support
  - PDF resume generation
  - Email automation
  - Dashboard analytics

## User Preferences
- **Framework**: FastAPI + PostgreSQL + SQLModel
- **Development Style**: Production-ready code with proper error handling
- **Deployment Target**: Replit (currently), Railway-compatible

## Project Structure
```
cloudhire-nexus-backend/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration management
│   ├── db.py                   # Database connection and session
│   ├── models/                 # SQLModel database models
│   │   ├── user.py
│   │   ├── job.py
│   │   ├── resume.py
│   │   ├── email_log.py
│   │   ├── followup.py
│   │   └── settings.py
│   ├── schemas/                # Pydantic validation schemas
│   │   ├── job_schema.py
│   │   ├── resume_schema.py
│   │   ├── apply_schema.py
│   │   ├── settings_schema.py
│   │   └── ai_schema.py
│   ├── routes/                 # API route handlers
│   │   ├── health.py
│   │   ├── jobs.py
│   │   ├── resumes.py
│   │   ├── apply.py
│   │   ├── followups.py
│   │   ├── settings.py
│   │   ├── ai.py
│   │   └── dashboard.py
│   └── utils/                  # Utility modules
│       ├── logger.py
│       ├── classification.py
│       ├── visa_detector.py
│       ├── scoring.py
│       ├── parser.py
│       ├── scraper.py
│       ├── ai_engine.py
│       ├── pdf_resume.py
│       ├── email_sender.py
│       └── message_builder.py
├── worker/
│   ├── worker_main.py          # Background worker with APScheduler
│   ├── scheduler.py            # Follow-up scheduling logic
│   └── utils/
│       └── notifier.py         # Webhook notifications
├── generated_resumes/          # Generated PDF storage
├── logs/                       # Application logs
├── uploads/                    # File uploads
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
├── README.md                   # Project documentation
├── .gitignore                  # Git ignore rules
└── .env.example                # Environment variables template
```

## Next Steps / Future Enhancements
Future phases could include:
- Web scraping integration for LinkedIn, Indeed, Naukri, Glassdoor
- Advanced analytics: job clusters, peak apply time analysis, hiring heatmap
- Resume A/B testing and template effectiveness tracking
- Slack/webhook notifications
- Company blacklist feature
- Role and country priority schedulers
- Message tone variations (Formal, Warm, Confident, Startup-friendly)

## Testing
API is currently running and verified:
- ✅ Health check endpoint responding
- ✅ Database tables created successfully
- ✅ All routes registered
- ✅ CORS enabled for frontend integration
- ✅ OpenAPI documentation available

## Security Notes

**CRITICAL - Development Version Only**:
- **No Authentication**: All API endpoints are currently unauthenticated. This is suitable for development/testing only.
- **Before Production**: You MUST add authentication (API key, OAuth, or JWT) to all endpoints, especially `/api/settings` which handles sensitive data.
- **Sensitive Data**: API keys and SMTP passwords are currently accessible through unauthenticated endpoints. Implement proper access controls before deployment.

## Known Limitations

1. **Follow-up Recipient Resolution**: The worker's automated follow-up system retrieves the recipient email from the original application EmailLog. If a job was manually added without applying through the system, follow-ups will use a placeholder address. 
   - **Workaround**: Always use the `/api/apply/{job_id}` endpoint to apply to jobs, which stores the recipient email.
   - **Future Enhancement**: Add a `contact_email` field to the Job model to store recruiter emails independently.

2. **Authentication**: No authentication layer is currently implemented (development only).

## Other Notes
- LSP diagnostics showing import warnings are expected until dependencies are installed (already done)
- The system uses job_metadata and email_metadata fields (not "metadata") to avoid SQLModel reserved words
- Email sending uses rotating identities for better deliverability
- PDF generation uses ReportLab for clean, professional resumes
- Worker system implements follow-up processing with email sending and status tracking
