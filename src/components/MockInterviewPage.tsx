import React, { useState } from 'react';

interface MockInterviewPageProps {
  onBack: () => void;
}

export const MockInterviewPage: React.FC<MockInterviewPageProps> = ({ onBack }) => {
  const [started, setStarted] = useState(false);

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
        <h1 className="text-4xl font-bold text-gray-900 mb-8">AI Mock Interview</h1>
        
        {!started ? (
          <div className="bg-white rounded-lg shadow-md p-8">
            <h2 className="text-2xl font-semibold mb-4">Get Started</h2>
            <p className="text-gray-600 mb-6">
              Practice with AI-powered mock interviews tailored to your target role.
            </p>
            <button
              onClick={() => setStarted(true)}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              Start Interview
            </button>
          </div>
        ) : (
          <div className="bg-white rounded-lg shadow-md p-8">
            <p className="text-gray-600">Interview interface will be implemented...</p>
          </div>
        )}
      </div>
    </div>
  );
};
