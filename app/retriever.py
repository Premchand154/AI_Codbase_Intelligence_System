import numpy as np
from parser import extract_code_chunks
from embedding import model, build_faiss_index


def retrieve_relevant_chunks(query,model,index,chunks,k=3):
    query_embedding=model.encode([query],convert_to_numpy=True)
    D,I=index.search(np.array(query_embedding), k)
    
    results=[]
    
    for idx in I[0]:
        chunk = chunks[idx]
        
        structured_chunk={
            "name":chunk.get("name","unknown"),
            "type":chunk.get("type","unknown"),
            "file":chunk.get("file","unknown"),
            "content":(
                chunk.get("content")
                or chunk.get("code")
                or chunk.get("text")
                or chunk.get("docstring")
                or ""
            )[:300]
        }
        
        results.append(structured_chunk)
        
    seen = set()
    unique_results = []
    for r in results:
        if r["content"] not in seen:
            unique_results.append(r)
            seen.add(r["content"])
        
    reranked=rerank_by_name(query, unique_results)    
    return reranked[:3]    


def build_retriever(file_path):
    chunks = extract_code_chunks(file_path)
    index, _ = build_faiss_index(chunks)
    return model, index, chunks

def rerank_by_name(query, retrieved):
    query_lower = query.lower()
    boosted = []

    for chunk in retrieved:
        score = 0

        if chunk["name"].lower() in query_lower:
            score += 5

        for word in query_lower.split():
            if word in chunk["content"].lower():
                score += 1

        boosted.append((score, chunk))

    boosted.sort(key=lambda x: x[0], reverse=True)
    return [c for _, c in boosted]

queries=[
    "Explain factorial",
    "How is mean calculated?",
    "Where is multiplication implemented?"
]


if __name__ == "__main__":
    file_path = r"F:\ML\Project\AI_Codebase_Intelligence\demo.py"
    model, index, chunks = build_retriever(file_path)

    for q in queries:
        print(f"\nQuery: {q}")
        retrieved = retrieve_relevant_chunks(q, model, index, chunks)
        print(f"Top {len(retrieved)} relevant chunks:")
        for r in retrieved:
            print("-", r["name"])