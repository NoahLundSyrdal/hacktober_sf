# demo_target_safe_login

A minimal, intentionally-safe login demo for automated fuzz testing.

This app exposes a single GET endpoint `/login` that accepts no input and
returns a static JSON payload indicating that authentication is unavailable.
OpenAPI and interactive docs are disabled to avoid exposing extra interfaces.

Run locally:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --host 127.0.0.1 --port 8002
```

Endpoint:
- GET /login -> {"login": "unavailable", "message": "This demo does not perform authentication."}

Safety note: The endpoint intentionally processes no user-controlled input and
so is safe to run under fuzzing or automated test agents.
