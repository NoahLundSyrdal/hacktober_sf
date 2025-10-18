# demo_target/app.py
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import random, time

app = FastAPI()
DB = {}

class NoteIn(BaseModel):
    title: str
    body: str

@app.post("/notes")
def create_note(n: NoteIn):
    note_id = str(len(DB) + 1)
    DB[note_id] = {"id": note_id, "title": n.title, "body": n.body}
    return DB[note_id]

@app.get("/notes/{note_id}")
def read_note(note_id: str):
    return DB.get(note_id, {"error": "not found"})

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    # intentionally vibey: no size check, random slowdowns
    if random.random() < 0.15:
        time.sleep(2.5)
    content = await file.read()
    return {"name": file.filename, "size": len(content)}

@app.get("/admin/hidden")
def secret():
    # intentionally accessible if discovered
    return {"secret": "you found me!"}
