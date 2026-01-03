import { useState } from "react";
import { WelcomeScreen } from "./components/WelcomeScreen";
import { LoginPage } from "./components/LoginPage";
import { Dashboard } from "./components/Dashboard";
import { MockInterviewPage } from "./components/MockInterviewPage";
import { ResumeBuilderPage } from "./components/ResumeBuilderPage";
import { ResumeAnalyzerPage } from "./components/ResumeAnalyzerPage";
import { FluencyTesterPage } from "./components/FluencyTesterPage";
import { ChatboxPage } from "./components/ChatboxPage";
import { ProgressDashboard } from "./components/ProgressDashboard";
import { InterviewTipsPage } from "./components/InterviewTipsPage";

type Page = 
  | 'welcome' 
  | 'login' 
  | 'dashboard' 
  | 'mock-interview' 
  | 'resume-builder' 
  | 'resume-analyzer' 
  | 'fluency-tester' 
  | 'chatbox' 
  | 'progress'
  | 'tips';

export default function App() {
  const [currentPage, setCurrentPage] = useState<Page>('welcome');

  const renderPage = () => {
    switch (currentPage) {
      case 'welcome':
        return (
          <WelcomeScreen
            onGetStarted={() => setCurrentPage('login')}
            onLogin={() => setCurrentPage('login')}
          />
        );
      
      case 'login':
        return (
          <LoginPage
            onBack={() => setCurrentPage('welcome')}
            onLoginSuccess={() => setCurrentPage('dashboard')}
          />
        );
      
      case 'dashboard':
        return <Dashboard onNavigate={(page) => setCurrentPage(page as Page)} />;
      
      case 'mock-interview':
        return <MockInterviewPage onBack={() => setCurrentPage('dashboard')} />;
      
      case 'resume-builder':
        return <ResumeBuilderPage onBack={() => setCurrentPage('dashboard')} />;
      
      case 'resume-analyzer':
        return <ResumeAnalyzerPage onBack={() => setCurrentPage('dashboard')} />;
      
      case 'fluency-tester':
        return <FluencyTesterPage onBack={() => setCurrentPage('dashboard')} />;
      
      case 'chatbox':
        return <ChatboxPage onBack={() => setCurrentPage('dashboard')} />;
      
      case 'progress':
        return <ProgressDashboard onBack={() => setCurrentPage('dashboard')} />;
      
      case 'tips':
        return <InterviewTipsPage onBack={() => setCurrentPage('dashboard')} />;
      
      default:
        return <WelcomeScreen onGetStarted={() => setCurrentPage('login')} onLogin={() => setCurrentPage('login')} />;
    }
  };

  return (
    <div className="min-h-screen">
      {renderPage()}
    </div>
  );
}
