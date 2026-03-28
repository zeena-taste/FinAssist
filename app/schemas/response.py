from pydantic import BaseModel
from typing import Optional, Any

class AgentQueryResponseData(BaseModel):
    message: str
    action_taken: Optional[str] = None
    result: Optional[Any] = None
    financial_score: Optional[float] = None

class AgentQueryResponse(BaseModel):
    status: str
    data: AgentQueryResponseData
