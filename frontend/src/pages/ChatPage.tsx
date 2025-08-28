import React, { useEffect, useState } from 'react';
import FileUploader from '../components/FileUploader';
import ChatInterface from '../components/ChatInterface';
import CorpusStatus from '../components/CorpusStatus';
import { api } from '../lib/api';
import { Message, DocumentInfo, UploadResponse, QueryResponse } from '../lib/types';

const ChatPage = () => {
  // State variables for managing the application
  const [messages, setMessages] = useState<Message[]>([]);
  const [documents, setDocuments] = useState<DocumentInfo[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    // Initialize backend and check health on component mount
    const initializeBackend = async () => {
      try {
        // Check backend health
        await api.healthCheck();
        
      } catch (error) {
        // Add a message to inform the user
        setMessages(prev => [...prev, {
          id: Date.now().toString(),
          content: 'Warning: Backend connection failed. Please check if the server is running.',
          role: 'assistant',
          timestamp: new Date()
        }]);
      }
    };
    
    initializeBackend();
  }, []);

  const handleFileUpload = async (files: File[]) => {
    setIsUploading(true);
    
    try {
      // Call the API to upload files, clearing previous documents
      const response = await api.uploadFiles(files, true);
      
      // Update documents state
      setDocuments(response.documents);
      
      // Success - no message added to chat
      
    } catch (error) {
      // Add error message to chat
      setMessages(prev => [...prev, {
        id: Date.now().toString(),
        content: `Upload failed: ${error instanceof Error ? error.message : 'Unknown error'}`,
        role: 'assistant',
        timestamp: new Date()
      }]);
    } finally {
      setIsUploading(false);
    }
  };

  const handleSendMessage = async (content: string) => {
    // Check if documents exist
    if (documents.length === 0) {
      setMessages(prev => [...prev, {
        id: Date.now().toString(),
        content: 'Please upload some documents first before asking questions.',
        role: 'assistant',
        timestamp: new Date()
      }]);
      return;
    }
    
    // Add user message to chat
    const userMessage: Message = {
      id: Date.now().toString(),
      content,
      role: 'user',
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMessage]);
    
    setIsLoading(true);
    
    try {
      // Call api.queryKnowledgeBase()
      const response: QueryResponse = await api.queryKnowledgeBase(content);
      
      // Add assistant response
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: response.answer,
        role: 'assistant',
        timestamp: new Date(),
        chunks: response.chunks
      };
      
      setMessages(prev => [...prev, assistantMessage]);
      
    } catch (error) {
      // Handle errors gracefully
      setMessages(prev => [...prev, {
        id: (Date.now() + 1).toString(),
        content: `Error: ${error instanceof Error ? error.message : 'Failed to get response'}`,
        role: 'assistant',
        timestamp: new Date()
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClearCorpus = async () => {
    try {
      // Upload empty file list to clear previous documents
      await api.uploadFiles([], true);
      
      // Reset all state variables
      setDocuments([]);
      setMessages([]);
      
    } catch (error) {
      console.error('Error clearing corpus:', error);
      // Add error message to chat
      setMessages(prev => [...prev, {
        id: Date.now().toString(),
        content: `Failed to clear corpus: ${error instanceof Error ? error.message : 'Unknown error'}`,
        role: 'assistant',
        timestamp: new Date()
      }]);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto p-4">
        <header className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">RAG System</h1>
          <p className="text-gray-600">Upload PDFs and ask questions about your documents</p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Sidebar - File Upload & Corpus Status */}
          <div className="space-y-6">
            <FileUploader 
              onUpload={handleFileUpload} 
              isUploading={isUploading} 
              hasDocuments={documents.length > 0}
            />
            <CorpusStatus 
              documents={documents} 
              onClearCorpus={handleClearCorpus} 
            />
          </div>

          {/* Main Chat Area */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 h-[600px]">
              <ChatInterface 
                messages={messages}
                onSendMessage={handleSendMessage}
                isLoading={isLoading}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;
