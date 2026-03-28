from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import websockets
import asyncio
import json
from app.config import settings

router = APIRouter()

MODEL_NAME = "models/gemini-3.1-flash-live-preview"

@router.websocket("/proxy/{user_id}")
async def voice_proxy_endpoint(client_ws: WebSocket, user_id: str):
    await client_ws.accept()

    if not settings.GEMINI_API_KEY:
        await client_ws.close(code=1008, reason="API Key Missing for Multimodal Live Audio")
        return

    gemini_uri = f"wss://generativelanguage.googleapis.com/ws/google.ai.generativelanguage.v1alpha.GenerativeService.BidiGenerateContent?key={settings.GEMINI_API_KEY}"
    
    try:
        async with websockets.connect(gemini_uri) as gemini_ws:
            
            init_msg = {
                "setup": {
                    "model": MODEL_NAME,
                    "generationConfig": {
                        "responseModalities": ["AUDIO"]
                    }
                }
            }
            await gemini_ws.send(json.dumps(init_msg))
            
            setup_response = await gemini_ws.recv()
            print(f"[VOICE] Setup mapping complete natively for {user_id}: {setup_response[:50]}...")

            async def forward_to_gemini():
                try:
                    while True:
                        data = await client_ws.receive()
                        if 'bytes' in data:
                            import base64
                            b64_audio = base64.b64encode(data['bytes']).decode("utf-8")
                            realtime_packet = {
                                "clientContent": {
                                    "turns": [
                                        {
                                            "role": "user",
                                            "parts": [{"inlineData": {"mimeType": "audio/pcm;rate=16000", "data": b64_audio}}]
                                        }
                                    ],
                                    "turnComplete": True
                                }
                            }
                            await gemini_ws.send(json.dumps(realtime_packet))
                        elif 'text' in data:
                             await gemini_ws.send(data['text'])
                except WebSocketDisconnect:
                     pass
                except Exception as e:
                     print(f"Error forwarding audio stream to Gemini natively: {e}")

            async def forward_to_client():
                try:
                    while True:
                        gemini_msg = await gemini_ws.recv()
                        await client_ws.send_text(gemini_msg)
                except websockets.exceptions.ConnectionClosed:
                     pass
                except Exception as e:
                     print(f"Error returning audio chunks to client frontend natively: {e}")

            t1 = asyncio.create_task(forward_to_gemini())
            t2 = asyncio.create_task(forward_to_client())
            
            done, pending = await asyncio.wait([t1, t2], return_when=asyncio.FIRST_COMPLETED)
            for task in pending:
                task.cancel()

    except WebSocketDisconnect:
        print(f"Voice client {user_id} disconnected natively.")
    except Exception as e:
        print(f"Voice Proxy Systemic Flow Error: {e}")
        try:
             await client_ws.close()
        except:
             pass
