from sentence_transformers import SentenceTransformer
from parser import extract_code_chunks
import faiss
import numpy as np

model=SentenceTransformer('all-MiniLM-L6-v2')


def _chunk_to_text(chunk):
    chunk_type = chunk.get("type", "unknown")
    chunk_name = chunk.get("name", "unnamed")

    content = (
        chunk.get("content")
        or chunk.get("code")
        or chunk.get("text")
        or chunk.get("docstring")
        or ""
    )

    if not content:
        return None

    return f"{chunk_type} {chunk_name}:\n{content}"

def build_faiss_index(chunks):
    texts=[]

    for chunk in chunks:
        if not isinstance(chunk, dict):
            continue
        text = _chunk_to_text(chunk)
        if text:
            texts.append(text)

    if not texts:
        raise ValueError("No valid chunk content found to build embeddings.")

    embeddings=model.encode(texts, convert_to_numpy=True)

    dimension=embeddings.shape[1]
    print(f"Embedding Dimension: {dimension}")
    index=faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    
    print(f"Total vectors in index: {index.ntotal}")
    return index,embeddings 

if __name__ == "__main__":
    file_path = r"F:\ML\Project\AI_Codebase_Intelligence\demo.py"
    chunks = extract_code_chunks(file_path)

    index, embeddings = build_faiss_index(chunks)
