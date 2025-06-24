from fastapi import FastAPI
from pydantic import BaseModel

class QueryRequest(BaseModel):
    question: str
    top_k: int = 1