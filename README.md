# RAG Chat Application

A production-grade conversational AI application featuring Retrieval-Augmented Generation (RAG) capabilities, built with Gradio and Ollama. The application provides an intuitive chat interface with document upload functionality and real-time visualization of the AI's thinking process.

## 🌟 Features

- **Interactive Chat Interface** - Clean, responsive Gradio-based UI
- **RAG Capabilities** - Upload and query documents for context-aware responses
- **Thinking Visualization** - Real-time display of the LLM's reasoning process
- **Document Management** - Upload, view, and manage multiple documents
- **Streaming Responses** - Watch responses generate in real-time
- **History Tracking** - Monitor conversation size and context

## 🏗️ Architecture

This project follows clean architecture principles with clear separation of concerns:

```
app/
├── main.py                    # Application entry point
├── handlers/                  # Business logic layer
│   ├── chat_handlers.py      # Chat and message processing
│   └── document_handlers.py  # Document management
├── ui/                        # Presentation layer
│   └── chat_interface.py     # Gradio UI definition
├── chat_config.py            # RAG pipeline configuration
└── settings.py               # Application settings
```

See [ARCHITECTURE.md](app/ARCHITECTURE.md) for detailed documentation.

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- [Ollama](https://ollama.ai/) installed and running
- An Ollama model pulled (e.g., `ollama pull llama2`)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/rags-chat.git
cd rags-chat
```

2. Create and activate virtual environment:
```bash
cd app
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r reqs.txt
```

4. Configure settings:
```bash
# Edit app/settings.py to set your Ollama host and model
export OLLAMA_HOST="http://localhost:11434"
export MODEL="llama2"
```

### Running the Application

```bash
cd app
python main.py
```

The application will start and open in your default browser at `http://localhost:7860`.

## 💡 Usage

### Basic Chat
1. Type your message in the input box
2. Press Enter or click Send
3. Watch the AI's thinking process in the right panel
4. See the final response in the main chat

### Document Upload
1. Open the "Document Manager" accordion
2. Click "Upload Documents" and select files
3. Ask questions about the uploaded documents
4. The AI will use document context in its responses

## 🛠️ Technical Details

### Key Technologies
- **Gradio** - Web UI framework
- **Ollama** - Local LLM runtime
- **Python 3.11+** - Core language

### Design Patterns
- **Separation of Concerns** - UI, business logic, and configuration are separated
- **Single Responsibility** - Each module has one clear purpose
- **Dependency Injection** - Components receive dependencies explicitly
- **Generator Pattern** - Efficient streaming response handling

### Code Quality
- Comprehensive docstrings
- Type hints for better IDE support
- Modular, testable architecture
- Professional error handling

## 📁 Project Structure

```
rags-chat/
├── app/
│   ├── main.py              # Entry point
│   ├── handlers/            # Business logic
│   │   ├── chat_handlers.py
│   │   └── document_handlers.py
│   ├── ui/                  # User interface
│   │   └── chat_interface.py
│   ├── chat_config.py       # RAG implementation
│   ├── settings.py          # Configuration
│   ├── reqs.txt            # Dependencies
│   └── ARCHITECTURE.md      # Architecture docs
├── README.md               # This file
└── REFACTORING_SUMMARY.md  # Refactoring details
```

## 🧪 Testing

To verify the installation:
```bash
python -m py_compile main.py handlers/*.py ui/*.py
```

## 🔧 Configuration

Edit `app/settings.py` to configure:
- `OLLAMA_HOST` - Ollama server URL
- `MODEL` - LLM model to use

## 📝 Development

### Adding New Features

1. **New handler**: Add to `handlers/` and update `__init__.py`
2. **UI changes**: Modify `ui/chat_interface.py`
3. **Configuration**: Update `settings.py` or `chat_config.py`

See [ARCHITECTURE.md](app/ARCHITECTURE.md) for detailed guidelines.

### Code Style
- Follow PEP 8
- Use meaningful variable names
- Add docstrings to all functions
- Keep functions focused and small

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [Gradio](https://gradio.app/)
- Powered by [Ollama](https://ollama.ai/)
- Inspired by modern RAG architectures

## 📧 Contact

**Your Name** - [@roustam](https://github.com/roustam)
**Reach me on Telegram** - [@roustam](https://t.me/Rou1999)
Project Link: [https://github.com/yourusername/rags-chat](https://github.com/yourusername/rags-chat)

---

⭐ Star this repo if you find it helpful!
