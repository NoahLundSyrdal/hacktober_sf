"""
MoodNotes: a small, intentionally imperfect FastAPI app designed for fuzz-testing by the VibeFuzz Agent.
It allows users to create and retrieve mood notes, upload files, and includes random bugs, latency spikes,
and hidden routes so the agent can find and report issues.
"""

from fastapi import FastAPI, UploadFile, File, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
import time

app = FastAPI(title="MoodNotes API")
DB = {}
RESULTS = []
NOTE_ID_COUNTER = 0

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_timing_header(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = (time.time() - start) * 1000
    response.headers["X-Response-Time-ms"] = str(round(duration, 2))
    return response


class NoteCreate(BaseModel):
    title: str
    body: str
    mood: int


class FuzzResult(BaseModel):
    endpoint: str
    method: str
    status: int
    verdict: str
    notes: str
    request: dict
    response: dict
    latency_ms: float


@app.post("/notes")
async def create_note(note: NoteCreate):
    global NOTE_ID_COUNTER
    
    if len(note.title) > 60:
        raise ValueError("Title too long!")
    
    if note.mood < 1 or note.mood > 10:
        raise HTTPException(status_code=400, detail="Mood must be between 1 and 10")
    
    NOTE_ID_COUNTER += 1
    note_id = str(NOTE_ID_COUNTER)
    
    DB[note_id] = {
        "id": note_id,
        "title": note.title,
        "body": note.body,
        "mood": note.mood
    }
    
    return DB[note_id]


@app.get("/notes/{note_id}")
async def get_note(note_id: str):
    if note_id not in DB:
        return {"error": "note not found"}
    return DB[note_id]


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if random.random() < 0.15:
        time.sleep(2.5)
    
    content = await file.read()
    
    if len(content) > 1_000_000:
        raise HTTPException(status_code=500, detail="File too large!")
    
    return {
        "filename": file.filename,
        "size": len(content)
    }


@app.get("/stats")
async def get_stats():
    if len(DB) == 0:
        raise HTTPException(status_code=500, detail="No notes available for stats!")
    
    total_mood = sum(note["mood"] for note in DB.values())
    average_mood = round(total_mood / len(DB), 1)
    
    return {
        "average_mood": average_mood,
        "note_count": len(DB)
    }


@app.get("/admin/hidden", include_in_schema=False)
async def hidden_endpoint():
    return {"secret": "you found the hidden mood core!"}


@app.post("/results")
async def submit_result(result: FuzzResult):
    RESULTS.append(result.dict())
    return {"status": "recorded", "total_results": len(RESULTS)}


@app.get("/results/latest")
async def get_latest_results():
    return RESULTS[-10:]



@app.get("/healthz")
async def health_check():
    return {"status": "ok"}
