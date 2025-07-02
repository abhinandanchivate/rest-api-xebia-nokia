
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime

class UserCreateReq(BaseModel):# Request schema for creating a user
    name:str
    email: EmailStr
    age: Optional[int] =None
    is_active: Optional[bool] = Field(default=True, description="Indicates if the user is active")
    role_id: Optional[int] = Field(default=None, description="ID of the role assigned to the user")

    @field_validator('age')
    def check_age(cls, v):
        if v is not None and (v < 0 or v > 120):
            # Instead of raising ValueError, return a clear validation error message
            raise ValueError('Age must be between 0 and 120')
        return v
class UserResponseSchema(BaseModel): 
    id: int
    name: str
    email: EmailStr
    age: Optional[int] = None
    is_active: bool = Field(default=True, description="Indicates if the user is active")
    role_id: Optional[int] = Field(default=None, description="ID of the role assigned to the user")
    created_at: datetime
    updated_at: datetime
    class Config:
        #from_attributes = True  # This allows Pydantic to read attributes from SQLAlchemy models
        orm_mode = True  # This allows Pydantic to work with SQLAlchemy models directly
