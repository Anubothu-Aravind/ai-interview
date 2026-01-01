import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import InterviewPage from './pages/InterviewPage';
import History from './components/History';
import { apiService } from './services/api';
import './styles/App.css';

function App() {
  const [healthStatus, setHealthStatus] = useState<{
    supabase: boolean;
    openai: boolean;
  }>({ supabase: false, openai: false });

  useEffect(() => {
    checkHealth();
  }, []);

  const checkHealth = async () => {
    try {
      const health = await apiService.healthCheck();
      setHealthStatus({
        supabase: health.supabase_connected,
        openai: health.openai_configured,
      });
    } catch (err) {
      console.error('Health check failed:', err);
    }
  };

  return (
    <Router>
      <div className="app">
        <header className="app-header">
          <div className="header-content">
            <h1 className="main-title">🎯 AI Interview System</h1>
            <nav className="nav-menu">
              <Link to="/" className="nav-link">
                🏠 Home
              </Link>
              <Link to="/history" className="nav-link">
                📚 History
              </Link>
            </nav>
          </div>
        </header>

        <aside className="sidebar">
          <div className="status-panel">
            <h3>📊 System Status</h3>
            <div className="status-item">
              <span>Supabase:</span>
              <span className={healthStatus.supabase ? 'status-ok' : 'status-error'}>
                {healthStatus.supabase ? '✅ Connected' : '❌ Not Connected'}
              </span>
            </div>
            <div className="status-item">
              <span>OpenAI:</span>
              <span className={healthStatus.openai ? 'status-ok' : 'status-error'}>
                {healthStatus.openai ? '✅ Ready' : '❌ Not Configured'}
              </span>
            </div>
          </div>

          <div className="info-panel">
            <h3>📖 How It Works</h3>
            <ol>
              <li>Upload resume & job description</li>
              <li>AI asks 10 questions one-by-one</li>
              <li>Answer via voice recording</li>
              <li>Get instant AI feedback</li>
              <li>View final results</li>
            </ol>
          </div>
        </aside>

        <main className="main-content">
          <Routes>
            <Route path="/" element={<InterviewPage />} />
            <Route path="/history" element={<History />} />
          </Routes>
        </main>

        <footer className="app-footer">
          <p>© 2024 AI Interview System | Powered by OpenAI & React</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;
