from datetime import date

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from typing import Optional

from sqlalchemy import asc, desc, and_

from models import Crop, Field
from schemas import CropCreate, CropUpdate


ACTIVE_CROP_STATUSES = {
    "Planned",
    "Growing",
    "Ready for Harvest",
}


# ============================================================
# CREATE CROP
# ============================================================

def create_crop(
    db: Session,
    crop_data: CropCreate
):
    # --------------------------------------------------------
    # Check field
    # --------------------------------------------------------

    field = (
        db.query(Field)
        .filter(Field.id == crop_data.field_id)
        .first()
    )

    if not field:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Field not found"
        )

    # --------------------------------------------------------
    # Inactive fields cannot be cultivated
    # --------------------------------------------------------

    if field.status != "Active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive or maintained fields cannot be used for cultivation"
        )

    # --------------------------------------------------------
    # Date validation
    # --------------------------------------------------------

    if (
        crop_data.expected_harvest_date
        < crop_data.planting_date
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Expected harvest date cannot be before planting date"
        )

    # --------------------------------------------------------
    # Check overlapping active crops
    # --------------------------------------------------------

    overlapping_crop = (
        db.query(Crop)
        .filter(
            Crop.field_id == crop_data.field_id,

            Crop.status.in_(
                ACTIVE_CROP_STATUSES
            ),

            Crop.planting_date
            <= crop_data.expected_harvest_date,

            Crop.expected_harvest_date
            >= crop_data.planting_date
        )
        .first()
    )

    if overlapping_crop:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Field already has an active crop "
                "during the selected cultivation period"
            )
        )

    # --------------------------------------------------------
    # Create crop
    # --------------------------------------------------------

    crop = Crop(
        field_id=crop_data.field_id,
        crop_name=crop_data.crop_name,
        crop_type=crop_data.crop_type,
        planting_date=crop_data.planting_date,
        expected_harvest_date=crop_data.expected_harvest_date,
        seed_quantity=crop_data.seed_quantity,
        status=crop_data.status
    )

    db.add(crop)
    db.commit()
    db.refresh(crop)

    return crop


# ============================================================
# GET ALL CROPS
# ============================================================

def get_all_crops(
    db: Session,
    crop_name: str | None = None,
    crop_status: str | None = None,
    from_date: date | None = None,
    to_date: date | None = None,
    page: int = 1,
    limit: int = 10,
    sort_by: str = "id",
    sort_order: str = "desc"
):
    query = db.query(Crop)

    # --------------------------------------------------------
    # Search by crop name
    # --------------------------------------------------------

    if crop_name:
        query = query.filter(
            Crop.crop_name.ilike(
                f"%{crop_name}%"
            )
        )

    # --------------------------------------------------------
    # Filter by crop status
    # --------------------------------------------------------

    if crop_status:
        query = query.filter(
            Crop.status == crop_status
        )

    # --------------------------------------------------------
    # Filter from date
    # --------------------------------------------------------

    if from_date:
        query = query.filter(
            Crop.planting_date >= from_date
        )

    # --------------------------------------------------------
    # Filter to date
    # --------------------------------------------------------

    if to_date:
        query = query.filter(
            Crop.planting_date <= to_date
        )

    # --------------------------------------------------------
    # Sorting
    # --------------------------------------------------------

    allowed_sort_fields = {
        "id": Crop.id,
        "crop_name": Crop.crop_name,
        "planting_date": Crop.planting_date,
        "expected_harvest_date": Crop.expected_harvest_date,
        "status": Crop.status
    }

    sort_column = allowed_sort_fields.get(
        sort_by,
        Crop.id
    )

    if sort_order.lower() == "asc":
        query = query.order_by(
            sort_column.asc()
        )
    else:
        query = query.order_by(
            sort_column.desc()
        )

    # --------------------------------------------------------
    # Pagination
    # --------------------------------------------------------

    offset = (page - 1) * limit

    return (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )


# ============================================================
# GET CROP BY ID
# ============================================================

def get_crop_by_id(
    db: Session,
    crop_id: int
):
    crop = (
        db.query(Crop)
        .filter(Crop.id == crop_id)
        .first()
    )

    if not crop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crop not found"
        )

    return crop


# ============================================================
# UPDATE CROP
# ============================================================

def update_crop(
    db: Session,
    crop_id: int,
    crop_data: CropUpdate
):
    crop = get_crop_by_id(
        db,
        crop_id
    )

    # --------------------------------------------------------
    # Harvested crops cannot be modified
    # --------------------------------------------------------

    if crop.status == "Harvested":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Harvested crops cannot be modified"
        )

    update_data = crop_data.model_dump(
        exclude_unset=True
    )

    # --------------------------------------------------------
    # Determine final dates
    # --------------------------------------------------------

    final_planting_date = update_data.get(
        "planting_date",
        crop.planting_date
    )

    final_harvest_date = update_data.get(
        "expected_harvest_date",
        crop.expected_harvest_date
    )

    # --------------------------------------------------------
    # Date validation
    # --------------------------------------------------------

    if final_harvest_date < final_planting_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Expected harvest date cannot be before planting date"
        )

    # --------------------------------------------------------
    # Check overlapping crops if dates change
    # --------------------------------------------------------

    if (
        "planting_date" in update_data
        or "expected_harvest_date" in update_data
    ):
        overlapping_crop = (
            db.query(Crop)
            .filter(
                Crop.field_id == crop.field_id,

                Crop.id != crop.id,

                Crop.status.in_(
                    ACTIVE_CROP_STATUSES
                ),

                Crop.planting_date
                <= final_harvest_date,

                Crop.expected_harvest_date
                >= final_planting_date
            )
            .first()
        )

        if overlapping_crop:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    "Updated cultivation period overlaps "
                    "with another active crop"
                )
            )

    # --------------------------------------------------------
    # Update crop
    # --------------------------------------------------------

    for field, value in update_data.items():
        setattr(
            crop,
            field,
            value
        )

    db.commit()
    db.refresh(crop)

    return crop

def get_crops_filtered(
    db: Session,
    crop_name: Optional[str] = None,
    status: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    page: int = 1,
    limit: int = 10,
    sort_by: str = "id",
    sort_order: str = "desc"
):
    """
    Search, filter, sort and paginate crops.
    """

    query = db.query(Crop)

    # --------------------------------------------------------
    # Search crop name
    # --------------------------------------------------------

    if crop_name:

        query = query.filter(
            Crop.crop_name.ilike(
                f"%{crop_name.strip()}%"
            )
        )

    # --------------------------------------------------------
    # Filter status
    # --------------------------------------------------------

    if status:

        query = query.filter(
            Crop.status == status
        )

    # --------------------------------------------------------
    # Date range
    # --------------------------------------------------------

    if start_date:

        query = query.filter(
            Crop.planting_date >= start_date
        )

    if end_date:

        query = query.filter(
            Crop.planting_date <= end_date
        )

    # --------------------------------------------------------
    # Sorting
    # --------------------------------------------------------

    sort_columns = {
        "id": Crop.id,
        "crop_name": Crop.crop_name,
        "planting_date": Crop.planting_date,
        "expected_harvest_date": Crop.expected_harvest_date,
        "seed_quantity": Crop.seed_quantity,
        "status": Crop.status
    }

    sort_column = sort_columns.get(
        sort_by
    )

    if not sort_column:

        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid sort_by. "
                "Allowed: id, crop_name, "
                "planting_date, expected_harvest_date, "
                "seed_quantity, status"
            )
        )

    if sort_order.lower() == "asc":

        query = query.order_by(
            asc(sort_column)
        )

    elif sort_order.lower() == "desc":

        query = query.order_by(
            desc(sort_column)
        )

    else:

        raise HTTPException(
            status_code=400,
            detail="sort_order must be asc or desc"
        )

    # --------------------------------------------------------
    # Pagination
    # --------------------------------------------------------

    total = query.count()

    offset = (
        (page - 1) * limit
    )

    crops = (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "data": crops
    }