# Smart Agriculture Farm Management System

A FastAPI-based Smart Agriculture Farm Management System for managing farms, fields, crops, harvests, sales, irrigation, and treatments.

---

# Features

- User Registration and Login
- JWT Authentication
- Farm Management
- Field Management
- Crop Management
- Harvest Management
- Sales Management
- Irrigation Management
- Treatment Management
- Sales Search and Filtering
- Sales Pagination
- Sales Sorting
- Input Validation
- Error Handling
- PostgreSQL Database
- SQLAlchemy ORM
- Alembic Migrations
- Pytest Automated Testing
- Swagger API Documentation

---

# Technology Stack

- Python 3.10+
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic
- PostgreSQL
- Alembic
- JWT Authentication
- Passlib / Bcrypt
- Pytest
- HTTPX

---

# Project Structure

Smart-Agriculture-Farm-Management-System/
│
├── routers/
├── services/
├── tests/
├── alembic/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── crud.py
├── requirements.txt
├── alembic.ini
├── .env
├── .gitignore
└── README.md

---

# Installation

Clone the repository.

Navigate to the project directory.

Create a Python virtual environment.

Activate the virtual environment.

Install the required dependencies using requirements.txt.

---

# Database Configuration

The application uses PostgreSQL.

- Database: smart_agriculture
- Host: localhost
- Port: 5432

Configure the database connection using environment variables.

Do not commit database passwords, secret keys, or .env files to GitHub.

---

# Database Migration

Alembic is used for database migration management.

Migration operations include:

- Create Migration
- Apply Migration
- Check Current Migration
- View Migration History

---

# Run the Application

Start the FastAPI application using Uvicorn.

Application:

http://127.0.0.1:8000

---

# API Documentation

Swagger UI:

http://127.0.0.1:8000/docs

ReDoc:

http://127.0.0.1:8000/redoc

---

# Authentication

The application uses JWT-based authentication.

Authentication workflow:

Register User

↓

Login

↓

Receive JWT Access Token

↓

Authorize in Swagger

↓

Access Protected APIs

Protected APIs require authentication.

Unauthenticated requests return HTTP 401 Unauthorized.

---

# Application Workflow

Register User

↓

Login

↓

Create Farm

↓

Create Field

↓

Create Crop

↓

Create Harvest

↓

Create Sale

↓

Manage Irrigation

↓

Manage Treatments

↓

Search / Filter / Sort / Paginate

---

# Farm Management

The system provides functionality for managing farms.

Farm management includes:

- Create Farm
- Get Farm
- Update Farm
- Delete Farm
- Farm Validation

---

# Field Management

Fields are associated with farms.

Field management includes:

- Create Field
- Get Fields
- Get Field by ID
- Update Field
- Delete Field
- Field Validation
- Field Status Management

Field information includes:

- Field Name
- Area
- Soil Type
- Irrigation Type
- Status
- Farm Association

---

# Crop Management

Crops are associated with fields.

Crop management includes:

- Create Crop
- Get Crops
- Get Crop by ID
- Update Crop
- Delete Crop
- Crop Validation
- Crop Status Management

Crop information includes:

- Crop Name
- Crop Type
- Planting Date
- Expected Harvest Date
- Seed Quantity
- Field Association
- Status

---

# Harvest Management

Harvest records are associated with crops.

Harvest management includes:

- Create Harvest
- Get Harvests
- Get Harvest by ID
- Update Harvest
- Delete Harvest
- Harvest Validation
- Revenue Calculation
- Storage Management

Harvest information includes:

- Crop
- Harvest Date
- Quantity
- Unit
- Quality Grade
- Market Price
- Total Revenue
- Remarks
- Storage Location

---

# Sales Management

Sales are associated with harvested crops.

Sales management includes:

- Create Sale
- Get Sales
- Get Sale by ID
- Update Sale
- Delete Sale
- Search Sales
- Payment Status Filtering
- Pagination
- Sorting
- Authentication
- Input Validation

Sales information includes:

- Buyer Name
- Harvest
- Price Per Unit
- Sale Date
- Quantity
- Total Amount
- Payment Status

---

# Sales Search

The system supports searching and filtering sales records.

Sales can be filtered by payment status.

The sales API supports:

- Search
- Filtering
- Pagination
- Sorting

---

# Sales Pagination

Sales records support pagination.

Pagination includes:

- Page Number
- Page Limit
- Total Records
- Paginated Data

Validation is applied to page and limit parameters.

Page must be greater than zero.

Limit must be between 1 and 100.

---

# Sales Sorting

Sales records support sorting.

Supported sorting fields include:

- buyer_name
- harvest_id
- id
- payment_status
- price_per_unit
- quantity
- sale_date
- total_amount

Supported sort orders:

- asc
- desc

Invalid sorting fields and sorting orders return appropriate HTTP 400 Bad Request responses.

---

# Irrigation Management

The system provides irrigation management for agricultural fields and crops.

Irrigation management includes:

- Irrigation Records
- Irrigation Scheduling
- Irrigation Information
- Irrigation Validation

---

# Treatment Management

Treatments are associated with crops.

Treatment management includes:

- Create Treatment
- Get Treatments
- Get Treatment by ID
- Update Treatment
- Delete Treatment
- Crop Treatment History
- Fertilizer Treatment
- Pesticide Treatment
- Treatment Validation

Treatment information includes:

- Crop
- Product Name
- Product Type
- Quantity
- Applied Date
- Cost
- Remarks

---

# Treatment Validation

Treatment quantity must be greater than zero.

Treatment cost must be greater than zero.

The system validates:

- Zero Quantity
- Negative Quantity
- Zero Cost
- Negative Cost
- Non-existing Crop

Invalid input returns HTTP 422 Unprocessable Entity.

Non-existing crops return HTTP 404 Not Found.

---

# Crop Treatment History

The system provides treatment history for individual crops.

Treatment history contains:

- Treatment ID
- Crop ID
- Product Name
- Product Type
- Quantity
- Applied Date
- Cost
- Remarks

The system returns HTTP 404 Not Found when the requested crop does not exist.

---

# Error Handling

The application uses standard HTTP status codes.

- 200 OK
- 201 Created
- 204 No Content
- 400 Bad Request
- 401 Unauthorized
- 404 Not Found
- 409 Conflict
- 422 Unprocessable Entity

The application validates request data and returns appropriate error responses.

---

# Testing

The project uses Pytest for automated testing.

Run all tests using:

pytest -v

Run individual test modules when required.

The test suite validates:

- Authentication
- Authorization
- Farm Management
- Field Management
- Crop Management
- Harvest Management
- Sales Management
- Irrigation Management
- Treatment Management
- Search
- Filtering
- Pagination
- Sorting
- Input Validation
- Error Handling
- Unauthorized Access

---

# Test Results

All automated tests passed successfully.

123 tests passed.

0 tests failed.

2 warnings were reported.

Test execution time:

77.88 seconds.

---

# Test Coverage

The automated test suite covers:

- Authentication
- Farm Management
- Field Management
- Crop Management
- Harvest Management
- Sales Management
- Irrigation Management
- Treatment Management

Sales testing includes:

- Create Sale
- Get Sales
- Search Sales
- Payment Status Search
- Sales Pagination
- Invalid Page
- Invalid Limit
- Invalid Sort Field
- Invalid Sort Order
- Ascending Sort
- Unauthorized Get Sales
- Unauthorized Create Sale

Treatment testing includes:

- Create Treatment
- Get Treatments
- Crop Treatment History
- Zero Quantity Validation
- Negative Quantity Validation
- Zero Cost Validation
- Negative Cost Validation
- Non-existing Crop Validation
- Fertilizer Treatment
- Pesticide Treatment
- Unauthorized Get Treatments
- Unauthorized Create Treatment

---

# Security

The application uses JWT authentication for protected APIs.

Sensitive configuration should be stored using environment variables.

The following should not be committed to GitHub:

- .env
- venv/
- __pycache__/
- *.pyc
- .pytest_cache/

---

# Useful Commands

Create virtual environment:

python -m venv venv

Activate virtual environment:

.\venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

Create migration:

alembic revision --autogenerate -m "initial migration"

Apply migration:

alembic upgrade head

Check migration:

alembic current

View migration history:

alembic history

Start application:

uvicorn main:app --reload

Run tests:

pytest -v

---

# API Access

Application:

http://127.0.0.1:8000

Swagger:

http://127.0.0.1:8000/docs

ReDoc:

http://127.0.0.1:8000/redoc

---

# Completed

- ✅ Authentication
- ✅ JWT Authorization
- ✅ Farm Management
- ✅ Field Management
- ✅ Crop Management
- ✅ Harvest Management
- ✅ Sales Management
- ✅ Sales Search and Filtering
- ✅ Sales Pagination
- ✅ Sales Sorting
- ✅ Irrigation Management
- ✅ Treatment Management
- ✅ Input Validation
- ✅ Error Handling
- ✅ PostgreSQL Database
- ✅ SQLAlchemy ORM
- ✅ Alembic Migrations
- ✅ Swagger API Documentation
- ✅ Automated Testing
- ✅ 123/123 Tests Passing

---

# Author

**Srikanth Bethamcharla**

**Smart Agriculture Farm Management System**
