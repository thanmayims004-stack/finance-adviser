import React, { useState, useEffect } from 'react';
import Portfolio from './Portfolio';
import RiskProfile from './RiskProfile';
import FinancialGoals from './FinancialGoals';
import FinancialMilestones from './FinancialMilestones';
import RIAAdvice from './RIAAdvice';
import TechnicalTrace from './TechnicalTrace';
import { getInvestments, getRiskProfile, getFinancialGoals, createRiskProfile, createFinancialGoal, getRIAAdvice } from '../services/api';

const RIADashboard: React.FC = () => {
  const [investments, setInvestments] = useState<{ data: any[]; query_used: string; status: string }>({ data: [], query_used: '', status: 'loading' });
  const [riskProfile, setRiskProfile] = useState<{ data: any; query_used: string; status: string }>({ data: null, query_used: '', status: 'loading' });
  const [goals, setGoals] = useState<{ data: any[]; query_used: string; status: string }>({ data: [], query_used: '', status: 'loading' });
  const [riaAdvice, setRIAAdvice] = useState<{ advice: string; query_used: string; status: string } | null>(null);
  const [isLoadingAdvice, setIsLoadingAdvice] = useState(false);
  const [activeTab, setActiveTab] = useState('portfolio');

  useEffect(() => {
    fetchRIAData();
  }, []);

  const fetchRIAData = async () => {
    try {
      const [investmentsData, riskData, goalsData] = await Promise.all([
        getInvestments(),
        getRiskProfile(),
        getFinancialGoals()
      ]);

      setInvestments(investmentsData);
      setRiskProfile(riskData);
      setGoals(goalsData);
    } catch (error) {
      console.error('Error fetching RIA data:', error);
    }
  };

  const handleCreateRiskProfile = async (profile: { age: number; risk_tolerance: string }) => {
    try {
      await createRiskProfile(profile);
      // Refresh risk profile data
      const updatedProfile = await getRiskProfile();
      setRiskProfile(updatedProfile);
    } catch (error) {
      console.error('Error creating risk profile:', error);
    }
  };

  const handleCreateGoal = async (goal: { 
    goal_name: string; 
    target_amount: number; 
    current_amount: number; 
    target_date: string; 
    goal_type: string 
  }) => {
    try {
      await createFinancialGoal(goal);
      // Refresh goals data
      const updatedGoals = await getFinancialGoals();
      setGoals(updatedGoals);
    } catch (error) {
      console.error('Error creating goal:', error);
    }
  };

  const handleRefreshGoals = async () => {
    try {
      const updatedGoals = await getFinancialGoals();
      setGoals(updatedGoals);
    } catch (error) {
      console.error('Error refreshing goals:', error);
    }
  };

  const handleGetRIAAdvice = async () => {
    setIsLoadingAdvice(true);
    try {
      const advice = await getRIAAdvice();
      setRIAAdvice(advice);
    } catch (error) {
      console.error('Error getting RIA advice:', error);
    } finally {
      setIsLoadingAdvice(false);
    }
  };

  const tabs = [
    { id: 'portfolio', label: 'Portfolio', icon: '💼' },
    { id: 'risk', label: 'Risk Profile', icon: '🎯' },
    { id: 'goals', label: 'Financial Goals', icon: '🎯' },
    { id: 'milestones', label: 'Milestones', icon: '🏆' },
    { id: 'advice', label: 'RIA Advice', icon: '🧠' }
  ];

  return (
    <div className="min-h-screen bg-black text-white">
      {/* Header */}
      <div className="bg-gray-900 border-b border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <span className="text-2xl mr-3">🏦</span>
              <h1 className="text-xl font-bold text-white">RIA Investment Adviser</h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-400">Professional Portfolio Management</span>
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="bg-gray-900 border-b border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex space-x-8">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors duration-200 ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-400'
                    : 'border-transparent text-gray-400 hover:text-gray-300 hover:border-gray-600'
                }`}
              >
                <span className="mr-2">{tab.icon}</span>
                {tab.label}
              </button>
            ))}
          </nav>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Tab Content */}
        {activeTab === 'portfolio' && (
          <div className="space-y-6">
            <Portfolio investments={investments} />
          </div>
        )}

        {activeTab === 'risk' && (
          <div className="space-y-6">
            <RiskProfile 
              riskProfile={riskProfile} 
              onCreateProfile={handleCreateRiskProfile}
            />
          </div>
        )}

        {activeTab === 'goals' && (
          <div className="space-y-6">
            <FinancialGoals 
              goals={goals} 
              onCreateGoal={handleCreateGoal}
              onRefreshGoals={handleRefreshGoals}
            />
          </div>
        )}

        {activeTab === 'milestones' && (
          <div className="space-y-6">
            <FinancialMilestones />
          </div>
        )}

        {activeTab === 'advice' && (
          <div className="space-y-6">
            <RIAAdvice 
              advice={riaAdvice}
              onGetAdvice={handleGetRIAAdvice}
              isLoading={isLoadingAdvice}
            />
          </div>
        )}

        {/* Technical Trace */}
        <TechnicalTrace 
          query={activeTab === 'portfolio' ? investments.query_used : 
                 activeTab === 'risk' ? riskProfile.query_used :
                 activeTab === 'goals' ? goals.query_used :
                 riaAdvice?.query_used || ''}
          status={activeTab === 'portfolio' ? investments.status : 
                  activeTab === 'risk' ? riskProfile.status :
                  activeTab === 'goals' ? goals.status :
                  riaAdvice?.status || 'success'}
          endpoint={`/api/${activeTab === 'portfolio' ? 'investments' : 
                       activeTab === 'risk' ? 'risk-profile' :
                       activeTab === 'goals' ? 'financial-goats' :
                       'ria-advice'}`}
        />
      </div>

      {/* Footer */}
      <div className="bg-gray-900 border-t border-gray-800 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <span className="text-sm text-gray-400">
                Powered by AI • Certified Financial Planner Analysis
              </span>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-xs text-gray-500">
                50/30/20 Portfolio Strategy
              </span>
              <span className="text-xs text-gray-500">
                Risk-Adjusted Recommendations
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RIADashboard;
