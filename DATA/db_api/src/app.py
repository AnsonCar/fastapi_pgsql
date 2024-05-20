# DataBase API
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scalar_fastapi import get_scalar_api_reference

from utils.orm import create_db_and_tables
from setting import APP_NAME

app = FastAPI(title=APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# Test The API Working
@app.get("/", tags=["Root"])
async def index():
    return {"message": f"Welcome to {APP_NAME}!"}


@app.get("/scalar", tags=["Root"])
#  include_in_schema=False
async def scalar_html():
    return get_scalar_api_reference(
        title=APP_NAME,
        openapi_url=app.openapi_url,
    )


# User
from src.user.routes import router as UserRoutes

app.include_router(UserRoutes, tags=["User"], prefix="/api/v1/user")

# Login
from src.auth.routes import router as AuthRoutes

app.include_router(AuthRoutes, tags=["Auth"], prefix="/api/v1/auth")
