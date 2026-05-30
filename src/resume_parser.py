from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# llm
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY")
)

def load_resume(resume_path: str) -> Chroma:
    """Load PDF resume and store in ChromaDB"""
    
    loader = PyPDFLoader(resume_path)
    documents = loader.load()
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(documents)
    
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory="./chroma_db"
    )
    
    print(f"Resume loaded — {len(chunks)} chunks stored")
    return vectorstore


def extract_profile(vectorstore: Chroma) -> str:
    """Extract structured profile from resume"""
    
    results = vectorstore.similarity_search(
        "skills experience education projects",
        k=10
    )
    
    resume_text = "\n".join([doc.page_content for doc in results])
    
    prompt = f"""
Extract a structured profile from this resume text.

Resume:
{resume_text}

Return exactly this format:
SKILLS: (list all technical skills)
EXPERIENCE: (years of experience and roles)
EDUCATION: (degree, university, year)
PROJECTS: (key projects with technologies used)
LEVEL: (entry/mid/senior based on experience)
SUMMARY: (2 sentence professional summary)
"""
    
    response = llm.invoke(prompt)
    return response.content