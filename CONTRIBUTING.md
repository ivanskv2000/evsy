# Contributing to Evsy

First of all — **thank you** for considering a contribution to **Evsy**!  
We deeply appreciate every bit of help, whether it's fixing a bug, suggesting an improvement, or just pointing out something unclear.

## 🫶 You don’t have to code to contribute

We welcome all kinds of contributions:

- 🐛 **Bug reports** — Found something broken? Let us know!
- 💡 **Feature suggestions** — Got an idea to improve Evsy?
- 🎨 **Design help** — We love thoughtful UI/UX suggestions.
- 📚 **Docs feedback** — Is something unclear? Missing? Tell us.
- 🙏 Just saying “this helped” — Encouragement matters, too.

Create an [issue](https://github.com/ivanskv2000/evsy/issues) or open a [discussion](https://github.com/ivanskv2000/evsy/discussions) — we’d love to hear from you.

---

## 🧑‍💻 If you do want to contribute code

### Backend (FastAPI, Poetry)

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

### Frontend (Vue 3, Vite)

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
   npm run format
   npm run lint
   ```

## Opening a pull request

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
