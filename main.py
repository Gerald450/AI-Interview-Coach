from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from retrieve import ProcessQuery

class Question(BaseModel):
    question: str
    


app = FastAPI()

@app.post("/")
def getUserQuestion(question: Question):
    response = ProcessQuery(question.question)
    return response.generate()