# 🧪 Testing Guide - SADOCKDOG Platform

## 📋 Overview

SADOCKDOG uses a comprehensive testing strategy to ensure code quality and reliability:

- **Backend**: pytest with fast/slow test separation
- **Frontend**: Vitest (unit tests) + Playwright (E2E tests)
- **CI/CD**: Automated testing on every PR/push

## 🐍 Backend Testing (Python)

### Test Organization

Tests are organized by type:
- **Unit tests**: Fast, isolated tests (default)
- **Integration tests**: Database/service integration
- **Slow tests**: Marked with `@pytest.mark.slow` (skipped in CI)

### Running Tests

**Run fast tests only (CI default):**
```bash
cd autogpt_platform/backend
poetry run pytest -v -m "not slow"
```

**Run all tests (including slow/integration):**
```bash
cd autogpt_platform/backend
poetry run pytest -v
```

**Run only slow tests:**
```bash
cd autogpt_platform/backend
poetry run pytest -v -m slow
```

**Run specific test file:**
```bash
cd autogpt_platform/backend
poetry run pytest -v backend/util/test_json.py
```

**Run with coverage:**
```bash
cd autogpt_platform/backend
poetry run pytest --cov=backend --cov-report=html
```

### Marking Tests as Slow

To mark a test as slow (integration/long-running):

```python
import pytest

@pytest.mark.slow
def test_complex_integration():
    # This test will be skipped in CI
    pass
```

### Test Database

Tests use an isolated PostgreSQL container:
- Automatically spun up by `run_tests.py`
- Reset before each test run
- Cleaned up after tests complete

## 🎨 Frontend Testing (TypeScript)

### Test Organization

- **Unit tests** (`.test.ts`, `.test.tsx`): Fast, isolated component/utility tests
- **E2E tests** (`.spec.ts`): Full user flow tests with Playwright

### Unit Tests (Vitest)

**Run unit tests:**
```bash
cd autogpt_platform/frontend
pnpm test:unit
```

**Run in watch mode:**
```bash
cd autogpt_platform/frontend
pnpm test:unit:watch
```

**Run with coverage:**
```bash
cd autogpt_platform/frontend
pnpm test:unit:coverage
```

**Example unit test:**
```typescript
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';

describe('MyComponent', () => {
  it('renders correctly', () => {
    render(<MyComponent title="Hello" />);
    expect(screen.getByText('Hello')).toBeInTheDocument();
  });
});
```

### E2E Tests (Playwright)

**Run E2E tests:**
```bash
cd autogpt_platform/frontend
pnpm test:e2e
```

**Run in UI mode:**
```bash
cd autogpt_platform/frontend
pnpm test-ui
```

**Generate tests interactively:**
```bash
cd autogpt_platform/frontend
pnpm gentests
```

**Example E2E test:**
```typescript
import { test, expect } from '@playwright/test';

test('user can login', async ({ page }) => {
  await page.goto('/login');
  await page.fill('[name="email"]', 'test@example.com');
  await page.fill('[name="password"]', 'password123');
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL('/dashboard');
});
```

## 🚀 CI/CD Testing

### Backend CI

Runs on every PR/push to `master` or `dev`:
- ✅ Linting (Ruff)
- ✅ Formatting (Black + isort)
- ✅ Fast tests only (`-m "not slow"`)

**Workflow**: `.github/workflows/ci-backend.yml`

### Frontend CI

Runs on every PR/push to `master` or `dev`:
- ✅ Linting (ESLint + Prettier)
- ✅ TypeScript type checking
- ✅ Next.js build
- ✅ API client generation

**Workflow**: `.github/workflows/ci-frontend.yml`

### Nightly/Manual Tests

Slow tests can be run manually or on a nightly schedule:
```bash
# Backend - all tests
poetry run pytest -v

# Frontend - full E2E suite
pnpm test:e2e
```

## 📊 Coverage Reports

### Backend Coverage

```bash
cd autogpt_platform/backend
poetry run pytest --cov=backend --cov-report=html
# Open htmlcov/index.html in browser
```

### Frontend Coverage

```bash
cd autogpt_platform/frontend
pnpm test:unit:coverage
# Open coverage/index.html in browser
```

## ✅ Best Practices

### Backend

1. **Write fast tests by default** - Only mark tests as `@pytest.mark.slow` if absolutely necessary
2. **Use fixtures** - Leverage pytest fixtures for setup/teardown
3. **Mock external services** - Don't hit real APIs in unit tests
4. **Test edge cases** - Especially error handling
5. **Keep tests isolated** - Each test should be independent

### Frontend

1. **Prefer unit tests** - They're faster and easier to debug
2. **Use E2E for critical flows** - Login, checkout, core user journeys
3. **Mock API calls** - Use MSW or similar for API mocking
4. **Test accessibility** - Use jest-dom matchers and axe
5. **Keep tests readable** - Descriptive test names and clear assertions

## 🐛 Debugging Tests

### Backend

```bash
# Run with verbose output
poetry run pytest -vv

# Run with print statements visible
poetry run pytest -s

# Run with debugger on failure
poetry run pytest --pdb

# Run last failed tests
poetry run pytest --lf
```

### Frontend (Unit)

```bash
# Run in watch mode
pnpm test:unit:watch

# Run specific test file
pnpm vitest run src/components/Button.test.tsx

# Run with UI
pnpm vitest --ui
```

### Frontend (E2E)

```bash
# Run in headed mode (see browser)
pnpm test:e2e --headed

# Run with debugger
pnpm test:e2e --debug

# Run specific test
pnpm test:e2e tests/login.spec.ts
```

## 📝 Writing New Tests

### Backend Test Template

```python
import pytest
from backend.your_module import your_function

def test_your_function_success():
    """Test successful execution."""
    result = your_function("input")
    assert result == "expected"

def test_your_function_error():
    """Test error handling."""
    with pytest.raises(ValueError):
        your_function("invalid")

@pytest.mark.slow
def test_database_integration():
    """Test with real database (slow)."""
    # Complex integration test
    pass
```

### Frontend Unit Test Template

```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { MyComponent } from './MyComponent';

describe('MyComponent', () => {
  it('renders with props', () => {
    render(<MyComponent title="Test" />);
    expect(screen.getByText('Test')).toBeInTheDocument();
  });

  it('handles user interaction', async () => {
    const onClick = vi.fn();
    render(<MyComponent onClick={onClick} />);
    
    fireEvent.click(screen.getByRole('button'));
    expect(onClick).toHaveBeenCalledOnce();
  });
});
```

### Frontend E2E Test Template

```typescript
import { test, expect } from '@playwright/test';

test.describe('Feature Name', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/feature');
  });

  test('user can perform action', async ({ page }) => {
    await page.click('[data-testid="action-button"]');
    await expect(page.locator('.result')).toBeVisible();
  });
});
```

## 🔄 Continuous Improvement

- **Monitor test duration** - Move slow tests to `@pytest.mark.slow`
- **Review failing tests** - Fix or update outdated tests
- **Increase coverage** - Target >80% coverage for critical paths
- **Refactor flaky tests** - Ensure tests are deterministic
- **Update dependencies** - Keep testing libraries up to date

---

**Last Updated**: November 2025  
**Maintained by**: SADOCKDOG Team
