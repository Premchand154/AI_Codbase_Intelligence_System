import ast
import os


def extract_code_chunks(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        source = f.read()

    ext = os.path.splitext(file_path)[1].lower()

    # If not Python → fallback to whole file chunk
    if ext != ".py":
        return [{
            "file": file_path,
            "type": "file",
            "name": os.path.basename(file_path),
            "lineno": 1,
            "docstring": None,
            "content": source
        }]

    # Try Python AST parsing
    try:
        tree = ast.parse(source)
    except SyntaxError:
        # If invalid Python → fallback to whole file
        return [{
            "file": file_path,
            "type": "file",
            "name": os.path.basename(file_path),
            "lineno": 1,
            "docstring": None,
            "content": source
        }]

    chunks = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            chunk = ast.get_source_segment(source, node)
            chunks.append({
                "file": file_path,
                "type": "class",
                "name": node.name,
                "lineno": node.lineno,
                "docstring": ast.get_docstring(node),
                "content": chunk
            })

        elif isinstance(node, ast.FunctionDef):
            chunk = ast.get_source_segment(source, node)
            chunks.append({
                "file": file_path,
                "type": "function",
                "name": node.name,
                "lineno": node.lineno,
                "docstring": ast.get_docstring(node),
                "content": chunk
            })

    # If no functions/classes found → fallback to whole file
    if not chunks:
        return [{
            "file": file_path,
            "type": "file",
            "name": os.path.basename(file_path),
            "lineno": 1,
            "docstring": None,
            "content": source
        }]

    return chunks
if __name__=="__main__":
    chunks=extract_code_chunks(r"F:\ML\Project\AI_Codebase_Intelligence\demo.py")
    class_names=[]
    function_names=[]
    for chunk in chunks:
        if chunk["type"]=="class":
            class_names.append(chunk["name"])
        elif chunk["type"]=="function":
            function_names.append(chunk["name"])
    print("Classes:",class_names)
    print("Functions:",function_names)
    print("Number of chunks:",len(chunks))