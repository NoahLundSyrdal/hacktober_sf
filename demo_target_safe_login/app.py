from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from pathlib import Path
import secrets
import os

# Disable OpenAPI and doc UIs to avoid exposing extra interfaces.
app = FastAPI(
    title="Demo Target Safe Login",
    description=(
        "A deliberately-safe login demo that accepts a single credential pair "
        "and otherwise performs no authentication. OpenAPI/docs are disabled."
    ),
    openapi_url=None,
    docs_url=None,
    redoc_url=None,
)


CREDS_PATH = Path(__file__).parent / "credentials.txt"


class LoginRequest(BaseModel):
    username: str
    password: str

    @validator("username")
    def username_valid(cls, v: str) -> str:
        v = v.strip()
        if not (1 <= len(v) <= 64):
            raise ValueError("username length must be 1..64")
        import re

        if not re.match(r"^[A-Za-z0-9._-]+$", v):
            raise ValueError("username contains invalid characters")
        return v

    @validator("password")
    def password_valid(cls, v: str) -> str:
        if not (1 <= len(v) <= 128):
            raise ValueError("password length must be 1..128")
        return v


def _ensure_credentials():
    """Ensure a single random credential pair exists on disk and return it.

    The file is created with restrictive permissions (0o600) when first
    generated. If the file already exists, we read from it. This keeps the
    working credential external to the code but local to the demo folder.
    """
    if CREDS_PATH.exists():
        try:
            text = CREDS_PATH.read_text(encoding="utf-8")
            user, pwd = text.split("\n", 1)
            return user.strip(), pwd.strip()
        except Exception:
            # If the file is corrupted, remove it and re-generate.
            try:
                CREDS_PATH.unlink()
            except Exception:
                pass

    username = "user-" + secrets.token_urlsafe(6)
    password = secrets.token_urlsafe(16)
    data = f"{username}\n{password}\n"

    # Write with restrictive permissions when possible
    fd = os.open(str(CREDS_PATH), os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    try:
        os.write(fd, data.encode("utf-8"))
    finally:
        os.close(fd)

    return username, password


# create or load the credential once at import-time
_USERNAME, _PASSWORD = _ensure_credentials()


@app.post("/login")
async def login(req: LoginRequest):
    """Process a login request using a strict input schema and only one valid pair.

    Returns 200 on success and 403 on failure. Because validation is strict and
    there's only one valid credential pair, this reduces the attack surface for
    fuzzers while allowing a single working login for tests.
    """
    if req.username == _USERNAME and req.password == _PASSWORD:
        return {"login": "success", "message": "authenticated"}
    raise HTTPException(status_code=403, detail="invalid credentials")
