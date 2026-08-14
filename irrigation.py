from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from dependencies import (
    get_current_user,
    require_roles
)

from models import User

from schemas import (
    IrrigationCreate,
    IrrigationResponse
)

from services.irrigation_service import (
    create_irrigation,
    get_all_irrigation,
    get_irrigation_by_field
)


router = APIRouter(
    tags=["Irrigation"]
)


# ============================================================
# CREATE IRRIGATION
# ============================================================

@router.post(
    "/irrigation",
    response_model=IrrigationResponse,
    status_code=status.HTTP_201_CREATED
)
def create_irrigation_api(

    irrigation_data: IrrigationCreate,

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

    return create_irrigation(
        db=db,
        irrigation_data=irrigation_data
    )


# ============================================================
# GET ALL IRRIGATION
# ============================================================

@router.get(
    "/irrigation",
    response_model=list[IrrigationResponse]
)
def get_irrigation_api(

    db: Session = Depends(
        get_db
    ),

    current_user: User = Depends(
        get_current_user
    )
):

    return get_all_irrigation(
        db=db
    )


# ============================================================
# GET FIELD IRRIGATION HISTORY
# ============================================================

@router.get(
    "/fields/{field_id}/irrigation",
    response_model=list[IrrigationResponse]
)
def get_field_irrigation_api(

    field_id: int,

    db: Session = Depends(
        get_db
    ),

    current_user: User = Depends(
        get_current_user
    )
):

    return get_irrigation_by_field(
        db=db,
        field_id=field_id
    )