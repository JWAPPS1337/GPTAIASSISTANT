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

    def get_document_info(self) -> str:
        """Return a summary of loaded documents."""
        try:
            documents = self.load_documents()
            info = []
            for doc in documents:
                filename = os.path.basename(doc.metadata.get('file_name', 'Unknown'))
                info.append(f"- {filename}")
            return "\n".join(info)
        except Exception as e:
            return f"Error getting document info: {str(e)}" 