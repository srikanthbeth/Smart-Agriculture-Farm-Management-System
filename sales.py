from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db

from dependencies import (
    get_current_user,
    require_roles
)

from models import User

from schemas import (
    SaleCreate,
    SaleResponse
)

from services.sales_service import (
    create_sale,
    get_all_sales,
    get_sale_by_id,
    get_sales_filtered
)


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    tags=["Produce Sales"]
)


# ============================================================
# CREATE SALE
# ============================================================

@router.post(
    "/sales",
    response_model=SaleResponse,
    status_code=status.HTTP_201_CREATED
)
def create_sale_api(
    sale_data: SaleCreate,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        require_roles(
            "Admin",
            "Farm Manager",
            "Farmer"
        )
    )
):
    return create_sale(
        db=db,
        sale_data=sale_data
    )


# ============================================================
# GET ALL SALES
# ============================================================

@router.get(
    "/sales",
    response_model=list[SaleResponse]
)
def get_sales_api(
    db: Session = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):
    return get_all_sales(
        db=db
    )


# ============================================================
# SEARCH / FILTER / PAGINATION
# IMPORTANT:
# This route MUST come before /sales/{sale_id}
# ============================================================

@router.get(
    "/sales/search"
)
def search_sales_api(
    payment_status: Optional[str] = None,

    buyer: Optional[str] = None,

    page: int = 1,

    limit: int = 10,

    sort_by: str = "id",

    sort_order: str = "desc",

    db: Session = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    # --------------------------------------------------------
    # PAGE VALIDATION
    # --------------------------------------------------------

    if page < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="page must be greater than 0"
        )

    # --------------------------------------------------------
    # LIMIT VALIDATION
    # --------------------------------------------------------

    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="limit must be between 1 and 100"
        )

    # --------------------------------------------------------
    # PAYMENT STATUS VALIDATION
    # --------------------------------------------------------

    allowed_payment_statuses = {
        "Pending",
        "Paid",
        "Partial",
        "Failed"
    }

    if (
        payment_status is not None
        and payment_status not in allowed_payment_statuses
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Invalid payment_status. "
                "Allowed: "
                + ", ".join(
                    sorted(allowed_payment_statuses)
                )
            )
        )

    # --------------------------------------------------------
    # BUYER VALIDATION
    # --------------------------------------------------------

    if buyer is not None:
        buyer = buyer.strip()

        if not buyer:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="buyer cannot be empty"
            )

    # --------------------------------------------------------
    # SORT FIELD VALIDATION
    # --------------------------------------------------------

    allowed_sort_fields = {
        "id",
        "buyer_name",
        "harvest_id",
        "quantity",
        "price_per_unit",
        "total_amount",
        "sale_date",
        "payment_status"
    }

    if sort_by not in allowed_sort_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Invalid sort_by. "
                "Allowed: "
                + ", ".join(
                    sorted(allowed_sort_fields)
                )
            )
        )

    # --------------------------------------------------------
    # SORT ORDER VALIDATION
    # --------------------------------------------------------

    sort_order = sort_order.lower()

    if sort_order not in {"asc", "desc"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="sort_order must be asc or desc"
        )

    # --------------------------------------------------------
    # GET FILTERED SALES
    # --------------------------------------------------------

    return get_sales_filtered(
        db=db,
        payment_status=payment_status,
        buyer=buyer,
        page=page,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order
    )


# ============================================================
# GET SALE BY ID
# IMPORTANT:
# Keep this route AFTER /sales/search
# ============================================================

@router.get(
    "/sales/{sale_id}",
    response_model=SaleResponse
)
def get_sale_api(
    sale_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    if sale_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="sale_id must be greater than 0"
        )

    return get_sale_by_id(
        db=db,
        sale_id=sale_id
    )