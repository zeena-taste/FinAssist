from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as agent_router
from app.api.ws_routes import router as ws_router
from app.api.vision_routes import router as vision_router
from app.api.voice_routes import router as voice_router
from app.db.database import engine, Base

# Create tables if not exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FinAassist API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agent_router, prefix="/agent", tags=["Agent"])
app.include_router(ws_router, prefix="/ws/chat", tags=["Websocket Chat"])
app.include_router(vision_router, prefix="/vision", tags=["Multimodal Vision"])
app.include_router(voice_router, prefix="/ws/voice", tags=["Websocket Audio Proxy"])

@app.get("/")
def read_root():
    return {"message": "Welcome to FinAassist API"}
