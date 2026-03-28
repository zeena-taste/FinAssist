from typing import Dict, Any

def calculate_score(context: Dict[str, Any]) -> float:
    """
    Score = 100 
      - (debt_ratio * 30)
      - (expense_volatility * 20)
      - (non_essential_spending * 25)
      + (savings_rate * 35)
    """
    income = context.get('income', 0)
    expenses_dict = context.get('expenses', {})
    total_expenses = sum(expenses_dict.values())
    alerts = context.get('alerts', [])
    savings_rate = context.get('savings_rate', 0.0)
    
    debt_payments = expenses_dict.get('loan_repayment', 0)
    debt_ratio = debt_payments / income if income > 0 else 0
    
    non_essential = expenses_dict.get('airtime', 0) + expenses_dict.get('eating_out', 0) + expenses_dict.get('entertainment', 0)
    non_essential_spending = non_essential / total_expenses if total_expenses > 0 else 0
    
    expense_volatility = min(1.0, len(alerts) * 0.2)
    
    score = 100.0 - (debt_ratio * 30.0) - (expense_volatility * 20.0) - (non_essential_spending * 25.0) + (savings_rate * 50.0)
    return round(min(100.0, max(0.0, score)), 2)
