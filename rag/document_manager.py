# rag/document_manager.py

import os
import json
import shutil
from datetime import datetime
from rag.pipeline import RAGPipeline

class DocumentManager:
    def __init__(self, base_dir="documents"):
        self.base_dir = base_dir
        self.indexes_dir = f"{base_dir}/indexes"
        self.chats_dir = f"{base_dir}/chats"
        self.pipelines = {}  # active pipelines memory mein
        
        # Folders banao agar nahi hain
        os.makedirs(self.indexes_dir, exist_ok=True)
        os.makedirs(self.chats_dir, exist_ok=True)

    def get_saved_documents(self) -> list[str]:
        """Saved documents ki list return karo"""
        docs = []
        for name in os.listdir(self.indexes_dir):
            if os.path.isdir(f"{self.indexes_dir}/{name}"):
                docs.append(name)
        return sorted(docs)

    def is_indexed(self, doc_name: str) -> bool:
        """Check karo document already indexed hai ya nahi"""
        index_path = f"{self.indexes_dir}/{doc_name}/index.faiss"
        return os.path.exists(index_path)

    def index_document(self, pdf_path: str, doc_name: str) -> RAGPipeline:
        """Document process karo aur save karo"""
        # Is document ka folder banao
        doc_index_dir = f"{self.indexes_dir}/{doc_name}"
        os.makedirs(doc_index_dir, exist_ok=True)

        # Pipeline banao aur index karo
        pipeline = RAGPipeline(index_dir=doc_index_dir)
        pipeline.index_document(pdf_path)

        # Memory mein save karo
        self.pipelines[doc_name] = pipeline
        
        # Chat history initialize karo
        self._init_chat(doc_name)
        
        return pipeline

    def load_document(self, doc_name: str) -> RAGPipeline:
        """Already saved document load karo"""
        # Agar already memory mein hai
        if doc_name in self.pipelines:
            return self.pipelines[doc_name]
        
        # Disk se load karo
        doc_index_dir = f"{self.indexes_dir}/{doc_name}"
        pipeline = RAGPipeline(index_dir=doc_index_dir)
        pipeline.load_existing_index()
        
        self.pipelines[doc_name] = pipeline
        return pipeline

    def delete_document(self, doc_name: str):
        """Document aur uski chat delete karo"""
        # Index folder delete
        index_path = f"{self.indexes_dir}/{doc_name}"
        if os.path.exists(index_path):
            shutil.rmtree(index_path)
        
        # Chat file delete
        chat_path = f"{self.chats_dir}/{doc_name}.json"
        if os.path.exists(chat_path):
            os.remove(chat_path)
        
        # Memory se remove
        if doc_name in self.pipelines:
            del self.pipelines[doc_name]

    # ─── Chat Management ───────────────────────────────

    def _init_chat(self, doc_name: str):
        """Nai chat history file banao"""
        chat_path = f"{self.chats_dir}/{doc_name}.json"
        if not os.path.exists(chat_path):
            self._save_chat(doc_name, [])

    def get_chat_history(self, doc_name: str) -> list:
        """Document ki chat history load karo"""
        chat_path = f"{self.chats_dir}/{doc_name}.json"
        if os.path.exists(chat_path):
            with open(chat_path, "r") as f:
                return json.load(f)
        return []

    def add_message(self, doc_name: str, role: str, content: str):
        """Chat mein naya message add karo"""
        history = self.get_chat_history(doc_name)
        history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        self._save_chat(doc_name, history)

    def clear_chat(self, doc_name: str):
        """Chat history clear karo"""
        self._save_chat(doc_name, [])

    def _save_chat(self, doc_name: str, history: list):
        """Chat history disk pe save karo"""
        chat_path = f"{self.chats_dir}/{doc_name}.json"
        with open(chat_path, "w") as f:
            json.dump(history, f, indent=2)