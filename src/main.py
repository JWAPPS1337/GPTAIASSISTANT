import os
from document_loader import DocumentLoader
from index_manager import IndexManager
from query_engine import QueryManager

def main():
    try:
        # Initialize components
        docs_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")
        doc_loader = DocumentLoader(docs_path)
        index_manager = IndexManager()
        
        # Load and index documents
        documents = doc_loader.load_documents()
        index_manager.create_index(documents)
        
        # Setup query engine
        query_manager = QueryManager(index_manager.get_query_engine())
        
        # Print document summary
        print("\nLoaded Documents:")
        print(doc_loader.get_document_info())
        
        # Start interactive session
        query_manager.interactive_mode()
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 