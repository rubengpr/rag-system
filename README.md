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
  - `pdf_processor.py` - PDF text extraction and chunking ✅
  - `search.py` - Custom TF-IDF and semantic search 🔄
  - `llm_client.py` - Mistral AI integration 🔄
  - `rag_pipeline.py` - Main RAG orchestration 🔄
- `routes/` - API endpoint definitions

**Frontend (React + TypeScript)**
- `ChatPage.tsx` - Main application page ✅
- `FileUploader.tsx` - PDF file upload ✅
- `ChatInterface.tsx` - Chat conversation ✅
- `Message.tsx` - Message display with citations ✅
- `CorpusStatus.tsx` - Knowledge base status ✅

## How It Operates

### 1. Document Ingestion ✅
- User uploads PDF files through web interface
- System extracts text and chunks into overlapping segments (1000 chars, 200 char overlap)
- Chunks are stored with metadata in memory
- File validation (PDF only, 10MB limit)
- Support for clearing previous documents

### 2. Query Processing 🔄
- System detects query intent (whether search is needed)
- Transforms query for better retrieval
- Performs hybrid search combining TF-IDF and semantic approaches

### 3. Search & Retrieval 🔄
- **TF-IDF Search**: Keyword-based using custom implementation
- **Semantic Search**: Word overlap and Jaccard similarity
- **Hybrid**: Combines both with weighted scoring
- Results are ranked and filtered by relevance threshold

### 4. Response Generation 🔄
- Relevant chunks are sent to Mistral AI
- LLM generates answer based on retrieved context
- Response includes source citations and confidence scores

## Key Features

- **PDF Processing**: Text extraction and intelligent chunking ✅
- **File Upload Interface**: Drag & drop PDF upload with validation ✅
- **Chat Interface**: Modern React-based chat UI ✅
- **Corpus Management**: View uploaded documents and clear knowledge base ✅
- **Backend Health Monitoring**: Health check endpoint and frontend status ✅
- **Security**: File type validation, size limits, CORS configuration ✅

## Current Implementation Status

### ✅ Completed
- **Backend Infrastructure**: FastAPI app with CORS, health checks
- **PDF Processing**: Text extraction, cleaning, chunking with overlap
- **File Upload API**: `/ingest` endpoint with file validation
- **Data Models**: Pydantic models for all data structures
- **Frontend UI**: Complete React application with TypeScript
- **File Upload Component**: Drag & drop interface with progress
- **Chat Interface**: Message display and input components
- **Corpus Status**: Document management and clearing
- **API Client**: Frontend-backend communication layer

### 🔄 In Progress
- **Search Implementation**: TF-IDF and semantic search algorithms
- **LLM Integration**: Mistral AI client for answer generation
- **RAG Pipeline**: Complete query-to-answer workflow
- **Query Processing**: Intent detection and query transformation

### 📋 Planned
- **Advanced Search**: Vector embeddings and similarity search
- **User Authentication**: Multi-user support and access control
- **Document Management**: Edit, delete, and organize uploaded documents

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

3. **Backend Dependencies**
```bash
pip install -r requirements.txt
```

4. **Frontend Dependencies**
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

1. **Upload Documents**: Drag and drop PDF files through the web interface
2. **View Corpus Status**: See uploaded documents and manage knowledge base
3. **Chat Interface**: Ask questions about your documents (RAG pipeline in development)
4. **Clear Corpus**: Remove all uploaded documents and start fresh

## Technology Stack

### Backend
- **FastAPI**: Modern web framework with automatic API docs
- **PyPDF2**: PDF text extraction and processing
- **Pydantic**: Data validation and serialization
- **Uvicorn**: ASGI server for production deployment

### Frontend
- **React 18**: Modern React with hooks and functional components
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first CSS framework
- **Vite**: Fast build tool and development server

### Development Tools
- **ESLint**: Code quality and consistency
- **PostCSS**: CSS processing and optimization
- **Hot Reload**: Fast development iteration

## API Endpoints

### Document Management
- `POST /ingest` - Upload and process PDF files
- `GET /health` - Backend health check

### Query (In Development)
- `POST /query` - Query knowledge base (placeholder implementation)

## Project Status

- ✅ **Project structure and boilerplate**
- ✅ **Backend infrastructure and PDF processing**
- ✅ **Frontend UI components and file upload**
- ✅ **API endpoints and data models**
- 🔄 **Search algorithms and RAG pipeline**
- 🔄 **LLM integration and response generation**
- 📋 **Advanced features and optimizations**

---

**Built for StackAI Forward Deployed Engineer technical task**
