import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from document_loader import DocumentLoader
from index_manager import IndexManager
from query_engine import QueryManager

app = FastAPI(title="GPT AI Assistant API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    try:
        documents = doc_loader.load_documents()
        index_manager.create_index(documents)
    except Exception as e:
        print(f"Error during startup: {str(e)}")

@app.get("/documents", response_model=List[DocumentInfo])
async def get_documents():
    """Get information about loaded documents"""
    try:
        return doc_loader.get_document_info()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
async def query(request: QueryRequest):
    """Process a query and return the response"""
    try:
        query_manager = QueryManager(index_manager.get_query_engine())
        response = query_manager.process_query(request.query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a new document"""
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
    uvicorn.run(app, host="0.0.0.0", port=8000) 