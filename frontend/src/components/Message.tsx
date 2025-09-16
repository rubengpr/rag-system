import ReactMarkdown from 'react-markdown';
import { Message as MessageType, DocumentInfo, ChunkInfo } from '../lib/types';

interface MessageProps {
  message: MessageType;
  documents?: DocumentInfo[];
}

// Define proper types for ReactMarkdown components
interface MarkdownComponentProps {
  children?: React.ReactNode;
  href?: string;
}

const Message = ({ message, documents = [] }: MessageProps) => {
  const isUser = message.role === 'user';
  
  // Create a map of document IDs to titles
  const documentMap = new Map(documents.map(doc => [doc.id, doc.filename]));
  
  // Custom components for ReactMarkdown with proper typing
  const markdownComponents = {
    p: ({ children }: MarkdownComponentProps) => <p className="mb-3 last:mb-0">{children}</p>,
    h1: ({ children }: MarkdownComponentProps) => <h1 className="text-2xl font-bold mb-4 mt-6 first:mt-0">{children}</h1>,
    h2: ({ children }: MarkdownComponentProps) => <h2 className="text-xl font-bold mb-3 mt-5 first:mt-0">{children}</h2>,
    h3: ({ children }: MarkdownComponentProps) => <h3 className="text-lg font-bold mb-2 mt-4 first:mt-0">{children}</h3>,
    ul: ({ children }: MarkdownComponentProps) => <ul className="list-disc list-inside mb-3 space-y-1">{children}</ul>,
    ol: ({ children }: MarkdownComponentProps) => <ol className="list-decimal list-inside mb-3 space-y-1">{children}</ol>,
    li: ({ children }: MarkdownComponentProps) => <li className="text-gray-700">{children}</li>,
    code: ({ children }: MarkdownComponentProps) => <code className="bg-gray-100 px-1 py-0.5 rounded text-sm font-mono">{children}</code>,
    pre: ({ children }: MarkdownComponentProps) => <pre className="bg-gray-100 p-3 rounded-lg overflow-x-auto mb-3">{children}</pre>,
    blockquote: ({ children }: MarkdownComponentProps) => <blockquote className="border-l-4 border-blue-500 pl-4 italic text-gray-600 mb-3">{children}</blockquote>,
    strong: ({ children }: MarkdownComponentProps) => <strong className="font-bold">{children}</strong>,
    em: ({ children }: MarkdownComponentProps) => <em className="italic">{children}</em>,
    a: ({ children, href }: MarkdownComponentProps) => <a href={href} className="text-blue-600 hover:text-blue-800 underline" target="_blank" rel="noopener noreferrer">{children}</a>,
    table: ({ children }: MarkdownComponentProps) => <table className="min-w-full border border-gray-300 mb-3">{children}</table>,
    thead: ({ children }: MarkdownComponentProps) => <thead className="bg-gray-50">{children}</thead>,
    tbody: ({ children }: MarkdownComponentProps) => <tbody>{children}</tbody>,
    tr: ({ children }: MarkdownComponentProps) => <tr className="border-b border-gray-300 hover:bg-gray-50">{children}</tr>,
    th: ({ children }: MarkdownComponentProps) => <th className="px-3 py-2 text-left font-medium text-gray-700 border-r border-gray-300">{children}</th>,
    td: ({ children }: MarkdownComponentProps) => <td className="px-3 py-2 border-r border-gray-300">{children}</td>,
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
              <ReactMarkdown components={markdownComponents}>{message.content}</ReactMarkdown>
            </div>
          )}
        </div>
        
        {/* Citations for assistant messages with chunks */}
        {!isUser && message.chunks && message.chunks.length > 0 && (
          <div className="mt-3 pt-3 border-t border-gray-200">
            <p className="text-xs text-gray-500 mb-2 font-medium">📚 Sources ({message.chunks.length}):</p>
            <div className="space-y-2">
              {message.chunks.map((chunk: ChunkInfo) => (
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
