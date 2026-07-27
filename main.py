from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from retrieve import ProcessQuery

class Question(BaseModel):
    question: str

app = FastAPI()

@app.post("/ask")
def answer_question(body: Question):
    response = ProcessQuery(body.question)
    return response.generate()