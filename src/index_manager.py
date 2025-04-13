from typing import Optional
from llama_index.core import VectorStoreIndex, Settings, SimpleDirectoryReader
from llama_index.llms.ollama import Ollama
from llama_index.core import Document
import numpy as np

class IndexManager:
    def __init__(self, model_name: str = "mistral"):
        self.model_name = model_name
        self.index: Optional[VectorStoreIndex] = None
        self._setup_models()

    def _setup_models(self):
        """Initialize the LLM and embedding models."""
        try:
            # Setup LLM
            llm = Ollama(model=self.model_name, request_timeout=60.0)
            Settings.llm = llm
            print(f"Initialized LLM with model: {self.model_name}")

            # Use default embedding model
            print("Using default embedding model")

        except Exception as e:
            raise Exception(f"Failed to initialize models: {str(e)}")

    def create_index(self, documents: list[Document]):
        """Create a vector index from the provided documents."""
        try:
            print("Creating vector index...")
            self.index = VectorStoreIndex.from_documents(
                documents,
                show_progress=True
            )
            print("Index created successfully")
        except Exception as e:
            raise Exception(f"Failed to create index: {str(e)}")

    def get_query_engine(self, similarity_top_k: int = 3):
        """Get a query engine from the index."""
        if not self.index:
            raise ValueError("Index not created. Call create_index() first.")
        
        return self.index.as_query_engine(
            similarity_top_k=similarity_top_k,
            response_mode="compact"
        ) 