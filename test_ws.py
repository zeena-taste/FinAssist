import asyncio
import websockets
import json

async def test_chat():
    uri = "ws://localhost:8000/ws/chat/usr_12345"
    print(f"Connecting to {uri}...")
    try:
        async with websockets.connect(uri) as websocket:
            print("---------- Connected to Live Chat ----------")
            msg = "Which bank in Ghana has the lowest loan rate right now? Search online."
            print(f"> Sending: {msg}")
            
            await websocket.send(msg)
            
            # The ai may send multiple packets since it loops through actions before chatting
            for _ in range(4):
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=20.0)
                    data = json.loads(response)
                    
                    print(f"\n< Received {data.get('type', 'UNKNOWN').upper()} Packet:")
                    print(json.dumps(data, indent=2))
                    
                    if data.get("type") == "chat":
                        print("---------- Chat Loop Finished ----------")
                        break
                except asyncio.TimeoutError:
                    print("Timeout waiting for response.")
                    break
                except Exception as e:
                    print(f"Socket error or closed: {e}")
                    break
    except Exception as e:
        print(f"Failed to connect: {e}\n(Make sure uvicorn app.main:app is running!)")

if __name__ == "__main__":
    asyncio.run(test_chat())
