import React, { useState } from 'react';
import SpendingPieChart from './PieChart';
import TechnicalTrace from './TechnicalTrace';
import { SpendingData } from '../types';
import { TrendingUp, TrendingDown, DollarSign, Target } from 'lucide-react';

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
    <div className="space-y-8">
      {/* Premium Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="premium-card rounded-xl p-6 hover:scale-105 transition-transform duration-300">
          <div className="flex items-center justify-between mb-4">
            <div className="p-3 bg-gradient-to-br from-emerald-500/20 to-emerald-600/20 rounded-xl">
              <DollarSign className="w-6 h-6 text-emerald-400" />
            </div>
            <TrendingUp className="w-5 h-5 text-emerald-400" />
          </div>
          <div className="text-slate-400 text-sm mb-2">Total Spending</div>
          <div className="text-3xl font-bold text-premium">{formatCurrency(totalSpending)}</div>
          <div className="mt-2 text-xs text-slate-500">This period</div>
        </div>
        <div className="premium-card rounded-xl p-6 hover:scale-105 transition-transform duration-300">
          <div className="flex items-center justify-between mb-4">
            <div className="p-3 bg-gradient-to-br from-blue-500/20 to-blue-600/20 rounded-xl">
              <Target className="w-6 h-6 text-blue-400" />
            </div>
            <TrendingDown className="w-5 h-5 text-blue-400" />
          </div>
          <div className="text-slate-400 text-sm mb-2">Categories</div>
          <div className="text-3xl font-bold text-blue-400">{spendingData.data.length}</div>
          <div className="mt-2 text-xs text-slate-500">Active categories</div>
        </div>
        <div className="premium-card rounded-xl p-6 hover:scale-105 transition-transform duration-300">
          <div className="flex items-center justify-between mb-4">
            <div className="p-3 bg-gradient-to-br from-purple-500/20 to-purple-600/20 rounded-xl">
              <TrendingUp className="w-6 h-6 text-purple-400" />
            </div>
            <div className="w-5 h-5 rounded-full bg-purple-400 premium-glow"></div>
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
      <div className="premium-card rounded-xl p-8">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-3">
            <div className="p-3 bg-gradient-to-br from-emerald-500/20 to-emerald-600/20 rounded-xl">
              <TrendingUp className="w-6 h-6 text-emerald-400" />
            </div>
            <h3 className="text-2xl font-bold text-premium">AI Financial Insights</h3>
          </div>
          <div className="px-3 py-1 bg-emerald-500/20 rounded-full border border-emerald-500/30">
            <span className="text-xs text-emerald-400 font-medium">Powered by AI</span>
          </div>
        </div>
        <div className="flex items-center space-x-4">
          <button
            onClick={handleGetAdvice}
            disabled={isAdviceLoading}
            className="premium-btn px-6 py-3 text-white font-semibold rounded-xl flex items-center space-x-3 disabled:opacity-50"
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
