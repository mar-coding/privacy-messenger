# Privacy Messenger

A privacy-first messenger.

> Status: early scaffolding — backend skeleton only. APIs and clients are not implemented yet.

## Stack

- **Python 3.13** + **FastAPI**
- **uv** for dependency management
- **pydantic-settings** for configuration
- **ruff** + **mypy (strict)** for linting and typing
- **pre-commit** with emoji-prefixed commit messages

## Project layout

```
.
├── back/                # FastAPI backend
│   ├── app/
│   │   ├── core/        # cross-cutting (logging, …)
│   │   ├── settings/    # pydantic-settings config
│   │   └── main.py      # FastAPI app + lifespan + CORS
│   └── pyproject.toml
├── hooks/               # custom git hooks (commit-msg emoji check)
├── .pre-commit-config.yaml
└── .env                 # local environment (not committed in real setups)
```

## Getting started

Requires Python 3.13 and [uv](https://github.com/astral-sh/uv).

```bash
# install dependencies
cd back
uv sync

# run the API (dev)
uv run fastapi dev app/main.py
```

In `dev`, interactive docs are exposed at:

- Swagger UI — `http://localhost:8000/docs`
- ReDoc — `http://localhost:8000/redoc`
- OpenAPI schema — `http://localhost:8000/api/v1/openapi.json`

In `staging` / `production` these endpoints are disabled.

## Configuration

Settings are loaded from the repo-root `.env` via `pydantic-settings`. Common knobs:

| Variable                | Default | Notes                                       |
|-------------------------|---------|---------------------------------------------|
| `ENVIRONMENT`           | `dev`   | one of `dev`, `staging`, `production`       |
| `DEBUG_MODE`            | `FALSE` | enables `DEBUG`-level logging               |
| `UNDER_DEVELOPMENT`     | `FALSE` | dev shortcuts (e.g. fixed OTP `123456`)     |
| `BACKEND_CORS_ORIGINS`  | —       | comma-separated list of allowed origins     |

## Development

```bash
# install pre-commit hooks (run once per clone)
pre-commit install --hook-type pre-commit --hook-type commit-msg

# lint / format / typecheck
cd back
uv run ruff check .
uv run ruff format .
uv run mypy .
```

Commit messages must start with a gitmoji-style prefix, e.g.:

```
:sparkles: add message routing
:bug: fix CORS in staging
```

The `hooks/commit-msg-check.sh` hook enforces this.

## License

See [LICENSE](LICENSE).
