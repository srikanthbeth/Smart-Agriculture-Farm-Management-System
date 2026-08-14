from datetime import datetime, date

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from database import Base


# ============================================================
# USER MODEL
# ============================================================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(150), unique=True, nullable=False, index=True)

    password_hash = Column(String(255), nullable=False)

    role = Column(String(50), nullable=False, default="Farmer")

    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    farms = relationship(
        "Farm",
        back_populates="created_by_user"
    )


# ============================================================
# FARM MODEL
# ============================================================

class Farm(Base):
    __tablename__ = "farms"

    id = Column(Integer, primary_key=True, index=True)

    farm_name = Column(String(150), unique=True, nullable=False, index=True)

    location = Column(String(255), nullable=False, index=True)

    total_area = Column(Float, nullable=False)

    owner_name = Column(String(150), nullable=False)

    status = Column(
        String(50),
        nullable=False,
        default="Active"
    )

    created_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    created_by_user = relationship(
        "User",
        back_populates="farms"
    )

    fields = relationship(
        "Field",
        back_populates="farm",
        cascade="all, delete-orphan"
    )


# ============================================================
# FIELD MODEL
# ============================================================

class Field(Base):
    __tablename__ = "fields"

    id = Column(Integer, primary_key=True, index=True)

    farm_id = Column(
        Integer,
        ForeignKey("farms.id"),
        nullable=False,
        index=True
    )

    field_name = Column(String(150), nullable=False)

    area = Column(Float, nullable=False)

    soil_type = Column(String(100), nullable=False)

    irrigation_type = Column(String(100), nullable=False)

    status = Column(
        String(50),
        nullable=False,
        default="Active"
    )

    farm = relationship(
        "Farm",
        back_populates="fields"
    )

    crops = relationship(
        "Crop",
        back_populates="field",
        cascade="all, delete-orphan"
    )

    irrigation_records = relationship(
        "Irrigation",
        back_populates="field",
        cascade="all, delete-orphan"
    )


# ============================================================
# CROP MODEL
# ============================================================

class Crop(Base):
    __tablename__ = "crops"

    id = Column(Integer, primary_key=True, index=True)

    field_id = Column(
        Integer,
        ForeignKey("fields.id"),
        nullable=False,
        index=True
    )

    crop_name = Column(
        String(150),
        nullable=False,
        index=True
    )

    crop_type = Column(
        String(100),
        nullable=False
    )

    planting_date = Column(
        Date,
        nullable=False
    )

    expected_harvest_date = Column(
        Date,
        nullable=False
    )

    seed_quantity = Column(
        Float,
        nullable=False
    )

    status = Column(
        String(50),
        nullable=False,
        default="Planned",
        index=True
    )

    field = relationship(
        "Field",
        back_populates="crops"
    )

    treatments = relationship(
        "CropTreatment",
        back_populates="crop",
        cascade="all, delete-orphan"
    )

    health_records = relationship(
        "CropHealth",
        back_populates="crop",
        cascade="all, delete-orphan"
    )

    alerts = relationship(
        "Alert",
        back_populates="crop",
        cascade="all, delete-orphan"
    )

    harvests = relationship(
        "Harvest",
        back_populates="crop",
        cascade="all, delete-orphan"
    )


# ============================================================
# IRRIGATION MODEL
# ============================================================

class Irrigation(Base):
    __tablename__ = "irrigation"

    id = Column(Integer, primary_key=True, index=True)

    field_id = Column(
        Integer,
        ForeignKey("fields.id"),
        nullable=False,
        index=True
    )

    irrigation_date = Column(
        Date,
        nullable=False
    )

    water_quantity = Column(
        Float,
        nullable=False
    )

    duration_minutes = Column(
        Integer,
        nullable=False
    )

    irrigation_status = Column(
        String(50),
        nullable=False
    )

    remarks = Column(
        Text,
        nullable=True
    )

    field = relationship(
        "Field",
        back_populates="irrigation_records"
    )


# ============================================================
# CROP TREATMENT MODEL
# ============================================================

class CropTreatment(Base):
    __tablename__ = "crop_treatments"

    id = Column(Integer, primary_key=True, index=True)

    crop_id = Column(
        Integer,
        ForeignKey("crops.id"),
        nullable=False,
        index=True
    )

    product_name = Column(
        String(150),
        nullable=False
    )

    product_type = Column(
        String(100),
        nullable=False
    )

    quantity = Column(
        Float,
        nullable=False
    )

    applied_date = Column(
        Date,
        nullable=False
    )

    cost = Column(
        Float,
        nullable=False
    )

    remarks = Column(
        Text,
        nullable=True
    )

    crop = relationship(
        "Crop",
        back_populates="treatments"
    )


# ============================================================
# CROP HEALTH MODEL
# ============================================================

class CropHealth(Base):
    __tablename__ = "crop_health"

    id = Column(Integer, primary_key=True, index=True)

    crop_id = Column(
        Integer,
        ForeignKey("crops.id"),
        nullable=False,
        index=True
    )

    inspection_date = Column(
        Date,
        nullable=False
    )

    health_status = Column(
        String(50),
        nullable=False,
        index=True
    )

    disease_name = Column(
        String(150),
        nullable=True
    )

    severity = Column(
        String(50),
        nullable=True
    )

    remarks = Column(
        Text,
        nullable=True
    )

    crop = relationship(
        "Crop",
        back_populates="health_records"
    )


# ============================================================
# ALERT MODEL
# ============================================================

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)

    crop_id = Column(
        Integer,
        ForeignKey("crops.id"),
        nullable=False,
        index=True
    )

    message = Column(
        Text,
        nullable=False
    )

    alert_type = Column(
        String(100),
        nullable=False
    )

    is_read = Column(
        Boolean,
        default=False,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    crop = relationship(
        "Crop",
        back_populates="alerts"
    )


# ============================================================
# HARVEST MODEL
# ============================================================
# ============================================================
# HARVEST MODEL
# ============================================================

class Harvest(Base):

    __tablename__ = "harvests"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    crop_id = Column(
        Integer,
        ForeignKey("crops.id"),
        nullable=False,
        index=True
    )

    harvest_date = Column(
        Date,
        nullable=False
    )

    quantity = Column(
        Float,
        nullable=False
    )

    unit = Column(
        String(50),
        nullable=False
    )

    quality_grade = Column(
        String(50),
        nullable=False,
        index=True
    )

    market_price = Column(
        Float,
        nullable=False
    )

    total_revenue = Column(
        Float,
        nullable=False
    )

    remarks = Column(
        String(500),
        nullable=True
    )

    storage_location = Column(
        String(255),
        nullable=True
    )

    crop = relationship(
        "Crop",
        back_populates="harvests"
    )

    sales = relationship(
        "Sale",
        back_populates="harvest",
        cascade="all, delete-orphan"
    )
# ============================================================
# SALE MODEL
# ============================================================

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)

    harvest_id = Column(
        Integer,
        ForeignKey("harvests.id"),
        nullable=False,
        index=True
    )

    buyer_name = Column(
        String(150),
        nullable=False,
        index=True
    )

    quantity = Column(
        Float,
        nullable=False
    )

    price_per_unit = Column(
        Float,
        nullable=False
    )

    total_amount = Column(
        Float,
        nullable=False
    )

    sale_date = Column(
        Date,
        nullable=False
    )

    payment_status = Column(
        String(50),
        nullable=False,
        index=True
    )

    harvest = relationship(
        "Harvest",
        back_populates="sales"
    )