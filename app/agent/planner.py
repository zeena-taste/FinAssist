from app.agent.executor import execute

def decide(decision_json: dict) -> dict:
    """Parse decision and route to executor or just return response."""
    action = decision_json.get("action")
    params = decision_json.get("params", {})
    response_text = decision_json.get("response", "")
    
    result = None
    action_taken = None
    
    if action:
        result = execute(action, params)
        action_taken = action
        
    return {
        "message": response_text,
        "action_taken": action_taken,
        "result": result
    }
