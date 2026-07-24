import faiss
import numpy as np

embeddings = np.load("embeddings.npy").astype("float32")

dimension = embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)

index.add(embeddings)


faiss.write_index(index, "interview.index")