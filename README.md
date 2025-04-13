# Local GPT Document Q&A

A privacy-focused document Q&A system that runs entirely offline using Ollama and LlamaIndex.

## Features

- 🔒 100% offline operation - no cloud dependencies
- 📚 Support for PDF, TXT, and DOCX files
- 💬 Interactive chat interface
- 🔍 Contextual answers with source tracking
- ⚡ Fast local inference using Mistral model

## Prerequisites

1. Install [Ollama](https://ollama.ai/)
2. Pull the Mistral model:
   ```bash
   ollama pull mistral
   ```

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `docs` folder and add your documents:
   ```bash
   mkdir docs
   # Add your PDF, TXT, or DOCX files to the docs folder
   ```

## Usage

1. Start the Q&A system:
   ```bash
   python src/main.py
   ```

2. Ask questions about your documents in natural language
3. Type 'exit' to quit

## Project Structure

```
.
├── docs/               # Place your documents here
├── src/
│   ├── main.py        # Entry point
│   ├── document_loader.py    # Document loading and parsing
│   ├── index_manager.py     # Vector index management
│   └── query_engine.py      # Query processing and response generation
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Future Enhancements

- [ ] Desktop GUI (Tauri/Electron)
- [ ] Source chunk highlighting
- [ ] Markdown export
- [ ] Auto-reload on document changes 