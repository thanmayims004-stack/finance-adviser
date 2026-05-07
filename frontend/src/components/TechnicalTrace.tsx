import React from 'react';

interface TechnicalTraceProps {
  query: string;
  status: string;
  endpoint: string;
}

const TechnicalTrace: React.FC<TechnicalTraceProps> = ({ query, status, endpoint }) => {
  return (
    <div className="bg-gray-100 dark:bg-gray-800 rounded-lg p-4 mt-6 border border-gray-300 dark:border-gray-600">
      <div className="flex items-center mb-3">
        <span className="text-lg mr-2">🔍</span>
        <h4 className="font-mono text-sm font-semibold text-gray-800 dark:text-gray-200">
          Technical Trace: SQL Execution
        </h4>
      </div>
      
      <div className="space-y-2">
        <div className="flex items-center space-x-2">
          <span className="text-xs font-mono text-gray-600 dark:text-gray-400 uppercase tracking-wide">
            Endpoint:
          </span>
          <code className="text-xs bg-gray-200 dark:bg-gray-700 px-2 py-1 rounded font-mono text-blue-600 dark:text-blue-400">
            {endpoint}
          </code>
        </div>
        
        <div className="flex items-center space-x-2">
          <span className="text-xs font-mono text-gray-600 dark:text-gray-400 uppercase tracking-wide">
            Status:
          </span>
          <span className={`text-xs font-medium font-mono ${
            status === 'success' ? 'text-green-600 dark:text-green-400' : 
            status === 'error' ? 'text-red-600 dark:text-red-400' : 'text-yellow-600 dark:text-yellow-400'
          }`}>
            {status.toUpperCase()}
          </span>
        </div>
        
        <div>
          <span className="text-xs font-mono text-gray-600 dark:text-gray-400 uppercase tracking-wide block mb-1">
            Query:
          </span>
          <pre className="text-xs font-mono bg-gray-50 dark:bg-gray-900 p-3 rounded border border-gray-200 dark:border-gray-700 overflow-x-auto text-gray-800 dark:text-gray-200">
            {query}
          </pre>
        </div>
      </div>
    </div>
  );
};

export default TechnicalTrace;
