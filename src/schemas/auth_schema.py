from pydantic import BaseModel
from typing import Literal


class TokenData(BaseModel):
    sub: str
    role: Literal['user', 'admin']


class Token(BaseModel):
    access_token: str
    token_type: str
