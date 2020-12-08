from pydantic import BaseModel, Field, constr
from typing import List, Optional
from datetime import datetime


class Employment(BaseModel):
    id: Optional[str]
    account: Optional[str]
    employer: Optional[str]
    status: Optional[str]
    type: Optional[str]
    job_title: Optional[str]
    platform_user_id: Optional[str]
    hire_datetime: Optional[str]
    termination_datetime: Optional[str]
    termination_reason: Optional[str]


class OtherExperiences(BaseModel):
    title: str
    description: str


class Education(BaseModel):
    school: str
    degree: str
    area: str
    attended_date: str


class Language(BaseModel):
    name: str
    level: str


class Profile(BaseModel):
    id: Optional[str]
    account: Optional[constr(strip_whitespace=True)]
    employer: Optional[str]
    full_name: str
    first_name: str
    last_name: str
    email: Optional[str]
    phone_number: Optional[str]
    birth_date: Optional[str]
    picture_url: Optional[str]
    address_line1: Optional[str]
    address_line2: Optional[str]
    address_state: Optional[str]
    address_postal_code: Optional[str]
    address_country: str
    address_city: str
    ssn: Optional[str]
    marital_status: Optional[str]
    gender: Optional[str]
    employments: Optional[List[Employment]]
    languages: Optional[List[Language]]
    others: Optional[List[OtherExperiences]]
    skills: Optional[List[str]]
    price: str
    title: str
    status: str
    avaibility: str
    description: str
    timezone: Optional[str]
    updated: Optional[str]
