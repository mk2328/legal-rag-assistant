# ⚖️ Legal RAG Assistant (Secure & Authenticated)

An AI-powered legal document assistant with a full RAG (Retrieval-Augmented Generation) pipeline, now featuring **secure Google Authentication** and **user-isolated workspaces**. Upload your legal PDFs — contracts, NDAs, agreements — and chat with them in a private, encrypted-like environment.

-----

## 📸 Overview

This application has evolved from a local-only tool into a secure, multi-user compatible platform. By integrating Google OAuth, every user maintains their own private folder for document indexes and chat histories, ensuring data privacy.

-----

## 🧠 How It Works

The core RAG pipeline remains robust, but it is now gated by an authentication layer to ensure users only access their own documents.

1.  **Secure Login** — Users authenticate via Google OAuth2.
2.  **User Isolation** — Upon login, the system creates/loads a dedicated workspace directory: `documents/{email_address}/`.
3.  **PDF Processing** — PyMuPDF extracts text, which is then chunked and embedded.
4.  **FAISS Indexing** — Vectors are stored in the user-specific directory.
5.  **Generation** — Groq's `llama-3.3-70b-versatile` generates answers based solely on the authenticated user's documents.

-----

## ✨ New Features

  * **Secure Authentication**: Google Login integrated via `streamlit_oauth`.
  * **Privacy-First Design**: Documents and chat histories are isolated per user email to prevent data cross-contamination.
  * **Premium Aesthetic**: Complete UI overhaul featuring custom CSS, a responsive hero section, and interactive status indicators.
  * **Persistent Management**: Multi-document management with per-document chat history.

-----

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| **Authentication** | `streamlit-oauth`, `PyJWT` |
| **Frontend** | Streamlit (Custom CSS) |
| **PDF Parsing** | PyMuPDF (fitz) |
| **Embedding Model** | `all-MiniLM-L6-v2` |
| **Vector Database** | FAISS |
| **LLM** | Groq API (`llama-3.3-70b-versatile`) |
| **Language** | Python 3.10+ |

-----

## 📁 Project Structure

Your project now organizes user-specific data dynamically.

```
legal-rag-assistant/
├── .streamlit/             # Config and Secrets
├── documents/              # User-specific data roots
│   └── user_email_com/     # Isolated user directory
│       ├── chats/          # Chat history per user
│       └── indexes/        # FAISS indexes per user
├── rag/                    # Backend logic
├── app.py                  # Streamlit UI & Auth flow
├── .env                    # Environment variables
└── requirements.txt        # Updated dependencies
```

-----

## 🚀 Getting Started

### Prerequisites

  * Python 3.10+
  * A free [Groq API key](https://console.groq.com)
  * A [Google Cloud Project](https://console.cloud.google.com/) with OAuth 2.0 Client IDs configured.

### 1\. Setup Environment

Create a `.env` file in the root folder:

```text
GROQ_API_KEY=your_groq_api_key_here
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8501
```

### 2\. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3\. Run the App

```bash
streamlit run app.py
```

-----

## 💡 Usage

1.  **Authenticate**: Sign in securely using your Google account.
2.  **Upload**: Navigate to the sidebar, upload a legal PDF, and click **Process Document**.
3.  **Interact**: Select your document from the sidebar and start chatting.
4.  **Manage**: Use the "Clear Chat" button or delete documents directly from the sidebar.

-----

## 🙋‍♀️ Author

**Muskan Kamran**
Full-Stack & AI Agent Specialist

-----

## 📄 License

This project is open source and available under the [MIT License](https://www.google.com/search?q=LICENSE).