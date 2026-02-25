from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.settings import settings
from app.api.v1.routes import api_router
app = FastAPI(title = settings.app_name,
              description="An API for managing votes,questions,options,users",
              version=settings.app_version)


app.include_router(api_router)



# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

