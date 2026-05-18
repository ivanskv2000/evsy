# Global AI Agent Guidelines (Evsy Monorepo)

## 📦 Project Overview
- **Repository Structure:** Single monorepo divided into two distinct operational scopes.
  - `/backend`: Python FastAPI application.
  - `/frontend`: Vue 3 + Vite + Shadcn-vue single-page application.
- **Goal:** Maintain professional, production-grade architecture, keeping abstractions clean, readable, and highly maintainable.

## 🚦 Strict Workflow Protocol
Before modifying, generating, or deleting any files, the agent MUST follow these steps in exact order:
1. **Plan First:** Present a comprehensive architectural review, design summary, or pseudo-code strategy. Wait for explicit user greenlight.
2. **Git Branching:** Checkout to a distinct feature or refactor branch from `main` using the Conventional Commits specification (e.g., `feat(backend)/...`, `refactor(frontend)/...`).
3. **Execution:** Apply the changes within the tightly scoped workspace directory.
4. **Finalize:** Upon user validation, stage and commit changes with concise, structured commit messages.
5. **Documentation:** Auto-generate a pull request summary titled `pr_description.md` in the project root adhering to the workspace markdown template.

---

## 🐍 Backend Specifics (`/backend`)
*Focus rules when operating within the backend directory:*
- **Framework:** FastAPI utilizing Pydantic for data validation and configuration management (`pydantic-settings`).
- **Isolation:** Strictly separate environment settings (Dev, Demo, Prod) via an environment variable switch.
- **Testing Requirements:** Test configurations must run against completely isolated, non-destructive transactional test databases.

---

## 🍦 Frontend Specifics (`/frontend`)
*Focus rules when operating within the frontend directory:*
- **Framework Stack:** Vue 3 (Composition API, `<script setup>`), Vite, Tailwind CSS v4, and Shadcn-vue via `reka-ui`.
- **State Management:** Server state must be tightly managed via TanStack Query (Vue Query). Pinia is strictly reserved for transient global application primitives like Authentication.
- **Data Synchronization:** UI component tables must synchronize filtering, sorting, and pagination state unidirectionally using TanStack Table's native state updaters feeding directly into `vue-router` query parameters. Avoid redundant watchers or cyclical loop patterns.