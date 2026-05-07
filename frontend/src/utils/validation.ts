// Form validation utilities

export interface ValidationRule {
  required?: boolean;
  minLength?: number;
  maxLength?: number;
  min?: number;
  max?: number;
  pattern?: RegExp;
  custom?: (value: any) => string | null;
}

export interface ValidationRules {
  [key: string]: ValidationRule;
}

export interface ValidationResult {
  isValid: boolean;
  errors: { [key: string]: string };
}

export const validateForm = (data: any, rules: ValidationRules): ValidationResult => {
  const errors: { [key: string]: string } = {};

  Object.keys(rules).forEach(field => {
    const value = data[field];
    const rule = rules[field];

    // Required validation
    if (rule.required && (!value || value.toString().trim() === '')) {
      errors[field] = `${field.charAt(0).toUpperCase() + field.slice(1)} is required`;
      return;
    }

    // Skip other validations if field is empty and not required
    if (!value && !rule.required) {
      return;
    }

    // String length validations
    if (typeof value === 'string') {
      if (rule.minLength && value.length < rule.minLength) {
        errors[field] = `${field.charAt(0).toUpperCase() + field.slice(1)} must be at least ${rule.minLength} characters`;
      }
      if (rule.maxLength && value.length > rule.maxLength) {
        errors[field] = `${field.charAt(0).toUpperCase() + field.slice(1)} must not exceed ${rule.maxLength} characters`;
      }
    }

    // Number validations
    if (typeof value === 'number' || !isNaN(value)) {
      const numValue = Number(value);
      if (rule.min !== undefined && numValue < rule.min) {
        errors[field] = `${field.charAt(0).toUpperCase() + field.slice(1)} must be at least ${rule.min}`;
      }
      if (rule.max !== undefined && numValue > rule.max) {
        errors[field] = `${field.charAt(0).toUpperCase() + field.slice(1)} must not exceed ${rule.max}`;
      }
    }

    // Pattern validation
    if (rule.pattern && !rule.pattern.test(value.toString())) {
      errors[field] = `${field.charAt(0).toUpperCase() + field.slice(1)} format is invalid`;
    }

    // Custom validation
    if (rule.custom) {
      const customError = rule.custom(value);
      if (customError) {
        errors[field] = customError;
      }
    }
  });

  return {
    isValid: Object.keys(errors).length === 0,
    errors
  };
};

// Common validation rules
export const commonValidations = {
  goalName: {
    required: true,
    minLength: 2,
    maxLength: 100,
    pattern: /^[a-zA-Z0-9\s\-_]+$/,
    custom: (value: string) => {
      if (!value.trim()) return 'Goal name cannot be empty';
      return null;
    }
  },
  targetAmount: {
    required: true,
    min: 1,
    max: 1000000000,
    custom: (value: number) => {
      if (value <= 0) return 'Target amount must be greater than 0';
      return null;
    }
  },
  currentAmount: {
    required: false,
    min: 0,
    max: 1000000000,
    custom: (value: number) => {
      if (value < 0) return 'Current amount cannot be negative';
      return null;
    }
  },
  targetDate: {
    required: true,
    custom: (value: string) => {
      const date = new Date(value);
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      
      if (date <= today) {
        return 'Target date must be in the future';
      }
      return null;
    }
  },
  age: {
    required: true,
    min: 18,
    max: 120,
    custom: (value: number) => {
      if (!Number.isInteger(value)) return 'Age must be a whole number';
      return null;
    }
  },
  annualIncome: {
    required: true,
    min: 0,
    max: 1000000000,
    custom: (value: number) => {
      if (value < 0) return 'Annual income cannot be negative';
      return null;
    }
  }
};

// Goal form validation rules
export const goalFormRules: ValidationRules = {
  goal_name: commonValidations.goalName,
  target_amount: commonValidations.targetAmount,
  current_amount: commonValidations.currentAmount,
  target_date: commonValidations.targetDate,
  goal_type: {
    required: true
  }
};

// Risk profile form validation rules
export const riskProfileRules: ValidationRules = {
  age: commonValidations.age,
  risk_tolerance: {
    required: true,
    custom: (value: string) => {
      const validOptions = ['Conservative', 'Balanced', 'Aggressive'];
      if (!validOptions.includes(value)) {
        return 'Please select a valid risk tolerance level';
      }
      return null;
    }
  },
  annual_income: commonValidations.annualIncome,
  investment_horizon: {
    required: true,
    min: 1,
    max: 50,
    custom: (value: number) => {
      if (!Number.isInteger(value)) return 'Investment horizon must be a whole number';
      return null;
    }
  }
};
