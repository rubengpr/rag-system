// API client for communicating with the backend

import { UploadResponse, QueryResponse, HealthResponse, SystemStatusResponse } from './types';

// Use environment variable for production, fallback to local development
const API_BASE = (import.meta as any).env?.VITE_API_URL || '/api';

export const api = {
  async uploadFiles(files: File[], clearPrevious: boolean = false): Promise<UploadResponse> {
    try {
      const formData = new FormData();
      files.forEach(file => {
        formData.append('files', file);
      });
      
      // Add the clear_previous parameter
      formData.append('clear_previous', clearPrevious.toString());

      const response = await fetch(`${API_BASE}/ingest/`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        let errorMessage = `Upload failed: ${response.status}`;
        try {
          const errorData = await response.json();
          errorMessage = errorData.detail || errorMessage;
        } catch (jsonError) {
          // If JSON parsing fails, use the status text or default message
          errorMessage = response.statusText || errorMessage;
        }
        throw new Error(errorMessage);
      }

      return await response.json();
    } catch (error) {
      console.error('Upload error:', error);
      throw error;
    }
  },
  
  async queryKnowledgeBase(query: string): Promise<QueryResponse> {
    try {
      const response = await fetch(`${API_BASE}/query/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) {
        let errorMessage = `Query failed: ${response.status}`;
        try {
          const errorData = await response.json();
          errorMessage = errorData.detail || errorMessage;
        } catch (jsonError) {
          // If JSON parsing fails, use the status text or default message
          errorMessage = response.statusText || errorMessage;
        }
        throw new Error(errorMessage);
      }

      return await response.json();
    } catch (error) {
      console.error('Query error:', error);
      throw error;
    }
  },
  
  async healthCheck(): Promise<HealthResponse> {
    try {
      const response = await fetch(`${API_BASE}/health`);
      
      if (!response.ok) {
        throw new Error(`Health check failed: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Health check error:', error);
      throw error;
    }
  },

  async getSystemStatus(): Promise<SystemStatusResponse> {
    try {
      const response = await fetch(`${API_BASE}/status`);
      
      if (!response.ok) {
        throw new Error(`System status check failed: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('System status error:', error);
      throw error;
    }
  },
};
