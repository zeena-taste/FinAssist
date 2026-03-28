from pydantic import BaseModel
from typing import Optional, Dict, Any

class AgentQueryRequest(BaseModel):
    user_id: str
    message: str
    metadata: Optional[Dict[str, Any]] = None
