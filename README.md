# Local AI Assistant

A fully local AI assistant powered by Ollama with Mistral AI, featuring document Q&A capabilities through LlamaIndex and a modern React/Next.js frontend. This application runs completely locally without any cloud dependencies.

## Features

- 🏠 **Fully Local**: All processing and data stays on your machine - no cloud services
- 🤖 **Mistral AI**: Powered by Mistral via Ollama for high-quality responses
- 📚 **Document Processing**: Handles various document formats for local Q&A
- 🔍 **Local Embeddings**: Uses HuggingFace embeddings for document retrieval
- 🖥️ **Modern UI**: Clean, responsive interface with React and TailwindCSS
- 🛡️ **Privacy-Focused**: Your data never leaves your device
- 🌍 **Self-Hosted**: Run your own AI assistant on your hardware

## Prerequisites

Before starting, make sure you have:

1. [Node.js](https://nodejs.org/) (v18+)
2. [Python](https://www.python.org/) (v3.9+)
3. [Ollama](https://ollama.ai) installed

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/local-ai-assistant.git
cd local-ai-assistant
```

2. Install Python dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Install frontend dependencies:
```bash
npm install
```

4. Pull the Mistral model with Ollama:
```bash
ollama pull mistral
```

## Usage

1. Start Ollama (if not already running):
```bash
ollama serve
```

2. Start the FastAPI backend:
```bash
python src/main.py
```

3. Start the Next.js frontend (in a new terminal):
```bash
npm run dev
```

4. Access the application at `http://localhost:3000`

## Document Q&A

To use the document Q&A feature:

1. Place your documents (PDF, DOCX, TXT, etc.) in the `docs` folder
2. The system will automatically index them on startup
3. Use the chat interface to ask questions about your documents

## Project Structure

```
.
├── app/                 # Next.js application
│   ├── api/             # Frontend API routes
│   ├── components/      # React components
├── components/          # Shared React components
├── lib/                 # Utility functions and modules
│   ├── auth/            # Local authentication system
├── db/                  # Local database files
├── docs/                # Place your documents here for Q&A
├── src/                 # FastAPI backend
│   ├── main.py          # FastAPI server
│   ├── index_manager.py # LlamaIndex integration
│   └── document_loader.py # Document loading utilities
├── package.json         # Frontend dependencies
└── requirements.txt     # Backend dependencies
```

## Configuration

You can configure the application by modifying environment variables:

- `OLLAMA_BASE_URL`: URL for Ollama API (default: http://localhost:11434)
- `OLLAMA_MODEL`: Model to use (default: mistral)

## Advanced Usage

### Custom Models

You can use any model supported by Ollama:

```bash
# Pull additional models
ollama pull llama3
ollama pull phi

# Update the OLLAMA_MODEL environment variable
OLLAMA_MODEL=llama3 python src/main.py
```

### Customizing Embeddings

The application uses HuggingFace's sentence-transformers for embeddings. You can modify `src/index_manager.py` to use different embedding models.

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This software is provided as-is. It's designed for local use and doesn't collect or share any data. All processing happens on your local device. 