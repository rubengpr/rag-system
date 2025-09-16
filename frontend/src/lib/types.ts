// Frontend types that mirror backend models

export interface ChunkInfo {
  id: string;
  content: string;
  document_id: string;
}

export interface QueryRequest {
  query: string;
}

export interface QueryResponse {
  answer: string;
  chunks: ChunkInfo[];
  processing_time?: number;
  confidence_score?: number;
  intent?: string;
  reference_mapping?: Record<number, ChunkInfo>;
}

export interface DocumentInfo {
  id: string;
  filename: string;
}

export interface UploadResponse {
  documents: DocumentInfo[];
}

export interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
  chunks?: ChunkInfo[];
  reference_mapping?: Record<number, ChunkInfo>;
}

// Health check response type
export interface HealthResponse {
  status: string;
  timestamp: number;
}

// System status response type
export interface SystemStatusResponse {
  status: string;
  timestamp: number;
  storage?: {
    total_documents: number;
    total_chunks: number;
    storage_size_bytes: number;
  };
  error?: string;
}
