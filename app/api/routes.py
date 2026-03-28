from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import datetime

from app.db.database import get_db
from app.schemas.request import AgentQueryRequest
from app.schemas.response import AgentQueryResponse, AgentQueryResponseData
from app.services.context_builder import build_context
from app.finance.scoring import calculate_score
from app.agent.brain import reason
from app.agent.planner import decide
from app.models.user import User
from app.models.transaction import Transaction

router = APIRouter()

@router.post("/query", response_model=AgentQueryResponse)
def agent_query(request: AgentQueryRequest, db: Session = Depends(get_db)):
    try:
        context = build_context(db, request.user_id)
        if not context:
            raise HTTPException(status_code=404, detail="User not found")
            
        score = calculate_score(context)
        decision_json = reason(context, request.message)
        planned_outcome = decide(decision_json)
        
        response_data = AgentQueryResponseData(
            message=planned_outcome["message"],
            action_taken=planned_outcome["action_taken"],
            result=planned_outcome["result"],
            financial_score=score
        )
        
        return AgentQueryResponse(status="success", data=response_data)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/seed-demo")
def seed_demo(db: Session = Depends(get_db)):
    """Seeds a demo user 'usr_12345' for testing. Safe to call multiple times."""
    existing = db.query(User).filter(User.id == "usr_12345").first()
    if existing:
        return {"status": "already_seeded", "user_id": "usr_12345"}

    now = datetime.datetime.utcnow()
    user = User(id="usr_12345", name="Kwame Mensah", phone="+233555123456", language="English")
    db.add(user)

    transactions = [
        {"amount": 100000, "category": "income", "days_ago": 30},
        {"amount": 100000, "category": "income", "days_ago": 0},
        {"amount": 8000,   "category": "food",   "days_ago": 25},
        {"amount": 3000,   "category": "transport", "days_ago": 24},
        {"amount": 25000,  "category": "momo_transfer", "days_ago": 20},
        {"amount": 15000,  "category": "loan_repayment", "days_ago": 15},
        {"amount": 12000,  "category": "food",   "days_ago": 5},
        {"amount": 5000,   "category": "entertainment", "days_ago": 1},
    ]
    for t in transactions:
        db.add(Transaction(
            user_id="usr_12345",
            amount=t["amount"],
            category=t["category"],
            timestamp=now - datetime.timedelta(days=t["days_ago"])
        ))
    db.commit()
    return {"status": "seeded", "user_id": "usr_12345", "message": "Demo user ready!"}
