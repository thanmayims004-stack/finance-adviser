import React, { useState } from 'react';

interface RiskProfileData {
  id: number;
  age: number;
  risk_tolerance: string;
  created_at: string;
}

interface RiskProfileProps {
  riskProfile: { data: RiskProfileData | null; query_used: string; status: string };
  onCreateProfile: (profile: { age: number; risk_tolerance: string }) => Promise<void>;
}

const RiskProfile: React.FC<RiskProfileProps> = ({ riskProfile, onCreateProfile }) => {
  const [showForm, setShowForm] = useState(false);
  const [age, setAge] = useState('');
  const [riskTolerance, setRiskTolerance] = useState('Medium');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!age) return;

    setIsSubmitting(true);
    try {
      await onCreateProfile({ age: parseInt(age), risk_tolerance: riskTolerance });
      setShowForm(false);
      setAge('');
      setRiskTolerance('Medium');
    } catch (error) {
      console.error('Error creating risk profile:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const getRiskColor = (tolerance: string) => {
    switch (tolerance.toLowerCase()) {
      case 'low':
        return 'text-blue-400 bg-blue-900';
      case 'medium':
        return 'text-yellow-400 bg-yellow-900';
      case 'high':
        return 'text-red-400 bg-red-900';
      default:
        return 'text-gray-400 bg-gray-900';
    }
  };

  const getRiskEmoji = (tolerance: string) => {
    switch (tolerance.toLowerCase()) {
      case 'low':
        return '🛡️';
      case 'medium':
        return '⚖️';
      case 'high':
        return '🚀';
      default:
        return '📊';
    }
  };

  const getRiskDescription = (tolerance: string) => {
    switch (tolerance.toLowerCase()) {
      case 'low':
        return 'Conservative investor focused on capital preservation';
      case 'medium':
        return 'Balanced investor seeking growth with moderate risk';
      case 'high':
        return 'Aggressive investor seeking maximum returns';
      default:
        return 'Risk tolerance not specified';
    }
  };

  return (
    <div className="bg-gray-900 rounded-lg p-6 border border-gray-800">
      <div className="flex justify-between items-center mb-6">
        <h3 className="text-xl font-bold text-white flex items-center">
          <span className="text-2xl mr-2">🎯</span>
          Risk Profile
        </h3>
        {!riskProfile.data && (
          <button
            onClick={() => setShowForm(true)}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors duration-200"
          >
            Set Profile
          </button>
        )}
      </div>

      {riskProfile.data ? (
        <div className="space-y-4">
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center">
                <span className="text-3xl mr-3">{getRiskEmoji(riskProfile.data.risk_tolerance)}</span>
                <div>
                  <h4 className="text-lg font-semibold text-white">
                    {riskProfile.data.risk_tolerance} Risk Tolerance
                  </h4>
                  <p className="text-gray-400 text-sm">Age: {riskProfile.data.age}</p>
                </div>
              </div>
              <div className={`px-3 py-1 rounded-full text-sm font-medium ${getRiskColor(riskProfile.data.risk_tolerance)}`}>
                {riskProfile.data.risk_tolerance}
              </div>
            </div>
            
            <p className="text-gray-300 mb-4">
              {getRiskDescription(riskProfile.data.risk_tolerance)}
            </p>

            <div className="grid grid-cols-3 gap-4 mt-4">
              <div className="text-center">
                <p className="text-gray-400 text-xs mb-1">Suggested Bonds</p>
                <p className="text-white font-bold">
                  {riskProfile.data.risk_tolerance === 'Low' ? '60%' : 
                   riskProfile.data.risk_tolerance === 'Medium' ? '40%' : '20%'}
                </p>
              </div>
              <div className="text-center">
                <p className="text-gray-400 text-xs mb-1">Suggested Stocks</p>
                <p className="text-white font-bold">
                  {riskProfile.data.risk_tolerance === 'Low' ? '30%' : 
                   riskProfile.data.risk_tolerance === 'Medium' ? '50%' : '70%'}
                </p>
              </div>
              <div className="text-center">
                <p className="text-gray-400 text-xs mb-1">Suggested Alternatives</p>
                <p className="text-white font-bold">
                  {riskProfile.data.risk_tolerance === 'Low' ? '10%' : 
                   riskProfile.data.risk_tolerance === 'Medium' ? '10%' : '10%'}
                </p>
              </div>
            </div>
          </div>

          <button
            onClick={() => setShowForm(true)}
            className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-colors duration-200"
          >
            Update Profile
          </button>
        </div>
      ) : (
        <div className="text-center py-8">
          <div className="text-6xl mb-4">🎯</div>
          <p className="text-gray-400 mb-4">No risk profile set yet</p>
          <button
            onClick={() => setShowForm(true)}
            className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors duration-200"
          >
            Create Risk Profile
          </button>
        </div>
      )}

      {/* Risk Profile Form Modal */}
      {showForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-gray-800 rounded-lg p-6 w-full max-w-md border border-gray-700">
            <h4 className="text-xl font-bold text-white mb-4">Set Your Risk Profile</h4>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-gray-300 text-sm font-medium mb-2">
                  Age
                </label>
                <input
                  type="number"
                  value={age}
                  onChange={(e) => setAge(e.target.value)}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                  min="18"
                  max="100"
                  required
                />
              </div>

              <div>
                <label className="block text-gray-300 text-sm font-medium mb-2">
                  Risk Tolerance
                </label>
                <select
                  value={riskTolerance}
                  onChange={(e) => setRiskTolerance(e.target.value)}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                >
                  <option value="Low">Low 🛡️ - Conservative</option>
                  <option value="Medium">Medium ⚖️ - Balanced</option>
                  <option value="High">High 🚀 - Aggressive</option>
                </select>
              </div>

              <div className="flex space-x-3 pt-4">
                <button
                  type="button"
                  onClick={() => setShowForm(false)}
                  className="flex-1 px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-colors duration-200"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="flex-1 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors duration-200 disabled:opacity-50"
                >
                  {isSubmitting ? 'Saving...' : 'Save Profile'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* SQL Trace */}
      <div className="mt-6 p-3 bg-gray-800 rounded border border-gray-700">
        <p className="text-xs text-gray-400 font-mono">
          Query: {riskProfile.query_used}
        </p>
      </div>
    </div>
  );
};

export default RiskProfile;
