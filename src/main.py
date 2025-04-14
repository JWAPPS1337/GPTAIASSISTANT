import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from llama_index.core import Document, VectorStoreIndex, Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from document_loader import DocumentLoader
from index_manager import IndexManager
from query_engine import QueryManager

app = FastAPI(title="GPT AI Assistant API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "ok", "message": "Server is running"}

# Initialize components
docs_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")
doc_loader = DocumentLoader(docs_path)
index_manager = IndexManager()

class QueryRequest(BaseModel):
    query: str

class DocumentInfo(BaseModel):
    filename: str
    size: int
    type: str

@app.on_event("startup")
async def startup_event():
    """Initialize the index on startup"""
    print("Starting up server...")
    try:
        print("Loading documents...")
        documents = doc_loader.load_documents()
        print(f"Loaded {len(documents)} documents")
        print("Creating index...")
        index_manager.create_index(documents)
        print("Index created successfully")
    except Exception as e:
        print(f"Error during startup: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")

@app.get("/documents", response_model=List[DocumentInfo])
async def get_documents():
    """Get information about loaded documents"""
    try:
        return doc_loader.get_document_info()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
@app.get("/query")
async def query(request: QueryRequest):
    """Process a query and return the response"""
    try:
        query_manager = QueryManager(index_manager.get_query_engine())
        response = query_manager.process_query(request.query)
        return {
            "id": str(hash(request.query)),  # Generate a unique ID for the message
            "content": response["response"],
            "role": "assistant",
            "createdAt": "",  # The frontend will handle the timestamp
            "updatedAt": "",
            "sources": response["sources"] if "sources" in response else []
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a new document"""
    return {"message": "Upload is temporarily disabled"}
    try:
        # Save the uploaded file
        file_path = os.path.join(docs_path, file.filename)
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Reload documents and recreate index
        documents = doc_loader.load_documents()
        index_manager.create_index(documents)
        
        return {"message": "Document uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    try:
        print("Starting server on http://127.0.0.1:5001")
        uvicorn.run(app, host="127.0.0.1", port=5001, log_level="debug")
    except Exception as e:
        print(f"Failed to start server: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}") 