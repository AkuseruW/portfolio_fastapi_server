from config.models import Skills_to_Project, Images
from dependencies.uploads import upload_image_to_cloudinary


async def upload_project_images(image, project_id):
    file = await upload_image_to_cloudinary(image)
    new_image = Images(
        image=file["secure_url"],
        public_id=file["public_id"],
        project_id=project_id,
    )

    return new_image


def is_skill_already_added(project_id, skill_id, db):
    existing_skill = (
        db.query(Skills_to_Project)
        .filter_by(projects_id=project_id, skills_id=skill_id)
        .first()
    )
    return existing_skill is not None


async def add_skill_to_project(project_id, skill, db):
    if not is_skill_already_added(project_id, skill, db):
        new_skill = Skills_to_Project(
            skills_id=skill,
            projects_id=project_id,
        )
        db.add(new_skill)
        return new_skill
    else:
        return None


async def remove_skill_from_project(project_id, skill, db):
    skill_to_remove = (
        db.query(Skills_to_Project)
        .filter_by(projects_id=project_id, skills_id=skill)
        .first()
    )

    if skill_to_remove:
        db.delete(skill_to_remove)
        db.commit()
