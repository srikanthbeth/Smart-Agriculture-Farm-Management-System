from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from dependencies import get_current_user, require_roles
from models import User
from schemas import CropCreate, CropResponse, CropUpdate

from services.crop_service import (
    create_crop,
    get_all_crops,
    get_crop_by_id,
    update_crop,
    get_crops_filtered,
)


router = APIRouter(
    prefix="/crops",
    tags=["Crops"]
)


# ============================================================
# CREATE CROP
# ============================================================

@router.post(
    "",
    response_model=CropResponse,
    status_code=status.HTTP_201_CREATED
)
def create_crop_api(
    crop_data: CropCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            "Admin",
            "Farm Manager",
            "Farmer"
        )
    )
):
    return create_crop(
        db=db,
        crop_data=crop_data
    )


# ============================================================
# SEARCH / FILTER / PAGINATION
# IMPORTANT: THIS MUST COME BEFORE /{crop_id}
# ============================================================

@router.get(
    "/search"
)
def search_crops_api(
    crop_name: Optional[str] = Query(
        default=None
    ),
    status: Optional[str] = Query(
        default=None
    ),
    start_date: Optional[date] = Query(
        default=None
    ),
    end_date: Optional[date] = Query(
        default=None
    ),
    page: int = Query(
        default=1
    ),
    limit: int = Query(
        default=10
    ),
    sort_by: str = Query(
        default="id"
    ),
    sort_order: str = Query(
        default="desc"
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    # --------------------------------------------------------
    # Date validation
    # --------------------------------------------------------

    if (
        start_date
        and end_date
        and start_date > end_date
    ):
        raise HTTPException(
            status_code=400,
            detail="start_date cannot be after end_date"
        )

    # --------------------------------------------------------
    # Pagination validation
    # --------------------------------------------------------

    if page < 1:
        raise HTTPException(
            status_code=400,
            detail="page must be greater than 0"
        )

    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=400,
            detail="limit must be between 1 and 100"
        )

    # --------------------------------------------------------
    # Sort validation
    # --------------------------------------------------------

    if sort_order.lower() not in {
        "asc",
        "desc"
    }:
        raise HTTPException(
            status_code=400,
            detail="sort_order must be asc or desc"
        )

    return get_crops_filtered(
        db=db,
        crop_name=crop_name,
        status=status,
        start_date=start_date,
        end_date=end_date,
        page=page,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order
    )


# ============================================================
# GET CROPS
# ============================================================

@router.get(
    "",
    response_model=list[CropResponse]
)
def get_crops_api(
    crop_name: Optional[str] = Query(
        default=None
    ),
    crop_status: Optional[str] = Query(
        default=None
    ),
    from_date: Optional[date] = Query(
        default=None
    ),
    to_date: Optional[date] = Query(
        default=None
    ),
    page: int = Query(
        default=1,
        ge=1
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100
    ),
    sort_by: str = Query(
        default="id"
    ),
    sort_order: str = Query(
        default="desc"
    ),
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    # --------------------------------------------------------
    # Sort order validation
    # --------------------------------------------------------

    if sort_order.lower() not in {
        "asc",
        "desc"
    }:
        raise HTTPException(
            status_code=400,
            detail="sort_order must be 'asc' or 'desc'"
        )

    # --------------------------------------------------------
    # Date validation
    # --------------------------------------------------------

    if (
        from_date
        and to_date
        and from_date > to_date
    ):
        raise HTTPException(
            status_code=400,
            detail="from_date cannot be after to_date"
        )

    return get_all_crops(
        db=db,
        crop_name=crop_name,
        crop_status=crop_status,
        from_date=from_date,
        to_date=to_date,
        page=page,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order
    )


# ============================================================
# GET CROP BY ID
# IMPORTANT: KEEP THIS AFTER /search
# ============================================================

@router.get(
    "/{crop_id}",
    response_model=CropResponse
)
def get_crop_api(
    crop_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    return get_crop_by_id(
        db=db,
        crop_id=crop_id
    )


# ============================================================
# UPDATE CROP
# ============================================================

@router.put(
    "/{crop_id}",
    response_model=CropResponse
)
def update_crop_api(
    crop_id: int,
    crop_data: CropUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            "Admin",
            "Farm Manager",
            "Farmer"
        )
    )
):
    return update_crop(
        db=db,
        crop_id=crop_id,
        crop_data=crop_data
    )