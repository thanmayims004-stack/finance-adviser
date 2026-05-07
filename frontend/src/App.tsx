import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import Dashboard from './components/Dashboard';
import { getSpendingData, checkHealth, getFinancialAdvice } from './services/api';
import { SpendingData } from './types';

const App: React.FC = () => {
  const [isDarkMode, setIsDarkMode] = useState(true);
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
      <div className="bg-gray-900 min-h-screen">
        <Header isDarkMode={isDarkMode} toggleDarkMode={toggleDarkMode} />
        
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Status Bar */}
          <div className="mb-8">
            <div className={`flex items-center space-x-2 ${
              dbStatus === 'connected' ? 'text-green-400' : 'text-red-400'
            }`}>
              <div className={`w-3 h-3 rounded-full ${
                dbStatus === 'connected' ? 'bg-green-400' : 'bg-red-400'
              }`}></div>
              <span className="text-sm font-medium">
                Database {dbStatus === 'connected' ? 'Connected' : 'Disconnected'}
              </span>
            </div>
          </div>

          {/* Main Dashboard */}
          <Dashboard 
            spendingData={spendingData}
            isLoading={isLoading}
            onGetAdvice={getFinancialAdvice}
          />

          {/* Refresh Button */}
          <div className="flex justify-center mt-8">
            <button
              onClick={fetchData}
              disabled={isLoading}
              className="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white font-medium rounded-lg transition-colors duration-200 flex items-center space-x-2"
            >
              {isLoading ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                  <span>Loading...</span>
                </>
              ) : (
                <>
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                  <span>Refresh Data</span>
                </>
              )}
            </button>
          </div>
        </main>
      </div>
    </div>
  );
};

export default App;
