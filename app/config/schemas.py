from pydantic import BaseModel
from datetime import datetime


class ChatRequest(BaseModel):
    """schema for request body of '/chat' route"""

    query: str
    document_id: str


class ChatResponse(BaseModel):
    """schema for '/chat' route response model"""

    response: str


class LogsRequest(BaseModel):
    """schema for request body of '/logs' route"""

    document_id: str | None = None


class LogResponse(BaseModel):
    """schema for '/logs' route response model"""

    query: str
    context: list
    response: str
    document_id: str
    request_time: datetime
    response_time: datetime
    duration: float
