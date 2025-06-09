# Contributing to Evsy

First of all — **thank you** for considering a contribution to **Evsy**!  
We deeply appreciate every bit of help, whether it's fixing a bug, suggesting an improvement, or just pointing out something unclear.

## 🫶 You don’t have to code to contribute

Not a developer? No problem — Evsy welcomes all kinds of contributions:

- Report bugs — If something’s not working as expected, let us know.
- Suggest features — Ideas to improve workflows or usability are always appreciated.
- Give design feedback — UI/UX suggestions help us make Evsy more intuitive.
- Improve the docs — Flag anything confusing or missing.
- Share your experience — Even a quick "this was helpful" can go a long way.

You can open an [issue](https://github.com/ivanskv2000/evsy/issues) — we’d love to hear from you.


## 🧑‍💻 Contributing code

### Docker-compose setup (recommended)

You can setup both the backend and frontend in dev mode with hot-reloading:

```bash
make dev
```

This launches everything via `docker-compose.dev.yaml`:

- FastAPI backend on `localhost:8000`
- Vite frontend on `localhost:3000`


When you need to create a new migration:

```bash
make revision name="your_migration_name"
```

...and then apply it:

```bash
make migrate
```

After you're done developing, just do:

```bash
make down
```

Alternatively, you can setup your backend and frontend independently.

### Backend (FastAPI + Poetry)

1. **Install [Poetry](https://python-poetry.org/docs/#installation)**.
2. Install dependencies:

   ```bash
   cd ./backend
   poetry install
   cp .env.example .env
   ```

3. Run the server:

   ```bash
    make dev
   ```

4. Run tests:

   ```bash
   make test
   ```

5. Check formatting and style:

   ```bash
   make format && make lint
   ```

### Frontend (Vue 3 + Vite)

1. Install dependencies:

   ```bash
    cd ./frontend
    npm ci
    cp .env.example .env
   ```

2. Run the app:

   ```bash
    npm run dev
   ```

3. Lint and format:

   ```bash
   npm run format && npm run lint
   ```

## 📦 Opening a pull request

1. Create a new branch:
   ```bash
   git checkout -b feat/your-change
   ```

2. Use [Conventional Commits](https://www.conventionalcommits.org/) for commit messages:
```
feat: add something new
fix: fix a bug
docs: update documentation
refactor: improve internal code
chore: misc changes like configs
```

3.Push your branch and open a PR. CI will verify formatting, linting, and tests.
