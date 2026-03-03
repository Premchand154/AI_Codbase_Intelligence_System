```markdown
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![FAISS](https://img.shields.io/badge/FAISS-VectorSearch-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
```

# AI Codebase Intelligence System

An AI-powered code analysis system that allows you to upload a code file and interact with it using natural language.

It uses **semantic search + LLM grounding** to provide accurate, context-aware answers about your code.

---

# Project Overview

> **RAG-based AI Codebase Intelligence System**

It combines:

* AST-based code parsing
* Sentence-transformer embeddings
* FAISS vector search
* Smart reranking
* Ollama (DeepSeek Coder) LLM
* Streamlit UI

---


## Features

* Semantic code search using FAISS
* SentenceTransformer embeddings (`all-MiniLM-L6-v2`)
* DeepSeek-Coder via Ollama
* AST-based Python parsing (functions & classes)
* Multiple analysis modes:

  * QA Mode
  * Bug Detection
  * Architecture Analysis
  * Optimization Suggestions
* Streamlit Web UI
* Docker support

---

## Architecture

```
User Query
    ↓
Code Parser (AST)
    ↓
Chunking (functions/classes)
    ↓
Embeddings (SentenceTransformer)
    ↓
FAISS Vector Search
    ↓
Reranking
    ↓
Ollama (DeepSeek-Coder)
    ↓
Grounded Answer
```

---

## Core Components

### Code Parser

File: 

* Uses Python AST
* Extracts:

  * Classes
  * Functions
* Fallback for non-Python files

---

### Embedding & Indexing

File: 

* SentenceTransformer (`all-MiniLM-L6-v2`)
* FAISS `IndexFlatL2`
* Converts code chunks → vectors

---

### Retriever

File: 

* Embeds query
* Vector similarity search
* Name-based reranking
* Deduplication

---

### LLM Engine

File: 

* Uses Ollama
* Model: `deepseek-coder`
* Streaming response
* Supports:

  * QA
  * Bug analysis
  * Architecture explanation
  * Optimization advice

---

### Streamlit App

File: 

* Upload code file
* Select analysis mode
* View retrieved chunks
* See LLM output

---

## Installation

### Clone Repo

```bash
git clone https://github.com/yourusername/AI-Codebase-Intelligence.git
cd AI-Codebase-Intelligence
```

---

### Install Requirements

File: 

```bash
pip install -r requirements.txt
```

---

### Install Ollama

Install from:

[https://ollama.ai](https://ollama.ai)

Then pull model:

```bash
ollama pull deepseek-coder
```

---

### Run Application

```bash
streamlit run app/main.py
```

---

## Run with Docker

```bash
docker build -t ai-code-intelligence .
docker run -p 8501:8501 ai-code-intelligence
```

---

## Example Queries

* "Explain factorial step by step"
* "Is there recursion in this file?"
* "Find performance bottlenecks"
* "Explain system architecture"
* "Suggest Pythonic improvements"

---

## Future Improvements

* Multi-file codebase support
* Persistent vector database
* Project-wide architecture graph
* GitHub repo ingestion
* Test generation
* Code modification suggestions
* Support for more languages
* CI integration

---

## Tech Stack

* Python
* Streamlit
* FAISS
* SentenceTransformers
* Ollama
* DeepSeek-Coder

---




