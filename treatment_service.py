from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models import Crop, CropTreatment
from schemas import CropTreatmentCreate


# ============================================================
# CREATE CROP TREATMENT
# ============================================================

def create_crop_treatment(
    db: Session,
    treatment_data: CropTreatmentCreate
):

    # --------------------------------------------------------
    # Check crop exists
    # --------------------------------------------------------

    crop = (
        db.query(Crop)
        .filter(
            Crop.id == treatment_data.crop_id
        )
        .first()
    )

    if not crop:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crop not found"
        )

    # --------------------------------------------------------
    # Create treatment
    # --------------------------------------------------------

    treatment = CropTreatment(
        crop_id=treatment_data.crop_id,
        product_name=treatment_data.product_name,
        product_type=treatment_data.product_type,
        quantity=treatment_data.quantity,
        applied_date=treatment_data.applied_date,
        cost=treatment_data.cost,
        remarks=treatment_data.remarks
    )

    db.add(treatment)
    db.commit()
    db.refresh(treatment)

    return treatment


# ============================================================
# GET ALL TREATMENTS
# ============================================================

def get_all_crop_treatments(
    db: Session
):

    return (
        db.query(CropTreatment)
        .order_by(
            CropTreatment.id.desc()
        )
        .all()
    )


# ============================================================
# GET TREATMENT HISTORY FOR CROP
# ============================================================

def get_crop_treatment_history(
    db: Session,
    crop_id: int
):

    # --------------------------------------------------------
    # Check crop exists
    # --------------------------------------------------------

    crop = (
        db.query(Crop)
        .filter(
            Crop.id == crop_id
        )
        .first()
    )

    if not crop:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crop not found"
        )

    # --------------------------------------------------------
    # Get complete treatment history
    # --------------------------------------------------------

    return (
        db.query(CropTreatment)
        .filter(
            CropTreatment.crop_id == crop_id
        )
        .order_by(
            CropTreatment.applied_date.desc(),
            CropTreatment.id.desc()
        )
        .all()
    )


# ============================================================
# GET TOTAL TREATMENT COST FOR CROP
# ============================================================

def get_total_treatment_cost(
    db: Session,
    crop_id: int
):

    crop = (
        db.query(Crop)
        .filter(
            Crop.id == crop_id
        )
        .first()
    )

    if not crop:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crop not found"
        )

    treatments = (
        db.query(CropTreatment)
        .filter(
            CropTreatment.crop_id == crop_id
        )
        .all()
    )

    total_cost = sum(
        treatment.cost
        for treatment in treatments
    )

    return total_cost