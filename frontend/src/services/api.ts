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
