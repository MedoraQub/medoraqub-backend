from fastapi import FastAPI
from app.db.database import engine, Base
from app.db.base import *  # IMPORTANT: ensures all models are registered

# Create FastAPI app FIRST
app = FastAPI(title="MedoraQub API")

# Create database tables (only for development phase)
Base.metadata.create_all(bind=engine)

# Import routers AFTER app is created
from app.modules.auth.router import router as auth_router
from app.modules.users.routes import router as user_router

# Include routers
app.include_router(auth_router)
app.include_router(user_router)


@app.get("/")
def root():
    return {"message": "MedoraQub Backend Running Successfully"}


@app.get("/test-db")
def test_db():
    return {"database": "Connected successfully"}