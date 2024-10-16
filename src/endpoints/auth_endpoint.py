from fastapi import APIRouter, Depends, HTTPException, Cookie
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from src.core.security import authenticate_user, create_access_token, create_refresh_token, refresh_jwt_token, \
    get_tokens_response
from src.schemas.auth_schema import TokenData, Token


router = APIRouter()


@router.post('/token', response_model=Token)
async def login_for_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail='Incorrect Email or Password')

    return get_tokens_response(user.email, user.role)


@router.get('/refresh', response_model=Token)
async def refresh_access_token(refresh_token: str | None = Cookie(None)):
    if refresh_token is None:
        raise HTTPException(status_code=401, detail='No refresh token')

    access_token = refresh_jwt_token(refresh_token)
    return Token(access_token=access_token, token_type="bearer")


