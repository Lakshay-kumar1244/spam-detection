from fastapi import APIRouter
from pydantic import BaseModel
from backend.app.models.spam_model import predict_spam

router = APIRouter()

class TextInput(BaseModel):
    text: str

@router.post("/check_spam")
def check_spam(input: TextInput):
    response = predict_spam(input.text)
    return response
