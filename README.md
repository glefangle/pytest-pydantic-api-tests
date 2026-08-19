# pytest-pydantic-api-tests

REST API test framework: `requests` + `pytest` + `pydantic` (contract validation) + Allure Report.

11 scenarios against the public [dummyjson.com](https://dummyjson.com) API:
users CRUD, authentication (login, Bearer-protected profile, negative cases).

## Architecture

```
pytest-pydantic-api-tests/
├── src/
│   ├── api/                 # Service layer -- endpoint wrappers returning parsed models
│   │   ├── users_api.py     # GET/POST/PUT/DELETE /users*, list & pagination
│   │   └── auth_api.py      # POST /auth/login, GET /auth/me (Bearer)
│   ├── clients/             # HTTP client: session, logging, Allure attachments
│   ├── config/              # pydantic-settings, .env-driven configuration
│   └── schemas/             # Pydantic models of API contracts (response validation)
├── tests/                   # Test scenarios only -- no transport or parsing logic
│   ├── test_users.py        # 6 tests: get, 404, list/pagination, create, update, delete
│   └── test_auth.py         # 5 tests: login success, /auth/me, 3x parametrized failures
├── .github/workflows/ci.yml # CI: lint -> typecheck -> test -> Allure report -> Pages
├── pyproject.toml           # Ruff, Mypy, coverage config
├── Makefile                 # Standardised dev commands
└── pytest.ini
```

### Design principles

- **Layered architecture** -- tests hold business logic; everything else is reusable.
- **Contract validation** -- every response is parsed into a Pydantic model with
  snake_case Python attributes and `Field(alias=...)` for camelCase wire format;
  schema drift fails the test.
- **Full observability** -- each request/response is logged and attached to the
  Allure report automatically; environment.properties are generated per run.
- **Flake control** -- `pytest-rerunfailures` retries, `pytest-xdist` parallelization.

## Quick start

```bash
pip install -r requirements.txt -r requirements-dev.txt
cp .env.example .env                 # defaults work out of the box for dummyjson
pytest                               # all tests
pytest -m smoke                      # smoke subset
pytest -n auto                       # parallel run
pytest --cov --cov-report=term-missing  # with coverage
allure serve allure-results          # local report
```

### Dev commands (via Make)

```bash
make lint        # ruff check + ruff format --check
make format      # ruff check --fix + ruff format
make typecheck   # mypy src tests
make test        # pytest
make test-cov    # pytest --cov
make report      # allure serve allure-results
make clean       # remove caches and generated artifacts
```

## Code quality toolchain

| Tool | Purpose | Config |
|------|---------|--------|
| [Ruff](https://docs.astral.sh/ruff/) | Lint + format (replaces flake8, isort, black) | `pyproject.toml [tool.ruff]` |
| [Mypy](https://mypy.readthedocs.io/) | Static type checking (pydantic plugin enabled) | `pyproject.toml [tool.mypy]` |
| [pre-commit](https://pre-commit.com/) | Git hooks -- runs Ruff on every commit | `.pre-commit-config.yaml` |
| [pytest-cov](https://pytest-cov.readthedocs.io/) | Coverage reporting | `Makefile test-cov` |

Ruff rules: E/W (pycodestyle), F (pyflakes), I (isort), N (pep8-naming), UP (pyupgrade),
B (bugbear), C4 (comprehensions), SIM (simplify), PT (pytest-style), RUF (ruff-specific).

## Configuration

All settings come from environment variables or `.env` (see `.env.example`):

| Variable | Default | Purpose |
|----------|---------|---------|
| BASE_URL | https://dummyjson.com | Target environment |
| AUTH_USERNAME | emilys | Login used by auth tests |
| AUTH_PASSWORD | emilyspass | Password used by auth tests |
| TIMEOUT | 30 | Per-request timeout, s |
| LOG_LEVEL | INFO | Logging verbosity |

## CI / Allure

Every push/PR runs: **lint -> typecheck -> test**. The Allure report (with trend history)
is published to GitHub Pages: `https://glefangle.github.io/pytest-pydantic-api-tests/`.

## License

[MIT](LICENSE)
