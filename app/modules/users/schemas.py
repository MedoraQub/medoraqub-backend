from pydantic import BaseModel, EmailStr, ConfigDict


# Used for creating a user (request body)
class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str


# Used for returning user data (response body)
class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    is_active: bool
    role: str

    model_config = ConfigDict(from_attributes=True)