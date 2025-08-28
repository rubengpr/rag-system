import React from 'react';
import { Message as MessageType, ChunkInfo } from '../lib/types';

interface MessageProps {
  message: MessageType;
}

const Message = ({ message }: MessageProps) => {
  const isUser = message.role === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-3xl px-4 py-2 rounded-lg ${
          isUser 
            ? 'bg-blue-500 text-white' 
            : 'bg-white border border-gray-200 text-gray-800'
        }`}
      >
        <div className="whitespace-pre-wrap">
          {message.content}
        </div>
        
        {/* Citations for assistant messages with chunks */}
        {!isUser && message.chunks && message.chunks.length > 0 && (
          <div className="mt-3 pt-3 border-t border-gray-200">
            <p className="text-xs text-gray-500 mb-2 font-medium">📚 Sources ({message.chunks.length}):</p>
            <div className="space-y-2">
              {message.chunks.map((chunk, index) => (
                <div key={chunk.id} className="text-xs bg-gray-50 p-2 rounded border-l-2 border-blue-300">
                  <div className="flex justify-between items-start mb-1">
                    <span className="font-medium text-gray-700">
                      Document {chunk.document_id.slice(0, 8)}...
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
