from pydantic import BaseModel


class UserInfo(BaseModel):
    sub: str
    name: str = ""
    extra: dict = {}
