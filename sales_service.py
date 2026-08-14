from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from models import Harvest, Sale
from schemas import SaleCreate

from typing import Optional
from sqlalchemy import asc, desc


# ============================================================
# CREATE SALE
# ============================================================

def create_sale(
    db: Session,
    sale_data: SaleCreate
):

    # --------------------------------------------------------
    # Check harvest exists
    # --------------------------------------------------------

    harvest = (
        db.query(Harvest)
        .filter(
            Harvest.id == sale_data.harvest_id
        )
        .first()
    )

    if not harvest:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Harvest not found"
        )

    # --------------------------------------------------------
    # Check sale date
    # --------------------------------------------------------

    if sale_data.sale_date < harvest.harvest_date:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Sale date cannot be before "
                "harvest date"
            )
        )

    # --------------------------------------------------------
    # Calculate already sold quantity
    # --------------------------------------------------------

    sold_quantity = (
        db.query(
            func.coalesce(
                func.sum(Sale.quantity),
                0
            )
        )
        .filter(
            Sale.harvest_id == sale_data.harvest_id
        )
        .scalar()
    )

    sold_quantity = float(
        sold_quantity or 0
    )

    # --------------------------------------------------------
    # Calculate remaining quantity
    # --------------------------------------------------------

    available_quantity = (
        harvest.quantity - sold_quantity
    )

    # --------------------------------------------------------
    # Prevent over-selling
    # --------------------------------------------------------

    if sale_data.quantity > available_quantity:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Insufficient harvested quantity. "
                f"Available quantity: "
                f"{available_quantity} "
                f"{harvest.unit}"
            )
        )

    # --------------------------------------------------------
    # Calculate total amount
    # --------------------------------------------------------

    total_amount = (
        sale_data.quantity
        * sale_data.price_per_unit
    )

    # --------------------------------------------------------
    # Create sale
    # --------------------------------------------------------

    sale = Sale(
        harvest_id=sale_data.harvest_id,
        buyer_name=sale_data.buyer_name,
        quantity=sale_data.quantity,
        price_per_unit=sale_data.price_per_unit,
        total_amount=total_amount,
        sale_date=sale_data.sale_date,
        payment_status=sale_data.payment_status
    )

    db.add(sale)
    db.commit()
    db.refresh(sale)

    return sale


# ============================================================
# GET ALL SALES
# ============================================================

def get_all_sales(
    db: Session
):

    return (
        db.query(Sale)
        .order_by(
            Sale.id.desc()
        )
        .all()
    )


# ============================================================
# GET SALE BY ID
# ============================================================

def get_sale_by_id(
    db: Session,
    sale_id: int
):

    sale = (
        db.query(Sale)
        .filter(
            Sale.id == sale_id
        )
        .first()
    )

    if not sale:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale not found"
        )

    return sale



def get_sales_filtered(
    db: Session,
    payment_status: Optional[str] = None,
    buyer: Optional[str] = None,
    page: int = 1,
    limit: int = 10,
    sort_by: str = "id",
    sort_order: str = "desc"
):
    """
    Filter, sort and paginate sales.
    """

    # --------------------------------------------------------
    # Validate pagination
    # --------------------------------------------------------

    if page <= 0:
        raise HTTPException(
            status_code=400,
            detail="page must be greater than 0"
        )

    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=400,
            detail="limit must be between 1 and 100"
        )

    # --------------------------------------------------------
    # Validate sort order
    # --------------------------------------------------------

    if sort_order.lower() not in {"asc", "desc"}:
        raise HTTPException(
            status_code=400,
            detail="sort_order must be asc or desc"
        )

    # --------------------------------------------------------
    # Sort columns
    # --------------------------------------------------------

    sort_columns = {
        "id": Sale.id,
        "buyer_name": Sale.buyer_name,
        "quantity": Sale.quantity,
        "price_per_unit": Sale.price_per_unit,
        "total_amount": Sale.total_amount,
        "sale_date": Sale.sale_date,
        "payment_status": Sale.payment_status,
        "harvest_id": Sale.harvest_id,
    }

    # --------------------------------------------------------
    # Validate sort field
    # --------------------------------------------------------

    sort_column = sort_columns.get(sort_by)

    if sort_column is None:
        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid sort_by. "
                "Allowed: id, buyer_name, harvest_id, "
                "quantity, price_per_unit, total_amount, "
                "sale_date, payment_status"
            )
        )

    # --------------------------------------------------------
    # Base query
    # --------------------------------------------------------

    query = db.query(Sale)

    # --------------------------------------------------------
    # Payment status filter
    # --------------------------------------------------------

    if payment_status:
        query = query.filter(
            Sale.payment_status == payment_status
        )

    # --------------------------------------------------------
    # Buyer search
    # --------------------------------------------------------

    if buyer:
        query = query.filter(
            Sale.buyer_name.ilike(
                f"%{buyer.strip()}%"
            )
        )

    # --------------------------------------------------------
    # Sorting
    # --------------------------------------------------------

    if sort_order.lower() == "asc":
        query = query.order_by(
            asc(sort_column)
        )
    else:
        query = query.order_by(
            desc(sort_column)
        )

    # --------------------------------------------------------
    # Total records
    # --------------------------------------------------------

    total = query.count()

    # --------------------------------------------------------
    # Pagination
    # --------------------------------------------------------

    offset = (page - 1) * limit

    sales = (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )

    # --------------------------------------------------------
    # Response
    # --------------------------------------------------------

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "data": sales
    }