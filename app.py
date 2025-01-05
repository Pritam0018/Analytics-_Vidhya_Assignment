import streamlit as st
import os
import pandas as pd
from langchain_groq import ChatGroq
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain.schema import Document  # Import Document class
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load the GROQ API Key
os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

# HuggingFace Embeddings
os.environ['HF_TOKEN'] = os.getenv("HF_TOKEN")
from langchain_huggingface import HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Initialize LLM with Groq API
llm = ChatGroq(groq_api_key=groq_api_key, model_name="Llama3-8b-8192")

# Prompt template for RAG
prompt = ChatPromptTemplate.from_template(
    """
    Based on the provided context, answer the question and provide only 5 relevant course titles.
    <context>
    {context}
    <context>
    Question:{input}
    Answer with only 5 relevant course titles, please.
    """
)

# Function to load and process course data from CSV and create vector embeddings
def create_vector_embedding():
    if "vectors" not in st.session_state:
        # Load course data from CSV
        course_data = pd.read_csv("D:\\PROJECTS\\web_scrap\\analytics_vidhya_courses.csv")

        # Ensure the CSV contains a 'title' column
        if "title" not in course_data.columns:
            st.error("CSV file must contain a 'title' column.")
            return

        # Prepare documents from the course titles using the Document class
        st.session_state.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        st.session_state.documents = [
            Document(page_content=row["title"], metadata={"title": row["title"]})
            for _, row in course_data.iterrows()
        ]

        # Split text into manageable chunks (e.g., course titles in this case)
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.documents)

        # Create the vector store
        st.session_state.vectors = FAISS.from_documents(st.session_state.final_documents, st.session_state.embeddings)

# Streamlit app UI
st.title("Smart Course Search System")

# User input for query
user_prompt = st.text_input("Enter your query to search for courses:")

# Button to trigger vector embedding creation
if st.button("|Click Here|"):
    create_vector_embedding()  # Use the path to your CSV file
    st.write("Result:")

import time

# Process user query
if user_prompt:
    # Create the document chain
    document_chain = create_stuff_documents_chain(llm, prompt)

    # Retrieve the documents based on the user query
    retriever = st.session_state.vectors.as_retriever()
    retriever_chain = create_retrieval_chain(retriever, document_chain)

    # Measure response time
    start = time.process_time()
    response = retriever_chain.invoke({'input': user_prompt})
    st.write(f"Response time: {time.process_time() - start} seconds")

    # Display the response
    st.subheader("Response:")
    st.write(response['answer'])

    # Display relevant course titles with links (only 2 or 3 titles)
    with st.expander("Relevant Courses"):
        relevant_courses = response.get('context', [])[:3]  # Limit to 3 courses
        for doc in relevant_courses:
            st.write(f"- **{doc.metadata['title']}**")
            st.write('---------------------------')
