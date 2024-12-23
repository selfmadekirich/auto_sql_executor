from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Token, UserInDB, UserSingUp
from ..meta_extraction.models import OkResponse
from .utils import (
    authenticate_user,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_user,
    get_password_hash
)
from database import get_session
from datetime import timedelta
from repository.users import save_user


router = APIRouter()


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db=Depends(get_session)
) -> Token:
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": user.scopes},
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post('/signup')
async def create_user(
    data: UserSingUp,
    db: Annotated[AsyncSession, Depends(get_session)]
) -> OkResponse:
    user = await get_user(db, data.username)
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    await save_user(
        db,
        data=UserInDB(
            username=data.username,
            hashed_password=get_password_hash(data.password),
            scopes=data.scopes
        ))
    return OkResponse()
