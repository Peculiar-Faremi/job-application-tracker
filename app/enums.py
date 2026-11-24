from enum import Enum
from sqlalchemy import text

# Enums are dropdown menus sqlalchemy also supports
class ApplicationStatus(str, Enum):
    APPLIED = "Applied"
    INTERVIEWING = "Interviewing"
    OFFER = "Offer"
    REJECTED = "Rejected"
    GHOSTED = "Ghosted"

class ApplicationSource(str, Enum):
    LINKEDIN = "LinkedIn"
    INDEED = "Indeed"
    COMPANY_WEBSITE = "Company Website"
    REFERRAL = "Referral"
    OTHER = "Other"
