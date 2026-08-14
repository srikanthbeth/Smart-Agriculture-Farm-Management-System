from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from typing import Optional

from database import get_db
from dependencies import get_current_user, require_roles
from models import User
from schemas import FarmCreate, FarmResponse, FarmUpdate
from services.farm_service import (
    create_farm,
    get_all_farms,
    get_farm_by_id,
    update_farm,
)

from services.farm_service import (
    get_farms_filtered
)

router = APIRouter(
    prefix="/farms",
    tags=["Farms"]
)


# ============================================================
# CREATE FARM
# ============================================================

@router.post(
    "",
    response_model=FarmResponse,
    status_code=status.HTTP_201_CREATED
)
def create_farm_api(
    farm_data: FarmCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            "Admin",
            "Farm Manager",
            "Farmer"
        )
    )
):
    return create_farm(
        db=db,
        farm_data=farm_data,
        user_id=current_user.id
    )


# ============================================================
# GET ALL FARMS
# ============================================================

@router.get(
    "",
    response_model=list[FarmResponse]
)
def get_farms_api(
    page: int = Query(
        default=1,
        ge=1
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100
    ),
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):
    return get_all_farms(
        db=db,
        page=page,
        limit=limit
    )



@router.get("/search")

def search_farms_api(

    location: Optional[str] = None,

    status: Optional[str] = None,

    page: int = 1,

    limit: int = 10,

    sort_by: str = "id",

    sort_order: str = "desc",

    db: Session = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    return get_farms_filtered(
        db=db,
        location=location,
        status=status,
        page=page,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order
    )


# ============================================================
# GET FARM BY ID
# ============================================================

@router.get(
    "/{farm_id}",
    response_model=FarmResponse
)
def get_farm_api(
    farm_id: int,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):
    return get_farm_by_id(
        db=db,
        farm_id=farm_id
    )


# ============================================================
# UPDATE FARM
# ============================================================

@router.put(
    "/{farm_id}",
    response_model=FarmResponse
)
def update_farm_api(
    farm_id: int,
    farm_data: FarmUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            "Admin",
            "Farm Manager"
        )
    )
):
    return update_farm(
        db=db,
        farm_id=farm_id,
        farm_data=farm_data
    )