# Contributing to SADOCKDOG Platform 🤝

First off, thank you for considering contributing to SADOCKDOG! It's people like you that make SADOCKDOG such a great platform.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Commit Messages](#commit-messages)
- [Testing](#testing)
- [Documentation](#documentation)

## 📜 Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## 🚀 Getting Started

### Prerequisites

- Docker & Docker Compose V2
- Python 3.13+
- Node.js 20+
- pnpm 8+
- Git
- VSCode (recommended)

### Setup Development Environment

1. **Fork and Clone**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/SADOCKDOG.git
   cd SADOCKDOG/autogpt_platform
   ```

2. **Set up environment**:
   ```bash
   cp .env.default .env
   # Edit .env with your configuration
   ```

3. **Start services**:
   ```bash
   docker compose up -d
   ```

4. **Verify setup**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8006/docs
   - SADOCKDOG Chat: http://localhost:3000/sadockdog

## 🔄 Development Workflow

### Branch Strategy

- `master` - Production-ready code
- `dev` - Development branch
- `feature/*` - New features
- `fix/*` - Bug fixes
- `docs/*` - Documentation updates
- `refactor/*` - Code refactoring

### Creating a Feature

```bash
# Create feature branch from dev
git checkout dev
git pull origin dev
git checkout -b feature/your-feature-name

# Make changes, commit, push
git add .
git commit -m "feat: add your feature"
git push origin feature/your-feature-name

# Create PR on GitHub
```

## 📝 Pull Request Process

1. **Before Creating PR**:
   - [ ] Update documentation if needed
   - [ ] Add/update tests
   - [ ] Run tests locally
   - [ ] Check code formatting
   - [ ] Update CHANGELOG.md (if applicable)

2. **PR Requirements**:
   - [ ] Fill out PR template completely
   - [ ] Link related issues
   - [ ] Ensure CI checks pass
   - [ ] Request review
   - [ ] Resolve all conversations

3. **PR Title Format**:
   ```
   <type>(<scope>): <description>
   
   Examples:
   feat(backend): add Android agent execution endpoint
   fix(frontend): resolve SADOCKDOG chat connection issue
   docs(readme): update installation instructions
   ```

4. **Review Process**:
   - Maintainers will review within 2-3 business days
   - Address feedback promptly
   - Keep PR updated with master
   - Be patient and respectful

## 💻 Coding Standards

### Backend (Python)

```python
# Use Black for formatting
poetry run black .

# Use isort for imports
poetry run isort .

# Use ruff for linting
poetry run ruff check .

# Type hints required
def process_agent(agent_id: str, config: dict) -> AgentResponse:
    ...

# Docstrings for public functions
def create_android_app(name: str) -> App:
    """
    Creates a new Android application.
    
    Args:
        name: The application name
        
    Returns:
        App instance with configuration
    """
    ...
```

### Frontend (TypeScript/React)

```typescript
// Use function declarations for components
function AgentSelector({ agents }: Props) {
  // Component logic
}

// Separate business logic into hooks
function useAgentSelector() {
  // Hook logic
}

// Use design system components
import { Button } from "@/components/ui/button";

// Phosphor Icons only
import { RocketLaunch } from "@phosphor-icons/react";
```

### File Organization

```
backend/
  backend/
    blocks/           # Agent blocks
      android/       # Android-specific blocks
        __init__.py
        android_agent.py
        test_android_agent.py
    
frontend/
  src/
    app/
      (platform)/
        sadockdog/   # SADOCKDOG features
          page.tsx
          useSadockdog.ts
          components/
```

## 💬 Commit Messages

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting, missing semi-colons, etc
- `refactor`: Code restructuring
- `perf`: Performance improvements
- `test`: Adding tests
- `chore`: Maintenance tasks
- `ci`: CI/CD changes

### Scopes:
- `backend`
- `frontend`
- `android-agent`
- `cli`
- `manager`
- `docker`
- `docs`

### Examples:

```bash
feat(android-agent): add Material Design 3 support
fix(backend): resolve agent execution timeout
docs(readme): update SADOCKDOG setup instructions
refactor(frontend): extract agent selector logic to hook
test(backend): add tests for Android agent creation
ci: add CodeQL security scanning workflow
```

## 🧪 Testing

### Backend Tests

```bash
cd backend

# Run all tests
poetry run pytest

# Run specific test
poetry run pytest backend/blocks/test/test_block.py -xvs

# Run with coverage
poetry run pytest --cov=backend --cov-report=html
```

### Frontend Tests

```bash
cd frontend

# Run E2E tests
pnpm test

# Run component tests (Storybook)
pnpm storybook

# Type checking
pnpm types
```

### Test Requirements

- All new features must include tests
- Bug fixes should include regression tests
- Aim for >80% code coverage
- Tests must pass before PR merge

## 📚 Documentation

### What to Document

- New features or changes to existing features
- New API endpoints
- Configuration options
- Breaking changes
- Usage examples

### Where to Document

- **Code**: Inline comments and docstrings
- **README.md**: High-level overview and getting started
- **SECURITY.md**: Security-related features
- **API docs**: Swagger/OpenAPI in backend
- **Storybook**: Component documentation in frontend

### Documentation Style

```markdown
## Feature Name

Brief description of what it does.

### Usage

\`\`\`python
# Example code
result = do_something(param="value")
\`\`\`

### Parameters

- `param` (str): Description

### Returns

- Description of return value
```

## 🎯 Areas for Contribution

Looking for ideas? Here are some areas we'd love help with:

### High Priority
- 🐛 Bug fixes
- 📚 Documentation improvements
- ✅ Test coverage
- ♿ Accessibility improvements

### Features
- 🤖 New agent types
- 🔌 Integration blocks
- 📱 Mobile interface improvements
- 🎨 UI/UX enhancements

### Infrastructure
- 🚀 Performance optimizations
- 🔒 Security enhancements
- 📊 Monitoring and observability
- 🐳 Docker improvements

## ❓ Questions?

- 💬 Create a [Discussion](https://github.com/SADOCKDOG/SADOCKDOG/discussions)
- 🐛 Open an [Issue](https://github.com/SADOCKDOG/SADOCKDOG/issues)
- 📧 Email the maintainers

## 📜 License

By contributing, you agree that your contributions will be licensed under the PolyForm Shield License 1.0.0.

## 🙏 Thank You!

Your contributions make SADOCKDOG better for everyone. We appreciate your time and effort!

---

**Happy Contributing! 🎉**

*Last updated: November 8, 2025*
