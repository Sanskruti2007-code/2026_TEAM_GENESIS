from pydantic import BaseModel, Field
from typing import Optional


class CommandRequest(BaseModel):
    text: str = Field(..., description="User's voice command converted to text")
    language: str = Field(default="mr-IN", description="Command language")
    user_id: Optional[str] = None


class CommandResponse(BaseModel):
    success: bool
    message: str
    action: Optional[str] = None
    data: Optional[dict] = None