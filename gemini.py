import os

from dotenv import load_dotenv
from google import genai

load_dotenv()
import sys
from pathlib import Path

from rich import print

sys.path.insert(0, str(Path(__file__).parent / "Interview_dataset_pipeline"))
from app.models.interview import (
    Category,
    Difficulty,
)
from app.prompts.database import build_database_prompt

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
prompt = build_database_prompt(Category.DATABASES, Difficulty.MEDIUM)
print(prompt)

client = genai.Client(api_key=GEMINI_API_KEY)
response = client.models.generate_content(
    model='gemini-3.6-flash',
    contents = {'text': prompt},
    config={
        'temperature':1,
        'top_k': 20,
        'top_p': 0.95,
    }
)

print(response.candidates[0].content.parts[0].text)