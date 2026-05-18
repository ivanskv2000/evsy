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
3. **Execution:** Apply code modifications within the tightly scoped workspace directory.
4. **Code Quality & Validation:** Before asking for user confirmation, you must ensure the code is clean and passes all local checks. Run the following commands based on the affected workspace:
   - **If Backend changed:** Run `make format` followed by `make lint` inside the `/backend` directory.
   - **If Frontend changed:** Run `npm run format` followed by `npm run lint` inside the `/frontend` directory.
5. **Testing Suite Execution:** Run the test suite to ensure zero regressions. You must invoke tests in **non-interactive, run-once mode** so the process does not hang:
   - **Backend:** Run `make test` from the `/backend` folder.
   - **Frontend:** Run `npm run test:unit -- --run` (or the equivalent non-watching continuous integration command) from the `/frontend` folder.
6. **Test Coverage Prompt:** Once checks pass, explicitly prompt the user: *"Would you like me to prepare or update any unit tests specific to these changes before we commit?"*
7. **Finalize:** Upon user validation, stage and commit changes with concise, structured commit messages following the Conventional Commits format.
8. **Documentation:** Auto-generate or update a pull request summary saving it directly to `pr_description.md` in the project root. The layout of this file must copy the formal structure defined in the repository's native GitHub file: `.github/PULL_REQUEST_TEMPLATE.md`.
9. 
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

---

## 🏁 Completion Signal
When every protocol step is completely finished, your final output to the user MUST explicitly print this statement on a standalone line for tracking visibility:

🚀 **Success! Pull Request documentation has been successfully generated/updated in `pr_description.md`.**