from sqlalchemy.orm import Session
from app.models.user import User
from app.models.transaction import Transaction
from app.finance.analytics import detect_spending_spikes, categorize_transactions, calculate_savings_rate

def build_context(db: Session, user_id: str) -> dict:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {}

    transactions = db.query(Transaction).filter(Transaction.user_id == user_id).all()
    
    income_txs = [t for t in transactions if t.category == 'income']
    expense_txs = [t for t in transactions if t.category != 'income']

    total_income = sum(t.amount for t in income_txs)
    total_expenses = sum(t.amount for t in expense_txs)
    
    expenses_breakdown = categorize_transactions(expense_txs)
    savings_rate = calculate_savings_rate(total_income, total_expenses)
    alerts = detect_spending_spikes(expense_txs)

    return {
        "user_profile": {
            "name": user.name,
            "phone": user.phone,
            "language": user.language
        },
        "income": total_income,
        "expenses": expenses_breakdown,
        "savings_rate": round(savings_rate, 2),
        "alerts": alerts
    }
