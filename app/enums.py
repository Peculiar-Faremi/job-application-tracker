import enum
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, TIMESTAMP, text

# Enums are dropdown menus sqlalchemy also supoorts
class ApplicationStatus(str, enum.Enum):
    APPLIED = "Applied"
    INTERVIEWING = "Interviewing"
    OFFER = "Offer"
    REJECTED = "Rejected"
    GHOSTED = "Ghosted"

class ApplicationSource(str, enum.Enum):
    LINKEDIN = "LinkedIn"
    INDEED = "Indeed"
    COMPANY_WEBSITE = "Company Website"
    REFERRAL = "Referral"
    OTHER = "Other"