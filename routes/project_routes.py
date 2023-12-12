from typing import List
from sqlalchemy.orm import Session
from config.database import get_db
from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile, File
import config.schemas as schemas
from config.models import Projects
from dependencies.projects_dependencies import (
    add_skill_to_project,
    remove_skill_from_project,
    upload_project_images,
)
from dependencies.uploads import delete_image
from dependencies.users_dependencies import get_current_user

router = APIRouter(prefix="/api/projects", tags=["projects"])
authenticated_router = APIRouter(prefix="/api/projects", tags=["projects"], dependencies=[Depends(get_current_user)])
unauthenticated_router = APIRouter(prefix="/api/projects", tags=["projects"])


@unauthenticated_router.get("/", status_code=200, response_model=list[schemas.Projects])
async def get_projects(db: Session = Depends(get_db)):
    projects = db.query(Projects).all()
    projects_with_images = [
        schemas.Projects(
            id=project.id,
            link=project.link,
            created_at=project.created_at,
            description=project.description,
            name=project.name,
            dateOfCreation=project.dateOfCreation,
            updated_at=project.updated_at,
            images=[
                schemas.Image(
                    id=image.id,
                    image=image.image,
                )
                for image in project.images
            ],
            skills=[
                schemas.Skills(
                    id=skill.id,
                    name=skill.name,
                    icones=skill.icones,
                )
                for skill in project.skills
            ]
        )
        for project in projects
    ]
    
    return projects_with_images


@unauthenticated_router.get("/{id}")
async def get_project(id: int, db: Session = Depends(get_db)):
    project = db.get(Projects, id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    project_with_images = project.__dict__ | {"images": project.images}
    project_with_skills = project_with_images | {"skills": project.skills}

    return project_with_skills


@authenticated_router.post("/", status_code=201, response_model=None)
async def create_project(
    name: str = Form(...),
    description: str = Form(...),
    link: str = Form(...),
    dateOfCreation: str = Form(...),
    skills: str = Form(...),
    images: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
):
    if (
        not skills
        or not name
        or not description
        or not link
        or not dateOfCreation
        or not images
    ):
        raise HTTPException(status_code=400, detail="Missing required field")

    project = Projects(
        name=name, description=description, link=link, dateOfCreation=dateOfCreation
    )

    for image in images:
        new_image = await upload_project_images(image, project_id=project.id)
        project.images.append(new_image)

    db.add(project)

    for skill in skills:
        await add_skill_to_project(project_id=project.id, skill=skill, db=db)

    db.commit()

    return project


@authenticated_router.patch("/{id}")
async def update_project(
    id: int,
    name: str = Form(...),
    description: str = Form(...),
    link: str = Form(...),
    dateOfCreation: str = Form(...),
    skills: List[int] = Form(...),
    images: List[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    project = db.get(Projects, id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if images:
        for image in images:
            new_image = await upload_project_images(image, project_id=project.id)
            project.images.append(new_image)

    project.name = name
    project.description = description
    project.link = link
    project.dateOfCreation = dateOfCreation

    existing_skill_ids = [skill.id for skill in project.skills]
    skills_to_remove = set(existing_skill_ids) - set(skills)

    for skill_id_to_remove in skills_to_remove:
        await remove_skill_from_project(
            project_id=project.id, skill=skill_id_to_remove, db=db
        )

    for skill in skills:
        await add_skill_to_project(project_id=project.id, skill=skill, db=db)

    db.commit()
    db.refresh(project)

    return project


@authenticated_router.delete("/{id}", status_code=200)
async def delete_project(id: int, db: Session = Depends(get_db)):
    project = db.get(Projects, id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    for image in project.images:
        await delete_image(image.public_id)

    db.delete(project)
    db.commit()

    return {"message": "Project deleted successfully"}