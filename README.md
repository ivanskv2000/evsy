# Evsy
Evsy is a lightweight admin panel for managing and documenting product analytics events and their properties.

![Evsy main page screenshot.](screenshot.png)

Check out the live demo at [demo.evsy.dev](https://demo.evsy.dev/)
- Login: `demo@evsy.dev`
- Password: `bestructured`

## ✨ About
Evsy is an open-source application that helps product teams, analysts, and developers structure, document, and maintain a single source of truth for product analytics events and fields.

## 📚 Features
- Create and document events and fields.
- Organize by type, tag, or team.
- Export events as Swagger-compatible schemas.
- Sign in with email/password or OAuth2 (GitHub & Google).


**Future roadmap includes:**
- Role-based access control;
- History of changes and event versioning;
- Full-text search;
- ... and more!

## 🚀 Quick Start
To run Evsy via Docker compose, just do:
1. `cp .env.example .env`
2. `make up`

> Make sure to review .env.example &mdash; there are comments that might be useful for configuring your setup.

## ⚙️ Tech Stack
Evsy combines a Python FastAPI backend and a Vue3 frontend, developed and versioned together.

- Backend: FastAPI + Pydantic + SQLAlchemy + Alembic
- Frontend: Vue 3 + Vite
- Component library: [shadcn-vue](https://www.shadcn-vue.com/)

## 🤝 Contributing
We welcome all kinds of contributions: code, ideas, design suggestions, and bug reports.
[Read the contributing guide →](CONTRIBUTING.md)

## Build Status
[![Backend CI](https://github.com/ivanskv2000/evsy/actions/workflows/backend.yml/badge.svg)](https://github.com/ivanskv2000/evsy/actions/workflows/backend.yml)
[![Frontend CI](https://github.com/ivanskv2000/evsy/actions/workflows/frontend.yml/badge.svg)](https://github.com/ivanskv2000/evsy/actions/workflows/frontend.yml)




