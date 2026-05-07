import React from 'react';

interface StatsCardProps {
  title: string;
  value: string;
  change?: string;
  changeType?: 'increase' | 'decrease' | 'neutral';
  icon?: React.ReactNode;
}

const StatsCard: React.FC<StatsCardProps> = ({ 
  title, 
  value, 
  change, 
  changeType = 'neutral',
  icon 
}) => {
  const getChangeColor = () => {
    switch (changeType) {
      case 'increase':
        return 'text-red-400';
      case 'decrease':
        return 'text-green-400';
      default:
        return 'text-dark-muted';
    }
  };

  return (
    <div className="bg-dark-secondary rounded-lg p-6 border border-dark-accent">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-dark-muted text-sm font-medium">{title}</p>
          <p className="text-2xl font-bold text-dark-text mt-2">{value}</p>
          {change && (
            <p className={`text-sm mt-2 ${getChangeColor()}`}>
              {changeType === 'increase' && '↑'}
              {changeType === 'decrease' && '↓'}
              {change}
            </p>
          )}
        </div>
        {icon && (
          <div className="text-blue-400">
            {icon}
          </div>
        )}
      </div>
    </div>
  );
};

export default StatsCard;
