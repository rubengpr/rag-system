import React, { useEffect } from 'react';
import FileUploader from '../components/FileUploader';
import ChatInterface from '../components/ChatInterface';
import CorpusStatus from '../components/CorpusStatus';
import { api } from '../lib/api';
import { Message, DocumentInfo, UploadResponse, QueryResponse } from '../lib/types';

const ChatPage = () => {
  // TODO: Add state variables for:
  // - messages: Message[]
  // - documents: DocumentInfo[]
  // - isUploading: boolean
  // - isLoading: boolean

  useEffect(() => {
    // TODO: Check backend health on component mount
    // TODO: Call api.healthCheck()
  }, []);

  const handleFileUpload = async (files: File[]) => {
    // TODO: Implement file upload logic
    // TODO: Set uploading state
    // TODO: Call api.uploadFiles()
    // TODO: Update documents and total chunks
    // TODO: Add success/error messages
    // TODO: Handle errors gracefully
  };

  const handleSendMessage = async (content: string) => {
    // TODO: Implement message sending logic
    // TODO: Check if documents exist
    // TODO: Add user message to chat
    // TODO: Call api.queryKnowledgeBase()
    // TODO: Add assistant response
    // TODO: Handle errors gracefully
  };

  const handleClearCorpus = () => {
    // TODO: Implement corpus clearing logic
    // TODO: Reset all state variables
    // TODO: Clear messages
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
            <FileUploader onUpload={handleFileUpload} isUploading={false} />
            <CorpusStatus 
              documents={[]} 
              onClearCorpus={handleClearCorpus} 
            />
          </div>

          {/* Main Chat Area */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 h-[600px]">
              <ChatInterface 
                messages={[]}
                onSendMessage={handleSendMessage}
                isLoading={false}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;
