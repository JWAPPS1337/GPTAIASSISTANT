import streamlit as st
from document_loader import DocumentLoader
from index_manager import IndexManager

# Set page config
st.set_page_config(
    page_title="Local Document Q&A",
    page_icon="📚",
    layout="centered"
)

# Configure Streamlit to be accessible
import os
os.environ['STREAMLIT_SERVER_PORT'] = '8502'
os.environ['STREAMLIT_SERVER_ADDRESS'] = '0.0.0.0'
os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'

# Add custom CSS to make it cleaner
st.markdown("""
    <style>
    .stApp {
        max-width: 800px;
        margin: 0 auto;
    }
    .stTextInput {
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def initialize_qa_system():
    """Initialize the QA system once and cache it."""
    try:
        docs_path = "docs"  # Relative path from the root
        doc_loader = DocumentLoader(docs_path)
        index_manager = IndexManager()
        
        # Load and index documents
        documents = doc_loader.load_documents()
        index_manager.create_index(documents)
        
        return index_manager.get_query_engine()
    except Exception as e:
        st.error(f"Error initializing system: {str(e)}")
        return None

# Main UI
st.title("📚 Local Document Q&A")

# Initialize the QA system
query_engine = initialize_qa_system()

if query_engine:
    # Input text box
    user_question = st.text_input(
        "Ask a question about your documents",
        placeholder="Enter your question here...",
        key="question_input"
    )

    # Submit button
    if st.button("Submit", type="primary"):
        if user_question:
            try:
                with st.spinner("Processing your question..."):
                    # Get the response
                    response = query_engine.query(user_question)
                    
                    # Display the response in a clean format
                    st.markdown("### Answer")
                    st.write(response.response)
                    
                    # Display sources if available
                    if hasattr(response, 'source_nodes') and response.source_nodes:
                        st.markdown("### Sources")
                        for i, node in enumerate(response.source_nodes, 1):
                            source = node.metadata.get('file_name', 'Unknown')
                            st.text(f"{i}. {source}")
            except Exception as e:
                st.error(f"Error processing question: {str(e)}")
        else:
            st.warning("Please enter a question first.") 