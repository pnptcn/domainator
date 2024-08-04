from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from rq import Queue
from worker import conn, predict_NuExtract

app = FastAPI()
q = Queue("nuextract", connection=conn)

class ExtractRequest(BaseModel):
    text: str
    schema: str

@app.post("/extract")
async def extract(request: ExtractRequest, background_tasks: BackgroundTasks):
    job = q.enqueue(predict_NuExtract, request.text, request.schema)
    background_tasks.add_task(notify_completion, job.id)
    return {"job_id": job.id}

def notify_completion(job_id):
    # Implement WebSocket or other notification mechanism here
    pass
