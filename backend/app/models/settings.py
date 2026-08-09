from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, SecretStr


ProviderName = Literal["gemini", "openai"]


class APIKeySaveRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    provider: ProviderName
    api_key: SecretStr = Field(
        min_length=10,
        max_length=500,
        description="User-provided Gemini or OpenAI API key",
    )


class APIProviderRequest(BaseModel):
    provider: ProviderName


class APIKeyStatusResponse(BaseModel):
    gemini: bool = False
    openai: bool = False


class APIKeyActionResponse(BaseModel):
    success: bool
    message: str
    status: APIKeyStatusResponse