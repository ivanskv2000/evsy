# Evsy
Evsy is a lightweight admin panel for managing and documenting product analytics events and their properties.

(!) Evsy is currently in active development. Expect rapid improvements and frequent updates!

## ✨ About
Evsy is an open-source application for managing analytics events — including event descriptions, their attributes (fields), and tags.

It helps product teams, analysts, and developers structure and document their events in a convenient, extensible way.

## 📚 Features
- Create and document events and fields.
- Organize them by type, tag, or team.
- Export events to Swagger schemas.
- Sign up via email/password or OAuth2 (GitHub & Google)

**Future roadmap includes:**
- Roles and user management;
- Audit log (history of changes) and event versioning;
- Full-text search;
- Additional event states (`draft`, `archived`);
- Markdown descriptions;
- Grafana integration;
- ... and more!

## 🚀 Quick Start
To run Evsy via Docker compose, do:
1. `cp .env.example .env`
2. `make up`

### Alternative: deploy to Render
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/ivanskv2000/evsy)

## ⚙️ Tech Stack
- Backend: FastAPI + Pydantic + SQLAlchemy + Alembic
- Frontend: Vue 3 + Vite + Shadcn

## 🧩 Project Structure
Evsy is a project combining a Python backend and a modern JS frontend, developed and versioned together.

```
evsy/
├── backend/              # FastAPI backend (Python, Poetry-managed)
│   ├── app/              # Application code
│   └── tests/            # Pytest test suite
├── frontend/             # Vue 3 + Vite frontend (npm-managed)
│   ├── src/              # Application code
│   └── public/           # Static assets
├── .github/workflows/    # CI workflows
├── VERSION               # Current version of the project
├── bump_version.py       # Version bumping script (manual semantic versioning)
├── Makefile              # Developer commands (e.g. `make up`)
├── docker-compose.yaml   # Docker compose configuration
├── Makefile              # Developer commands (e.g. `make up`)
└── README.md             # Project overview
```

## 🤝 Contributing
We welcome all kinds of contributions — code, ideas, design suggestions, and bug reports.
[Read the contributing guide →](CONTRIBUTING.md)

## Build Status
[![Backend CI](https://github.com/ivanskv2000/evsy/actions/workflows/backend.yml/badge.svg)](https://github.com/ivanskv2000/evsy/actions/workflows/backend.yml)
[![Frontend CI](https://github.com/ivanskv2000/evsy/actions/workflows/frontend.yml/badge.svg)](https://github.com/ivanskv2000/evsy/actions/workflows/frontend.yml)




