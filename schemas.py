from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


# ============================================================
# COMMON VALIDATION VALUES
# ============================================================

USER_ROLES = {
    "Admin",
    "Farm Manager",
    "Farmer",
    "Field Worker",
}

FARM_STATUSES = {
    "Active",
    "Inactive",
    "Under Maintenance",
}

CROP_STATUSES = {
    "Planned",
    "Growing",
    "Ready for Harvest",
    "Harvested",
    "Failed",
}

HEALTH_STATUSES = {
    "Healthy",
    "Warning",
    "Critical",
}

PAYMENT_STATUSES = {
    "Pending",
    "Paid",
    "Partial",
    "Failed",
}

IRRIGATION_STATUSES = {
    "Scheduled",
    "Completed",
    "Cancelled",
}

QUALITY_GRADES = {
    "A",
    "B",
    "C",
}


# ============================================================
# AUTHENTICATION SCHEMAS
# ============================================================

class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72)
    role: str = "Farmer"

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str):
        value = value.strip()

        if not value:
            raise ValueError("Username cannot be empty")

        return value

    @field_validator("role")
    @classmethod
    def validate_role(cls, value: str):
        if value not in USER_ROLES:
            raise ValueError(
                f"Invalid role. Allowed roles: {', '.join(sorted(USER_ROLES))}"
            )

        return value


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ============================================================
# FARM SCHEMAS
# ============================================================

class FarmCreate(BaseModel):
    farm_name: str = Field(..., min_length=2, max_length=150)
    location: str = Field(..., min_length=2, max_length=255)
    total_area: float = Field(..., gt=0)
    owner_name: str = Field(..., min_length=2, max_length=150)
    status: str = "Active"

    @field_validator("farm_name", "location", "owner_name")
    @classmethod
    def validate_text_fields(cls, value: str):
        value = value.strip()

        if not value:
            raise ValueError("Field cannot be empty")

        return value

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str):
        if value not in FARM_STATUSES:
            raise ValueError(
                f"Invalid farm status. Allowed: {', '.join(sorted(FARM_STATUSES))}"
            )

        return value


class FarmUpdate(BaseModel):
    farm_name: Optional[str] = Field(None, min_length=2, max_length=150)
    location: Optional[str] = Field(None, min_length=2, max_length=255)
    total_area: Optional[float] = Field(None, gt=0)
    owner_name: Optional[str] = Field(None, min_length=2, max_length=150)
    status: Optional[str] = None

    @field_validator("farm_name", "location", "owner_name")
    @classmethod
    def validate_optional_text(cls, value: Optional[str]):
        if value is not None:
            value = value.strip()

            if not value:
                raise ValueError("Field cannot be empty")

        return value

    @field_validator("status")
    @classmethod
    def validate_optional_status(cls, value: Optional[str]):
        if value is not None and value not in FARM_STATUSES:
            raise ValueError(
                f"Invalid farm status. Allowed: {', '.join(sorted(FARM_STATUSES))}"
            )

        return value


class FarmResponse(BaseModel):
    id: int
    farm_name: str
    location: str
    total_area: float
    owner_name: str
    status: str
    created_by: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class FieldCreate(BaseModel):
    farm_id: int | None = Field(None, gt=0)

    field_name: str = Field(
        ...,
        min_length=2,
        max_length=150
    )

    area: float = Field(
        ...,
        gt=0
    )

    soil_type: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    irrigation_type: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    status: str = "Active"

    @field_validator(
        "field_name",
        "soil_type",
        "irrigation_type",
    )
    @classmethod
    def validate_field_text(cls, value: str):
        value = value.strip()

        if not value:
            raise ValueError("Field cannot be empty")

        return value

    @field_validator("status")
    @classmethod
    def validate_field_status(cls, value: str):
        if value not in FARM_STATUSES:
            raise ValueError(
                f"Invalid field status. "
                f"Allowed values: {FARM_STATUSES}"
            )

        return value


class FieldUpdate(BaseModel):
    field_name: Optional[str] = Field(None, min_length=2, max_length=150)
    area: Optional[float] = Field(None, gt=0)
    soil_type: Optional[str] = Field(None, min_length=2, max_length=100)
    irrigation_type: Optional[str] = Field(None, min_length=2, max_length=100)
    status: Optional[str] = None

    @field_validator(
        "field_name",
        "soil_type",
        "irrigation_type",
    )
    @classmethod
    def validate_optional_field_text(cls, value: Optional[str]):
        if value is not None:
            value = value.strip()

            if not value:
                raise ValueError("Field cannot be empty")

        return value

    @field_validator("status")
    @classmethod
    def validate_optional_field_status(cls, value: Optional[str]):
        if value is not None and value not in FARM_STATUSES:
            raise ValueError(
                f"Invalid field status. Allowed: {', '.join(sorted(FARM_STATUSES))}"
            )

        return value


class FieldResponse(BaseModel):
    id: int
    farm_id: int
    field_name: str
    area: float
    soil_type: str
    irrigation_type: str
    status: str

    model_config = ConfigDict(from_attributes=True)


# ============================================================
# CROP SCHEMAS
# ============================================================

class CropCreate(BaseModel):
    field_id: int
    crop_name: str = Field(..., min_length=2, max_length=150)
    crop_type: str = Field(..., min_length=2, max_length=100)
    planting_date: date
    expected_harvest_date: date
    seed_quantity: float = Field(..., gt=0)
    status: str = "Planned"

    @field_validator("crop_name", "crop_type")
    @classmethod
    def validate_crop_text(cls, value: str):
        value = value.strip()

        if not value:
            raise ValueError("Field cannot be empty")

        return value

    @field_validator("expected_harvest_date")
    @classmethod
    def validate_harvest_date(
        cls,
        value: date,
        info,
    ):
        planting_date = info.data.get("planting_date")

        if planting_date and value < planting_date:
            raise ValueError(
                "Expected harvest date cannot be before planting date"
            )

        return value

    @field_validator("status")
    @classmethod
    def validate_crop_status(cls, value: str):
        if value not in CROP_STATUSES:
            raise ValueError(
                f"Invalid crop status. Allowed: {', '.join(sorted(CROP_STATUSES))}"
            )

        return value


class CropUpdate(BaseModel):
    crop_name: Optional[str] = Field(
        None,
        min_length=2,
        max_length=150
    )

    crop_type: Optional[str] = Field(
        None,
        min_length=2,
        max_length=100
    )

    planting_date: Optional[date] = None

    expected_harvest_date: Optional[date] = None

    seed_quantity: Optional[float] = Field(
        None,
        gt=0
    )

    status: Optional[str] = None

    @field_validator("crop_name", "crop_type")
    @classmethod
    def validate_optional_crop_text(cls, value):
        if value is not None:
            value = value.strip()

            if not value:
                raise ValueError(
                    "Field cannot be empty"
                )

        return value

    @field_validator("status")
    @classmethod
    def validate_optional_crop_status(cls, value):
        if value is not None and value not in CROP_STATUSES:
            raise ValueError(
                f"Invalid crop status. "
                f"Allowed: {', '.join(sorted(CROP_STATUSES))}"
            )

        return value


class CropResponse(BaseModel):
    id: int
    field_id: int
    crop_name: str
    crop_type: str
    planting_date: date
    expected_harvest_date: date
    seed_quantity: float
    status: str

    model_config = ConfigDict(from_attributes=True)


# ============================================================
# IRRIGATION SCHEMAS
# ============================================================


IRRIGATION_STATUSES = {
    "Scheduled",
    "In Progress",
    "Completed",
    "Cancelled"
}

class IrrigationCreate(BaseModel):
    field_id: int
    irrigation_date: date
    water_quantity: float = Field(..., gt=0)
    duration_minutes: int = Field(..., gt=0)
    irrigation_status: str = "Completed"
    remarks: Optional[str] = None

    @field_validator("irrigation_status")
    @classmethod
    def validate_irrigation_status(cls, value: str):
        if value not in IRRIGATION_STATUSES:
            raise ValueError(
                f"Invalid irrigation status. Allowed: {', '.join(sorted(IRRIGATION_STATUSES))}"
            )

        return value


class IrrigationResponse(BaseModel):
    id: int
    field_id: int
    irrigation_date: date
    water_quantity: float
    duration_minutes: int
    irrigation_status: str
    remarks: Optional[str]

    model_config = ConfigDict(from_attributes=True)


# ============================================================
# CROP TREATMENT SCHEMAS
# ============================================================

TREATMENT_PRODUCT_TYPES = {
    "Fertilizer",
    "Pesticide",
    "Herbicide",
    "Fungicide",
    "Insecticide"
}


class CropTreatmentCreate(BaseModel):

    crop_id: int = Field(
        ...,
        gt=0
    )

    product_name: str = Field(
        ...,
        min_length=2,
        max_length=150
    )

    product_type: str = Field(
        ...,
        min_length=2,
        max_length=50
    )

    quantity: float = Field(
        ...,
        gt=0
    )

    applied_date: date

    cost: float = Field(
        ...,
        gt=0
    )

    remarks: Optional[str] = None

    @field_validator("product_name")
    @classmethod
    def validate_product_name(cls, value):

        value = value.strip()

        if not value:
            raise ValueError(
                "Product name cannot be empty"
            )

        return value

    @field_validator("product_type")
    @classmethod
    def validate_product_type(cls, value):

        value = value.strip()

        if value not in TREATMENT_PRODUCT_TYPES:
            raise ValueError(
                f"Invalid product type. "
                f"Allowed: "
                f"{', '.join(sorted(TREATMENT_PRODUCT_TYPES))}"
            )

        return value

    @field_validator("remarks")
    @classmethod
    def validate_treatment_remarks(cls, value):

        if value is not None:

            value = value.strip()

            if not value:
                return None

        return value


class CropTreatmentResponse(BaseModel):

    id: int
    crop_id: int
    product_name: str
    product_type: str
    quantity: float
    applied_date: date
    cost: float
    remarks: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

# ============================================================
# CROP HEALTH SCHEMAS
# ============================================================

class CropHealthCreate(BaseModel):
    crop_id: int
    inspection_date: date
    health_status: str
    disease_name: Optional[str] = None
    severity: Optional[str] = None
    remarks: Optional[str] = None

    @field_validator("health_status")
    @classmethod
    def validate_health_status(cls, value: str):
        if value not in HEALTH_STATUSES:
            raise ValueError(
                f"Invalid health status. Allowed: {', '.join(sorted(HEALTH_STATUSES))}"
            )

        return value


class CropHealthResponse(BaseModel):
    id: int
    crop_id: int
    inspection_date: date
    health_status: str
    disease_name: Optional[str]
    severity: Optional[str]
    remarks: Optional[str]

    model_config = ConfigDict(from_attributes=True)


# ============================================================
# ALERT SCHEMAS
# ============================================================

class AlertResponse(BaseModel):
    id: int
    crop_id: int
    message: str
    alert_type: str
    is_read: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============================================================
# HARVEST SCHEMAS
# ============================================================

QUALITY_GRADES = {
    "A",
    "B",
    "C"
}

HARVEST_UNITS = {
    "kg",
    "quintal",
    "ton",
    "litre",
    "piece"
}


# ============================================================
# HARVEST SCHEMAS
# ============================================================
from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, field_validator


HARVEST_UNITS = {
    "kg",
    "quintal",
    "ton",
    "liter",
    "piece"
}

QUALITY_GRADES = {
    "A",
    "B",
    "C"
}


# ============================================================
# HARVEST CREATE
# ============================================================
class HarvestCreate(BaseModel):

    crop_id: int = Field(
        ...,
        gt=0
    )

    harvest_date: date

    quantity: float = Field(
        ...,
        gt=0
    )

    unit: str = Field(
        ...,
        min_length=1,
        max_length=30
    )

    quality_grade: str = Field(
        ...,
        min_length=1,
        max_length=30
    )

    market_price: float = Field(
        default=0,
        ge=0
    )

    total_revenue: float = Field(
        default=0,
        ge=0
    )

    remarks: Optional[str] = Field(
        default=None,
        max_length=500
    )

    storage_location: Optional[str] = Field(
        default=None,
        max_length=150
    )

    @field_validator("unit")
    @classmethod
    def validate_unit(cls, value):

        value = value.strip().lower()

        if value not in HARVEST_UNITS:
            raise ValueError(
                f"Invalid unit. Allowed: "
                f"{', '.join(sorted(HARVEST_UNITS))}"
            )

        return value

    @field_validator("quality_grade")
    @classmethod
    def validate_quality_grade(cls, value):

        value = value.strip().upper()

        if value not in QUALITY_GRADES:
            raise ValueError(
                f"Invalid quality grade. Allowed: "
                f"{', '.join(sorted(QUALITY_GRADES))}"
            )

        return value

    @field_validator("storage_location")
    @classmethod
    def validate_storage_location(cls, value):

        if value is not None:
            value = value.strip()

            if not value:
                return None

        return value

    @field_validator("remarks")
    @classmethod
    def validate_remarks(cls, value):

        if value is not None:
            value = value.strip()

            if not value:
                return None

        return value
        


# ============================================================
# HARVEST RESPONSE
# ============================================================

class HarvestResponse(BaseModel):

    id: int

    crop_id: int

    harvest_date: date

    quantity: float

    unit: str

    quality_grade: str

    market_price: float

    total_revenue: float

    remarks: Optional[str] = None

    storage_location: Optional[str] = None

    model_config = {
        "from_attributes": True
    }



# ============================================================
# SALES SCHEMAS
# ============================================================

class SaleCreate(BaseModel):

    harvest_id: int = Field(..., gt=0)

    buyer_name: str = Field(
        ...,
        min_length=2,
        max_length=150
    )

    quantity: float = Field(
        ...,
        gt=0
    )

    price_per_unit: float = Field(
        ...,
        gt=0
    )

    sale_date: date

    payment_status: str = "Pending"

    @field_validator("buyer_name")
    @classmethod
    def validate_buyer_name(cls, value: str):

        value = value.strip()

        if not value:
            raise ValueError(
                "Buyer name cannot be empty"
            )

        return value

    @field_validator("payment_status")
    @classmethod
    def validate_payment_status(cls, value: str):

        value = value.strip()

        if value not in PAYMENT_STATUSES:
            raise ValueError(
                f"Invalid payment status. Allowed: "
                f"{', '.join(sorted(PAYMENT_STATUSES))}"
            )

        return value


class SaleResponse(BaseModel):
    id: int
    harvest_id: int
    buyer_name: str
    quantity: float
    price_per_unit: float
    total_amount: float
    sale_date: date
    payment_status: str

    model_config = ConfigDict(from_attributes=True)


# ============================================================
# DASHBOARD SCHEMA
# ============================================================


class DashboardResponse(BaseModel):

    total_farms: int

    total_fields: int

    active_crops: int

    crops_ready_for_harvest: int

    critical_crop_alerts: int

    total_harvest_quantity: float

    total_sales: int

    total_revenue: float

    total_treatment_cost: float


class FarmRevenueResponse(BaseModel):

    farm_id: int

    farm_name: str

    total_revenue: float


class CropProductionResponse(BaseModel):

    crop_id: int

    crop_name: str

    total_production: float



# ============================================================
# PAGINATION SCHEMA
# ============================================================

class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=10, ge=1, le=100)
    sort_order: str = "asc"

    @field_validator("sort_order")
    @classmethod
    def validate_sort_order(cls, value: str):
        value = value.lower()

        if value not in {"asc", "desc"}:
            raise ValueError("sort_order must be 'asc' or 'desc'")

        return value