from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class SignInRequest(BaseModel):
    email: str
    password: str


class Image(BaseModel):
    image: str
    id: int


class Create_Experience(BaseModel):
    title: str
    description: str
    startTime: int
    endTime: Optional[int]
    link: Optional[str]


class Experiences(Create_Experience):
    id: int


class Admin_Schema(BaseModel):
    username: str
    email: str
    full_name: str
    about: str
    age: int
    password: str


class Skills(BaseModel):
    id: int
    name: str
    icones: str


class Skills_with_category(Skills):
    category: str


class Skills_CategoryCreate(BaseModel):
    name: str


class Skills_Category(Skills_CategoryCreate):
    id: int
    skills: List[Skills]


class Projects(BaseModel):
    id: int
    name: str
    description: str
    link: str
    dateOfCreation: date
    images: List[Image]
    skills: List[Skills]
