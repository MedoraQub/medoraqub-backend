from fastapi import FastAPI
from app.db.database import engine
from app.db.base import *  # important: registers models
from app.db.database import Base
from app.modules.users.routes import router as user_router
from app.modules.auth.router import router as auth_router

app.include_router(auth_router)

app = FastAPI(title="MedoraQub API")

Base.metadata.create_all(bind=engine)

app.include_router(user_router)

@app.get("/")
def root():
    return {"message": "MedoraQub Backend Running Successfully"}

@app.get("/test-db")
def test_db():
    return {"database": "Connected successfully"}