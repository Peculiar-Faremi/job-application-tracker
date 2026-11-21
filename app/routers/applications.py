from typing import List, Optional
from fastapi import APIRouter, Depends, status, Query, HTTPException 
from sqlalchemy.orm import Session
from app import models, schemas, oauth2
from app.database import get_db
from app.services import applications as application_service
from app.oauth2 import get_current_user
from app.schemas import ApplicationResponse, ApplicationCreate, ApplicationStatusUpdate
import json
from app.redis_client import r
from app.rate_limit import limit_requests

router = APIRouter(prefix="/applications", tags=["Applications"])

def clear_user_cache(current_user: models.User = Depends(get_current_user)):
    # Applications changed, so delete this user's saved lists
    for key in r.scan_iter(f"applications:user:{current_user.id}:*"): #Find all keys that start with this string
        r.unlink(key) # then delete this at the background

@router.post("/create", response_model= ApplicationResponse, status_code=status.HTTP_201_CREATED)
def create_application(new_app: ApplicationCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):   
    return application_service.create_application(db, new_app, current_user.id,)

@router.get("/getall", response_model= list[ApplicationResponse], status_code= status.HTTP_200_OK, dependencies=[Depends(limit_requests)])
def get_all_applications(db: Session = Depends(get_db),
                        current_user=Depends(get_current_user),
                        skip:int=Query(0, le=100, ge=0), #default skip is 0, max limit is 100, min limit is 0
                        limit:int=Query(10, le=100, ge=1), #default limit is 10, max limit is 100, min limit is 1
                        search: Optional[str] = Query(None)): #liberty to search for keywords in the application name or description.
    cache_key = f"applications:user:{current_user.id}:skip:{skip}:limit:{limit}:search:{search}"
    cached = r.get(cache_key)
    if cached:
        return json.loads(cached)
    applications = application_service.get_all_applications(
        db, current_user.id, skip=skip, limit=limit, search=search
    )
    data = [ApplicationResponse.model_validate(p).model_dump(mode="json") for p in applications]
    # Save for 60 seconds, then Redis deletes it
    r.set(cache_key, json.dumps(data), ex=60)
    return data

@router.get("/company", response_model=list[schemas.ApplicationResponse], status_code=status.HTTP_200_OK, dependencies=[Depends(limit_requests)])
def get_applications_by_company(company_name: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    cache_key = f"applications:user:{current_user.id}:company:{company_name}"
     
    cached = r.get(cache_key)
    if cached:
        return json.loads(cached)
    applications = application_service.get_by_company_application(db, current_user.id, company_name)
    # Serialized the LIST of applications for Redis 
    data = [
        schemas.ApplicationResponse.model_validate(app).model_dump(mode="json") 
        for app in applications
    ] 
    r.set(cache_key, json.dumps(data), ex=60)
    return data

@router.patch("/{application_id}/status", response_model= ApplicationStatusUpdate, status_code=status.HTTP_200_OK, dependencies=[Depends(clear_user_cache)])
def update_status_application(application_id:int,
                              new_status: ApplicationStatusUpdate,
                              db: Session=Depends(get_db), 
                              current_user: models.User = Depends(get_current_user)
                              ):
    return application_service.update_application(db=db, user_id=current_user.id, application_id=application_id, new_status=new_status.status)

@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    return application_service.delete_application(
        db=db, 
        user_id=current_user.id, 
        application_id=application_id
    )