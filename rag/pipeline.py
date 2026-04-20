# rag/pipeline.py

from rag.loader import process_pdf
from rag.embedder import get_embeddings
from rag.vector_store import VectorStore
from rag.llm import ask_llm
import os

class RAGPipeline:
    def __init__(self, index_dir="faiss_index"): 
        self.store = VectorStore(index_dir=index_dir)  
        self.is_indexed = False

    def index_document(self, pdf_path: str):
        print(f"Processing {pdf_path}...")
        chunks = process_pdf(pdf_path)
        embeddings = get_embeddings(chunks)
        self.store.build(embeddings, chunks)
        self.store.save()
        self.is_indexed = True
        print(f"Done! {len(chunks)} chunks indexed.")

    def load_existing_index(self):
        self.store.load()
        self.is_indexed = True

    def ask(self, question: str) -> str:
        if not self.is_indexed:
            return "Pehle koi document index karo!"
        query_vec = get_embeddings([question])
        chunks = self.store.search(query_vec[0])
        return ask_llm(question, chunks)