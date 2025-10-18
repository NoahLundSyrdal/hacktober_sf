# fuzzer/main.py
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from .engine import run_simple_scan
from .store import init_db, list_findings
import uvicorn

app = FastAPI(title="VibeFuzz Controller")

class ScanRequest(BaseModel):
    target: str
    mode: str = "quick"  # quick | deep

@app.on_event("startup")
def startup():
    init_db()

@app.post("/scan")
async def start_scan(req: ScanRequest, background_tasks: BackgroundTasks):
    # enqueue background scan
    background_tasks.add_task(run_simple_scan, req.target, )
    return {"status": "started", "target": req.target, "mode": req.mode}

@app.get("/findings")
def findings():
    return list_findings(200)

if __name__ == "__main__":
    uvicorn.run("fuzzer.main:app", host="0.0.0.0", port=8000, reload=True)
