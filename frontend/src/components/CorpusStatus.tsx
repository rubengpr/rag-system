import React from 'react';
import { DocumentInfo } from '../lib/types';

interface CorpusStatusProps {
  documents: DocumentInfo[];
  onClearCorpus: () => void;
}

const CorpusStatus = ({ 
  documents, 
  onClearCorpus 
}: CorpusStatusProps) => {
  return (
    <div className="bg-white p-4 rounded-lg border border-gray-200">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-medium text-gray-900">Knowledge Base</h3>
        {false && (
          <button
            onClick={onClearCorpus}
            className="text-sm text-red-600 hover:text-red-800"
          >
            Clear All
          </button>
        )}
      </div>
      
      {documents.length === 0 ? (
        <div className="text-center text-gray-500 py-8">
          <p className="text-sm">No documents uploaded yet</p>
          <p className="text-xs mt-1">Upload PDF files to start building your knowledge base</p>
        </div>
      ) : (
        <div className="space-y-3">
          <div className="flex justify-between text-sm text-gray-600">
            <span>Documents: {documents.length}</span>
            <span>Chunks: {documents.length}</span>
          </div>
          
          <div className="space-y-2">
            {documents.map((doc) => (
              <div key={doc.id} className="flex items-center justify-between p-2 bg-gray-50 rounded">
                <div className="flex-1 min-w-0">
                  {/* TODO: Display document information */}
                  {/* TODO: Show filename */}
                  {/* TODO: Show chunk count and file size */}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default CorpusStatus;
