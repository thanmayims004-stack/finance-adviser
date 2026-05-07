import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { SpendingData } from '../types';

interface SpendingChartProps {
  data: SpendingData[];
  isLoading?: boolean;
}

const SpendingChart: React.FC<SpendingChartProps> = ({ data, isLoading = false }) => {
  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-dark-secondary border border-dark-accent rounded-lg p-3 shadow-lg">
          <p className="text-dark-text font-semibold">{label}</p>
          <p className="text-green-400">
            Amount: {formatCurrency(payload[0].value)}
          </p>
          <p className="text-dark-muted text-sm">
            Transactions: {payload[0].payload.count}
          </p>
        </div>
      );
    }
    return null;
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-96 bg-dark-secondary rounded-lg">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (!data || data.length === 0) {
    return (
      <div className="flex items-center justify-center h-96 bg-dark-secondary rounded-lg">
        <p className="text-dark-muted">No spending data available</p>
      </div>
    );
  }

  return (
    <div className="w-full h-96 bg-dark-secondary rounded-lg p-4">
      <h3 className="text-xl font-bold text-dark-text mb-4">Spending by Category</h3>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={data}
          margin={{
            top: 20,
            right: 30,
            left: 20,
            bottom: 60,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
          <XAxis 
            dataKey="category" 
            angle={-45}
            textAnchor="end"
            height={100}
            tick={{ fill: '#9ca3af' }}
          />
          <YAxis 
            tick={{ fill: '#9ca3af' }}
            tickFormatter={formatCurrency}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend 
            wrapperStyle={{ color: '#f3f4f6' }}
          />
          <Bar 
            dataKey="amount" 
            fill="#3b82f6" 
            name="Spending Amount"
            radius={[8, 8, 0, 0]}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default SpendingChart;
