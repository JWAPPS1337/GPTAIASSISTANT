# Local Document Q&A System

A local-first document question-answering system built with LlamaIndex and FastEmbed, featuring a Streamlit web interface. This tool allows businesses to query their documents locally without relying on cloud services.

## Features

- 🏠 **Fully Local**: All processing happens on your machine - no cloud dependencies
- 📚 **Document Processing**: Handles various document formats
- 🔍 **Fast Embedding**: Uses FastEmbed for efficient document embedding
- 🖥️ **Web Interface**: Clean Streamlit UI for easy interaction
- 🚀 **Quick Setup**: Simple installation and configuration

## Installation

1. Clone the repository:
```bash
git clone [your-repo-url]
cd [repo-name]
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Place your documents in the `docs` directory

2. Run the Streamlit interface:
```bash
python -m streamlit run src/app.py
```

3. Access the web interface at `http://localhost:8502`

## Project Structure

```
.
├── src/
│   ├── app.py              # Streamlit web interface
│   ├── document_loader.py  # Document loading utilities
│   └── index_manager.py    # LlamaIndex integration
├── docs/                   # Place your documents here
├── requirements.txt        # Project dependencies
└── README.md              # This file
```

## Dependencies

- Python 3.8+
- LlamaIndex
- FastEmbed
- Streamlit
- Other dependencies listed in requirements.txt

## Local Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install development dependencies:
```bash
pip install -r requirements.txt
```

## License

MIT License - See LICENSE file for details 