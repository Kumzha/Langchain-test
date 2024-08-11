from pydantic import BaseModel

class FileSubmitRequest(BaseModel):
    file_content: str
    
