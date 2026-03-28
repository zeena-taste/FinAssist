import datetime
from sqlalchemy.orm import Session
from app.db.database import engine, Base, SessionLocal
from app.models.user import User
from app.models.transaction import Transaction

def seed_data():
    # Make sure we reset perfectly for this to take effect
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Create dummy user
    dummy_user = User(
        id="usr_12345",
        name="Kwame Mensah",
        phone="+233555123456",
        language="English"
    )
    db.add(dummy_user)
    db.commit()

    now = datetime.datetime.utcnow()
    # Create transactions simulating African spending pattern
    transactions = [
        {"amount": 100000, "category": "income", "days_ago": 30},
        {"amount": 100000, "category": "income", "days_ago": 0},
        {"amount": 5000, "category": "airtime", "days_ago": 28},
        {"amount": 8000, "category": "food", "days_ago": 25},
        {"amount": 3000, "category": "transport", "days_ago": 24},
        {"amount": 25000, "category": "momo_transfer", "days_ago": 20},
        {"amount": 15000, "category": "loan_repayment", "days_ago": 15},
        {"amount": 6000, "category": "airtime", "days_ago": 12}, 
        {"amount": 4000, "category": "transport", "days_ago": 10},
        {"amount": 12000, "category": "food", "days_ago": 5},
        {"amount": 8000, "category": "food", "days_ago": 2},
        {"amount": 5000, "category": "entertainment", "days_ago": 1},
    ]

    for t_data in transactions:
        t = Transaction(
            user_id="usr_12345",
            amount=t_data["amount"],
            category=t_data["category"],
            timestamp=now - datetime.timedelta(days=t_data["days_ago"])
        )
        db.add(t)

    db.commit()
    db.close()
    print("Database seeded successfully with 'usr_12345'!")

if __name__ == "__main__":
    seed_data()
