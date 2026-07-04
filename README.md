# Nexus AI

Nexus AI is an AI infrastructure platform designed to simplify the development, deployment, and management of AI-powered applications.

Instead of directly integrating with individual LLM providers, Nexus AI aims to provide a unified backend for authentication, project management, API keys, intelligent model routing, evaluation, and future AI workflows.

---

## Current Progress

### Backend Foundation

- ✅ FastAPI application
- ✅ Configuration management using `.env`
- ✅ PostgreSQL integration
- ✅ SQLAlchemy ORM
- ✅ Alembic database migrations
- ✅ User model
- ✅ Initial `users` table

---

## Tech Stack

### Backend

- Python
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Pydantic Settings

### Development

- Git
- GitHub
- Uvicorn

---

## Project Structure

```text
backend/
├── alembic/
├── app/
│   ├── core/
│   ├── db/
│   ├── models/
│   └── main.py
├── alembic.ini
└── requirements.txt
```

---

## Roadmap

- [x] Backend setup
- [x] Configuration system
- [x] Database connection
- [x] User model
- [x] Database migrations
- [ ] Authentication
- [ ] Projects
- [ ] API Key Management
- [ ] AI Gateway
- [ ] Intelligent Model Router
- [ ] Evaluation Engine
- [ ] Dashboard

---

## Vision

The long-term goal of Nexus AI is to become a unified AI infrastructure platform that abstracts multiple AI providers behind a single interface while providing authentication, project management, observability, evaluation, and intelligent routing.

---

## Status

🚧 Currently under active development.


