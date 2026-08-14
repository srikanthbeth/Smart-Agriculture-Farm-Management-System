from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from dependencies import get_current_user, require_roles
from models import User
from schemas import FieldCreate, FieldResponse
from services.field_service import (
    create_field,
    get_fields_by_farm,
)


# ============================================================
# MAIN FIELD ROUTER
# ============================================================

router = APIRouter(
    prefix="/farms",
    tags=["Fields"]
)


# ============================================================
# TEST / SUPPORT FIELD ROUTER
# ============================================================

fields_test_router = APIRouter(
    tags=["Fields"]
)


# ============================================================
# CREATE FIELD
# POST /farms/{farm_id}/fields
# ============================================================

@router.post(
    "/{farm_id}/fields",
    response_model=FieldResponse,
    status_code=status.HTTP_201_CREATED
)
def create_field_api(
    farm_id: int,
    field_data: FieldCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            "Admin",
            "Farm Manager",
            "Farmer"
        )
    )
):
    return create_field(
        db=db,
        farm_id=farm_id,
        field_data=field_data
    )


# ============================================================
# GET FIELDS BY FARM
# GET /farms/{farm_id}/fields
# ============================================================

@router.get(
    "/{farm_id}/fields",
    response_model=list[FieldResponse]
)
def get_fields_api(
    farm_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    return get_fields_by_farm(
        db=db,
        farm_id=farm_id
    )


# ============================================================
# TEST / SUPPORT CREATE FIELD
# POST /fields
#
# This endpoint is kept because some tests/support code may
# create a field by sending farm_id in the request body.
# ============================================================

@fields_test_router.post(
    "/fields",
    response_model=FieldResponse,
    status_code=status.HTTP_201_CREATED
)
def create_field_without_farm_path_api(
    field_data: FieldCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            "Admin",
            "Farm Manager",
            "Farmer"
        )
    )
):
    return create_field(
        db=db,
        farm_id=field_data.farm_id,
        field_data=field_data
    )