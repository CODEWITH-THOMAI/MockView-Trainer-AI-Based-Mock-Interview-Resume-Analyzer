import React from 'react';

interface DashboardProps {
  onNavigate: (page: string) => void;
}

export const Dashboard: React.FC<DashboardProps> = ({ onNavigate }) => {
  const features = [
    { id: 'mock-interview', title: 'AI Mock Interview', description: 'Practice with AI-powered interviews', icon: '🎤' },
    { id: 'fluency-tester', title: 'Fluency Tester', description: 'Improve your speaking fluency', icon: '🗣️' },
    { id: 'resume-builder', title: 'Resume Builder', description: 'Create professional resumes', icon: '📄' },
    { id: 'resume-analyzer', title: 'Resume Analyzer', description: 'Get AI-powered resume feedback', icon: '🔍' },
    { id: 'chatbox', title: 'AI Chatbox', description: 'Conversational interview practice', icon: '💬' },
    { id: 'progress', title: 'Progress Dashboard', description: 'Track your improvement', icon: '📊' },
    { id: 'tips', title: 'Interview Tips', description: 'Learn interview strategies', icon: '💡' },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-gray-900">MockView Trainer</h1>
            <button className="text-gray-600 hover:text-gray-900">Profile</button>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">Welcome Back!</h2>
          <p className="text-xl text-gray-600">Choose a feature to get started</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature) => (
            <div
              key={feature.id}
              onClick={() => onNavigate(feature.id)}
              className="bg-white rounded-lg shadow-md p-6 cursor-pointer hover:shadow-xl transition transform hover:-translate-y-1"
            >
              <div className="text-4xl mb-4">{feature.icon}</div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">{feature.title}</h3>
              <p className="text-gray-600">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
