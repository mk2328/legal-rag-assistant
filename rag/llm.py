# rag/llm.py
import os
from groq import Groq
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

def get_groq_api_key():
    # pehle streamlit secrets try karo
    try:
        return st.secrets["GROQ_API_KEY"]
    except:
        return os.getenv("GROQ_API_KEY")

client =  Groq(api_key=get_groq_api_key())

def ask_llm(question: str, context_chunks: list[str]) -> str:
    context = "\n\n".join(context_chunks)
    
    prompt = f"""You are a legal document assistant.
Answer the question using ONLY the context provided below.
- Give complete answers, do not leave out exceptions or conditions
- If there is an "unless" or "except" clause, always mention it
- Use simple plain English, not legal jargon
If the answer is not in the context, say "I could not find this in the document."

CONTEXT:
{context}

QUESTION: {question}

ANSWER:"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,   
        max_tokens=1024
    )
    
    return response.choices[0].message.content