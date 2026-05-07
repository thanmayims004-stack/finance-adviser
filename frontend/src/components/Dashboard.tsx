import React, { useState } from 'react';
import SpendingPieChart from './PieChart';
import TechnicalTrace from './TechnicalTrace';
import { SpendingData } from '../types';
import { TrendingUp, TrendingDown, DollarSign, Target, Shield } from 'lucide-react';

interface DashboardProps {
  spendingData: { data: SpendingData[]; query_used: string; status: string };
  isLoading: boolean;
  onGetAdvice: () => Promise<{ advice: string; query_used: string; status: string }>;
}

const Dashboard: React.FC<DashboardProps> = ({ spendingData, isLoading, onGetAdvice }) => {
  const [advice, setAdvice] = useState<{ advice: string; query_used: string; status: string } | null>(null);
  const [isAdviceLoading, setIsAdviceLoading] = useState(false);

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  const getTotalSpending = () => {
    return spendingData.data.reduce((total, item) => total + item.amount, 0);
  };

  const getTopCategory = () => {
    if (spendingData.data.length === 0) return 'N/A';
    return spendingData.data.reduce((max, item) => 
      item.amount > max.amount ? item : max
    ).category;
  };

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

  const totalSpending = spendingData.data.reduce((sum, item) => sum + item.amount, 0);

  return (
    <div className="space-y-8">
      {/* Premium Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-gradient-to-br from-gray-800 to-gray-900 rounded-xl p-6 border border-gray-700 hover:border-blue-500 transition-all duration-300 transform hover:scale-105 hover:shadow-xl">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm font-medium">Total Spending</p>
              <p className="text-3xl font-bold text-white mt-1">{formatCurrency(getTotalSpending())}</p>
              <p className="text-xs text-gray-500 mt-2">Last 30 days</p>
            </div>
            <div className="bg-red-900/50 p-3 rounded-lg">
              <TrendingDown className="w-8 h-8 text-red-400" />
            </div>
          </div>
        </div>
        
        <div className="bg-gradient-to-br from-gray-800 to-gray-900 rounded-xl p-6 border border-gray-700 hover:border-emerald-500 transition-all duration-300 transform hover:scale-105 hover:shadow-xl">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm font-medium">Categories</p>
              <p className="text-3xl font-bold text-white mt-1">{spendingData.data.length}</p>
              <p className="text-xs text-gray-500 mt-2">Active categories</p>
            </div>
            <div className="bg-blue-900/50 p-3 rounded-lg">
              <DollarSign className="w-8 h-8 text-blue-400" />
            </div>
          </div>
        </div>
        
        <div className="bg-gradient-to-br from-gray-800 to-gray-900 rounded-xl p-6 border border-gray-700 hover:border-purple-500 transition-all duration-300 transform hover:scale-105 hover:shadow-xl">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm font-medium">Top Category</p>
              <p className="text-3xl font-bold text-white mt-1 truncate">{getTopCategory()}</p>
              <p className="text-xs text-gray-500 mt-2">Highest spending</p>
            </div>
            <div className="bg-emerald-900/50 p-3 rounded-lg">
              <Target className="w-8 h-8 text-emerald-400" />
            </div>
          </div>
          <div className="text-slate-400 text-sm mb-2">Avg per Category</div>
          <div className="text-3xl font-bold text-purple-400">
            {formatCurrency(spendingData.data.length > 0 ? totalSpending / spendingData.data.length : 0)}
          </div>
          <div className="mt-2 text-xs text-slate-500">Monthly average</div>
        </div>
      </div>

      {/* Pie Chart */}
      <SpendingPieChart data={spendingData.data} isLoading={isLoading} />

      {/* Premium Advice Section */}
      <div className="bg-gradient-to-br from-gray-800 to-gray-900 rounded-xl p-8 border border-gray-700">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-3">
            <div className="p-3 bg-gradient-to-br from-emerald-500/20 to-emerald-600/20 rounded-xl">
              <TrendingUp className="w-6 h-6 text-emerald-400" />
            </div>
            <h3 className="text-2xl font-bold text-white">AI Financial Insights</h3>
          </div>
          <div className="px-3 py-1 bg-emerald-500/20 rounded-full border border-emerald-500/30">
            <span className="text-xs text-emerald-400 font-medium">Powered by AI</span>
          </div>
        </div>
        <div className="flex items-center space-x-4">
          <button
            onClick={handleGetAdvice}
            disabled={isAdviceLoading}
            className="bg-gradient-to-r from-emerald-600 to-emerald-700 hover:from-emerald-700 hover:to-emerald-800 px-6 py-3 text-white font-semibold rounded-xl flex items-center space-x-3 disabled:opacity-50 transition-all duration-300 transform hover:scale-105 disabled:scale-100 shadow-lg hover:shadow-xl"
          >
            {isAdviceLoading ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                <span>Analyzing your finances...</span>
              </>
            ) : (
              <>
                <TrendingUp className="w-5 h-5" />
                <span>Get AI Advice</span>
              </>
            )}
          </button>
          <div className="flex items-center space-x-2 px-4 py-2 bg-slate-800/50 rounded-xl border border-slate-700">
            <Shield className="w-4 h-4 text-emerald-400" />
            <span className="text-sm text-slate-300">Secure & Private</span>
          </div>
        </div>

        {advice && (
          <div className="mt-6 p-6 bg-gradient-to-br from-slate-800/50 to-slate-900/50 rounded-xl border border-emerald-800/30">
            <div className="flex items-center space-x-2 mb-3">
              <TrendingUp className="w-5 h-5 text-emerald-400" />
              <h4 className="text-lg font-semibold text-emerald-400">AI Recommendation</h4>
            </div>
            <div className="text-slate-200 whitespace-pre-line leading-relaxed">{advice.advice}</div>
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
