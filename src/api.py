from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from document_loader import DocumentLoader
from index_manager import IndexManager
from query_engine import QueryManager

# Pydantic models for request/response
class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str
    sources: list[str]

# Initialize FastAPI app
app = FastAPI(title="GPT AI Assistant API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components at startup
docs_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")
doc_loader = DocumentLoader(docs_path)
index_manager = IndexManager()

# Load and index documents
documents = doc_loader.load_documents()
index_manager.create_index(documents)

# Setup query engine
query_manager = QueryManager(index_manager.get_query_engine())

@app.get("/")
async def root():
    return {"status": "ok", "message": "GPT AI Assistant API is running"}

@app.post("/api/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    try:
        # Get answer from query engine
        answer = query_manager.get_response(request.query)
        
        # For now, returning empty sources list - can be enhanced later
        return QueryResponse(answer=answer, sources=[])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 