from fastapi import  FastAPI
import requests
from schemas import FileSubmitRequest

API_UPSERT_URL = "http://localhost:3000/api/v1/vector/upsert/ba863175-2e49-450a-9e98-02cd7b738495"


app = FastAPI()

file_content = None

@app.post("/submitFile")
def submit_file(payload: FileSubmitRequest):

    payload.model_validate()
    global file_content
    file_content = payload

    # Send upsert request to Flowise Api    
    requests.post(API_UPSERT_URL)

    return file_content


@app.get("/submitFile")
def submit_file():  

    return file_content 
