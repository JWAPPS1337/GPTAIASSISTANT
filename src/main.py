import os
import json
import logging
from fastapi import FastAPI, UploadFile, File, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any, Union
from llama_index.core import Document, VectorStoreIndex, Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from document_loader import DocumentLoader
from index_manager import IndexManager
from query_engine import QueryManager
from auth_middleware import JWTMiddleware, get_current_user
import httpx
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Local AI Assistant API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add JWT middleware
app.add_middleware(JWTMiddleware)

# Configuration from environment variables
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "mistral")
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "localhost")
OLLAMA_PORT = int(os.environ.get("OLLAMA_PORT", "11434"))

# If OLLAMA_BASE_URL is not set but OLLAMA_HOST and OLLAMA_PORT are,
# construct the base URL
if not os.environ.get("OLLAMA_BASE_URL") and (os.environ.get("OLLAMA_HOST") or os.environ.get("OLLAMA_PORT")):
    OLLAMA_BASE_URL = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}"

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    model: str = OLLAMA_MODEL
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    stream: bool = False
    use_rag: bool = False  # Flag to indicate whether to use RAG

class QueryRequest(BaseModel):
    query: str
    temperature: float = 0.7

class DocumentInfo(BaseModel):
    filename: str
    size: int
    type: str

class ChatResponse(BaseModel):
    id: str
    content: str
    role: str = "assistant"
    createdAt: str = ""
    updatedAt: str = ""
    sources: List[Dict[str, Any]] = []

# Initialize components
docs_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")
doc_loader = DocumentLoader(docs_path)
index_manager = IndexManager(
    model_name=OLLAMA_MODEL,
    ollama_base_url=OLLAMA_BASE_URL
)

@app.get("/")
async def root():
    return {"status": "ok", "message": "Local AI Assistant API is running"}

@app.on_event("startup")
async def startup_event():
    """Initialize the index on startup"""
    logger.info("Starting up server...")
    try:
        logger.info(f"Checking Ollama availability at {OLLAMA_BASE_URL}...")
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{OLLAMA_BASE_URL}/api/tags")
                if response.status_code == 200:
                    models = response.json().get("models", [])
                    model_names = [model.get("name") for model in models]
                    if OLLAMA_MODEL not in model_names:
                        logger.warning(f"Model {OLLAMA_MODEL} not found in Ollama. Available models: {model_names}")
                        logger.info(f"You may need to pull the model using: ollama pull {OLLAMA_MODEL}")
                    else:
                        logger.info(f"Model {OLLAMA_MODEL} is available in Ollama")
                else:
                    logger.warning(f"Ollama returned status code {response.status_code}")
            except Exception as e:
                logger.error(f"Failed to connect to Ollama at {OLLAMA_BASE_URL}: {str(e)}")
                logger.error("Make sure Ollama is running and accessible")
                
        logger.info("Loading documents...")
        documents = doc_loader.load_documents()
        logger.info(f"Loaded {len(documents)} documents")
        
        logger.info("Creating index...")
        index_manager.create_index(documents)
        logger.info("Index created successfully")
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")

# Authentication dependency for protected endpoints
async def get_token(authorization: Optional[str] = Header(None)) -> Optional[str]:
    if authorization and authorization.startswith("Bearer "):
        return authorization.replace("Bearer ", "")
    return None

@app.get("/documents", response_model=List[DocumentInfo])
async def get_documents(token: Optional[str] = Depends(get_token)):
    """Get information about loaded documents"""
    try:
        return doc_loader.get_document_info()
    except Exception as e:
        logger.error(f"Error retrieving documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=ChatResponse)
async def query(request: QueryRequest, token: Optional[str] = Depends(get_token)):
    """Process a document query and return the response with sources"""
    try:
        query_manager = QueryManager(index_manager.get_query_engine())
        response = query_manager.process_query(request.query)
        
        return ChatResponse(
            id=str(hash(request.query)),
            content=response["response"],
            sources=response["sources"] if "sources" in response else []
        )
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, token: Optional[str] = Depends(get_token)):
    """Process a chat request with optional RAG"""
    try:
        logger.info(f"Received chat request for model: {request.model}")
        
        # Get user's last message
        user_message = next((msg.content for msg in reversed(request.messages) if msg.role == "user"), None)
        
        # If RAG is enabled and we have a user message, retrieve context
        context = ""
        sources = []
        if request.use_rag and user_message:
            logger.info("RAG enabled, retrieving context from documents...")
            
            # Get query engine from the index manager
            query_engine = index_manager.get_query_engine()
            
            # Use QueryManager to get context and sources
            query_manager = QueryManager(query_engine)
            query_result = query_manager.process_query(user_message)
            
            # Extract context and sources from the query result
            context = query_result.get("response", "")
            sources = query_result.get("sources", [])
            
            logger.info(f"Retrieved context of length {len(context)} with {len(sources)} sources")
        
        # Format messages for Ollama API
        formatted_messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        
        # If we have RAG context, add it to the system message or create one
        if context:
            # Check if there's an existing system message
            has_system = any(msg["role"] == "system" for msg in formatted_messages)
            
            if has_system:
                # Append the context to the existing system message
                for msg in formatted_messages:
                    if msg["role"] == "system":
                        msg["content"] += f"\n\nRelevant context from documents:\n{context}"
                        break
            else:
                # Create a new system message with the context
                formatted_messages.insert(0, {
                    "role": "system", 
                    "content": f"You are a helpful assistant. Use the following context from documents to answer the user's question if relevant:\n\n{context}"
                })
        
        # Set up the request to Ollama
        ollama_request = {
            "model": request.model,
            "messages": formatted_messages,
            "options": {
                "temperature": request.temperature
            }
        }
        
        if request.max_tokens:
            ollama_request["options"]["num_predict"] = request.max_tokens
            
        logger.debug(f"Sending to Ollama: {ollama_request}")
        
        # Make request to Ollama
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{OLLAMA_BASE_URL}/api/chat",
                json=ollama_request
            )
            
            if response.status_code != 200:
                logger.error(f"Ollama error: {response.text}")
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Ollama API error: {response.text}"
                )
            
            ollama_response = response.json()
            logger.debug(f"Received from Ollama: {ollama_response}")
            
            # Create response with content and sources if RAG was used
            return ChatResponse(
                id=str(int(time.time())),
                content=ollama_response.get("message", {}).get("content", ""),
                sources=sources if request.use_rag else []
            )
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error: {e}")
        raise HTTPException(status_code=500, detail=f"HTTP error: {str(e)}")
    except httpx.RequestError as e:
        logger.error(f"Request error: {e}")
        raise HTTPException(
            status_code=503,
            detail="Could not connect to Ollama. Is the service running?"
        )
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload")
async def upload_document(file: UploadFile = File(...), token: Optional[str] = Depends(get_token)):
    """Upload a new document"""
    try:
        # Save the uploaded file
        file_path = os.path.join(docs_path, file.filename)
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        logger.info(f"Document uploaded: {file.filename}")
        
        # Reload documents and recreate index
        documents = doc_loader.load_documents()
        index_manager.create_index(documents)
        
        return {"message": "Document uploaded successfully"}
    except Exception as e:
        logger.error(f"Error uploading document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ollama/models")
async def get_ollama_models(token: Optional[str] = Depends(get_token)):
    """Get available models from Ollama"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{OLLAMA_BASE_URL}/api/tags")
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Ollama API error: {response.text}"
                )
            
            return response.json()
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail="Could not connect to Ollama. Is the service running?"
        )
    except Exception as e:
        logger.error(f"Error getting Ollama models: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    try:
        logger.info("Starting server on http://127.0.0.1:5001")
        uvicorn.run(app, host="127.0.0.1", port=5001, log_level="info")
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}") 