from app.database import Base
from sqlalchemy import TIMESTAMP, func, Column, Integer, String, text, ForeignKey
from sqlalchemy.orm import relationship
from app.enums import Enum, ApplicationSource, ApplicationStatus


class Applications(Base):
    __tablename__ = "Applications"
    user_id= Column (Integer, ForeignKey("users.id", ondelete= "CASCADE"), nullable=False)  
    id = Column(Integer, primary_key=True, nullable=False)
    job_title = Column(String, nullable=False, unique=False)
    status_updated = Column(TIMESTAMP(timezone=True), onupdate=func.now())
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    job_link= Column(String, nullable=True, unique=True)
    source= Column(Enum(ApplicationSource), nullable=True)
    status = Column(Enum(ApplicationStatus), nullable=False, default=ApplicationStatus.APPLIED)
    custom_source= Column(String, nullable=True)
    company= Column(String, nullable=False)
    owner= relationship("User")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    applications = relationship("Applications", back_populates="owner")
    