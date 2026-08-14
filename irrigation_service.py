from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models import Field, Crop, Irrigation
from schemas import IrrigationCreate


ACTIVE_CROP_STATUSES = {
    "Planned",
    "Growing",
    "Ready for Harvest"
}


# ============================================================
# CREATE IRRIGATION
# ============================================================

def create_irrigation(
    db: Session,
    irrigation_data: IrrigationCreate
):

    # --------------------------------------------------------
    # Check field exists
    # --------------------------------------------------------

    field = (
        db.query(Field)
        .filter(
            Field.id == irrigation_data.field_id
        )
        .first()
    )

    if not field:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Field not found"
        )

    # --------------------------------------------------------
    # Field must be active
    # --------------------------------------------------------

    if field.status != "Active":

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Irrigation cannot be recorded for an inactive or maintained field"
        )

    # --------------------------------------------------------
    # Check active crop
    # --------------------------------------------------------

    active_crop = (
        db.query(Crop)
        .filter(
            Crop.field_id == irrigation_data.field_id,

            Crop.status.in_(
                ACTIVE_CROP_STATUSES
            )
        )
        .first()
    )

    if not active_crop:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Irrigation can be recorded only for fields with an active crop"
        )

    # --------------------------------------------------------
    # Create irrigation record
    # --------------------------------------------------------

    irrigation = Irrigation(
        field_id=irrigation_data.field_id,
        irrigation_date=irrigation_data.irrigation_date,
        water_quantity=irrigation_data.water_quantity,
        duration_minutes=irrigation_data.duration_minutes,
        irrigation_status=irrigation_data.irrigation_status,
        remarks=irrigation_data.remarks
    )

    db.add(irrigation)
    db.commit()
    db.refresh(irrigation)

    return irrigation


# ============================================================
# GET ALL IRRIGATION RECORDS
# ============================================================

def get_all_irrigation(
    db: Session
):

    return (
        db.query(Irrigation)
        .order_by(
            Irrigation.id.desc()
        )
        .all()
    )


# ============================================================
# GET IRRIGATION HISTORY BY FIELD
# ============================================================

def get_irrigation_by_field(
    db: Session,
    field_id: int
):

    # --------------------------------------------------------
    # Check field
    # --------------------------------------------------------

    field = (
        db.query(Field)
        .filter(
            Field.id == field_id
        )
        .first()
    )

    if not field:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Field not found"
        )

    # --------------------------------------------------------
    # Complete irrigation history
    # --------------------------------------------------------

    return (
        db.query(Irrigation)
        .filter(
            Irrigation.field_id == field_id
        )
        .order_by(
            Irrigation.irrigation_date.desc(),
            Irrigation.id.desc()
        )
        .all()
    )