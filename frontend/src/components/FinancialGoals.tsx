import React, { useState } from 'react';

interface FinancialGoal {
  id: number;
  goal_name: string;
  target_amount: number;
  current_amount: number;
  target_date: string;
  goal_type: string;
  progress_percentage: number;
  created_at: string;
}

interface FinancialGoalsProps {
  goals: { data: FinancialGoal[]; query_used: string; status: string };
  onCreateGoal: (goal: { goal_name: string; target_amount: number; current_amount: number; target_date: string; goal_type: string }) => Promise<void>;
  onRefreshGoals: () => Promise<void>;
}

const FinancialGoals: React.FC<FinancialGoalsProps> = ({ goals, onCreateGoal, onRefreshGoals }) => {
  const [showForm, setShowForm] = useState(false);
  const [editingGoal, setEditingGoal] = useState<number | null>(null);
  const [editTargetAmount, setEditTargetAmount] = useState('');
  const [formData, setFormData] = useState({
    goal_name: '',
    target_amount: '',
    current_amount: '',
    target_date: '',
    goal_type: 'Short-term'
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isUpdating, setIsUpdating] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.goal_name || !formData.target_amount || !formData.target_date) return;

    setIsSubmitting(true);
    try {
      await onCreateGoal({
        goal_name: formData.goal_name,
        target_amount: parseFloat(formData.target_amount),
        current_amount: parseFloat(formData.current_amount) || 0,
        target_date: formData.target_date,
        goal_type: formData.goal_type
      });
      setShowForm(false);
      setFormData({
        goal_name: '',
        target_amount: '',
        current_amount: '',
        target_date: '',
        goal_type: 'Short-term'
      });
    } catch (error) {
      console.error('Error creating goal:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(value);
  };

  const getProgressColor = (percentage: number) => {
    if (percentage >= 80) return 'bg-green-500';
    if (percentage >= 50) return 'bg-yellow-500';
    if (percentage >= 25) return 'bg-orange-500';
    return 'bg-red-500';
  };

  const getGoalEmoji = (goalType: string) => {
    switch (goalType.toLowerCase()) {
      case 'retirement':
      case 'long-term':
        return '🏖️';
      case 'emergency':
      case 'short-term':
        return '🚨';
      case 'house':
      case 'medium-term':
        return '🏠';
      default:
        return '🎯';
    }
  };

  const getGoalTypeColor = (goalType: string) => {
    switch (goalType.toLowerCase()) {
      case 'short-term':
        return 'text-blue-400 bg-blue-900';
      case 'medium-term':
        return 'text-yellow-400 bg-yellow-900';
      case 'long-term':
        return 'text-purple-400 bg-purple-900';
      default:
        return 'text-gray-400 bg-gray-900';
    }
  };

  const calculateDaysRemaining = (targetDate: string) => {
    const target = new Date(targetDate);
    const today = new Date();
    const diffTime = target.getTime() - today.getTime();
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays > 0 ? diffDays : 0;
  };

  const handleEditTarget = (goalId: number, currentTarget: number) => {
    setEditingGoal(goalId);
    setEditTargetAmount(currentTarget.toString());
  };

  const handleUpdateTarget = async (goalId: number) => {
    if (!editTargetAmount || parseFloat(editTargetAmount) <= 0) return;
    
    setIsUpdating(true);
    try {
      // Call API to update the goal target amount
      const response = await fetch(`http://localhost:8001/api/financial-goals/${goalId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          target_amount: parseFloat(editTargetAmount)
        }),
      });
      
      if (response.ok) {
        setEditingGoal(null);
        setEditTargetAmount('');
        // Refresh the goals data
        await onRefreshGoals();
      }
    } catch (error) {
      console.error('Error updating goal:', error);
    } finally {
      setIsUpdating(false);
    }
  };

  const handleCancelEdit = () => {
    setEditingGoal(null);
    setEditTargetAmount('');
  };

  return (
    <div className="bg-gray-900 rounded-lg p-6 border border-gray-800">
      <div className="flex justify-between items-center mb-6">
        <h3 className="text-xl font-bold text-white flex items-center">
          <span className="text-2xl mr-2">🎯</span>
          Financial Goals
        </h3>
        <button
          onClick={() => setShowForm(true)}
          className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors duration-200"
        >
          Add Goal
        </button>
      </div>

      {goals.data.length > 0 ? (
        <div className="space-y-4">
          {goals.data.map((goal) => {
            const daysRemaining = calculateDaysRemaining(goal.target_date);
            const remaining = goal.target_amount - goal.current_amount;
            
            return (
              <div key={goal.id} className="bg-gray-800 rounded-lg p-4 border border-gray-700">
                <div className="flex justify-between items-start mb-3">
                  <div className="flex items-center">
                    <span className="text-2xl mr-3">{getGoalEmoji(goal.goal_type)}</span>
                    <div>
                      <h4 className="text-lg font-semibold text-white">{goal.goal_name}</h4>
                      <p className="text-gray-400 text-sm">
                        Target: {goal.target_date} ({daysRemaining} days remaining)
                      </p>
                    </div>
                  </div>
                  <div className={`px-3 py-1 rounded-full text-xs font-medium ${getGoalTypeColor(goal.goal_type)}`}>
                    {goal.goal_type}
                  </div>
                </div>

                <div className="mb-3">
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-gray-400">Progress</span>
                    <span className="text-white font-medium">{goal.progress_percentage.toFixed(1)}%</span>
                  </div>
                  <div className="w-full bg-gray-700 rounded-full h-3">
                    <div 
                      className={`h-3 rounded-full transition-all duration-300 ${getProgressColor(goal.progress_percentage)}`}
                      style={{ width: `${Math.min(goal.progress_percentage, 100)}%` }}
                    ></div>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <p className="text-gray-400">Current</p>
                    <p className="text-white font-semibold">{formatCurrency(goal.current_amount)}</p>
                  </div>
                  <div className="text-right">
                    <div className="flex items-center justify-end space-x-2">
                      <p className="text-gray-400">Target</p>
                      <button
                        onClick={() => handleEditTarget(goal.id, goal.target_amount)}
                        className="text-blue-400 hover:text-blue-300 transition-colors duration-200"
                        title="Edit target amount"
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                        </svg>
                      </button>
                    </div>
                    {editingGoal === goal.id ? (
                      <div className="flex items-center space-x-1 mt-1">
                        <input
                          type="number"
                          value={editTargetAmount}
                          onChange={(e) => setEditTargetAmount(e.target.value)}
                          className="w-24 px-2 py-1 bg-gray-700 border border-gray-600 rounded text-white text-sm focus:outline-none focus:border-blue-500"
                          min="1"
                          step="0.01"
                        />
                        <button
                          onClick={() => handleUpdateTarget(goal.id)}
                          disabled={isUpdating}
                          className="text-green-400 hover:text-green-300 transition-colors duration-200"
                          title="Save"
                        >
                          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                          </svg>
                        </button>
                        <button
                          onClick={handleCancelEdit}
                          className="text-red-400 hover:text-red-300 transition-colors duration-200"
                          title="Cancel"
                        >
                          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                          </svg>
                        </button>
                      </div>
                    ) : (
                      <p className="text-white font-semibold">{formatCurrency(goal.target_amount)}</p>
                    )}
                  </div>
                </div>

                {remaining > 0 && (
                  <div className="mt-3 pt-3 border-t border-gray-700">
                    <p className="text-sm text-gray-400">
                      <span className="text-white font-medium">{formatCurrency(remaining)}</span> still needed
                    </p>
                  </div>
                )}

                {goal.progress_percentage >= 100 && (
                  <div className="mt-3 pt-3 border-t border-gray-700">
                    <p className="text-sm text-green-400 font-medium">🎉 Goal Achieved!</p>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      ) : (
        <div className="text-center py-8">
          <div className="text-6xl mb-4">🎯</div>
          <p className="text-gray-400 mb-4">No financial goals set yet</p>
          <button
            onClick={() => setShowForm(true)}
            className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors duration-200"
          >
            Create Your First Goal
          </button>
        </div>
      )}

      {/* Goal Form Modal */}
      {showForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-gray-800 rounded-lg p-6 w-full max-w-md border border-gray-700">
            <h4 className="text-xl font-bold text-white mb-4">Create Financial Goal</h4>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-gray-300 text-sm font-medium mb-2">
                  Goal Name
                </label>
                <input
                  type="text"
                  value={formData.goal_name}
                  onChange={(e) => setFormData({...formData, goal_name: e.target.value})}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                  placeholder="e.g., Emergency Fund, Retirement"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-gray-300 text-sm font-medium mb-2">
                    Target Amount
                  </label>
                  <input
                    type="number"
                    value={formData.target_amount}
                    onChange={(e) => setFormData({...formData, target_amount: e.target.value})}
                    className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                    placeholder="10000"
                    min="1"
                    required
                  />
                </div>
                <div>
                  <label className="block text-gray-300 text-sm font-medium mb-2">
                    Current Amount
                  </label>
                  <input
                    type="number"
                    value={formData.current_amount}
                    onChange={(e) => setFormData({...formData, current_amount: e.target.value})}
                    className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                    placeholder="0"
                    min="0"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-gray-300 text-sm font-medium mb-2">
                    Target Date
                  </label>
                  <input
                    type="date"
                    value={formData.target_date}
                    onChange={(e) => setFormData({...formData, target_date: e.target.value})}
                    className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                    required
                  />
                </div>
                <div>
                  <label className="block text-gray-300 text-sm font-medium mb-2">
                    Goal Type
                  </label>
                  <select
                    value={formData.goal_type}
                    onChange={(e) => setFormData({...formData, goal_type: e.target.value})}
                    className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                  >
                    <option value="Short-term">Short-term</option>
                    <option value="Medium-term">Medium-term</option>
                    <option value="Long-term">Long-term</option>
                  </select>
                </div>
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
                  {isSubmitting ? 'Creating...' : 'Create Goal'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* SQL Trace */}
      <div className="mt-6 p-3 bg-gray-800 rounded border border-gray-700">
        <p className="text-xs text-gray-400 font-mono">
          Query: {goals.query_used}
        </p>
      </div>
    </div>
  );
};

export default FinancialGoals;
