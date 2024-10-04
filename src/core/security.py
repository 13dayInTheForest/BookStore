from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends

from passlib.context import CryptContext
from src.core.config import settings
from jose import jwt, JWTError
from datetime import datetime, timedelta
from src.db.auth import get_user
from src.schemas.user_schemas import UserInDBSchema, UserSchema
from src.schemas.auth_schema import TokenData


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# ------------------------------------------------------------Work with JWT

def create_token(data: TokenData, token_expire_delta: timedelta) -> str:
    to_encode = data.dict()
    expire = datetime.utcnow() + token_expire_delta
    to_encode.update({'exp': expire})

    return jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)


def create_access_token(data: TokenData):
    return create_token(data, timedelta(minutes=settings.TOKEN_EXPIRE_MINUTES))


def create_refresh_token(data: TokenData):
    return create_token(data, timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))


async def authenticate_user(email: str, password: str) -> UserInDBSchema | bool:
    user = await get_user(email)
    if user is None or not verify_password(password, user.password):
        return False
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserSchema:
    credential_exception = HTTPException(
        status_code=401,
        detail='Invalid Credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    try:
        token_details = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        if token_details.get('sub') is None:
            raise credential_exception
    except JWTError:
        raise credential_exception

    user = await get_user(token_details.get('sub'))
    if user is None:
        raise credential_exception

    return user


def refresh_jwt_token(token):
    try:
        refresh_detail = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)

        if not refresh_detail.get('sub') and not refresh_detail.get('role'):
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        return create_access_token(TokenData(sub=refresh_detail.get('sub'), role='user'))

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")











