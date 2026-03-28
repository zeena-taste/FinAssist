from typing import List, Dict, Any

def detect_spending_spikes(transactions: List[Any], threshold_pct: float = 0.5) -> List[str]:
    """Detect categories where spending is unusually high compared to average."""
    alerts = []
    category_totals = {}
    for t in transactions:
        category_totals[t.category] = category_totals.get(t.category, 0) + t.amount

    # Simple check: if a category dominates > user-defined percent of expenses and isn't 'savings'
    total_spent = sum(category_totals.values())
    if total_spent == 0:
        return alerts

    for cat, amt in category_totals.items():
        if cat != "savings" and cat != "income":
            if amt / total_spent > threshold_pct:
                alerts.append(f"{cat} spending is unusually high at {amt} ({amt/total_spent:.0%})")
    return alerts

def categorize_transactions(transactions: List[Any]) -> Dict[str, float]:
    """Break down transactions by category."""
    totals = {}
    for t in transactions:
        if t.category not in totals:
            totals[t.category] = 0
        totals[t.category] += t.amount
    return totals

def calculate_savings_rate(income: float, expenses: float) -> float:
    """Calculate savings rate (0-1)."""
    if income == 0:
        return 0.0
    savings = income - expenses
    return max(0.0, savings / income)
