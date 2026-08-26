# Release Evidence

## Baseline

- Branch required for submission: `final-project`.
- Verification date: 2026-08-26.
- Local app run command: `python -m uvicorn app.main:app --reload`.
- `/health` result: FastAPI `TestClient` returned HTTP 200 with `status: ok` and a timezone-aware timestamp.
- Frontend check: `/` and `/app.js` both returned HTTP 200. The Taskflow create/edit board, filters, and task controls remain present in `frontend/index.html`; no product feature was added.
- Test command: `python -m pytest -q`.
- Test result: 6 passed. Pytest emitted a dependency deprecation warning from the installed FastAPI test client; it did not affect the tests.
- Packaging note: the source workspace contained two app copies under one pytest discovery root. The final submission isolates the complete app in this folder so the documented command collects only its intended suite.

## CI evidence

- Workflow file: `.github/workflows/ci.yml`.
- Verified green run: https://github.com/sarahosmane-beep/Final-Project-AUB/actions/runs/32986857615 (all test steps passed on 2026-08-26).
- Test command used by CI: `python -m pytest -q`.
- Dependency setup: Python 3.12 with `python -m pip install -r requirements.txt`.
- Shortcut check: no `continue-on-error`, no `|| true`, and pytest is not skipped.

## Docker evidence

- Build command: `docker build -t task-tracker-final .`.
- Run command: `docker run --rm -p 8000:8000 --name task-tracker-final task-tracker-final`.
- Build result: successful on Docker Engine 29.3.1 using Docker Desktop 4.66.1 on 2026-08-26.
- `/health` check: HTTP 200 with `{"status":"ok","timestamp":"2026-08-26T17:00:40.602026+00:00"}` from the running container.
- Frontend check: HTTP 200 from `/` in the running container.
- Non-root check: `docker exec task-tracker-final whoami` returned `appuser`.
- No-baked-secrets check: `.dockerignore` excludes `.env` and `.env.*` while allowing only the placeholder `.env.example`; the Dockerfile copies only `requirements.txt`, `app/`, and `frontend/`.
- Runtime command check: explicit Uvicorn command binds `0.0.0.0:8000`.

## Documentation claim-vs-reality log

| Claim checked | Evidence used | Result | Change made, if any |
|---|---|---|---|
| `python -m pytest -q` runs the full project suite | Ran the command from this folder | Pass: 6 tests | Added `pytest.ini` to make the intended test root explicit |
| `GET /health` returns HTTP 200 and `status: ok` | FastAPI `TestClient` request | Pass | None |
| The browser frontend is served at `/` and its script at `/app.js` | `TestClient` requests and route/source inspection | Pass: both returned 200 | Moved static files under required `frontend/` and updated two documented file paths in `app/main.py` |
| Docker runs as a non-root user and does not copy `.env` | Inspected `Dockerfile` and `.dockerignore` | Configuration pass; runtime pending | Added explicit `USER appuser` and narrow `COPY` commands |
| CI installs dependencies and runs pytest on push and pull request | Inspected `.github/workflows/ci.yml` | Configuration pass; hosted run pending | Added explicit Python 3.12 and test steps |

## Remaining submission checks

1. Submit the public GitHub repository URL only, as required by the brief.
