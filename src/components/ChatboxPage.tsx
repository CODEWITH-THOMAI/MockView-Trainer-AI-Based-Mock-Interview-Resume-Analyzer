import React from 'react';

interface ChatboxPageProps {
  onBack: () => void;
}

export const ChatboxPage: React.FC<ChatboxPageProps> = ({ onBack }) => {
  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <button onClick={onBack} className="text-blue-600 hover:text-blue-700">
            ← Back to Dashboard
          </button>
        </div>
      </nav>

      <div className="max-w-4xl mx-auto px-4 py-12">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">AI Chatbox</h1>
        <div className="bg-white rounded-lg shadow-md p-8">
          <p className="text-gray-600">AI chatbox interface will be implemented...</p>
        </div>
      </div>
    </div>
  );
};
