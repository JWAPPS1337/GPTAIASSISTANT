import os
from typing import List
from llama_index.core import Document
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter

class DocumentLoader:
    def __init__(self, docs_path: str = "./docs"):
        self.docs_path = docs_path
        self.node_parser = SentenceSplitter(chunk_size=1024, chunk_overlap=20)

    def load_documents(self) -> List[Document]:
        """Load and parse documents from the specified directory."""
        if not os.path.exists(self.docs_path):
            raise FileNotFoundError(f"Documents directory not found: {self.docs_path}")
        
        try:
            documents = SimpleDirectoryReader(self.docs_path).load_data()
            if not documents:
                raise ValueError(f"No documents found in {self.docs_path}")
            
            print(f"Loaded {len(documents)} documents from {self.docs_path}")
            return documents
        except Exception as e:
            raise Exception(f"Error loading documents: {str(e)}")

    def get_document_info(self) -> List[dict]:
        """Return information about loaded documents."""
        try:
            info = []
            for file in os.listdir(self.docs_path):
                file_path = os.path.join(self.docs_path, file)
                if os.path.isfile(file_path):
                    info.append({
                        "filename": file,
                        "size": os.path.getsize(file_path),
                        "type": os.path.splitext(file)[1][1:].upper()
                    })
            return info
        except Exception as e:
            raise Exception(f"Error getting document info: {str(e)}") 