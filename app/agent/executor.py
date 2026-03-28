from app.tools.sms import send_sms_report
from app.tools.momo import initiate_momo_payment
from app.tools.savings import schedule_savings_transfer
from app.tools.loan import generate_loan_assessment
from app.tools.search import search_internet

def execute(action: str, params: dict) -> dict:
    tools_map = {
        "send_sms_report": send_sms_report,
        "initiate_momo_payment": initiate_momo_payment,
        "schedule_savings_transfer": schedule_savings_transfer,
        "generate_loan_assessment": generate_loan_assessment,
        "search_internet": search_internet
    }
    
    if action in tools_map:
        try:
            return tools_map[action](params)
        except Exception as e:
            return {"status": "error", "message": str(e)}
    else:
        return {"status": "error", "message": f"Unknown action: {action}"}
