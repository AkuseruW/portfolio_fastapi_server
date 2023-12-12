from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from config.database import get_db
from config.models import Experiences
import config.schemas as schemas
from dependencies.users_dependencies import get_current_user


authenticated_router = APIRouter(prefix="/api/experiences", tags=["experiences"], dependencies=[Depends(get_current_user)])
unauthenticated_router = APIRouter(prefix="/api/experiences", tags=["experiences"])


@unauthenticated_router.get("/", status_code=200, response_model=list[schemas.Experiences])
async def get_experiences(db: Session = Depends(get_db)):
    return db.query(Experiences).order_by(Experiences.startTime).all()


@unauthenticated_router.get("/{id}")
async def get_experience(id: int, db: Session = Depends(get_db)):
    experience = db.get(Experiences, id)

    if not experience:
        raise HTTPException(status_code=404, detail="Experience not found")

    return experience


@authenticated_router.post("/", status_code=201, response_model=schemas.Create_Experience)
async def create_experience(
    request: schemas.Create_Experience, db: Session = Depends(get_db)
):
    experience = Experiences(
        title=request.title,
        description=request.description,
        startTime=request.startTime,
        endTime=request.endTime,
        link=request.link,
    )

    db.add(experience)
    db.commit()
    return experience


@authenticated_router.patch("/{id}", status_code=200, response_model=schemas.Create_Experience)
async def update_experience(
    id: int, request: schemas.Create_Experience, db: Session = Depends(get_db)
):
    experience = db.get(Experiences, id)

    if not experience:
        raise HTTPException(status_code=404, detail="Experience not found")

    experience.title = request.title
    experience.description = request.description
    experience.startTime = request.startTime
    experience.endTime = request.endTime
    experience.link = request.link
    db.commit()
    db.refresh(experience)

    return experience


@authenticated_router.delete("/{id}", status_code=200)
async def delete_experience(id: int, db: Session = Depends(get_db)):
    experience = db.get(Experiences, id)

    if not experience:
        raise HTTPException(status_code=404, detail="Experience not found")

    db.delete(experience)
    db.commit()

    return {"message": "Experience deleted successfully"}
