# models.py
from pydantic import BaseModel

class PromptRequest(BaseModel):
    prompt: str
