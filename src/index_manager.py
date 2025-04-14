from typing import Optional, List
import os
import logging
from llama_index.core import VectorStoreIndex, Settings, Document
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

logger = logging.getLogger(__name__)

class IndexManager:
    def __init__(self, model_name: str = "mistral", ollama_base_url: str = "http://localhost:11434"):
        """
        Initialize the IndexManager with the specified Ollama model.
        
        Args:
            model_name: The name of the Ollama model to use (default: "mistral")
            ollama_base_url: The base URL for the Ollama API (default: "http://localhost:11434")
        """
        self.model_name = model_name
        self.ollama_base_url = ollama_base_url
        self.index: Optional[VectorStoreIndex] = None
        self._setup_models()

    def _setup_models(self):
        """Initialize the LLM and embedding models."""
        try:
            # Setup LLM with Ollama
            llm = Ollama(
                model=self.model_name,
                request_timeout=60.0,
                base_url=self.ollama_base_url,
                temperature=0.1,  # Lower temperature for more deterministic responses in Q&A
                additional_kwargs={"num_ctx": 4096},  # Increase context window if available
            )
            Settings.llm = llm
            logger.info(f"Initialized LLM with Ollama model: {self.model_name} at {self.ollama_base_url}")

            # Create cache directory if it doesn't exist
            cache_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models_cache")
            os.makedirs(cache_dir, exist_ok=True)
            
            # Use HuggingFace for embeddings - faster and more efficient than OpenAI
            embed_model = HuggingFaceEmbedding(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                cache_folder=cache_dir
            )
            Settings.embed_model = embed_model
            logger.info("Using HuggingFace for embeddings (sentence-transformers/all-MiniLM-L6-v2)")

        except Exception as e:
            logger.error(f"Failed to initialize models: {str(e)}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise Exception(f"Failed to initialize models: {str(e)}")

    def create_index(self, documents: List[Document]):
        """Create a vector index from the provided documents."""
        try:
            logger.info(f"Creating vector index from {len(documents)} documents...")
            self.index = VectorStoreIndex.from_documents(
                documents,
                show_progress=True
            )
            logger.info("Index created successfully")
        except Exception as e:
            logger.error(f"Failed to create index: {str(e)}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise Exception(f"Failed to create index: {str(e)}")

    def get_query_engine(self, similarity_top_k: int = 3):
        """Get a query engine from the index."""
        if not self.index:
            logger.error("Index not created. Call create_index() first.")
            raise ValueError("Index not created. Call create_index() first.")
        
        return self.index.as_query_engine(
            similarity_top_k=similarity_top_k
        ) 