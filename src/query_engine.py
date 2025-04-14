from typing import Optional, Dict, List
from llama_index.core.query_engine import BaseQueryEngine

class QueryManager:
    def __init__(self, query_engine: BaseQueryEngine):
        self.query_engine = query_engine

    def process_query(self, query: str) -> Dict:
        """Process a user query and return the response with metadata."""
        try:
            response = self.query_engine.query(query)
            return {
                "response": str(response.response).strip(),
                "sources": [
                    {
                        "file_name": node.metadata.get("file_name", "Unknown"),
                        "score": float(node.score) if hasattr(node, "score") else None,
                        "text": node.text[:200] + "..." if len(node.text) > 200 else node.text
                    }
                    for node in response.source_nodes
                ] if hasattr(response, "source_nodes") else []
            }
        except Exception as e:
            raise Exception(f"Error processing query: {str(e)}") 