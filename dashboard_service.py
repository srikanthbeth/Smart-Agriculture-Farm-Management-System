from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from models import (
    Farm,
    Field,
    Crop,
    CropHealth,
    Harvest,
    Sale,
    CropTreatment
)


# ============================================================
# MAIN DASHBOARD
# ============================================================

def get_dashboard(
    db: Session
):
    """
    Return overall agriculture dashboard statistics.
    """

    # --------------------------------------------------------
    # Total Farms
    # --------------------------------------------------------

    total_farms = (
        db.query(Farm)
        .count()
    )

    # --------------------------------------------------------
    # Total Fields
    # --------------------------------------------------------

    total_fields = (
        db.query(Field)
        .count()
    )

    # --------------------------------------------------------
    # Active Crops
    # --------------------------------------------------------

    active_crops = (
        db.query(Crop)
        .filter(
            Crop.status == "Growing"
        )
        .count()
    )

    # --------------------------------------------------------
    # Crops Ready For Harvest
    # --------------------------------------------------------

    crops_ready_for_harvest = (
        db.query(Crop)
        .filter(
            Crop.status == "Ready for Harvest"
        )
        .count()
    )

    # --------------------------------------------------------
    # Critical Crop Alerts
    # --------------------------------------------------------

    critical_crop_alerts = (
        db.query(CropHealth)
        .filter(
            CropHealth.health_status == "Critical"
        )
        .count()
    )

    # --------------------------------------------------------
    # Total Harvest Quantity
    # --------------------------------------------------------

    total_harvest_quantity = (
        db.query(
            func.coalesce(
                func.sum(
                    Harvest.quantity
                ),
                0
            )
        )
        .scalar()
    )

    # --------------------------------------------------------
    # Total Sales
    # --------------------------------------------------------

    total_sales = (
        db.query(Sale)
        .count()
    )

    # --------------------------------------------------------
    # Total Revenue
    # --------------------------------------------------------

    total_revenue = (
        db.query(
            func.coalesce(
                func.sum(
                    Sale.total_amount
                ),
                0
            )
        )
        .scalar()
    )

    # --------------------------------------------------------
    # Total Treatment Cost
    # --------------------------------------------------------

    total_treatment_cost = (
        db.query(
            func.coalesce(
                func.sum(
                    CropTreatment.cost
                ),
                0
            )
        )
        .scalar()
    )

    return {
        "total_farms": total_farms,
        "total_fields": total_fields,
        "active_crops": active_crops,
        "crops_ready_for_harvest": (
            crops_ready_for_harvest
        ),
        "critical_crop_alerts": (
            critical_crop_alerts
        ),
        "total_harvest_quantity": (
            float(total_harvest_quantity or 0)
        ),
        "total_sales": total_sales,
        "total_revenue": (
            float(total_revenue or 0)
        ),
        "total_treatment_cost": (
            float(total_treatment_cost or 0)
        )
    }


# ============================================================
# FARM-WISE REVENUE
# ============================================================

def get_farm_wise_revenue(
    db: Session
):
    """
    Calculate total revenue for each farm.
    """

    results = (
        db.query(
            Farm.id.label("farm_id"),
            Farm.farm_name.label("farm_name"),
            func.coalesce(
                func.sum(
                    Sale.total_amount
                ),
                0
            ).label("total_revenue")
        )
        .join(
            Field,
            Field.farm_id == Farm.id
        )
        .join(
            Crop,
            Crop.field_id == Field.id
        )
        .join(
            Harvest,
            Harvest.crop_id == Crop.id
        )
        .join(
            Sale,
            Sale.harvest_id == Harvest.id
        )
        .group_by(
            Farm.id,
            Farm.farm_name
        )
        .order_by(
            func.sum(
                Sale.total_amount
            ).desc()
        )
        .all()
    )

    return [
        {
            "farm_id": row.farm_id,
            "farm_name": row.farm_name,
            "total_revenue": float(
                row.total_revenue or 0
            )
        }
        for row in results
    ]


# ============================================================
# CROP-WISE PRODUCTION
# ============================================================

def get_crop_wise_production(
    db: Session
):
    """
    Calculate total harvested quantity
    for each crop.
    """

    results = (
        db.query(
            Crop.id.label("crop_id"),
            Crop.crop_name.label("crop_name"),
            func.coalesce(
                func.sum(
                    Harvest.quantity
                ),
                0
            ).label("total_production")
        )
        .outerjoin(
            Harvest,
            Harvest.crop_id == Crop.id
        )
        .group_by(
            Crop.id,
            Crop.crop_name
        )
        .order_by(
            func.sum(
                Harvest.quantity
            ).desc()
        )
        .all()
    )

    return [
        {
            "crop_id": row.crop_id,
            "crop_name": row.crop_name,
            "total_production": float(
                row.total_production or 0
            )
        }
        for row in results
    ]