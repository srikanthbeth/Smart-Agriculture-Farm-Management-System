from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models import Crop, CropHealth, Alert
from schemas import CropHealthCreate


# ============================================================
# CREATE CROP HEALTH RECORD
# ============================================================

def create_crop_health(
    db: Session,
    health_data: CropHealthCreate
):

    # --------------------------------------------------------
    # Check crop
    # --------------------------------------------------------

    crop = (
        db.query(Crop)
        .filter(
            Crop.id == health_data.crop_id
        )
        .first()
    )

    if not crop:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crop not found"
        )

    # --------------------------------------------------------
    # Create health record
    # --------------------------------------------------------

    health_record = CropHealth(
        crop_id=health_data.crop_id,
        inspection_date=health_data.inspection_date,
        health_status=health_data.health_status,
        disease_name=health_data.disease_name,
        severity=health_data.severity,
        remarks=health_data.remarks
    )

    db.add(health_record)

    # --------------------------------------------------------
    # Critical health alert
    # --------------------------------------------------------

    if health_data.health_status == "Critical":

        severity = (
            health_data.severity
            if health_data.severity
            else "High"
        )

        alert = Alert(
            crop_id=health_data.crop_id,
            message=(
                f"Critical health condition detected "
                f"for crop '{crop.crop_name}'. "
                f"Immediate Farm Manager attention required."
            ),
            alert_type="Crop Health",
            severity=severity,
            is_read=False
        )

        db.add(alert)

    db.commit()

    db.refresh(health_record)

    return health_record


# ============================================================
# GET ALL HEALTH RECORDS
# ============================================================

def get_all_crop_health(
    db: Session
):

    return (
        db.query(CropHealth)
        .order_by(
            CropHealth.id.desc()
        )
        .all()
    )


# ============================================================
# GET CROP HEALTH HISTORY
# ============================================================

def get_crop_health_history(
    db: Session,
    crop_id: int
):

    # --------------------------------------------------------
    # Check crop
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
    # Get history
    # --------------------------------------------------------

    return (
        db.query(CropHealth)
        .filter(
            CropHealth.crop_id == crop_id
        )
        .order_by(
            CropHealth.inspection_date.desc(),
            CropHealth.id.desc()
        )
        .all()
    )


# ============================================================
# GET CRITICAL ALERTS
# ============================================================

def get_critical_alerts(
    db: Session
):

    return (
        db.query(Alert)
        .filter(
            Alert.alert_type == "Crop Health",
            Alert.is_read == False
        )
        .order_by(
            Alert.created_at.desc()
        )
        .all()
    )