import React from 'react';

interface FileUploaderProps {
  onUpload: (files: File[]) => void;
  isUploading: boolean;
}

const FileUploader = ({ onUpload, isUploading }: FileUploaderProps) => {
  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    // TODO: Implement file input handling
    // TODO: Extract files from input
    // TODO: Call onUpload with selected files
  };

  return (
    <div className="w-full">
      <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
        <input
          type="file"
          multiple
          accept=".pdf"
          onChange={handleFileInput}
          className="hidden"
          id="file-upload"
          disabled={isUploading}
        />
        <label htmlFor="file-upload" className="cursor-pointer">
          <div className="text-gray-600">
            <p className="text-lg font-medium">
              {isUploading ? 'Uploading...' : 'Click to browse PDF files'}
            </p>
            <p className="text-sm mt-2">
              Supports multiple PDF files
            </p>
          </div>
        </label>
      </div>
    </div>
  );
};

export default FileUploader;
