from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db

from dependencies import get_current_user

from models import User

from schemas import (
    DashboardResponse,
    FarmRevenueResponse,
    CropProductionResponse
)

from services.dashboard_service import (
    get_dashboard,
    get_farm_wise_revenue,
    get_crop_wise_production
)


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard & Reports"]
)


# ============================================================
# MAIN DASHBOARD
# ============================================================

@router.get(
    "",
    response_model=DashboardResponse
)
def dashboard_api(

    db: Session = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    return get_dashboard(
        db=db
    )


# ============================================================
# FARM-WISE REVENUE
# ============================================================

@router.get(
    "/farm-wise-revenue",
    response_model=list[FarmRevenueResponse]
)
def farm_wise_revenue_api(

    db: Session = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    return get_farm_wise_revenue(
        db=db
    )


# ============================================================
# CROP-WISE PRODUCTION
# ============================================================

@router.get(
    "/crop-wise-production",
    response_model=list[CropProductionResponse]
)
def crop_wise_production_api(

    db: Session = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    return get_crop_wise_production(
        db=db
    )