from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime
from app.enums import ApplicationStatus, ApplicationSource

class CreateUser(BaseModel):
    email:EmailStr #creating an email with the correct validator for email imported from pydantic
    password:str

    @field_validator("password")
    @classmethod
    def strong_password(cls, v: str):
        # You must check the length of the variable (v), not compare 6 to 12
        if not 6 <= len(v) <= 12:
            raise ValueError("Password must contain 6 to 12 characters")
        return v
     
class UserLogin(BaseModel): #logging in user schema
     email:EmailStr
     password:str

class UserResponse(BaseModel): #response shown when user creates or logs in.
    id:int
    email:EmailStr
    created_at:datetime

    model_config = {"from_attributes": True} #it enables readability of object from sqlalchemy database models
    
class ApplicationCreate(BaseModel):
    job_title: str
    job_link: str | None = None
    source: ApplicationSource | None = None 
    status: ApplicationStatus = ApplicationStatus.APPLIED
    company: str
    custom_source: str | None = None

    @field_validator("company")
    @classmethod
    def validate_and_clean_company(cls, v: str): 
        if not v or not v.strip():
            raise ValueError("Company name cannot be empty")
        return v.strip().title()

class ApplicationResponse(BaseModel):
    id: int 
    job_title: str
    status: ApplicationStatus
    company: str
    created_at: datetime
    status_updated: datetime | None
    model_config = {"from_attributes": True}

class ApplicationStatusUpdate(BaseModel):
    status: ApplicationStatus
    
class TokenData(BaseModel):
     id:int

class RefreshRequest(BaseModel):
    refresh_token:str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str