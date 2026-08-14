from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models import Farm, Field
from schemas import FieldCreate


# ============================================================
# CREATE FIELD
# ============================================================

def create_field(
    db: Session,
    farm_id: int,
    field_data: FieldCreate
):
    # --------------------------------------------------------
    # Check farm exists
    # --------------------------------------------------------

    farm = (
        db.query(Farm)
        .filter(Farm.id == farm_id)
        .first()
    )

    if not farm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farm not found"
        )

    # --------------------------------------------------------
    # Check farm status
    # --------------------------------------------------------

    if farm.status != "Active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Fields cannot be added to an inactive or maintained farm"
        )

    # --------------------------------------------------------
    # Check duplicate field name
    # --------------------------------------------------------

    existing_field = (
        db.query(Field)
        .filter(
            Field.farm_id == farm_id,
            Field.field_name == field_data.field_name
        )
        .first()
    )

    if existing_field:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Field with this name already exists in this farm"
        )

    # --------------------------------------------------------
    # Calculate already allocated area
    # --------------------------------------------------------

    existing_fields = (
        db.query(Field)
        .filter(Field.farm_id == farm_id)
        .all()
    )

    used_area = sum(
        field.area
        for field in existing_fields
    )

    available_area = farm.total_area - used_area

    # --------------------------------------------------------
    # Check available area
    # --------------------------------------------------------

    if field_data.area > available_area:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Field area exceeds available farm area. "
                f"Available area: {available_area}"
            )
        )

    # --------------------------------------------------------
    # Create field
    # --------------------------------------------------------

    field = Field(
        farm_id=farm_id,
        field_name=field_data.field_name,
        area=field_data.area,
        soil_type=field_data.soil_type,
        irrigation_type=field_data.irrigation_type,
        status=field_data.status
    )

    db.add(field)
    db.commit()
    db.refresh(field)

    return field


# ============================================================
# GET FIELDS FOR FARM
# ============================================================

def get_fields_by_farm(
    db: Session,
    farm_id: int
):
    # --------------------------------------------------------
    # Check farm exists
    # --------------------------------------------------------

    farm = (
        db.query(Farm)
        .filter(Farm.id == farm_id)
        .first()
    )

    if not farm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farm not found"
        )

    # --------------------------------------------------------
    # Get fields
    # --------------------------------------------------------

    return (
        db.query(Field)
        .filter(Field.farm_id == farm_id)
        .order_by(Field.id.desc())
        .all()
    )