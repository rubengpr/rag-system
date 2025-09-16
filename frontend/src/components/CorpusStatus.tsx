import { DocumentInfo } from '../lib/types';

interface CorpusStatusProps {
  documents: DocumentInfo[];
  onClearCorpus: () => void;
  isLoading?: boolean;
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
          <div className="space-y-2">
            {documents.map((doc) => (
              <div key={doc.id} className="flex items-center p-3 bg-gray-50 rounded-lg border border-gray-100">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center space-x-2">
                    <svg className="w-4 h-4 text-red-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 1 0 100 2H7a1 1 1 0 100-2H7z" clipRule="evenodd" />
                    </svg>
                    <span className="text-sm font-medium text-gray-900 truncate" title={doc.filename}>
                      {doc.filename}
                    </span>
                  </div>
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
