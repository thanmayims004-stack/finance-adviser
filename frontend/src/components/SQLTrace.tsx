import React from 'react';

interface SQLTraceProps {
  query: string;
  status: string;
  endpoint: string;
}

const SQLTrace: React.FC<SQLTraceProps> = ({ query, status, endpoint }) => {
  const getStatusColor = () => {
    switch (status) {
      case 'success':
        return 'border-green-400 bg-green-950';
      case 'error':
        return 'border-red-400 bg-red-950';
      default:
        return 'border-yellow-400 bg-yellow-950';
    }
  };

  const getStatusIcon = () => {
    switch (status) {
      case 'success':
        return '✅';
      case 'error':
        return '❌';
      default:
        return '⚠️';
    }
  };

  return (
    <div className="bg-dark-secondary rounded-lg p-6 border border-dark-accent">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-bold text-dark-text flex items-center">
          🔍 SQL Trace
        </h3>
        <div className="flex items-center space-x-2">
          <span className="text-sm text-dark-muted">Endpoint:</span>
          <code className="text-xs bg-dark-accent px-2 py-1 rounded text-blue-400">
            {endpoint}
          </code>
        </div>
      </div>

      <div className={`p-4 rounded-lg border-2 font-mono text-sm ${getStatusColor()}`}>
        <div className="flex items-start space-x-3">
          <span className="text-lg">{getStatusIcon()}</span>
          <div className="flex-1">
            <div className="flex items-center space-x-2 mb-2">
              <span className="text-xs text-dark-muted uppercase tracking-wide">
                Status:
              </span>
              <span className={`text-xs font-medium ${
                status === 'success' ? 'text-green-400' : 
                status === 'error' ? 'text-red-400' : 'text-yellow-400'
              }`}>
                {status.toUpperCase()}
              </span>
            </div>
            
            <div className="mb-2">
              <span className="text-xs text-dark-muted uppercase tracking-wide">
                Query:
              </span>
            </div>
            
            <pre className="text-dark-text whitespace-pre-wrap break-all">
              {query}
            </pre>
          </div>
        </div>
      </div>

      <div className="mt-4 text-xs text-dark-muted">
        <p>💡 This shows the exact SQL query executed to fetch your financial data.</p>
      </div>
    </div>
  );
};

export default SQLTrace;
