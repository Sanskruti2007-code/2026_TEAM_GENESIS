from fastapi import APIRouter, HTTPException, status

from app.models.settings import (
    APIKeyActionResponse,
    APIKeySaveRequest,
    APIKeyStatusResponse,
    ProviderName,
)
from app.services.api_key_store import api_key_store


router = APIRouter(
    prefix="/api/settings/ai",
    tags=["AI Settings"],
)


def get_current_status() -> APIKeyStatusResponse:
    return APIKeyStatusResponse(**api_key_store.get_status())


@router.get("", response_model=APIKeyStatusResponse)
async def read_api_key_status():
    """
    Returns only whether keys are configured.
    Actual API keys are never returned.
    """
    return get_current_status()


@router.post("", response_model=APIKeyActionResponse)
async def save_api_key(request: APIKeySaveRequest):
    """
    Saves the selected API key temporarily in backend RAM.
    """
    try:
        api_key_store.set_key(
            provider=request.provider,
            api_key=request.api_key.get_secret_value(),
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error

    provider_name = request.provider.capitalize()

    return APIKeyActionResponse(
        success=True,
        message=f"{provider_name} API key saved for this session.",
        status=get_current_status(),
    )


@router.delete(
    "/{provider}",
    response_model=APIKeyActionResponse,
)
async def delete_api_key(provider: ProviderName):
    """
    Removes the selected API key from backend RAM.
    """
    deleted = api_key_store.delete_key(provider)
    provider_name = provider.capitalize()

    if deleted:
        message = f"{provider_name} API key removed."
    else:
        message = f"{provider_name} API key was not configured."

    return APIKeyActionResponse(
        success=deleted,
        message=message,
        status=get_current_status(),
    )