from sentence_transformers import SentenceTransformer
import streamlit as st

# load the embedding model
# all-MiniLM-L6-v2 is small, fast, and works great for semantic search
# it converts any text into 384 numbers
# this line runs only once when the file is imported

@st.cache_resource
def get_embeddings_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = get_embeddings_model()


def get_embeddings(texts: list[str]):
    """
    Takes a list of text chunks and converts each one into numbers.
    Returns a 2D array where each row is one chunk's numbers.
    
    Example:
    Input:  ["chunk1 text", "chunk2 text"]
    Output: [[0.23, -0.11, ...], [0.54, 0.33, ...]]
    """
    
    print(f"Creating embeddings for {len(texts)} chunks...")
    
    # convert all chunks to numbers at once
    # show_progress_bar shows a loading bar in terminal
    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        batch_size=32  # process 32 chunks at a time
    )
    
    print(f"Done! Each chunk is now {embeddings.shape[1]} numbers")
    return embeddings