import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { Message as MessageType, ChunkInfo, DocumentInfo } from '../lib/types';

interface MessageProps {
  message: MessageType;
  documents?: DocumentInfo[];
}

const Message = ({ message, documents = [] }: MessageProps) => {
  const isUser = message.role === 'user';
  const [selectedReference, setSelectedReference] = useState<number | null>(null);
  
  // Create a map of document IDs to titles
  const documentMap = new Map(documents.map(doc => [doc.id, doc.filename]));
  
  // Custom components for ReactMarkdown
  const markdownComponents = {
    p: ({ children }: any) => <p className="mb-3 last:mb-0">{children}</p>,
    h1: ({ children }: any) => <h1 className="text-2xl font-bold mb-4 mt-6 first:mt-0">{children}</h1>,
    h2: ({ children }: any) => <h2 className="text-xl font-bold mb-3 mt-5 first:mt-0">{children}</h2>,
    h3: ({ children }: any) => <h3 className="text-lg font-bold mb-2 mt-4 first:mt-0">{children}</h3>,
    ul: ({ children }: any) => <ul className="list-disc list-inside mb-3 space-y-1">{children}</ul>,
    ol: ({ children }: any) => <ol className="list-decimal list-inside mb-3 space-y-1">{children}</ol>,
    li: ({ children }: any) => <li className="text-gray-700">{children}</li>,
    code: ({ children }: any) => <code className="bg-gray-100 px-1 py-0.5 rounded text-sm font-mono">{children}</code>,
    pre: ({ children }: any) => <pre className="bg-gray-100 p-3 rounded-lg overflow-x-auto mb-3">{children}</pre>,
    blockquote: ({ children }: any) => <blockquote className="border-l-4 border-blue-500 pl-4 italic text-gray-600 mb-3">{children}</blockquote>,
    strong: ({ children }: any) => <strong className="font-bold">{children}</strong>,
    em: ({ children }: any) => <em className="italic">{children}</em>,
    a: ({ children, href }: any) => <a href={href} className="text-blue-600 hover:text-blue-800 underline" target="_blank" rel="noopener noreferrer">{children}</a>,
    table: ({ children }: any) => <table className="min-w-full border border-gray-300 mb-3">{children}</table>,
    thead: ({ children }: any) => <thead className="bg-gray-50">{children}</thead>,
    tbody: ({ children }: any) => <tbody>{children}</tbody>,
    tr: ({ children }: any) => <tr className="border-b border-gray-300 hover:bg-gray-50">{children}</tr>,
    th: ({ children }: any) => <th className="px-3 py-2 text-left font-medium text-gray-700 border-r border-gray-300">{children}</th>,
    td: ({ children }: any) => <td className="px-3 py-2 border-r border-gray-300">{children}</td>,
  };

  // Function to render text with clickable references
  const renderTextWithReferences = (text: string, referenceMapping?: Record<number, ChunkInfo>) => {
    if (!referenceMapping) {
      return <ReactMarkdown components={markdownComponents}>{text}</ReactMarkdown>;
    }
    
    // Split text by reference numbers (¹, ², ³, etc.)
    const parts = text.split(/([¹²³⁴⁵⁶⁷⁸⁹])/);
    
    return parts.map((part, index) => {
      const refNumber = '¹²³⁴⁵⁶⁷⁸⁹'.indexOf(part) + 1;
      if (refNumber > 0 && referenceMapping[refNumber]) {
        return (
          <span key={index}>
            <sup 
              className="text-blue-600 hover:text-blue-800 cursor-pointer font-medium"
              onClick={() => setSelectedReference(selectedReference === refNumber ? null : refNumber)}
              title={`Click to view source ${refNumber}`}
            >
              {part}
            </sup>
          </span>
        );
      }
      return <ReactMarkdown key={index} components={markdownComponents}>{part}</ReactMarkdown>;
    });
  };

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-3xl px-4 py-2 rounded-lg ${
          isUser 
            ? 'bg-blue-500 text-white' 
            : 'bg-white border border-gray-200 text-gray-800'
        }`}
      >
        <div className="prose prose-sm max-w-none">
          {isUser ? (
            <div className="whitespace-pre-wrap">
              {message.content}
            </div>
          ) : (
            <div className="markdown-content">
              {renderTextWithReferences(message.content, message.reference_mapping)}
            </div>
          )}
        </div>
        
        {/* Selected Reference Display */}
        {!isUser && selectedReference && message.reference_mapping && message.reference_mapping[selectedReference] && (
          <div className="mt-3 pt-3 border-t border-gray-200">
            <div className="text-xs bg-blue-50 p-3 rounded border-l-4 border-blue-400">
              <div className="flex justify-between items-start mb-2">
                <span className="font-medium text-blue-800">
                  Source {selectedReference}: {documentMap.get(message.reference_mapping[selectedReference].document_id) || `Document ${message.reference_mapping[selectedReference].document_id.slice(0, 8)}...`}
                </span>
                <button 
                  onClick={() => setSelectedReference(null)}
                  className="text-blue-600 hover:text-blue-800 text-xs"
                >
                  ✕
                </button>
              </div>
              <div className="text-blue-700 text-sm">
                {message.reference_mapping[selectedReference].content}
              </div>
            </div>
          </div>
        )}
        
        {/* Citations for assistant messages with chunks */}
        {!isUser && message.chunks && message.chunks.length > 0 && (
          <div className="mt-3 pt-3 border-t border-gray-200">
            <p className="text-xs text-gray-500 mb-2 font-medium">📚 Sources ({message.chunks.length}):</p>
            <div className="space-y-2">
              {message.chunks.map((chunk, index) => (
                <div key={chunk.id} className="text-xs bg-gray-50 p-2 rounded border-l-2 border-blue-300">
                  <div className="flex justify-between items-start mb-1">
                    <span className="font-medium text-gray-700">
                      {documentMap.get(chunk.document_id) || `Document ${chunk.document_id.slice(0, 8)}...`}
                    </span>
                  </div>
                  <div className="text-gray-600 line-clamp-3">
                    {chunk.content.length > 200 
                      ? `${chunk.content.substring(0, 200)}...`
                      : chunk.content
                    }
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Message;
