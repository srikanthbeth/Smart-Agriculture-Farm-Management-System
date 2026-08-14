from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db

from dependencies import (
    get_current_user,
    require_roles
)

from models import User

from schemas import (
    CropHealthCreate,
    CropHealthResponse
)

from services.health_service import (
    create_crop_health,
    get_all_crop_health,
    get_crop_health_history,
    get_critical_alerts
)


router = APIRouter(
    tags=["Crop Health"]
)


# ============================================================
# CREATE HEALTH RECORD
# ============================================================

@router.post(
    "/crop-health",
    response_model=CropHealthResponse,
    status_code=status.HTTP_201_CREATED
)
def create_crop_health_api(

    health_data: CropHealthCreate,

    db: Session = Depends(
        get_db
    ),

    current_user: User = Depends(
        require_roles(
            "Admin",
            "Farm Manager",
            "Farmer",
            "Field Worker"
        )
    )
):

    return create_crop_health(
        db=db,
        health_data=health_data
    )


# ============================================================
# GET ALL HEALTH RECORDS
# ============================================================

@router.get(
    "/crop-health",
    response_model=list[CropHealthResponse]
)
def get_crop_health_api(

    db: Session = Depends(
        get_db
    ),

    current_user: User = Depends(
        get_current_user
    )
):

    return get_all_crop_health(
        db=db
    )


# ============================================================
# GET CROP HEALTH HISTORY
# ============================================================

@router.get(
    "/crops/{crop_id}/health-history",
    response_model=list[CropHealthResponse]
)
def get_crop_health_history_api(

    crop_id: int,

    db: Session = Depends(
        get_db
    ),

    current_user: User = Depends(
        get_current_user
    )
):

    return get_crop_health_history(
        db=db,
        crop_id=crop_id
    )


# ============================================================
# GET CRITICAL ALERTS
# ============================================================

@router.get(
    "/crop-health/alerts"
)
def get_critical_alerts_api(

    db: Session = Depends(
        get_db
    ),

    current_user: User = Depends(
        require_roles(
            "Admin",
            "Farm Manager"
        )
    )
):

    return get_critical_alerts(
        db=db
    )