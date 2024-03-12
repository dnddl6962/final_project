from pydantic import BaseModel

class NicknameCreate(BaseModel):
    nickname: str