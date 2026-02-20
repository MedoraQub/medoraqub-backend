from fastapi import FastAPI
from app.db.database import engine
from sqlalchemy import text

app = FastAPI(title="MedoraQub API")

@app.get("/")
def root():
    return {"message": "MedoraQub Backend Running Successfully"}

@app.get("/test-db")
def test_db():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"database": "Connected successfully"}
    except Exception as e:
        return {"error": str(e)}