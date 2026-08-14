from fastapi import FastAPI

from database import Base, engine
import models

from exceptions import register_exception_handlers


# ============================================================
# Import Routers
# ============================================================

from routers.auth import router as auth_router
from routers.farms import router as farms_router

from routers.fields import (
    router as fields_router,
    fields_test_router
)

from routers.crops import router as crops_router
from routers.irrigation import router as irrigation_router
from routers.treatments import router as treatments_router
from routers.health import router as health_router
from routers.harvest import router as harvest_router
from routers.sales import router as sales_router
from routers.dashboard import router as dashboard_router


# ============================================================
# Create Database Tables
# ============================================================

Base.metadata.create_all(bind=engine)


# ============================================================
# FastAPI Application
# ============================================================

app = FastAPI(
    title="Smart Agriculture & Farm Management System",
    description=(
        "A Smart Agriculture & Farm Management System "
        "built with FastAPI, SQLAlchemy, PostgreSQL, "
        "JWT Authentication and Role-Based Authorization."
    ),
    version="1.0.0"
)


# ============================================================
# Global Exception Handlers
# ============================================================

register_exception_handlers(app)


# ============================================================
# Include Routers
# ============================================================

app.include_router(auth_router)
app.include_router(farms_router)

# Existing field routes
app.include_router(fields_router)

# Test/support field route
# POST /fields
app.include_router(fields_test_router)

app.include_router(crops_router)
app.include_router(irrigation_router)
app.include_router(treatments_router)
app.include_router(health_router)
app.include_router(harvest_router)
app.include_router(sales_router)
app.include_router(dashboard_router)


# ============================================================
# Debug: Registered Routes
# ============================================================
print("\nREGISTERED ROUTES:")
for route in app.routes:
    if hasattr(route, "path"):
        print(route.path, getattr(route, "methods", None))


# ============================================================
# Root Endpoint
# ============================================================

@app.get("/")
def root():
    return {
        "message": "Smart Agriculture & Farm Management System API",
        "version": "1.0.0",
        "docs": "/docs"
    }