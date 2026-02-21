from fastapi import FastAPI
from app.db.database import engine, Base
from app.db import base  # This ensures models are registered

app = FastAPI(title="MedoraQub API")

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "MedoraQub Backend Running Successfully"}

@app.get("/test-db")
def test_db():
    return {"database": "Connected successfully"}