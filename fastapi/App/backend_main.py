from fastapi import  FastAPI
import requests
from schemas import FileSubmitRequest, MessageSubmitRequest

API_UPSERT_URL = "http://localhost:3000/api/v1/vector/upsert/ba863175-2e49-450a-9e98-02cd7b738495"
API_MESSAGE_URL = "http://localhost:3000/api/v1/prediction/ba863175-2e49-450a-9e98-02cd7b738495"

app = FastAPI()

file_content = None

@app.post("/submitFile")
def submit_file(payload: FileSubmitRequest):

    global file_content
    file_content = payload 

    # Upsert the file content to the vector database
    requests.post(API_UPSERT_URL)  
    
    return file_content


@app.get("/submitFile")
def submit_file():  

    return file_content 

@app.post("/submitMessage")
def submit_message(payload: MessageSubmitRequest):

    response = requests.post(API_MESSAGE_URL, json=payload.model_dump())
    return response.json()