from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Admin(Base):
    __tablename__ = "admin"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    about = Column(String)
    age = Column(Integer)
    password = Column(String)


class Skills(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    icones = Column(String)
    category_id = Column(Integer, ForeignKey("skills_category.id"))
    public_id = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    projects = relationship(
        "Projects", secondary="skills_to_projects", back_populates="skills"
    )
    category = relationship("Skills_Category", back_populates="skills")


class Skills_Category(Base):
    __tablename__ = "skills_category"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    skills = relationship("Skills", back_populates="category")


class Projects(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    link = Column(String, nullable=True)
    dateOfCreation = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    images = relationship("Images", back_populates="project")
    skills = relationship(
        "Skills", secondary="skills_to_projects", back_populates="projects"
    )


class Images(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, index=True)
    image = Column(String)
    project_id = Column(Integer, ForeignKey("projects.id"))
    public_id = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    project = relationship("Projects", back_populates="images")


class Skills_to_Project(Base):
    __tablename__ = "skills_to_projects"
    id = Column(Integer, primary_key=True, index=True)
    skills_id = Column(Integer, ForeignKey("skills.id"))
    projects_id = Column(Integer, ForeignKey("projects.id"))


class Experiences(Base):
    __tablename__ = "experiences"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    link = Column(String, nullable=True)
    startTime = Column(Integer, nullable=False)
    endTime = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
