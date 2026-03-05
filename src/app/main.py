# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from app.core.settings import settings
# from app.api.v1.routes import api_router


# app = FastAPI(title = settings.app_name,
#               description="An API for managing votes,questions,options,users",
#               version=settings.app_version)


# app.include_router(api_router)



# # Configure CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

app = FastAPI()

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@app.post("/login")
async def login(data: LoginRequest):
    # TEMP: hardcoded check (replace with DB later)
    if data.email == "test@example.com" and data.password == "password123":
        return {"message": "Login success", "user": {"email": data.email}}
    raise HTTPException(status_code=401, detail="Invalid email or password")

