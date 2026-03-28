import json
import requests
from app.config import settings

MODEL_NAME = "gemini-3.1-flash-live-preview"

SYSTEM_PROMPT = """You are FinAassist, an AI-powered financial agent for users in Africa.
You are currently in a LIVE CHAT session.

You MUST always return a valid JSON object. 
Depending on your decision, return ONE of the following formats:

1. Chatting with the user naturally:
{
  "type": "chat",
  "message": "Your conversational response here."
}

2. Taking an action:
{
  "type": "action",
  "action": "send_sms_report" | "initiate_momo_payment" | "schedule_savings_transfer" | "generate_loan_assessment" | "search_internet",
  "params": {
      "key": "value"
  },
  "reason": "Internal reasoning for taking this action."
}

Use the provided user context to make informed decisions.
If asked about current events, best bank deals, or information you do not natively know, use the "search_internet" action with a `query` parameter.
*CRITICAL*: When you execute a web search and receive results, you MUST extract the actual numbers and present a clear, comparative numerical breakdown for the user.
"""

def chat_reason(context: dict, chat_history: list) -> dict:
    if not settings.GEMINI_API_KEY:
        return {"type": "chat", "message": "API key missing for Live Chat."}

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={settings.GEMINI_API_KEY}"
    
    prompt = f"Context: {json.dumps(context)}\n\nChat History:\n"
    for msg in chat_history:
        prompt += f"[{msg['role']}]: {msg['content']}\n"
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        "generationConfig": {"responseMimeType": "application/json"}
    }
    
    try:
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        text_response = data["candidates"][0]["content"]["parts"][0]["text"]
        return json.loads(text_response)
        
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        error_msg = e.response.text
        if status_code == 404:
            return {"type": "chat", "message": f"REST API failed: Model format deprecated or unavailable ({MODEL_NAME})."}
        return {"type": "chat", "message": f"API error {status_code}: {error_msg[:100]}"}
    except Exception as e:
        return {"type": "chat", "message": f"Brain failed: {str(e)}"}
