# ⚖️ Legal RAG Assistant

An AI-powered legal document assistant built with a full RAG (Retrieval-Augmented Generation) pipeline. Upload any legal PDF — contracts, NDAs, agreements — and ask questions in plain English to get precise, context-aware answers instantly.

---

## 🖥️ Live Demo

> Coming soon — deploying on Streamlit Cloud

---

## 📸 Screenshots

### Dashboard
![Dashboard](screenshots/dashboard.png)

### Chat Interface
![Chat](screenshots/chat.png)

---

## 🧠 How It Works

This project uses a RAG pipeline — instead of relying only on the LLM's training data, it retrieves relevant information directly from your uploaded documents before generating an answer.

```
PDF Upload → Text Extraction → Chunking → Embedding → FAISS Index
                                                            ↓
User Question → Embed Question → Search Index → Retrieve Top 5 Chunks
                                                            ↓
                                              Groq LLM → Final Answer
```

### Step by Step

1. **PDF Loading** — PyMuPDF extracts raw text from every page of the uploaded document
2. **Chunking** — Text is split into 500-character overlapping chunks (100-char overlap) so no context is lost at boundaries
3. **Embedding** — Each chunk is converted into a 384-dimensional vector using `all-MiniLM-L6-v2`
4. **FAISS Index** — All vectors are stored in a FAISS index saved to disk for reuse
5. **Query** — User's question is embedded with the same model and compared against all stored vectors
6. **Retrieval** — Top 5 most semantically similar chunks are retrieved
7. **Generation** — Retrieved chunks are passed as context to Groq's `llama-3.3-70b-versatile` model which generates the final answer

---

## ✨ Features

- 📄 Upload and process multiple PDF documents
- 💬 Chat-style Q&A interface per document
- 🔍 Semantic search using vector embeddings
- 💾 Persistent document storage — indexes saved to disk
- 🗂️ Multi-document management — switch between documents
- 🗑️ Delete documents and their chat history
- 📝 Chat history saved per document
- ⚡ Fast inference via Groq API

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Frontend | Streamlit |
| PDF Parsing | PyMuPDF (fitz) |
| Text Chunking | LangChain Text Splitters |
| Embedding Model | sentence-transformers (all-MiniLM-L6-v2) |
| Vector Database | FAISS (faiss-cpu) |
| LLM | Groq API (llama-3.3-70b-versatile) |
| Language | Python 3.10+ |

---

## 📁 Project Structure

```
legal-rag-assistant/
│
├── app.py                      # Streamlit UI — main entry point
│
├── rag/
│   ├── __init__.py             # Makes rag a Python package
│   ├── loader.py               # PDF loading and text chunking
│   ├── embedder.py             # Text to vector conversion
│   ├── vector_store.py         # FAISS index management
│   ├── llm.py                  # Groq LLM integration
│   ├── pipeline.py             # Full RAG pipeline orchestration
│   └── document_manager.py     # Multi-document and chat management
│
├── documents/
│   ├── indexes/                # Saved FAISS indexes per document
│   └── chats/                  # Saved chat histories per document
│
├── .env                        # API keys (not pushed to GitHub)
├── requirements.txt            # Python dependencies
└── .gitignore                  # Files excluded from GitHub
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- A free Groq API key from [console.groq.com](https://console.groq.com)

### 1. Clone the Repository

```bash
git clone https://github.com/MuskanKamran/legal-rag-assistant.git
cd legal-rag-assistant
```

### 2. Create a Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Your API Key

Create a `.env` file in the root folder:

```
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Run the App

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## 💡 Usage

1. Click **Upload** in the sidebar and select a legal PDF
2. Click **Process Document** and wait for indexing to complete
3. Click on the document from the sidebar or dashboard
4. Type your question in the chat input
5. Get instant, context-aware answers from your document

### Example Questions

- *"Summarize this document"*
- *"What are the confidentiality obligations?"*
- *"Who are the parties involved?"*
- *"What happens if either party breaches the agreement?"*
- *"What is the duration of this contract?"*

---

## ⚙️ Configuration

You can adjust these values in `rag/loader.py` to tune performance:

```python
chunk_size=500      # characters per chunk — increase for more context
chunk_overlap=100   # overlapping characters — increase to reduce boundary loss
```

And in `rag/llm.py`:

```python
model="llama-3.3-70b-versatile"   # Groq model to use
temperature=0.2                    # lower = more factual answers
max_tokens=1024                    # maximum answer length
```

---

## 🔑 Environment Variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Your Groq API key from console.groq.com |

---

## 📦 Dependencies

```
streamlit
groq
faiss-cpu
sentence-transformers
pymupdf
python-dotenv
langchain
langchain-community
langchain-text-splitters
```

---

## 🙋‍♀️ Author

**Muskan Kamran**
Full-Stack & AI Agent Specialist

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
