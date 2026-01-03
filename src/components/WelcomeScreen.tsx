import React from 'react';

interface WelcomeScreenProps {
  onGetStarted: () => void;
  onLogin: () => void;
}

export const WelcomeScreen: React.FC<WelcomeScreenProps> = ({ onGetStarted, onLogin }) => {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-blue-600 to-purple-700 text-white p-8">
      <div className="text-center max-w-4xl">
        <h1 className="text-6xl font-bold mb-6">MockView Trainer</h1>
        <p className="text-2xl mb-8">AI-Based Mock Interview & Resume Analyzer</p>
        <p className="text-lg mb-12 text-gray-200">
          Master your interview skills with AI-powered mock interviews, fluency analysis, 
          and professional resume building tools.
        </p>
        <div className="flex gap-4 justify-center">
          <button
            onClick={onGetStarted}
            className="px-8 py-4 bg-white text-blue-600 rounded-lg font-semibold text-lg hover:bg-gray-100 transition"
          >
            Get Started
          </button>
          <button
            onClick={onLogin}
            className="px-8 py-4 bg-transparent border-2 border-white text-white rounded-lg font-semibold text-lg hover:bg-white hover:text-blue-600 transition"
          >
            Login
          </button>
        </div>
      </div>
    </div>
  );
};
