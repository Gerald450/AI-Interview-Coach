from sentence_transformers import SentenceTransformer
from rich import print
import numpy as np
import json
import faiss


checkpoint = "BAAI/bge-base-en-v1.5"

print("loading model......")
model = SentenceTransformer(checkpoint)

texts = []
metadata = []

#read jsonl
print("readind dataset....")
with open("interviews.jsonl" , "r", encoding="utf-8") as f:
    for line in f:
        item = json.loads(line)
        texts.append(item["question"])
        metadata.append(item)

print("Generate embeddings....")
embeddings = model.encode(
    texts,
    batch_size=100,
    show_progress_bar=True,
    convert_to_numpy=True,
    normalize_embeddings=True
).astype('float32')

np.save("embeddings.npy", embeddings)

print('Saving metadata to json file.....')
with open("metadata.json", "w") as f:
    json.dump(metadata, f, indent=2)
    

#index embeddings  
dimension = embeddings.shape[1]
index = faiss.IndexFlatIP(dimension) #create empty index file with same dimension

print('Indexing embeddings....')
index.add(embeddings)

print('Saving index to file....')
faiss.write_index(index, "interview.index")

