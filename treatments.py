from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db

from dependencies import (
    get_current_user,
    require_roles
)

from models import User

from schemas import (
    CropTreatmentCreate,
    CropTreatmentResponse
)

from services.treatment_service import (
    create_crop_treatment,
    get_all_crop_treatments,
    get_crop_treatment_history,
     get_total_treatment_cost
)


router = APIRouter(
    tags=["Crop Treatments"]
)


# ============================================================
# CREATE TREATMENT
# ============================================================

@router.post(
    "/crop-treatments",
    response_model=CropTreatmentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_treatment_api(

    treatment_data: CropTreatmentCreate,

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

    return create_crop_treatment(
        db=db,
        treatment_data=treatment_data
    )



# ============================================================
# GET TOTAL TREATMENT COST
# ============================================================

@router.get(
    "/crops/{crop_id}/treatments/total-cost"
)
def get_total_treatment_cost_api(

    crop_id: int,

    db: Session = Depends(
        get_db
    ),

    current_user: User = Depends(
        get_current_user
    )
):

    total_cost = get_total_treatment_cost(
        db=db,
        crop_id=crop_id
    )

    return {
        "crop_id": crop_id,
        "total_treatment_cost": total_cost
    }


# ============================================================
# GET ALL TREATMENTS
# ============================================================

@router.get(
    "/crop-treatments",
    response_model=list[CropTreatmentResponse]
)
def get_treatments_api(

    db: Session = Depends(
        get_db
    ),

    current_user: User = Depends(
        get_current_user
    )
):

    return get_all_crop_treatments(
        db=db
    )


# ============================================================
# GET CROP TREATMENT HISTORY
# ============================================================

@router.get(
    "/crops/{crop_id}/treatments",
    response_model=list[CropTreatmentResponse]
)
def get_crop_treatments_api(

    crop_id: int,

    db: Session = Depends(
        get_db
    ),

    current_user: User = Depends(
        get_current_user
    )
):

    return get_crop_treatment_history(
        db=db,
        crop_id=crop_id
    )