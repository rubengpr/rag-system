import React from 'react';
import { Message as MessageType, ChunkInfo } from '../lib/types';

interface MessageProps {
  message: MessageType;
}

const Message = ({ message }: MessageProps) => {
  // TODO: Determine if message is from user or assistant
  // TODO: Add isUser variable based on message.role

  return (
    <div className={`flex justify-start`}>
      <div
        className={`max-w-3xl px-4 py-2 rounded-lg bg-white border border-gray-200 text-gray-800`}
      >
        <div className="whitespace-pre-wrap">
          {/* TODO: Display message content */}
          {message.content}
        </div>
        
        {/* Citations for assistant messages */}
        {false && (message.chunks as ChunkInfo[])?.length > 0 && (
          <div className="mt-3 pt-3 border-t border-gray-200">
            <p className="text-xs text-gray-500 mb-2">Sources:</p>
            <div className="space-y-2">
              {(message.chunks as ChunkInfo[])?.map((chunk, index) => (
                <div key={chunk.id} className="text-xs bg-gray-50 p-2 rounded">
                  {/* TODO: Display chunk information */}
                  {/* TODO: Show document ID */}
                  {/* TODO: Show chunk content */}
                  {/* TODO: Show similarity score if available */}
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
