from pydantic import BaseModel
from typing import Optional

class AgentMetadata(BaseModel):
    name: str
    description: str
    model: Optional[str]
    use_vector: Optional[bool]
    doc_path: Optional[str]