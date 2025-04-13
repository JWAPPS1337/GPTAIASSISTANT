from typing import Optional, Dict, List
from llama_index.core.query_engine import BaseQueryEngine

class QueryManager:
    def __init__(self, query_engine: BaseQueryEngine):
        self.query_engine = query_engine

    def process_query(self, query: str) -> Dict:
        """Process a user query and return the response with metadata."""
        try:
            response = self.query_engine.query(query)
            return self._format_response(response)
        except Exception as e:
            raise Exception(f"Error processing query: {str(e)}")

    def _format_response(self, response) -> Dict:
        """Format the response with source information and metadata."""
        result = {
            "response": response.response.strip(),
            "sources": []
        }
        
        # Add source information if available
        if hasattr(response, 'source_nodes') and response.source_nodes:
            for node in response.source_nodes:
                source = {
                    "file_name": node.metadata.get('file_name', 'Unknown'),
                    "score": float(node.score) if hasattr(node, 'score') else None,
                    "text": node.text[:200] + "..." if len(node.text) > 200 else node.text
                }
                result["sources"].append(source)
        
        return result 