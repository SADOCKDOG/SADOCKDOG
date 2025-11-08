# Contributing to SADOCKDOG Platform

Thank you for your interest in contributing to SADOCKDOG! 🐕

## 📋 Development Workflow

### 1. Fork & Setup
```bash
# Fork the repository on GitHub
git clone https://github.com/YOUR_USERNAME/SADOCKDOG.git
cd SADOCKDOG
git remote add upstream https://github.com/SADOCKDOG/SADOCKDOG.git
```

### 2. Create a Feature Branch
```bash
# Always branch from 'dev'
git checkout dev
git pull upstream dev
git checkout -b feature/your-feature-name
```

### 3. Make Your Changes

**Backend Development:**
```bash
cd autogpt_platform/backend
poetry install
poetry run ruff check .  # Lint
poetry run black .       # Format
poetry run pytest -v backend/util/test_json.py  # Test
```

**Frontend Development:**
```bash
cd autogpt_platform/frontend
pnpm install
pnpm lint                # ESLint + Prettier
pnpm types               # TypeScript check
pnpm build               # Build
```

### 4. Commit Your Changes

Follow conventional commits:
```bash
feat(backend): add new API endpoint for agent creation
fix(frontend): resolve chat interface scrolling issue
docs: update deployment guide
ci: optimize test execution time
chore: cleanup unused dependencies
```

### 5. Push & Create Pull Request
```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub targeting the `dev` branch.

## ✅ CI/CD Requirements

Your PR must pass all checks before merge:

### Required Checks
- ✅ **Backend CI - Lint & Format** (Ruff + Black) - ~48s
- ✅ **Backend CI - Tests** (pytest) - ~1m50s
- ✅ **Frontend CI - Lint & Build** (ESLint + Next.js) - ~4m30s
- ✅ **Frontend CI - TypeScript Check** - ~1m20s
- ✅ **CodeQL Security Analysis** - ~2-12min

### Status Checks
All checks are **required** to pass. Branch protection enforces:
- ✅ Tests must pass
- ✅ Branch must be up-to-date with base
- ✅ All conversations must be resolved

## 🐛 Reporting Bugs

Use GitHub Issues with the **Bug Report** template:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment (OS, Python/Node version)
- Screenshots/logs if applicable

## 💡 Suggesting Features

Use GitHub Issues with the **Feature Request** template:
- Problem description
- Proposed solution
- Alternative solutions considered
- Impact assessment

## 📝 Code Style

### Python (Backend)
- Follow [PEP 8](https://pep8.org/)
- Use [Ruff](https://github.com/astral-sh/ruff) for linting
- Use [Black](https://github.com/psf/black) for formatting
- Type hints for public APIs

### TypeScript (Frontend)
- ESLint + Prettier configuration
- Strict TypeScript mode
- React functional components with hooks
- Clear component structure

## 🔐 Security

- ⛔ **Never** commit secrets or API keys
- Use environment variables for configuration
- Report security issues privately

## 🧪 Testing

### Backend
```bash
# Single test
poetry run pytest backend/util/test_json.py -v

# With output
poetry run pytest -v --tb=short
```

### Frontend
```bash
# Tests coming soon
pnpm test
```

## 📚 Documentation

- Update README.md for new features
- Add docstrings for new functions
- Keep architecture docs in sync

## 🎯 Quick Start

### Run Backend
```bash
cd autogpt_platform/backend
cp .env.example .env  # Configure environment
poetry install
poetry run uvicorn backend.app:app --reload
```

### Run Frontend
```bash
cd autogpt_platform/frontend
pnpm install
pnpm dev
```

## 🤝 Code Review

1. **Automated checks** run (CI/CD)
2. **Maintainer review**
3. **Feedback resolution**
4. **Approval & merge** to `dev`

## 📦 Release Flow

```
feature/* → dev (testing) → master (production)
```

## 🙏 Recognition

Contributors appear in:
- [Contributors page](https://github.com/SADOCKDOG/SADOCKDOG/graphs/contributors)
- Release notes

---

**Happy Coding!** 🚀

By contributing, you agree to the [License](LICENSE.md).
