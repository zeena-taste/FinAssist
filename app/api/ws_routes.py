from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.db.database import SessionLocal
from app.services.context_builder import build_context
from app.agent.live_brain import chat_reason
from app.agent.executor import execute
import json

router = APIRouter()

@router.websocket("/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    
    db = SessionLocal()
    context = build_context(db, user_id)
    chat_history = []
    
    try:
        while True:
            user_input = await websocket.receive_text()
            chat_history.append({"role": "User", "content": user_input})
            
            decision = chat_reason(context, chat_history)
            
            if decision.get("type") == "action":
                action_name = decision.get("action")
                params = decision.get("params", {})
                
                await websocket.send_json({
                    "type": "action_started", 
                    "action": action_name,
                    "params": params
                })
                
                result = execute(action_name, params)
                
                chat_history.append({
                    "role": "System", 
                    "content": f"[Action '{action_name}' Executed. Result Data: {json.dumps(result)}]"
                })
                
                if action_name == "search_internet" and result.get("status") == "success":
                    summary_decision = chat_reason(context, chat_history)
                    if summary_decision.get("type") == "chat":
                         chat_history.append({"role": "FinAassist", "content": summary_decision["message"]})
                         await websocket.send_json(summary_decision)
                    else:
                         await websocket.send_json(summary_decision)
                else: 
                     await websocket.send_json({
                         "type": "action_completed",
                         "action": action_name,
                         "result": result
                     })
                     
            elif decision.get("type") == "chat":
                chat_history.append({"role": "FinAassist", "content": decision["message"]})
                await websocket.send_json(decision)
            else:
                await websocket.send_json({"type": "error", "message": "Unrecognized JSON format from Brain."})
                
    except WebSocketDisconnect:
        print(f"Client {user_id} disconnected")
    except Exception as e:
        await websocket.send_json({"type": "error", "message": str(e)})
    finally:
        db.close()
