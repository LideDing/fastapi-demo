from pydantic import BaseModel



class HelloResponse(BaseModel):
    message: str
    current_time: str
    host: str
