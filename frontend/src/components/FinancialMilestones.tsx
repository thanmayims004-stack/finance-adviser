import React, { useState, useEffect } from 'react';
import { Target, TrendingUp, Calendar, DollarSign, Award, AlertCircle } from 'lucide-react';
import { getGoals, getGoalsAdvice } from '../services/api';

interface Goal {
  id: number;
  goal_name: string;
  target_amount: number;
  current_saved: number;
  deadline: string;
  goal_category: string;
  priority: string;
  progress_percentage: number;
  created_at: string;
  updated_at: string;
}

interface GoalsAdvice {
  advice: string;
  query_used: string;
  status: string;
}

const FinancialMilestones: React.FC = () => {
  const [goals, setGoals] = useState<{ data: Goal[]; query_used: string; status: string }>({
    data: [],
    query_used: '',
    status: 'loading'
  });
  const [goalsAdvice, setGoalsAdvice] = useState<GoalsAdvice | null>(null);
  const [isLoadingAdvice, setIsLoadingAdvice] = useState(false);

  useEffect(() => {
    fetchGoals();
  }, []);

  const fetchGoals = async () => {
    try {
      const goalsData = await getGoals();
      setGoals(goalsData);
    } catch (error) {
      console.error('Error fetching goals:', error);
    }
  };

  const handleGetGoalsAdvice = async () => {
    setIsLoadingAdvice(true);
    try {
      const advice = await getGoalsAdvice();
      setGoalsAdvice(advice);
    } catch (error) {
      console.error('Error getting goals advice:', error);
    } finally {
      setIsLoadingAdvice(false);
    }
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(value);
  };

  const getProgressColor = (percentage: number, goalCategory: string) => {
    // Blue for investment-related goals
    if (goalCategory.toLowerCase().includes('retirement') || 
        goalCategory.toLowerCase().includes('investment') ||
        goalCategory.toLowerCase().includes('savings')) {
      return 'bg-blue-500';
    }
    
    // Green for goals more than 50% complete
    if (percentage >= 50) return 'bg-emerald-500';
    
    // Yellow for goals less than 50% complete
    return 'bg-yellow-500';
  };

  const getProgressBgColor = (percentage: number, goalCategory: string) => {
    // Blue for investment-related goals
    if (goalCategory.toLowerCase().includes('retirement') || 
        goalCategory.toLowerCase().includes('investment') ||
        goalCategory.toLowerCase().includes('savings')) {
      return 'bg-blue-500/20';
    }
    
    // Green for goals more than 50% complete
    if (percentage >= 50) return 'bg-emerald-500/20';
    
    // Yellow for goals less than 50% complete
    return 'bg-yellow-500/20';
  };

  const getPriorityColor = (priority: string) => {
    switch (priority.toLowerCase()) {
      case 'high':
        return 'text-red-400 bg-red-500/20 border-red-500/30';
      case 'medium':
        return 'text-yellow-400 bg-yellow-500/20 border-yellow-500/30';
      case 'low':
        return 'text-green-400 bg-green-500/20 border-green-500/30';
      default:
        return 'text-gray-400 bg-gray-500/20 border-gray-500/30';
    }
  };

  const getGoalIcon = (category: string) => {
    switch (category.toLowerCase()) {
      case 'retirement':
        return '🏖️';
      case 'emergency':
        return '🚨';
      case 'housing':
        return '🏠';
      case 'education':
        return '🎓';
      case 'transport':
        return '🚗';
      case 'lifestyle':
        return '✈️';
      default:
        return '🎯';
    }
  };

  const calculateDaysRemaining = (deadline: string) => {
    const target = new Date(deadline);
    const today = new Date();
    const diffTime = target.getTime() - today.getTime();
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays > 0 ? diffDays : 0;
  };

  const getMilestoneStatus = (percentage: number, daysRemaining: number) => {
    if (percentage >= 100) return { icon: '🎉', text: 'Achieved!', color: 'text-emerald-400' };
    if (percentage >= 80) return { icon: '🔥', text: 'Almost there!', color: 'text-orange-400' };
    if (daysRemaining < 90 && percentage < 50) return { icon: '⚠️', text: 'Needs attention', color: 'text-yellow-400' };
    if (daysRemaining < 30) return { icon: '⏰', text: 'Urgent!', color: 'text-red-400' };
    return { icon: '📈', text: 'On track', color: 'text-blue-400' };
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="p-3 bg-gradient-to-br from-emerald-500/20 to-emerald-600/20 rounded-xl">
            <Target className="w-6 h-6 text-emerald-400" />
          </div>
          <div>
            <h3 className="text-2xl font-bold text-premium">Financial Milestones</h3>
            <p className="text-slate-400 text-sm">Track your progress toward financial goals</p>
          </div>
        </div>
        <button
          onClick={handleGetGoalsAdvice}
          disabled={isLoadingAdvice}
          className="premium-btn px-6 py-3 text-white font-semibold rounded-xl flex items-center space-x-2 disabled:opacity-50"
        >
          {isLoadingAdvice ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              <span>Analyzing goals...</span>
            </>
          ) : (
            <>
              <TrendingUp className="w-5 h-5" />
              <span>Get Goal Advice</span>
            </>
          )}
        </button>
      </div>

      {/* Color Legend */}
      <div className="bg-slate-800/50 rounded-xl p-4 border border-slate-700">
        <h4 className="text-sm font-semibold text-white mb-3">Progress Bar Colors:</h4>
        <div className="flex flex-wrap gap-4 text-xs">
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 rounded bg-emerald-500"></div>
            <span className="text-slate-300">More than 50% complete</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 rounded bg-yellow-500"></div>
            <span className="text-slate-300">Less than 50% complete</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 rounded bg-blue-500"></div>
            <span className="text-slate-300">Investment-related goals</span>
          </div>
        </div>
      </div>

      {/* Goals Progress Cards */}
      <div className="grid gap-6">
        {goals.data.map((goal) => {
          const daysRemaining = calculateDaysRemaining(goal.deadline);
          const milestoneStatus = getMilestoneStatus(goal.progress_percentage, daysRemaining);
          const remaining = goal.target_amount - goal.current_saved;
          
          return (
            <div key={goal.id} className="premium-card rounded-xl p-6 hover:scale-[1.02] transition-all duration-300">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center space-x-3">
                  <div className="text-3xl">{getGoalIcon(goal.goal_category)}</div>
                  <div>
                    <h4 className="text-lg font-semibold text-white">{goal.goal_name}</h4>
                    <div className="flex items-center space-x-2 mt-1">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium border ${getPriorityColor(goal.priority)}`}>
                        {goal.priority}
                      </span>
                      <div className="flex items-center text-xs text-slate-400">
                        <Calendar className="w-3 h-3 mr-1" />
                        {daysRemaining} days left
                      </div>
                    </div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="flex items-center space-x-1">
                    <span className="text-2xl">{milestoneStatus.icon}</span>
                    <span className={`text-sm font-medium ${milestoneStatus.color}`}>
                      {milestoneStatus.text}
                    </span>
                  </div>
                </div>
              </div>

              {/* Progress Bar */}
              <div className="mb-4">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm text-slate-400">Progress</span>
                  <span className="text-sm font-medium text-white">{goal.progress_percentage.toFixed(1)}%</span>
                </div>
                <div className={`w-full rounded-full h-4 ${getProgressBgColor(goal.progress_percentage, goal.goal_category)}`}>
                  <div 
                    className={`h-4 rounded-full transition-all duration-500 ${getProgressColor(goal.progress_percentage, goal.goal_category)}`}
                    style={{ width: `${Math.min(goal.progress_percentage, 100)}%` }}
                  ></div>
                </div>
              </div>

              {/* Financial Details */}
              <div className="grid grid-cols-3 gap-4 text-sm">
                <div>
                  <p className="text-slate-400 mb-1">Current</p>
                  <p className="text-white font-semibold flex items-center">
                    <DollarSign className="w-4 h-4 mr-1" />
                    {formatCurrency(goal.current_saved)}
                  </p>
                </div>
                <div className="text-center">
                  <p className="text-slate-400 mb-1">Target</p>
                  <p className="text-white font-semibold">
                    {formatCurrency(goal.target_amount)}
                  </p>
                </div>
                <div className="text-right">
                  <p className="text-slate-400 mb-1">Remaining</p>
                  <p className={`font-semibold ${remaining <= 0 ? 'text-emerald-400' : 'text-orange-400'}`}>
                    {remaining <= 0 ? 'Complete!' : formatCurrency(remaining)}
                  </p>
                </div>
              </div>

              {/* Deadline */}
              <div className="mt-4 pt-4 border-t border-slate-700">
                <div className="flex items-center justify-between text-xs">
                  <span className="text-slate-400">Target Date: {goal.deadline}</span>
                  <div className="flex items-center space-x-1">
                    <Award className="w-3 h-3 text-emerald-400" />
                    <span className="text-emerald-400">
                      {goal.progress_percentage >= 100 ? 'Achieved!' : `${goal.progress_percentage.toFixed(0)}% Complete`}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* AI Goals Advice */}
      {goalsAdvice && (
        <div className="premium-card rounded-xl p-6">
          <div className="flex items-center space-x-2 mb-4">
            <TrendingUp className="w-5 h-5 text-emerald-400" />
            <h4 className="text-lg font-semibold text-emerald-400">AI Goal Advice</h4>
          </div>
          <div className="text-slate-200 whitespace-pre-line leading-relaxed">
            {goalsAdvice.advice}
          </div>
        </div>
      )}

      {/* Empty State */}
      {goals.data.length === 0 && goals.status !== 'loading' && (
        <div className="text-center py-12">
          <Target className="w-16 h-16 text-slate-600 mx-auto mb-4" />
          <h4 className="text-xl font-semibold text-white mb-2">No Financial Goals Set</h4>
          <p className="text-slate-400 mb-6">
            Start tracking your financial goals to see your progress and get personalized advice.
          </p>
          <div className="inline-flex items-center space-x-2 px-4 py-2 bg-emerald-500/20 rounded-xl border border-emerald-500/30">
            <AlertCircle className="w-4 h-4 text-emerald-400" />
            <span className="text-emerald-400 text-sm">Add your first goal to get started</span>
          </div>
        </div>
      )}

      {/* SQL Trace */}
      <div className="mt-6 p-3 bg-slate-800/50 rounded border border-slate-700">
        <p className="text-xs text-slate-400 font-mono">
          Query: {goals.query_used}
        </p>
      </div>
    </div>
  );
};

export default FinancialMilestones;
