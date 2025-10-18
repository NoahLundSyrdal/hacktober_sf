# hacktober_sf

## Run locally (macOS / zsh)

This repo includes a small FastAPI demo application under `demo_target/`. If you get the "externally-managed-environment" (PEP 668) error when installing packages system-wide, use a virtual environment as shown below.

1. Create and activate a virtual environment (project root):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Upgrade pip and install dependencies:

```bash
python -m pip install --upgrade pip setuptools wheel
python -m pip install "fastapi" "uvicorn[standard]"
```

3. Freeze the exact package versions into `requirements.txt`:

```bash
python -m pip freeze > requirements.txt
```

4. Start the demo app (while the venv is active):

```bash
uvicorn demo_target.app:app --reload --port 8000
```

Open http://127.0.0.1:8000/docs for the interactive API docs.

Alternatives and notes:
- If you prefer not to use a venv, consider `pipx` for installing CLI tools or `brew` packages for system-wide installs. See PEP 668 for more context.
- `.venv` is already ignored by the repository `.gitignore`.


https://www.meetup.com/digitaloceansanfrancisco/events/311197949/?utm_source=GenerativeAISF.com&referrer=luma 

Then, it’s time to roll up your sleeves for the hackathon build session (3 hours), where you’ll collaborate, code, and create something awesome.