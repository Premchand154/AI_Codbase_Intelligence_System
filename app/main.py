import streamlit as st
import os
from retriever import build_retriever, retrieve_relevant_chunks
from llm_engine import generate_answer
from embedding import build_faiss_index
from parser import extract_code_chunks

st.set_page_config(page_title="AI Codebase Intelligence System",layout="wide")
st.title("AI Codebase Intelligence System")

uploaded_file = st.file_uploader("Upload your code file", type=["py", "js", "java", "cpp"])

@st.cache_resource
def build_cached_retriever(file_path):
    return build_retriever(file_path)

if uploaded_file is not None:
    file_path=f"temp_{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success("File uploaded succcessfully!")
    
    
    model,index,chunks=build_cached_retriever(file_path)
    
    query=st.text_input("Ask a question about your codebase:")
    
    mode = st.selectbox(
    "Analysis Mode",
    ["qa", "bug", "architecture", "optimize"]
    )
    
    if st.button("Analyze code") and query:
        results=retrieve_relevant_chunks(query, model, index, chunks,k=3)
        
        st.subheader("Retrieved Code Context")
        for r in results:
            st.code(r['content'], height=200)
            
        answer=generate_answer(query, results,mode=mode)
        st.subheader("LLM Analysis")
        st.info(answer)
            

