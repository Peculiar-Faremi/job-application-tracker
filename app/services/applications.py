from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.enums import ApplicationStatus 

def create_application(db:Session, new_app:schemas.ApplicationCreate, user_id:int):
    data=new_app.model_dump()
    data["user_id"]=user_id
    created_application= models.Applications(**data)
    db.add(created_application)
    db.commit()
    db.refresh(created_application)
    return created_application

def get_all_applications(db: Session, user_id:int, skip: int=0, limit: int=10, search: Optional[str] = None): #using skip and limit for pagination
    query= db.query(models.Applications).filter(models.Applications.user_id == user_id)
    if search:
        query=query.filter(models.Application.job_title.ilike(f"%{search}%") #searching for keywords in the application name or description using ilike for case-insensitive search
                           | models.Applications.company.ilike(f"%{search}%"))
    applications = query.offset(skip).limit(limit).all() #applied pagination using offset and limit in the query
    if not applications:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Applications not found")
    return applications

def get_by_company_application(db: Session, user_id:int, company_name: str):
   query= db.query(models.Applications).filter(
        models.Applications.user_id == user_id,
        models.Applications.company.ilike(f"%{company_name}%")
    ).all()
   return query

def update_application(db: Session, user_id: int, application_id: int, new_status: ApplicationStatus):
    application = db.query(models.Applications).filter(
        models.Applications.id == application_id,
        models.Applications.user_id == user_id
    ).first()
    if not application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    application.status = new_status
    db.commit()
    db.refresh(application)

    return application

def delete_application(db: Session, user_id:int, application_id: int):
    application = db.query(models.Applications).filter(
        models.Applications.id == application_id,
        models.Applications.user_id == user_id
    ).first()

    if not application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    db.delete(application)
    db.commit()
    return {"message": "Application deleted successfully"}