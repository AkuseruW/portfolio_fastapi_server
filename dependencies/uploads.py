import imghdr
from fastapi import UploadFile, HTTPException
import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv

load_dotenv()

CLOUD_NAME = os.environ.get("CLOUD_NAME")
API_KEY = os.environ.get("CLOUDINARY_API_KEY")
API_SECRET = os.environ.get("CLOUDINARY_API_SECRET")

cloudinary.config(
    cloud_name=CLOUD_NAME,
    api_key=API_KEY,
    api_secret=API_SECRET,
    secure=True,
)

# Limit the maximum file size to 5MB (adjust as needed)
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024


async def upload_image_to_cloudinary(file: UploadFile):
    # Validate file extension and contents
    image_format = imghdr.what(file.filename, await file.read(1024))
    if image_format not in {"jpeg", "png", "gif", "webp"}:
        raise HTTPException(status_code=400, detail="Format de l'image invalide")

    # Reset file read position after validation
    file.file.seek(0)

    # Check if the file size exceeds the maximum allowed size
    if file.size > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=413, detail="La taille de l'image ne doit pas dépasser 5 Mo."
        )

    response = cloudinary.uploader.upload(file.file, upload_preset="portfolio")
    return response


async def delete_image(public_id):
    cloudinary.uploader.destroy(public_id)
    return
