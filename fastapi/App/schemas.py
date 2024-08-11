from pydantic import BaseModel

class FileSubmitRequest(BaseModel):
    file_content: str
    
class MessageSubmitRequest(BaseModel):
    history: list[dict]
    question: str
