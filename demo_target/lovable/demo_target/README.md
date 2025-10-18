# MoodNotes DemoTarget App

MoodNotes is a small intentionally imperfect FastAPI application built to be fuzz-tested by the VibeFuzz Agent. It includes basic endpoints for mood notes, file uploads, hidden routes, and intentional bugs like random slowdowns and 500 errors.

## Features

- **Mood Notes**: Create and retrieve journal entries with mood ratings (1-10)
- **File Uploads**: Upload files with intentional size limitations and random latency
- **Stats**: Get analytics on mood trends (with bugs for edge cases)
- **Hidden Routes**: Undocumented admin endpoints for fuzzing discovery
- **Results API**: Store and retrieve fuzzing test results

## Intentional Bugs

1. **POST /notes**: Raises unhandled ValueError if title > 60 characters
2. **POST /upload**: Returns 500 error for files > 1MB
3. **POST /upload**: 15% random chance of 2.5s delay
4. **GET /stats**: Returns 500 error when no notes exist
5. **GET /admin/hidden**: Undocumented route with no authentication

## Installation

```bash
pip install -r requirements.txt
```

## Run the app

```bash
uvicorn app:app --reload
```

The API will be available at `http://127.0.0.1:8000`

## Example Requests

### Create a note

```bash
curl -X POST http://127.0.0.1:8000/notes \
  -H "Content-Type: application/json" \
  -d '{"title":"Morning Walk","body":"Felt good","mood":8}'
```

### Get a specific note

```bash
curl http://127.0.0.1:8000/notes/1
```

### Upload a file

```bash
curl -F "file=@test.txt" http://127.0.0.1:8000/upload
```

### Get stats

```bash
curl http://127.0.0.1:8000/stats
```

### Send a fuzzing result

```bash
curl -X POST http://127.0.0.1:8000/results \
  -H "Content-Type: application/json" \
  -d '{
    "endpoint":"/notes",
    "method":"POST",
    "status":200,
    "verdict":"OK",
    "notes":"test run",
    "request":{},
    "response":{},
    "latency_ms":123
  }'
```

### View latest fuzzing results

```bash
curl http://127.0.0.1:8000/results/latest
```

### Healthcheck

```bash
curl http://127.0.0.1:8000/healthz
```

### Access hidden admin route

```bash
curl http://127.0.0.1:8000/admin/hidden
```

## API Documentation

Once running, visit:
- Interactive API docs: http://127.0.0.1:8000/docs
- Alternative docs: http://127.0.0.1:8000/redoc

## Testing with VibeFuzz Agent

The app is designed to work with automated fuzzing agents. Use the `/results` endpoints to:
1. Submit test results via POST `/results`
2. Retrieve the latest 10 results via GET `/results/latest`

All responses include an `X-Response-Time-ms` header showing endpoint latency.
