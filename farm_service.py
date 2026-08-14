from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from typing import Optional

from models import Farm
from schemas import FarmCreate, FarmUpdate
from sqlalchemy import asc, desc

def create_farm(
    db: Session,
    farm_data: FarmCreate,
    user_id: int
):
    # --------------------------------------------------------
    # Check duplicate farm name
    # --------------------------------------------------------

    existing_farm = (
        db.query(Farm)
        .filter(Farm.farm_name == farm_data.farm_name)
        .first()
    )

    if existing_farm:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Farm with this name already exists"
        )

    # --------------------------------------------------------
    # Create farm
    # --------------------------------------------------------

    farm = Farm(
        farm_name=farm_data.farm_name,
        location=farm_data.location,
        total_area=farm_data.total_area,
        owner_name=farm_data.owner_name,
        status=farm_data.status,
        created_by=user_id
    )

    db.add(farm)
    db.commit()
    db.refresh(farm)

    return farm


def get_all_farms(
    db: Session,
    page: int = 1,
    limit: int = 10
):
    if page < 1:
        page = 1

    if limit < 1:
        limit = 10

    if limit > 100:
        limit = 100

    offset = (page - 1) * limit

    return (
        db.query(Farm)
        .order_by(Farm.id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


def get_farm_by_id(
    db: Session,
    farm_id: int
):
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

    return farm


def update_farm(
    db: Session,
    farm_id: int,
    farm_data: FarmUpdate
):
    # --------------------------------------------------------
    # Get farm
    # --------------------------------------------------------

    farm = get_farm_by_id(
        db,
        farm_id
    )

    update_data = farm_data.model_dump(
        exclude_unset=True
    )

    # --------------------------------------------------------
    # Check duplicate farm name
    # --------------------------------------------------------

    if "farm_name" in update_data:

        existing_farm = (
            db.query(Farm)
            .filter(
                Farm.farm_name == update_data["farm_name"],
                Farm.id != farm_id
            )
            .first()
        )

        if existing_farm:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Farm with this name already exists"
            )

    # --------------------------------------------------------
    # Update farm
    # --------------------------------------------------------

    for field, value in update_data.items():
        setattr(
            farm,
            field,
            value
        )

    db.commit()
    db.refresh(farm)

    return farm

def get_farms_filtered(
    db: Session,
    location: Optional[str] = None,
    status: Optional[str] = None,
    page: int = 1,
    limit: int = 10,
    sort_by: str = "id",
    sort_order: str = "desc"
):
    """
    Search, filter, sort and paginate farms.
    """

    query = db.query(Farm)

    # --------------------------------------------------------
    # Search by location
    # --------------------------------------------------------

    if location:

        query = query.filter(
            Farm.location.ilike(
                f"%{location.strip()}%"
            )
        )

    # --------------------------------------------------------
    # Filter by status
    # --------------------------------------------------------

    if status:

        query = query.filter(
            Farm.status == status
        )

    # --------------------------------------------------------
    # Allowed sorting fields
    # --------------------------------------------------------

    sort_columns = {
        "id": Farm.id,
        "farm_name": Farm.farm_name,
        "location": Farm.location,
        "total_area": Farm.total_area,
        "status": Farm.status
    }

    sort_column = sort_columns.get(
        sort_by
    )

    if not sort_column:

        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid sort_by. "
                "Allowed: id, farm_name, "
                "location, total_area, status"
            )
        )

    # --------------------------------------------------------
    # Sorting
    # --------------------------------------------------------

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

    farms = (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "data": farms
    }