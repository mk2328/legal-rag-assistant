import os
from groq import Groq
from dotenv import load_dotenv
import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError

# Local development ke liye load_dotenv
load_dotenv()

def get_groq_api_key():
    # .get() use karna safer hai taake agar key na mile toh error na de
    try:
        return st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
    except (StreamlitSecretNotFoundError, Exception):
        return os.getenv("GROQ_API_KEY")

def ask_llm(question: str, context_chunks: list[str]) -> str:
    # CLIENT KO YAHAN INITIALIZE KAREIN (Lazy Loading)
    api_key = get_groq_api_key()
    if not api_key:
        raise ValueError("GROQ_API_KEY nahi mili! Check your secrets/env.")
    
    client = Groq(api_key=api_key)
    
    context = "\n\n".join(context_chunks)
    
    prompt = f"""You are a legal document assistant.
    Answer the question using ONLY the context provided below.
    ... (rest of your prompt) ...
    CONTEXT: {context}
    QUESTION: {question}
    ANSWER:"""
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,   
        max_tokens=1024
    )
    
    return response.choices[0].message.content