from pydantic import BaseModel, conint, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: conint(gt=0)
    is_subscribed: bool = False