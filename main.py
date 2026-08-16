import os
import shutil

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


from ingest import ingest_file
from query import retrieve

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js default port
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

@app.post("/upload-file/")
def upload_file(file: UploadFile = File(...)):
    """
    ingest file, connect to chromadb, chunk the document, 
    basically send file through 'ingest.py' to store information
    """
    #temp_path = f"./data/data{file.filename}"

    filename = os.path.basename(file.filename)
    file_path = os.path.join("C:/projects/second_brain/data", filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        ingest_file(file_path)
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

    return {"message": f"{filename} has been ingested"}

@app.post("/query/")
def get_answer(request: QueryRequest):
    # TODO: takes in user question/request, client sends to server, server runs retrieve()
    # Claude gets answer, then answer comes back to client
    answer = retrieve(request.question)
    return {"answer": str(answer)}



@app.get("/health")
def health():
    """ health check to verify the server is running."""
    return {"status": "alive"}