from fastapi import APIRouter, Depends
from app.core.security import get_current_user

router = APIRouter()

@router.post("/question")
def register(data:str, current_user: dict= Depends(get_current_user)):
    pass
    return "Yes."
