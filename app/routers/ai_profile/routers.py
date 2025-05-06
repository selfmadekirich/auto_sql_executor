from fastapi import APIRouter, Depends
from typing import Annotated
from database import get_session
from uuid import UUID
from fastapi.security import OAuth2PasswordBearer
from routers.auth.models import Token
from routers.auth.utils import check_admin_privs
from services.fernet_service import get_fernet
from .models import (
    AIProfileDeleteOutput,
    AIProfileUpdateInput,
    AIProfileInput,
    AIProfileResponse,
    AIProfilesOptionValues,
    AIProfileFullResponse,
    AIProfilePartialResponse,
    SupportedModels,
    SupportedServices
)
from .utils import wrap_values, get_supported_models

from repository.ai_profiles import (
    get_ai_profiles,
    get_all_ai_profiles,
    delete_ai_profiles,
    insert_ai_profiles,
    update_ai_profiles
)

router = APIRouter(prefix="/profiles")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

tags = ["profiles"]


@router.get(
        "/",
        tags=tags)
async def get_profiles(
    option: AIProfilesOptionValues,
    token: Annotated[Token, Depends(oauth2_scheme)],
    db=Depends(get_session)
) -> list[AIProfileFullResponse] | list[AIProfilePartialResponse]:

    if option == AIProfilesOptionValues.all:
        check_admin_privs(token)

    return wrap_values(
       await get_all_ai_profiles(db),
       option
    )


@router.post(
        "/",
        response_model=AIProfileFullResponse,
        tags=tags)
async def save_profile(
    data: AIProfileInput,
    token: Annotated[Token, Depends(oauth2_scheme)],
    db=Depends(get_session),
    crypt_service=Depends(get_fernet)
):
    check_admin_privs(token)
    return await insert_ai_profiles(db, data, crypt_service)


@router.get("/{profile_id}", tags=tags)
async def get_profile(
    profile_id: UUID,
    token: Annotated[Token, Depends(oauth2_scheme)],
    db=Depends(get_session),
    crypt_service=Depends(get_fernet)
):
    check_admin_privs(token)
    return await get_ai_profiles(db, profile_id, crypt_service)


@router.patch("/{profile_id}", tags=tags)
async def update_profile(
    profile_id: UUID,
    data: AIProfileUpdateInput,
    token: Annotated[Token, Depends(oauth2_scheme)],
    db=Depends(get_session),
    crypt_service=Depends(get_fernet)
):
    check_admin_privs(token)
    return await update_ai_profiles(
        db, data, profile_id, crypt_service
    )


@router.delete("/{profile_id}", tags=tags)
async def delete_profile(
    profile_id: UUID,
    token: Annotated[Token, Depends(oauth2_scheme)],
    db=Depends(get_session)
) -> AIProfileDeleteOutput:
    check_admin_privs(token)
    return await delete_ai_profiles(db, profile_id)


@router.get(
        "/references/services",
        tags=tags)
def get_services(
    _: Annotated[Token, Depends(oauth2_scheme)],
) -> list[SupportedServices]:

    return [x.value for x in SupportedServices]


@router.get(
        "/references/services/{service_name}/models",
        tags=tags)
def get_models(
    service_name: str,
    _: Annotated[Token, Depends(oauth2_scheme)],
) -> list[str]:

    return get_supported_models(service_name)
