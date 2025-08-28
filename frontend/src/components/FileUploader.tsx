import React from 'react';

interface FileUploaderProps {
  onUpload: (files: File[]) => void;
  isUploading: boolean;
  hasDocuments: boolean;
}

const FileUploader = ({ onUpload, isUploading, hasDocuments }: FileUploaderProps) => {
  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []);
    if (files.length > 0) {
      onUpload(files);
    }
    // Reset the input so the same file can be selected again
    e.target.value = '';
  };

  return (
    <div className="w-full">
      <div className={`border-2 border-dashed rounded-lg p-6 text-center ${
        hasDocuments 
          ? 'border-neutral-300 bg-neutral-50' 
          : isUploading 
            ? 'border-blue-300 bg-blue-50' 
            : 'border-gray-300 bg-white'
      }`}>
        <input
          type="file"
          multiple
          accept=".pdf"
          onChange={handleFileInput}
          className="hidden"
          id="file-upload"
          disabled={isUploading || hasDocuments}
        />
        <label 
          htmlFor="file-upload" 
          className={`${hasDocuments ? 'cursor-not-allowed' : 'cursor-pointer'}`}
        >
          <div className={hasDocuments ? 'text-neutral-700' : 'text-gray-600'}>
            {hasDocuments ? (
              <>
                <p className="text-lg font-medium">
                  📚 Documents Uploaded
                </p>
                <p className="text-sm mt-2 text-neutral-700">
                  Refresh to upload new documents
                </p>
              </>
            ) : isUploading ? (
              <>
                <p className="text-lg font-medium">
                  ⏳ Uploading...
                </p>
                <p className="text-sm mt-2">
                  Please wait while we process your PDF
                </p>
              </>
            ) : (
              <>
                <p className="text-lg font-medium">
                  📁 Click to browse PDF files
                </p>
                <p className="text-sm mt-2">
                  Supports multiple PDF files
                </p>
              </>
            )}
          </div>
        </label>
      </div>
    </div>
  );
};

export default FileUploader;
