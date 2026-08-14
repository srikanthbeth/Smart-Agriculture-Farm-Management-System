from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from database import get_db

from typing import Optional
from datetime import date

from dependencies import (
    get_current_user,
    require_roles
)

from models import User

from schemas import (
    HarvestCreate,
    HarvestResponse
)

from services.harvest_service import (
    create_harvest,
    get_all_harvests,
    get_crop_harvest,
    get_harvests_filtered
)


router = APIRouter(
    tags=["Harvest Management"]
)


# ============================================================
# CREATE HARVEST
# ============================================================

@router.post(
    "/harvests",
    response_model=HarvestResponse,
    status_code=status.HTTP_201_CREATED
)
def create_harvest_api(

    harvest_data: HarvestCreate,

    db: Session = Depends(
        get_db
    ),

    current_user: User = Depends(
        require_roles(
            "Admin",
            "Farm Manager",
            "Farmer"
        )
    )
):

    return create_harvest(
        db=db,
        harvest_data=harvest_data
    )


# ============================================================
# GET ALL HARVESTS
# ============================================================

@router.get(
    "/harvests",
    response_model=list[HarvestResponse]
)
def get_harvests_api(

    db: Session = Depends(
        get_db
    ),

    current_user: User = Depends(
        get_current_user
    )
):

    return get_all_harvests(
        db=db
    )


# ============================================================
# SEARCH / FILTER / PAGINATION
# ============================================================

# ============================================================
# SEARCH / FILTER HARVESTS
# ============================================================

@router.get(
    "/harvests/search"
)
def search_harvests_api(

    quality_grade: Optional[str] = None,

    harvest_date: Optional[date] = None,

    page: int = 1,

    limit: int = 10,

    sort_by: str = "id",

    sort_order: str = "desc",

    db: Session = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    # --------------------------------------------------------
    # VALIDATE PAGE
    # --------------------------------------------------------

    if page < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="page must be greater than 0"
        )

    # --------------------------------------------------------
    # VALIDATE LIMIT
    # --------------------------------------------------------

    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="limit must be between 1 and 100"
        )

    # --------------------------------------------------------
    # VALIDATE SORT ORDER
    # --------------------------------------------------------

    if sort_order.lower() not in {"asc", "desc"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="sort_order must be either 'asc' or 'desc'"
        )

    # --------------------------------------------------------
    # VALIDATE SORT FIELD
    # --------------------------------------------------------

    allowed_sort_fields = {
        "id",
        "harvest_date",
        "quantity",
        "quality_grade",
        "market_price",
        "total_revenue"
    }

    if sort_by not in allowed_sort_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Invalid sort_by. "
                f"Allowed: {', '.join(sorted(allowed_sort_fields))}"
            )
        )

    # --------------------------------------------------------
    # CALL SERVICE
    # --------------------------------------------------------

    return get_harvests_filtered(
        db=db,
        quality_grade=quality_grade,
        harvest_date=harvest_date,
        page=page,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order
    )


# ============================================================
# GET HARVESTS FOR CROP
# ============================================================

@router.get(
    "/crops/{crop_id}/harvest",
    response_model=list[HarvestResponse]
)
def get_crop_harvest_api(

    crop_id: int,

    db: Session = Depends(
        get_db
    ),

    current_user: User = Depends(
        get_current_user
    )
):

    return get_crop_harvest(
        db=db,
        crop_id=crop_id
    )