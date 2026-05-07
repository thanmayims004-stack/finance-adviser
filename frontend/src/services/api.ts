import axios from 'axios';
import { SpendingData, MonthlySpending } from '../types';

const API_BASE_URL = 'http://localhost:8001';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

export const getSpendingData = async (): Promise<{ data: SpendingData[]; query_used: string; status: string }> => {
  try {
    const response = await api.get('/api/spending');
    return response.data;
  } catch (error) {
    console.error('Error fetching spending data:', error);
    return { data: [], query_used: 'Request failed', status: 'error' };
  }
};

export const getMonthlySpending = async (): Promise<MonthlySpending[]> => {
  try {
    const response = await api.get('/api/spending/monthly');
    return response.data;
  } catch (error) {
    console.error('Error fetching monthly spending:', error);
    return [];
  }
};

export const checkHealth = async (): Promise<{ status: string; database: string }> => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    console.error('Error checking health:', error);
    return { status: 'unhealthy', database: 'disconnected' };
  }
};

export const getAIAdvice = async (): Promise<{ advice: string; query_used: string; status: string }> => {
  try {
    const response = await api.get('/ai-advice');
    return response.data;
  } catch (error) {
    console.error('Error fetching AI advice:', error);
    return { 
      advice: 'Unable to get AI advice right now. Please try again later.', 
      query_used: 'Request failed',
      status: 'error' 
    };
  }
};

export const getFinancialAdvice = async (): Promise<{ advice: string; query_used: string; status: string }> => {
  try {
    const response = await api.get('/get-advice');
    return response.data;
  } catch (error) {
    console.error('Error fetching financial advice:', error);
    return { 
      advice: 'Unable to get financial advice right now. Please try again later.', 
      query_used: 'Request failed',
      status: 'error' 
    };
  }
};

// RIA API Functions
export const getInvestments = async (): Promise<{ data: any[]; query_used: string; status: string }> => {
  try {
    const response = await api.get('/api/investments');
    return response.data;
  } catch (error) {
    console.error('Error fetching investments:', error);
    return { data: [], query_used: 'Request failed', status: 'error' };
  }
};

export const getRiskProfile = async (): Promise<{ data: any; query_used: string; status: string }> => {
  try {
    const response = await api.get('/api/risk-profile');
    return response.data;
  } catch (error) {
    console.error('Error fetching risk profile:', error);
    return { data: null, query_used: 'Request failed', status: 'error' };
  }
};

export const createRiskProfile = async (profile: { age: number; risk_tolerance: string }): Promise<{ data: any; query_used: string; status: string }> => {
  try {
    const response = await api.post('/api/risk-profile', profile);
    return response.data;
  } catch (error) {
    console.error('Error creating risk profile:', error);
    return { data: null, query_used: 'Request failed', status: 'error' };
  }
};

export const getFinancialGoals = async (): Promise<{ data: any[]; query_used: string; status: string }> => {
  try {
    const response = await api.get('/api/financial-goats');
    return response.data;
  } catch (error) {
    console.error('Error fetching financial goals:', error);
    return { data: [], query_used: 'Request failed', status: 'error' };
  }
};

export const createFinancialGoal = async (goal: { goal_name: string; target_amount: number; current_amount: number; target_date: string; goal_type: string }): Promise<{ data: any; query_used: string; status: string }> => {
  try {
    const response = await api.post('/api/financial-goats', goal);
    return response.data;
  } catch (error) {
    console.error('Error creating financial goal:', error);
    return { data: null, query_used: 'Request failed', status: 'error' };
  }
};

export const getRIAAdvice = async (): Promise<{ advice: string; query_used: string; status: string }> => {
  try {
    const response = await api.get('/ria-advice');
    return response.data;
  } catch (error) {
    console.error('Error fetching RIA advice:', error);
    return { 
      advice: 'Unable to get RIA advice right now. Please try again later.', 
      query_used: 'Request failed',
      status: 'error' 
    };
  }
};

export const getGoalsAdvice = async (): Promise<{ advice: string; query_used: string; status: string }> => {
  try {
    const response = await api.get('/get-goals');
    return response.data;
  } catch (error) {
    console.error('Error fetching goals advice:', error);
    return { 
      advice: 'Unable to get goals advice right now. Please try again later.', 
      query_used: 'Request failed',
      status: 'error' 
    };
  }
};
