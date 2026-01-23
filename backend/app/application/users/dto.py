from pydantic import BaseModel, EmailStr

class UserRegisterIn(BaseModel):
    email: EmailStr
    password: str

class UserLoginIn(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserRegisterOut(BaseModel):
    id: int
    email: EmailStr