# schemas.py
from pydantic import BaseModel

class Nickname(BaseModel):
    nickname: str
