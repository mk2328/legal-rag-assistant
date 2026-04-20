import fitz  # pymupdf library, we import it as fitz
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

def load_pdf(file_path: str) -> str:
    """
    Opens a PDF file and extracts all text from it.
    Returns one big string containing all the text.
    """
    
    # stop if the file does not exist
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF file not found: {file_path}")
    
    # open the PDF using fitz (pymupdf)
    doc = fitz.open(file_path)

    # save page count BEFORE closing the document
    total_pages = len(doc)
    
    # this will hold all the text we extract
    full_text = ""
    
    # go through each page one by one
    for page_number, page in enumerate(doc):
        
        # extract text from this page
        text = page.get_text()
        
        # skip this page if it has no text (blank page)
        if text.strip():
            full_text += f"\n--- Page {page_number + 1} ---\n"
            full_text += text
    
    doc.close()
    
    print(f"PDF loaded: {total_pages} pages, {len(full_text)} characters")
    return full_text


def chunk_text(text: str) -> list[str]:
    """
    Automatically adjusts chunk size based on document length.
    Small doc  = smaller chunks = more precise answers
    Large doc  = bigger chunks  = more context per chunk
    """

    total_chars = len(text)

    # automatically decide chunk size based on document length
    if total_chars < 10_000:
        # small document — up to ~5 pages
        chunk_size = 400
        chunk_overlap = 80
    elif total_chars < 50_000:
        # medium document — 5 to 25 pages
        chunk_size = 600
        chunk_overlap = 120
    elif total_chars < 150_000:
        # large document — 25 to 75 pages
        chunk_size = 900
        chunk_overlap = 180
    else:
        # very large document — 75+ pages
        chunk_size = 1200
        chunk_overlap = 240

    print(f"Document size: {total_chars} chars → chunk_size={chunk_size}, overlap={chunk_overlap}")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " "]
    )

    chunks = splitter.split_text(text)
    chunks = [chunk.strip() for chunk in chunks if chunk.strip()]

    print(f"Total chunks created: {len(chunks)}")
    return chunks

def process_pdf(file_path: str) -> list[str]:
    """
    This is the main function that does two things:
    Step 1 - Load the PDF and get all text
    Step 2 - Break that text into chunks
    Returns the final list of chunks.
    """
    
    print(f"\nProcessing file: {file_path}")
    print("-" * 40)
    
    # step 1 - extract text from PDF
    text = load_pdf(file_path)
    
    # step 2 - break text into small chunks
    chunks = chunk_text(text)
    
    print(f"Done! {len(chunks)} chunks ready.\n")
    return chunks