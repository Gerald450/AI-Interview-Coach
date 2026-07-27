from sentence_transformers import SentenceTransformer
import faiss
import json
from ollama import chat
from rich import print



checkpoint = "BAAI/bge-base-en-v1.5"
print("Loading model.....")
model = SentenceTransformer(checkpoint)
print("Loading Index.....")
index = faiss.read_index("Interview_dataset_pipeline/datasets/interview.index")
print("Loading metadata.....")
with open("Interview_dataset_pipeline/datasets/metadata.json") as f:
    metadata = json.load(f)


class ProcessQuery:
    def __init__(self, query) -> None:
        self.query = query

    def generate(self,) -> str:
        query = [self.query]

        query_embedding = model.encode(
            query,
            normalize_embeddings=True
        ).astype("float32")

        k = 5
        print("Searching....")
        faiss.omp_set_num_threads(1)
        scores, indices = index.search(query_embedding, k)
        context = ""


        for i in range(len(scores)):
            for score, idx in zip(scores[i], indices[i]):
                context += f"""
                Question: {metadata[idx]["question"]}
                Answer: {metadata[idx]["answer"]}
                """

        prompt = f"""
        You are an expert software engineering interview coach.

        Use the interview examples below as reference.

        {context}

        Now answer this interview question:

        {query}

        Give a detailed but concise interview-quality answer.
        """

        print("Waiting for ollama response....")
        response = chat(
            model = "llama3.2:1b",
            messages=[
                {
                    "role": "user",
                    "content":prompt,
                }
            ]
        )
        print("Done!")

        return response["message"]["content"]