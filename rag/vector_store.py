import faiss
import numpy as np
import pickle
import os

class VectorStore:
    def __init__(self, index_dir="faiss_index"):
        self.index_dir = index_dir
        self.index = None
        self.chunks = []   # store the raw text chunks alongside

    def build(self, embeddings: np.ndarray, chunks: list[str]):
        dim = embeddings.shape[1]          # 384 for MiniLM
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings.astype("float32"))
        self.chunks = chunks

    def save(self):
        os.makedirs(self.index_dir, exist_ok=True)
        faiss.write_index(self.index, f"{self.index_dir}/index.faiss")
        with open(f"{self.index_dir}/chunks.pkl", "wb") as f:
            pickle.dump(self.chunks, f)
        print(f"Saved {self.index.ntotal} vectors to {self.index_dir}/")

    def load(self):
        self.index = faiss.read_index(f"{self.index_dir}/index.faiss")
        with open(f"{self.index_dir}/chunks.pkl", "rb") as f:
            self.chunks = pickle.load(f)
        print(f"Loaded {self.index.ntotal} vectors")

    def search(self, query_embedding: np.ndarray, top_k=5) -> list[str]:
        q = query_embedding.astype("float32").reshape(1, -1)
        _, indices = self.index.search(q, top_k)
        return [self.chunks[i] for i in indices[0] if i < len(self.chunks)]