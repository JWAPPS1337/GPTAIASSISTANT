from typing import Optional
from llama_index.core.query_engine import BaseQueryEngine

class QueryManager:
    def __init__(self, query_engine: BaseQueryEngine):
        self.query_engine = query_engine

    def process_query(self, query: str) -> str:
        """Process a user query and return the response."""
        try:
            response = self.query_engine.query(query)
            return self._format_response(response)
        except Exception as e:
            return f"Error processing query: {str(e)}"

    def _format_response(self, response) -> str:
        """Format the response with source information."""
        formatted = response.response.strip()
        
        # Add source information if available
        if hasattr(response, 'source_nodes') and response.source_nodes:
            formatted += "\n\nSources:"
            for i, node in enumerate(response.source_nodes, 1):
                source = node.metadata.get('file_name', 'Unknown')
                formatted += f"\n{i}. {source}"
        
        return formatted

    def interactive_mode(self):
        """Run an interactive Q&A session."""
        print("\nReady! Ask questions about your documents. Type 'exit' to quit.\n")
        
        while True:
            try:
                query = input("You: ").strip()
                if query.lower() in ["exit", "quit"]:
                    break
                if not query:
                    continue
                
                response = self.process_query(query)
                print("\nAI:", response, "\n")
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"\nError: {str(e)}\n") 