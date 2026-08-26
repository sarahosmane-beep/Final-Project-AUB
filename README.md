# Task Tracker API

A compact FastAPI task tracker with a browser-based Kanban board. Data is stored in memory and resets when the process stops.

## Final Project

Branch reviewed: `final-project`

### What this submission demonstrates

- The existing Task Tracker still runs within the intended course scope.
- CI runs the complete pytest suite on every push and pull request.
- The Docker image runs as a non-root user and exposes a healthy API on port 8000.
- AI review, security, verification, and ownership evidence is recorded in `docs/`.

### How to run locally

Requires Python 3.12 or newer.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

On macOS or Linux, activate with `source .venv/bin/activate`. Open <http://127.0.0.1:8000/> for the Kanban board or <http://127.0.0.1:8000/docs> for API documentation. Verify health with:

```bash
curl -i http://127.0.0.1:8000/health
```

### How to run tests

```bash
python -m pytest -q
```

### How to run with Docker

```bash
docker build -t task-tracker-final .
docker run --rm -p 8000:8000 --name task-tracker-final task-tracker-final
curl -i http://127.0.0.1:8000/health
```

Stop the foreground container with Ctrl+C.

### Evidence files

- `docs/release-evidence.md`
- `docs/final-ai-review.md`
- `docs/ai-playbook.md`

### AI assistance summary

AI helped package the existing app, draft CI and Docker configuration, review security, and organize the evidence. I verified the work by inspecting the diff, running the full tests, checking the frontend routes and `/health`, and testing the Docker workflow when available. I rejected the idea of adding authentication because it would violate the stated final-project scope and cannot be implemented responsibly as a last-minute release change.

## API

- `POST /tasks`
- `GET /tasks?status=ToDo&priority=High`
- `GET /tasks/{id}`
- `PATCH /tasks/{id}`
- `DELETE /tasks/{id}`
