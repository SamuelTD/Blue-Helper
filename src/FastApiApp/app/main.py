from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.v1.endpoints import auth, users, azurehelper
from app.db.session import engine
from sqlmodel import SQLModel
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="multiprocessing.resource_tracker")


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(title="Azure Helper", lifespan=lifespan)

app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(azurehelper.router, prefix="/api/v1", tags=["chatbot"])
