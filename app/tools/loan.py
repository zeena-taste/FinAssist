def generate_loan_assessment(params: dict) -> dict:
    """Compute basic loan capability."""
    income = params.get('income', 0)
    debt_ratio = params.get('debt_ratio', 0)
    safe_loan_amount = income * 0.3 if debt_ratio < 0.4 else 0
    risk_level = "High" if debt_ratio > 0.4 else "Low"
    print(f"[LOAN TOOL] Assessment - Risk: {risk_level}, Max Amount: {safe_loan_amount}")
    return {
        "status": "success", 
        "risk_level": risk_level, 
        "safe_loan_amount": safe_loan_amount
    }
