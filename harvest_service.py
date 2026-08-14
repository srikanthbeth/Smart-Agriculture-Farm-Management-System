# ============================================================
# HARVEST SERVICE
# ============================================================

from datetime import date
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import Harvest, Crop
from schemas import HarvestCreate


# ============================================================
# CREATE HARVEST
# ============================================================

# ============================================================
# CREATE HARVEST
# ============================================================

def create_harvest(
    db: Session,
    harvest_data: HarvestCreate
):

    # --------------------------------------------------------
    # Check crop exists
    # --------------------------------------------------------

    crop = (
        db.query(Crop)
        .filter(Crop.id == harvest_data.crop_id)
        .first()
    )

    if not crop:
        raise HTTPException(
            status_code=404,
            detail="Crop not found"
        )

    # --------------------------------------------------------
    # Validate Market Price
    # --------------------------------------------------------

    if harvest_data.market_price <= 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="market_price must be greater than 0"
        )

    # --------------------------------------------------------
    # Validate harvest date
    # --------------------------------------------------------

    if (
        hasattr(crop, "planting_date")
        and crop.planting_date
        and harvest_data.harvest_date < crop.planting_date
    ):
        raise HTTPException(
            status_code=400,
            detail="Harvest date cannot be before planting date"
        )

    # --------------------------------------------------------
    # Create Harvest
    # --------------------------------------------------------

    harvest = Harvest(
        crop_id=harvest_data.crop_id,
        harvest_date=harvest_data.harvest_date,
        quantity=harvest_data.quantity,
        unit=harvest_data.unit,
        quality_grade=harvest_data.quality_grade,
        market_price=harvest_data.market_price,
        total_revenue=harvest_data.total_revenue,
        remarks=harvest_data.remarks,
        storage_location=harvest_data.storage_location
    )

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    try:

        db.add(harvest)

        db.commit()

        db.refresh(harvest)

        return harvest

    except IntegrityError:

        db.rollback()

        raise HTTPException(
            status_code=400,
            detail="The requested operation violates a database constraint."
        )
# ============================================================
# GET ALL HARVESTS
# ============================================================

def get_all_harvests(
    db: Session
):

    return (
        db.query(Harvest)
        .order_by(Harvest.id.desc())
        .all()
    )


# ============================================================
# GET HARVESTS FOR CROP
# ============================================================

def get_crop_harvest(
    db: Session,
    crop_id: int
):

    # --------------------------------------------------------
    # Check crop exists
    # --------------------------------------------------------

    crop = (
        db.query(Crop)
        .filter(Crop.id == crop_id)
        .first()
    )

    if not crop:

        raise HTTPException(
            status_code=404,
            detail="Crop not found"
        )

    return (
        db.query(Harvest)
        .filter(Harvest.crop_id == crop_id)
        .order_by(Harvest.id.desc())
        .all()
    )


# ============================================================
# FILTER / SEARCH HARVESTS
# ============================================================

def get_harvests_filtered(
    db: Session,
    quality_grade=None,
    harvest_date=None,
    page: int = 1,
    limit: int = 10,
    sort_by: str = "id",
    sort_order: str = "desc"
):

    query = db.query(Harvest)

    # --------------------------------------------------------
    # Quality Grade Filter
    # --------------------------------------------------------

    if quality_grade:

        quality_grade = quality_grade.strip().upper()

        query = query.filter(
            Harvest.quality_grade == quality_grade
        )

    # --------------------------------------------------------
    # Harvest Date Filter
    # --------------------------------------------------------

    if harvest_date:

        query = query.filter(
            Harvest.harvest_date == harvest_date
        )

    # --------------------------------------------------------
    # Sorting
    # --------------------------------------------------------

    allowed_sort_fields = {
        "id": Harvest.id,
        "harvest_date": Harvest.harvest_date,
        "quantity": Harvest.quantity,
        "quality_grade": Harvest.quality_grade,
        "market_price": Harvest.market_price,
        "total_revenue": Harvest.total_revenue
    }

    sort_column = allowed_sort_fields.get(
        sort_by,
        Harvest.id
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
    # Total
    # --------------------------------------------------------

    total = query.count()

    # --------------------------------------------------------
    # Pagination
    # --------------------------------------------------------

    offset = (page - 1) * limit

    data = (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "data": data
    }