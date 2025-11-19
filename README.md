CloudHire Nexus Backend

A production-grade Python FastAPI backend for automated job searching, application management, resume generation, recruiter outreach, and follow-up automation.

Features
Dual-Mode Operation

AI Mode: Automated resume generation, message crafting, Q&A generation, job scoring using OpenAI or other models.

Manual Mode: Zero AI — user provides text manually.

Core Capabilities

Worldwide job source management

Smart job classification (Cloud, Support, Architect, DevOps-lite)

Visa sponsorship detection

Intelligent job scoring (0–100)

Dynamic resume generation (per job, country, template)

Recruiter email discovery + messaging

Rotating email identities

Application tracking & timelines

Automated follow-up engine

Analytics dashboard

Quick Start
Prerequisites

Python 3.11+

PostgreSQL database

Installation
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload

API Documentation

Visit once running:

Swagger: /docs

ReDoc: /redoc

Project Structure
cloudhire-nexus-backend/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── db.py
│   ├── models/
│   ├── schemas/
│   ├── routes/
│   └── utils/
├── worker/
│   ├── worker_main.py
│   └── utils/
├── requirements.txt
└── Dockerfile

Deployment Options

Render (Free)

Railway

Docker

Local

Security Notice

This backend requires authentication before public use. Add an API key layer before exposing endpoints.

License

MIT License
