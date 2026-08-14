from fastapi import FastAPI

app = FastAPI()

@app.post("/upload-file")
def upload_file(file_path: str):
    # TODO: ingest file, connect to chromadb, chunk the document, 
    # basically send file through 'ingest.py' to store information
    return {"message: document has been stored"}

@app.post("/query")
def get_answer(query: str):
    # TODO: takes in user question/request, client sends to server, server runs retrieve()
    # Claude gets answer, then answer comes back to client
    return {"answer: ..."}