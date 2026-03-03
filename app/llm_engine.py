from retriever import build_retriever, retrieve_relevant_chunks
import ollama


def generate_answer(query, retrieved, mode="qa"):
    
    context = "\n\n".join(
        f"{chunk['type']} {chunk['name']}:\n{chunk['content']}"
        for chunk in retrieved
    )

    if mode == "bug":
        instruction_block = """
Analyze the provided code for:
- Logical bugs
- Edge case failures
- Performance inefficiencies
- Code smells

Be critical and technical.
"""
    elif mode == "architecture":
        instruction_block = """
Explain the overall architecture:
- Major components
- Data flow
- Responsibilities
- Design patterns used
"""
    elif mode == "optimize":
        instruction_block = """
Suggest:
- Algorithmic improvements
- Time complexity improvements
- Memory optimizations
- Cleaner Pythonic refactoring
"""
    else:  # default QA
        instruction_block = """
Answer ONLY using the provided code.
If the answer is not in the context, say:
"Not found in provided code."
Be precise and technical.
Explain step by step if needed.
"""

    prompt = f"""
You are a senior software engineer performing grounded code analysis.

USER QUESTION:
{query}

CODE CONTEXT:
{context}

INSTRUCTIONS:
{instruction_block}
"""

    response = ollama.chat(
        model="deepseek-coder",
        messages=[
            {"role": "user", "content": prompt}
        ],
        stream=True
    )
    full_response = ""
    for chunk in response:
        content = chunk["message"]["content"]
        print(content, end="", flush=True)
        full_response += content

    return full_response

if __name__ == "__main__":
    file_path = r"F:\ML\Project\AI_Codebase_Intelligence\demo.py"

    # Build retriever once
    model, index, chunks = build_retriever(file_path)

    queries = [
        "Explain factorial step by step",
        "What does std_dev compute?",
        "Is there any recursion in this code?"
    ]

    for query in queries:
        print("\n" + "="*60)
    print("QUESTION:", query)

    retrieved = retrieve_relevant_chunks(query, model, index, chunks)

    answer = generate_answer(query, retrieved, mode="qa")

    print("\nANSWER:\n")
    print(answer)
    
    print("\nBUG ANALYSIS:")
    generate_answer(query, retrieved, mode="bug")
    print("\nARCHITECTURE ANALYSIS:")
    generate_answer(query, retrieved, mode="architecture")
    print("\nOPTIMIZATION SUGGESTIONS:")
    generate_answer(query, retrieved, mode="optimize")        