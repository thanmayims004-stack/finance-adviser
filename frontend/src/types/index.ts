export interface SpendingData {
  category: string;
  amount: number;
  count: number;
}

export interface MonthlySpending {
  month: string;
  expenses: number;
  income: number;
}

export interface Goal {
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
