from sentence_transformers import SentenceTransformer
from rich import print
import numpy as np
import json


checkpoint = "BAAI/bge-base-en-v1.5"

model = SentenceTransformer(checkpoint)

texts = []
metadata = []

#read jsonl

with open("interviews.jsonl" , "r", encoding="utf-8") as f:
    for line in f:
        item = json.loads(line)
        texts.append(item["question"])
        metadata.append(item)

embeddings = model.encode(
    texts,
    batch_size=100,
    show_progress_bar=True,
    convert_to_numpy=True,
    normalize_embeddings=True
)

np.save("embeddings.npy", embeddings)

with open("metadata.json", "w") as f:
    json.dump(metadata, f, indent=2)

