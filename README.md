# RAG System - Retrieval-Augmented Generation Pipeline

A simple RAG system built with FastAPI and React for processing PDF documents and answering questions using AI.

## System Design

### Architecture Overview

```
User Query → Intent Detection → Query Transformation → Search & Retrieval → LLM Generation → Response
```

### Components

**Backend (FastAPI)**
- `main.py` - FastAPI application with endpoints
- `config.py` - Configuration and settings
- `models.py` - Data models using Pydantic
- `core/` - Core business logic
  - `pdf_processor.py` - PDF text extraction and chunking
  - `search.py` - Custom TF-IDF and semantic search
  - `llm_client.py` - Mistral AI integration
  - `rag_pipeline.py` - Main RAG orchestration
- `routes/` - API endpoint definitions

**Frontend (React + TypeScript)**
- `ChatPage.tsx` - Main application page
- `FileUploader.tsx` - PDF file upload
- `ChatInterface.tsx` - Chat conversation
- `Message.tsx` - Message display with citations
- `CorpusStatus.tsx` - Knowledge base status

## How It Operates

### 1. Document Ingestion
- User uploads PDF files
- System extracts text and chunks into overlapping segments (1000 chars, 200 char overlap)
- Chunks are stored with metadata

### 2. Query Processing
- System detects query intent (whether search is needed)
- Transforms query for better retrieval
- Performs hybrid search combining TF-IDF and semantic approaches

### 3. Search & Retrieval
- **TF-IDF Search**: Keyword-based using custom implementation
- **Semantic Search**: Word overlap and Jaccard similarity
- **Hybrid**: Combines both with weighted scoring
- Results are ranked and filtered by relevance threshold

### 4. Response Generation
- Relevant chunks are sent to Mistral AI
- LLM generates answer based on retrieved context
- Response includes source citations and confidence scores

## Key Features

- **Custom Search**: TF-IDF and semantic search implemented from scratch (no external libraries)
- **PDF Processing**: Text extraction and intelligent chunking
- **Hybrid Retrieval**: Combines keyword and semantic approaches
- **Citation Tracking**: Links answers to source document chunks
- **Intent Detection**: Determines when search is necessary

## How to Run

### Prerequisites
- Python 3.8+
- Node.js 16+

### Setup

1. **Create Environment File**
```bash
cp scripts/env.example .env
```

2. **Configure API Keys**
```bash
# Edit .env file and add your Mistral AI API key
MISTRAL_API_KEY=your_actual_api_key_here
```

**⚠️ Security Note:** Never commit API keys to version control. The `.env` file is already in `.gitignore`.

3. **Backend**
```bash
pip install -r requirements.txt
```

4. **Frontend**
```bash
cd frontend
npm install
cd ..
```

5. **Start Development Servers**
```bash
./scripts/dev.sh
```

**Access Points:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Usage

1. Upload PDF documents through the web interface
2. Ask questions about the uploaded content
3. System searches chunks and generates AI-powered answers
4. View source citations and relevance scores

## Technology Choices

- **FastAPI**: Modern web framework with automatic API docs
- **React + TypeScript**: Type-safe frontend development
- **Custom Search**: TF-IDF and semantic algorithms (no external RAG libraries)
- **Mistral AI**: LLM for answer generation
- **JSON Storage**: Simple file-based storage for MVP

## Project Status

- ✅ Project structure and boilerplate
- 🔄 Backend implementation (in progress)
- 🔄 Frontend implementation (in progress)
- 🔄 Integration and testing

---

**Built for StackAI Forward Deployed Engineer technical task**
