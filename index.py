from fastapi import FastAPI
from config import models, database
from routes import (
    exp_routes,
    skills_category_routes,
    user_routes,
    skills_routes,
    project_routes,
)
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

routers = [
    exp_routes.authenticated_router,
    exp_routes.unauthenticated_router,
    
    user_routes.router,
    
    skills_routes.authenticated_router,
    skills_routes.unauthenticated_router,
    
    skills_category_routes.authenticated_router,
    skills_category_routes.unauthenticated_router,
    
    project_routes.authenticated_router,
    project_routes.unauthenticated_router,
]

for router in routers:
    app.include_router(router)

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api")
async def root():
    return {"message": "Hello World"}
