from app.security import hash_password
from app import models, schemas
from sqlalchemy.orm import Session

def create_user(db: Session, new_user: schemas.CreateUser):
    data = new_user.model_dump() #it converts the model into a dictionary
    data["password"] = hash_password(data["password"])
    user = models.User(**data) #it unpacks the dictionary into a keyword argument
    db.add(user)
    db.commit()
    db.refresh(user)
    return user