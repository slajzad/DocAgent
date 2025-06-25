
from pydantic import BaseModel

class TaskRequest(BaseModel):
    agent: str
    input: str
