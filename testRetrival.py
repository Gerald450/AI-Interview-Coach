from sentence_transformers import SentenceTransformer
import faiss
import json



checkpoint = "BAAI/bge-base-en-v1.5"
print("Loading model.....")
model = SentenceTransformer(checkpoint)

print("Loading Index.....")
index = faiss.read_index("interview.index")

print("Loading metadata.....")
with open("metadata.json") as f:
    metadata = json.load(f)
    
    
query = ["Explain AI Tokens", "What is dependency injections"]

query_embedding = model.encode(
    query,
    normalize_embeddings=True
).astype("float32")

k = 5
print("Searching....")
faiss.omp_set_num_threads(1)
scores, indices = index.search(query_embedding, k)


# print(scores)
# print("="*100)
# print(indices)


for score, idx in zip(scores[0], indices[0]):
    print("=" * 100)
    print("Similarity:", score)
    print(metadata[idx]["question"])