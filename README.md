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

### 2. Query Processing ✅
- System detects query intent (question, greeting, thanks, command, document_command, system_command, unclear, out_of_scope)
- **Smart intent handling**: Non-question intents get short, concise responses without RAG processing
- **Command handling**: Document management and system commands with appropriate UI guidance
- **Error handling**: Detects unclear queries and out-of-scope requests with helpful guidance
- Transforms query for better retrieval (remove filler words, expand acronyms)
- Performs hybrid search combining TF-IDF and semantic approaches only for questions
- Includes PII detection and query refusal for sensitive content

### 3. Search & Retrieval ✅
- **TF-IDF Search**: Keyword-based using custom implementation with NumPy
- **Semantic Search**: Word overlap and Jaccard similarity
- **Hybrid**: Combines both with weighted scoring and result ranking
- Results are ranked, filtered by relevance threshold, and boosted by content length
- Custom search engine built from scratch without external vector databases

### 4. Response Generation ✅
- Relevant chunks are sent to Mistral AI with context-aware prompts
- LLM generates answer based on retrieved context
- Response includes source citations, confidence scores, and validation
- Basic hallucination detection and response validation

## Key Features

- **PDF Processing**: Text extraction and intelligent chunking ✅
- **File Upload Interface**: Drag & drop PDF upload with validation ✅
- **Chat Interface**: Modern React-based chat UI ✅
- **Corpus Management**: View uploaded documents and clear knowledge base ✅
- **Backend Health Monitoring**: Health check endpoint and frontend status ✅
- **Security**: File type validation, size limits, CORS configuration ✅
- **Input Validation**: Comprehensive protection against XSS, SQL injection, and malicious content ✅
- **Rate Limiting**: API endpoint protection with configurable limits per IP address ✅

## Current Implementation Status

### ✅ Completed
- **Backend Infrastructure**: FastAPI app with CORS, health checks
- **PDF Processing**: Text extraction, cleaning, chunking with overlap
- **File Upload API**: `/ingest` endpoint with file validation
- **Query API**: `/query` endpoint with full RAG pipeline implementation
- **Data Models**: Pydantic models for all data structures with input validation
- **Frontend UI**: Complete React application with TypeScript
- **File Upload Component**: Drag & drop interface with progress
- **Chat Interface**: Message display and input components
- **Corpus Status**: Document management and clearing
- **API Client**: Frontend-backend communication layer
- **Search Engine**: Custom TF-IDF and semantic search built from scratch
- **LLM Integration**: Mistral AI client with rate limiting and retry logic
- **RAG Pipeline**: Complete query-to-answer workflow with context preparation
- **Security**: Input validation, PII detection, XSS protection, SQL injection prevention
- **Rate Limiting**: Comprehensive API protection with configurable limits

### 🔄 In Progress
- Performance optimizations and caching
- Advanced error handling and user feedback

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

**🔒 Rate Limiting:** All API endpoints are protected with configurable rate limits to prevent abuse and ensure system stability.

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
3. **Chat Interface**: Ask questions about your documents using the complete RAG pipeline
4. **Clear Corpus**: Remove all uploaded documents and start fresh

## Technology Stack

### Backend
- **FastAPI**: Modern web framework with automatic API docs
- **PyPDF2**: PDF text extraction and processing
- **Pydantic**: Data validation and serialization with security validation
- **NumPy**: Vector operations for TF-IDF calculations
- **Requests**: HTTP client for Mistral AI API integration
- **SlowAPI**: Rate limiting and API protection
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
- `POST /ingest` - Upload and process PDF files (Rate limited: 10/minute)
- `GET /health` - Backend health check (Rate limited: 60/minute)

### Query
- `POST /query` - Query knowledge base with full RAG pipeline (Rate limited: 30/minute)
- `GET /query/health` - Query service health check (Rate limited: 60/minute)

### Rate Limiting
All endpoints are protected with IP-based rate limiting:
- **Query endpoints**: 30 requests per minute per IP
- **File upload**: 10 uploads per minute per IP
- **Health checks**: 60 requests per minute per IP
- **Configurable limits** via environment variables

## Project Status

- ✅ **Project structure and boilerplate**
- ✅ **Backend infrastructure and PDF processing**
- ✅ **Frontend UI components and file upload**
- ✅ **API endpoints and data models**
- ✅ **Search algorithms and RAG pipeline**
- ✅ **LLM integration and response generation**
- ✅ **Security features and input validation**
- ✅ **Complete RAG system with full functionality**
- 📋 **Advanced features and optimizations**

---

**Built for StackAI Forward Deployed Engineer technical task**
