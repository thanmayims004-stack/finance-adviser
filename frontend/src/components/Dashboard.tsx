import React, { useState } from 'react';
import SpendingPieChart from './PieChart';
import TechnicalTrace from './TechnicalTrace';
import { SpendingData } from '../types';

interface DashboardProps {
  spendingData: { data: SpendingData[]; query_used: string; status: string };
  isLoading: boolean;
  onGetAdvice: () => Promise<{ advice: string; query_used: string; status: string }>;
}

const Dashboard: React.FC<DashboardProps> = ({ spendingData, isLoading, onGetAdvice }) => {
  const [advice, setAdvice] = useState<{ advice: string; query_used: string; status: string } | null>(null);
  const [isAdviceLoading, setIsAdviceLoading] = useState(false);

  const handleGetAdvice = async () => {
    setIsAdviceLoading(true);
    try {
      const result = await onGetAdvice();
      setAdvice(result);
    } catch (error) {
      setAdvice({
        advice: 'Failed to get advice. Please try again.',
        query_used: 'Request failed',
        status: 'error'
      });
    } finally {
      setIsAdviceLoading(false);
    }
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  const totalSpending = spendingData.data.reduce((sum, item) => sum + item.amount, 0);

  return (
    <div className="space-y-6">
      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-dark-secondary rounded-lg p-4 border border-dark-accent">
          <div className="text-dark-muted text-sm mb-1">Total Spending</div>
          <div className="text-2xl font-bold text-dark-text">{formatCurrency(totalSpending)}</div>
        </div>
        <div className="bg-dark-secondary rounded-lg p-4 border border-dark-accent">
          <div className="text-dark-muted text-sm mb-1">Categories</div>
          <div className="text-2xl font-bold text-dark-text">{spendingData.data.length}</div>
        </div>
        <div className="bg-dark-secondary rounded-lg p-4 border border-dark-accent">
          <div className="text-dark-muted text-sm mb-1">Avg per Category</div>
          <div className="text-2xl font-bold text-dark-text">
            {formatCurrency(spendingData.data.length > 0 ? totalSpending / spendingData.data.length : 0)}
          </div>
        </div>
      </div>

      {/* Pie Chart */}
      <SpendingPieChart data={spendingData.data} isLoading={isLoading} />

      {/* Get Advice Section */}
      <div className="bg-dark-secondary rounded-lg p-6 border border-dark-accent">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-xl font-bold text-dark-text">💡 Financial Advice</h3>
          <button
            onClick={handleGetAdvice}
            disabled={isAdviceLoading}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white font-medium rounded-lg transition-colors duration-200 flex items-center space-x-2"
          >
            {isAdviceLoading ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                <span>Analyzing...</span>
              </>
            ) : (
              <>
                <span>🤖</span>
                <span>Get Advice</span>
              </>
            )}
          </button>
        </div>

        {advice && (
          <div className={`p-4 rounded-lg border-2 ${
            advice.status === 'success' ? 'border-green-400 bg-green-950' : 
            'border-red-400 bg-red-950'
          }`}>
            <div className="text-dark-text whitespace-pre-line">{advice.advice}</div>
          </div>
        )}
      </div>

      {/* SQL Traces */}
      {/* Technical Trace Section */}
      <TechnicalTrace 
        query={spendingData.query_used}
        status={spendingData.status}
        endpoint="/api/spending"
      />
      
      {advice && (
        <TechnicalTrace 
          query={advice.query_used}
          status={advice.status}
          endpoint="/get-advice"
        />
      )}
    </div>
  );
};

export default Dashboard;
