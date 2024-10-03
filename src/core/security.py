from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException
from passlib.context import CryptContext
from src.core.config import settings
from jose import jwt, JWTError
from datetime import datetime, timedelta
from src.db.auth import get_user
from src.schemas.user_schemas import UserInDBSchema


pwd_context = CryptContext(schemes=[settings.ALGORITHM], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# ------------------------------------------------------------Work with JWT

def create_token(data: dict, token_expire_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + token_expire_delta
    to_encode.update({'exp': expire})

    return jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)


def create_access_token(data: dict):
    return create_token(data, timedelta(minutes=settings.TOKEN_EXPIRE_MINUTES))


def create_refresh_token(data: dict):
    return create_token(data, timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))


async def get_current_user(token: str) -> UserInDBSchema:
    credential_exception = HTTPException(
        status_code=401,
        detail='Invalid Credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    try:
        token_details = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        if token_details.get('id') is None:
            raise credential_exception
    except JWTError:
        raise credential_exception

    user = await get_user(token_details.get('user_id'))
    if user is None:
        raise credential_exception

    return user

