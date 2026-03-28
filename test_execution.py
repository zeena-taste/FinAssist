import sys
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.schemas.request import AgentQueryRequest
from app.api.routes import agent_query

def main():
    db = SessionLocal()
    req = AgentQueryRequest(
        user_id="usr_12345",
        message= input("Enter your query: ")
    )
    print("------------------------------------------")
    print("Sending query to agent...")
    print(f"Message: {req.message}")
    print("------------------------------------------")
    
    try:
        res = agent_query(req, db)
        print("Response Status:", res.status)
        print("Agent Message:", res.data.message)
        print("Action Taken:", res.data.action_taken)
        print("Result Details:", res.data.result)
        print("Financial Score:", res.data.financial_score)
    except Exception as e:
        print("Error during query:", str(e))
    finally:
        db.close()

if __name__ == "__main__":
    main()
