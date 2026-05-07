import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import Dashboard from './components/Dashboard';
import RIADashboard from './components/RIADashboard';
import { getSpendingData, checkHealth, getFinancialAdvice } from './services/api';
import { SpendingData } from './types';
import { Shield } from 'lucide-react';

const App: React.FC = () => {
  const [isDarkMode, setIsDarkMode] = useState(true);
  const [activeView, setActiveView] = useState<'finance' | 'ria'>('finance');
  const [spendingData, setSpendingData] = useState<{ data: SpendingData[]; query_used: string; status: string }>({
    data: [],
    query_used: '',
    status: ''
  });
  const [isLoading, setIsLoading] = useState(true);
  const [dbStatus, setDbStatus] = useState<'connected' | 'disconnected'>('disconnected');

  useEffect(() => {
    document.documentElement.classList.toggle('dark', isDarkMode);
  }, [isDarkMode]);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setIsLoading(true);
    try {
      const [spending, health] = await Promise.all([
        getSpendingData(),
        checkHealth()
      ]);

      setSpendingData(spending);
      setDbStatus(health.database === 'connected' ? 'connected' : 'disconnected');
    } catch (error) {
      console.error('Error fetching data:', error);
      setDbStatus('disconnected');
    } finally {
      setIsLoading(false);
    }
  };

  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode);
  };

  return (
    <div className={`min-h-screen ${isDarkMode ? 'dark' : ''}`}>
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
        <Header isDarkMode={isDarkMode} toggleDarkMode={toggleDarkMode} />
        
        {/* Premium Navigation Tabs */}
        <div className="bg-gradient-to-r from-slate-800/50 via-slate-900/50 to-slate-800/50 backdrop-blur-lg border-b border-emerald-800/30 shadow-xl">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <nav className="flex space-x-1">
              <button
                onClick={() => setActiveView('finance')}
                className={`py-4 px-6 border-b-2 font-medium text-sm transition-all duration-300 rounded-t-lg ${
                  activeView === 'finance'
                    ? 'border-emerald-500 text-emerald-400 bg-emerald-500/10'
                    : 'border-transparent text-slate-400 hover:text-slate-300 hover:bg-slate-700/30'
                }`}
              >
                <span className="mr-2">💰</span>
                Finance Tracker
              </button>
              <button
                onClick={() => setActiveView('ria')}
                className={`py-4 px-6 border-b-2 font-medium text-sm transition-all duration-300 rounded-t-lg ${
                  activeView === 'ria'
                    ? 'border-emerald-500 text-emerald-400 bg-emerald-500/10'
                    : 'border-transparent text-slate-400 hover:text-slate-300 hover:bg-slate-700/30'
                }`}
              >
                <span className="mr-2">🏦</span>
                RIA Adviser
              </button>
            </nav>
          </div>
        </div>

        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {activeView === 'finance' ? (
            <>
              {/* Premium Status Bar */}
              <div className="mb-8">
                <div className={`inline-flex items-center space-x-3 px-4 py-2 rounded-xl border ${
                  dbStatus === 'connected' 
                    ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400' 
                    : 'bg-red-500/10 border-red-500/30 text-red-400'
                }`}>
                  <div className={`w-3 h-3 rounded-full premium-glow ${
                    dbStatus === 'connected' ? 'bg-emerald-400' : 'bg-red-400'
                  }`}></div>
                  <span className="text-sm font-medium">
                    {dbStatus === 'connected' ? 'Database Connected' : 'Database Disconnected'}
                  </span>
                  {dbStatus === 'connected' && (
                    <Shield className="w-4 h-4 text-emerald-400" />
                  )}
                </div>
              </div>

              {/* Finance Dashboard */}
              <Dashboard 
                spendingData={spendingData}
                isLoading={isLoading}
                onGetAdvice={getFinancialAdvice}
              />

              {/* Premium Refresh Button */}
              <div className="flex justify-center mt-8">
                <button
                  onClick={fetchData}
                  disabled={isLoading}
                  className="premium-btn px-8 py-4 text-white font-semibold rounded-xl flex items-center space-x-3 disabled:opacity-50 text-lg"
                >
                  {isLoading ? (
                    <>
                      <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white"></div>
                      <span>Refreshing Data...</span>
                    </>
                  ) : (
                    <>
                      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                      </svg>
                      <span>Refresh Data</span>
                    </>
                  )}
                </button>
              </div>
            </>
          ) : (
            <RIADashboard />
          )}
        </main>
      </div>
    </div>
  );
};

export default App;
