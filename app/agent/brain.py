import json
import google.generativeai as genai
from app.config import settings

if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)

MODEL_NAME = "gemini-3.1-pro-preview"

SYSTEM_PROMPT = """You are FinAassist, an AI-powered financial agent for users in Africa.
Your job is to reason about a user's financial context and decide if you should reply conversationally or trigger an action.

You MUST always return a valid JSON object in the following format:
{
  "action": null | "send_sms_report" | "initiate_momo_payment" | "schedule_savings_transfer" | "generate_loan_assessment" | "search_internet",
  "params": {},
  "response": "A conversational message to the user explaining your action or reasoning.",
  "reason": "Internal reasoning for why you decided this."
}

Use the provided user context to make informed decisions.
If asked about current events, best bank deals, or information you do not natively know, use the "search_internet" action with a `query` parameter.
If the user asks to send money, use "initiate_momo_payment" with `amount` and `recipient` params.
If they ask for a loan assessment, use "generate_loan_assessment" passing their `income` and `debt_ratio` computed from context.
If they just ask a simple question, leave "action" as null and provide the answer in "response".
"""

def reason(context: dict, user_input: str) -> dict:
    if not settings.GEMINI_API_KEY:
        print("[BRAIN] No Gemini API key provided natively. Using mock reasoning.")
        return {
            "action": None,
            "params": {},
            "response": "Mocked response natively: Set GEMINI_API_KEY to enable AI.",
            "reason": "Missing API key fallback"
        }

    try:
        model = genai.GenerativeModel(
            MODEL_NAME, 
            system_instruction=SYSTEM_PROMPT,
            generation_config={"response_mime_type": "application/json"}
        )
        
        prompt = f"User Input: {user_input}\nContext: {json.dumps(context)}"
        response = model.generate_content(prompt)
        
        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            return {
                "action": None,
                "params": {},
                "response": "I encountered an error natively generating your request schema. Try again.",
                "reason": "JSON Parsing mapping error natively"
            }
    except Exception as e:
        return {
            "action": None,
            "params": {},
            "response": f"SDK Native deployment failure dynamically: {str(e)}",
            "reason": str(e)
        }
