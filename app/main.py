import os
import uuid
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, StreamingResponse
from .config import settings
from .database import engine, Base
from .tasks import import_csv_task, r
from pathlib import Path

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.post('/upload')
async def upload_csv(file: UploadFile = File(...)):
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    filename = f"{uuid.uuid4().hex}_{file.filename}"
    path = os.path.join(settings.UPLOAD_DIR, filename)

    with open(path, 'wb') as f:
        while chunk := await file.read(1024 * 1024):
            f.write(chunk)

    job_id = uuid.uuid4().hex
    import_csv_task.delay(path, job_id)
    return {"job_id": job_id}

@app.get('/jobs/{job_id}/events')
def job_events(job_id: str):
    def event_stream():
        pubsub = r.pubsub()
        pubsub.subscribe(f"job:{job_id}:progress")
        for message in pubsub.listen():
            if message["type"] != "message":
                continue
            yield f"data: {message['data'].decode()}\n\n"
    return StreamingResponse(event_stream(), media_type="text/event-stream")

@app.get('/', response_class=HTMLResponse)
def index():
    html_path = Path(__file__).resolve().parent.parent / 'frontend' / 'upload.html'
    return HTMLResponse(html_path.read_text())
