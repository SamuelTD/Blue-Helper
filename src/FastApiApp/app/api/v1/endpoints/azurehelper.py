from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.utils.search import search_similar_questions
from app.schemas.query import QueryRequest
from app.utils.loader import load_index_and_data

router = APIRouter()

index, questions, answers = load_index_and_data()

@router.post("/question")
def search_question(req: QueryRequest, current_user: dict= Depends(get_current_user)):
     return search_similar_questions(index, questions, answers, req.question, req.top_k)
