import React, { useState } from 'react';

interface AIAdviceProps {
  onGetAdvice: () => Promise<{ advice: string; status: string }>;
}

const AIAdvice: React.FC<AIAdviceProps> = ({ onGetAdvice }) => {
  const [advice, setAdvice] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [status, setStatus] = useState<string>('');

  const handleGetAdvice = async () => {
    setIsLoading(true);
    setAdvice('');
    
    try {
      const result = await onGetAdvice();
      setAdvice(result.advice);
      setStatus(result.status);
    } catch (error) {
      setAdvice('Something went wrong. Please try again.');
      setStatus('error');
    } finally {
      setIsLoading(false);
    }
  };

  const getStatusColor = () => {
    switch (status) {
      case 'success':
        return 'border-green-400 bg-green-950';
      case 'no_data':
        return 'border-yellow-400 bg-yellow-950';
      case 'no_api_key':
        return 'border-orange-400 bg-orange-950';
      case 'error':
        return 'border-red-400 bg-red-950';
      default:
        return 'border-blue-400 bg-blue-950';
    }
  };

  const getStatusIcon = () => {
    switch (status) {
      case 'success':
        return '✨';
      case 'no_data':
        return '📊';
      case 'no_api_key':
        return '🔑';
      case 'error':
        return '⚠️';
      default:
        return '🤖';
    }
  };

  return (
    <div className="bg-dark-secondary rounded-lg p-6 border border-dark-accent">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-bold text-dark-text flex items-center">
          🤖 AI Financial Advisor
        </h3>
        <button
          onClick={handleGetAdvice}
          disabled={isLoading}
          className="px-4 py-2 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 disabled:from-gray-600 disabled:to-gray-700 text-white font-medium rounded-lg transition-all duration-200 flex items-center space-x-2 transform hover:scale-105 disabled:scale-100"
        >
          {isLoading ? (
            <>
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
              <span>Thinking...</span>
            </>
          ) : (
            <>
              <span>✨</span>
              <span>Get AI Advice</span>
            </>
          )}
        </button>
      </div>

      {advice && (
        <div className={`mt-4 p-4 rounded-lg border-2 transition-all duration-300 ${getStatusColor()}`}>
          <div className="flex items-start space-x-3">
            <span className="text-2xl">{getStatusIcon()}</span>
            <div className="flex-1">
              <p className="text-dark-text leading-relaxed">
                {advice}
              </p>
              {status === 'no_api_key' && (
                <p className="text-sm text-dark-muted mt-2">
                  Add your Groq API key to the .env file to enable AI advice.
                </p>
              )}
            </div>
          </div>
        </div>
      )}

      {!advice && !isLoading && (
        <div className="mt-4 text-center py-8 border-2 border-dashed border-dark-accent rounded-lg">
          <div className="text-4xl mb-2">🤔</div>
          <p className="text-dark-muted">
            Click the button above to get personalized financial advice based on your spending data!
          </p>
        </div>
      )}
    </div>
  );
};

export default AIAdvice;
