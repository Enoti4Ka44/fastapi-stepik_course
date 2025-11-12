from pydantic import BaseModel
from typing import Optional

class Movietop(BaseModel):
    id: Optional[int] = None
    name: str
    cost: int
    director: str

class UserData(BaseModel):
    username: str
    password: str