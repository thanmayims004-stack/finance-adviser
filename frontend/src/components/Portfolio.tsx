import React from 'react';

interface Investment {
  id: number;
  investment_type: string;
  amount: number;
  purchase_date: string;
  current_value: number;
  description: string;
}

interface PortfolioProps {
  investments: { data: Investment[]; query_used: string; status: string };
}

const Portfolio: React.FC<PortfolioProps> = ({ investments }) => {
  const calculateTotalValue = () => {
    return investments.data.reduce((sum, inv) => sum + inv.current_value, 0);
  };

  const calculateTotalGain = () => {
    return investments.data.reduce((sum, inv) => sum + (inv.current_value - inv.amount), 0);
  };

  const calculateGainPercentage = () => {
    const totalCost = investments.data.reduce((sum, inv) => sum + inv.amount, 0);
    const totalValue = calculateTotalValue();
    return totalCost > 0 ? ((totalValue - totalCost) / totalCost) * 100 : 0;
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(value);
  };

  const getGainColor = (value: number) => {
    return value >= 0 ? 'text-green-400' : 'text-red-400';
  };

  return (
    <div className="bg-gray-900 rounded-lg p-6 border border-gray-800">
      <h3 className="text-xl font-bold text-white mb-6 flex items-center">
        <span className="text-2xl mr-2">💼</span>
        Portfolio Overview
      </h3>
      
      {/* Portfolio Summary */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="bg-gray-800 rounded-lg p-4">
          <p className="text-gray-400 text-sm mb-1">Total Value</p>
          <p className="text-2xl font-bold text-white">{formatCurrency(calculateTotalValue())}</p>
        </div>
        <div className="bg-gray-800 rounded-lg p-4">
          <p className="text-gray-400 text-sm mb-1">Total Gain/Loss</p>
          <p className={`text-2xl font-bold ${getGainColor(calculateTotalGain())}`}>
            {formatCurrency(calculateTotalGain())}
          </p>
        </div>
        <div className="bg-gray-800 rounded-lg p-4">
          <p className="text-gray-400 text-sm mb-1">Return %</p>
          <p className={`text-2xl font-bold ${getGainColor(calculateGainPercentage())}`}>
            {calculateGainPercentage().toFixed(2)}%
          </p>
        </div>
      </div>

      {/* Investment List */}
      <div className="space-y-3">
        <h4 className="text-lg font-semibold text-white mb-3">Investment Details</h4>
        {investments.data.map((investment) => {
          const gain = investment.current_value - investment.amount;
          const gainPercent = investment.amount > 0 ? (gain / investment.amount) * 100 : 0;
          
          return (
            <div key={investment.id} className="bg-gray-800 rounded-lg p-4 border border-gray-700">
              <div className="flex justify-between items-start mb-2">
                <div>
                  <h5 className="text-white font-semibold">{investment.investment_type}</h5>
                  <p className="text-gray-400 text-sm">{investment.description}</p>
                  <p className="text-gray-500 text-xs">Purchased: {investment.purchase_date}</p>
                </div>
                <div className="text-right">
                  <p className="text-white font-semibold">{formatCurrency(investment.current_value)}</p>
                  <p className={`text-sm ${getGainColor(gain)}`}>
                    {gain >= 0 ? '+' : ''}{formatCurrency(gain)} ({gainPercent.toFixed(1)}%)
                  </p>
                </div>
              </div>
              <div className="w-full bg-gray-700 rounded-full h-2 mt-2">
                <div 
                  className={`h-2 rounded-full ${gain >= 0 ? 'bg-green-500' : 'bg-red-500'}`}
                  style={{ width: `${Math.min(Math.max(gainPercent + 100, 0), 100)}%` }}
                ></div>
              </div>
            </div>
          );
        })}
      </div>

      {/* SQL Trace */}
      <div className="mt-6 p-3 bg-gray-800 rounded border border-gray-700">
        <p className="text-xs text-gray-400 font-mono">
          Query: {investments.query_used}
        </p>
      </div>
    </div>
  );
};

export default Portfolio;
