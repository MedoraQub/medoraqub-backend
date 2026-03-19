from fastapi import FastAPI
from app.db.database import engine
from app.db.base import Base

# Register ALL models before creating tables
from app.db import models

# =========================
# Create FastAPI App
# =========================

app = FastAPI(
    title="MedoraQub API",
    version="1.0.0"
)

# =========================
# Create Tables (Development Phase Only)
# =========================

Base.metadata.create_all(bind=engine)

# =========================
# Import Routers (Only Existing Ones)
# =========================

from app.modules.auth.router import router as auth_router
from app.modules.users.routes import router as user_router
from app.modules.cart.router import router as cart_router
from app.modules.pharmacy.router import router as pharmacy_router
from app.modules.medicines.router import router as medicines_router
from app.modules.inventory.router import router as inventory_router

# =========================
# Include Routers
# =========================

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(cart_router)
app.include_router(pharmacy_router)
app.include_router(medicines_router)
app.include_router(inventory_router)




# =========================
# Health & Root Endpoints
# =========================

@app.get("/", tags=["Health"])
def root():
    return {"message": "MedoraQub Backend Running Successfully"}

@app.get("/test-db", tags=["Health"])
def test_db():
    return {"database": "Connected successfully"}