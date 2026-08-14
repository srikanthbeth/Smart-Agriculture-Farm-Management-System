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

- **Python 3.10+**
- **FastAPI**
- **Uvicorn**
- **SQLAlchemy**
- **Pydantic**
- **PostgreSQL**
- **Alembic**
- **JWT Authentication**
- **Passlib / Bcrypt**
- **Pytest**
- **HTTPX**

---

# Project Structure

```text
Smart-Agriculture-Farm-Management-System/
│
├── routers/
│   ├── auth.py
│   ├── farms.py
│   ├── fields.py
│   ├── crops.py
│   ├── harvest.py
│   ├── sales.py
│   ├── irrigation.py
│   └── treatments.py
│
├── services/
│
├── tests/
│   ├── test_auth.py
│   ├── test_farms.py
│   ├── test_fields.py
│   ├── test_crops.py
│   ├── test_harvest.py
│   ├── test_sales.py
│   ├── test_irrigation.py
│   └── test_treatments.py
│
├── alembic/
│
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

Clone the repository:

git clone <your-github-repository-url>

Navigate to the project:

cd Smart-Agriculture-Farm-Management-System

Create a virtual environment:

python -m venv venv

Activate the virtual environment:

.\venv\Scripts\Activate.ps1

Install the required packages:

pip install -r requirements.txt
Database Configuration

The application uses PostgreSQL.

Database: smart_agriculture
Host: localhost
Port: 5432

Configure the database connection using your environment variables.

Example:

DATABASE_URL=postgresql://username:password@localhost:5432/smart_agriculture

Do not commit .env files or database passwords to GitHub.

Database Migration

Create a migration:

alembic revision --autogenerate -m "initial migration"

Apply the migration:

alembic upgrade head

Check the current migration:

alembic current

View migration history:

alembic history
Run the Application

Start the FastAPI application:

uvicorn main:app --reload

Application URL:

http://127.0.0.1:8000
Swagger API Documentation

Swagger UI:

http://127.0.0.1:8000/docs

ReDoc:

http://127.0.0.1:8000/redoc
Authentication

The application uses JWT-based authentication.

Authentication workflow:

Register
   ↓
Login
   ↓
Receive JWT Access Token
   ↓
Authorize in Swagger
   ↓
Access Protected APIs

Unauthenticated requests return:

401 Unauthorized

Example:

{
  "detail": "Not authenticated"
}
Application Workflow
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
Farm Management

The system provides functionality to manage farms.

Farm management includes:

Create Farm
Get Farm Details
Update Farm
Delete Farm
Farm Validation

Farms act as the main entity for managing agricultural fields and related activities.

Field Management

Fields are associated with farms.

Example field:

{
  "field_name": "North Field",
  "area": 20.0,
  "soil_type": "Loamy",
  "irrigation_type": "Drip"
}

Example response:

{
  "id": 53,
  "farm_id": 63,
  "field_name": "paymentsearch Field",
  "area": 20.0,
  "soil_type": "Loamy",
  "irrigation_type": "Drip",
  "status": "Active"
}

Field management allows farmers to maintain field information such as:

Field Name
Area
Soil Type
Irrigation Type
Field Status
Crop Management

Crops are associated with fields.

Example crop:

{
  "crop_name": "Rice",
  "crop_type": "Cereal",
  "planting_date": "2026-06-01",
  "expected_harvest_date": "2026-08-10",
  "seed_quantity": 50.0
}

Example response:

{
  "id": 40,
  "field_id": 53,
  "crop_name": "Rice",
  "crop_type": "Cereal",
  "planting_date": "2026-06-01",
  "expected_harvest_date": "2026-08-10",
  "seed_quantity": 50.0,
  "status": "Ready for Harvest"
}

Crop management includes:

Crop Creation
Crop Retrieval
Crop Updating
Crop Status Management
Crop Validation
Harvest Management

Harvest records are associated with crops.

Example harvest:

{
  "crop_id": 40,
  "harvest_date": "2026-08-10",
  "quantity": 100.0,
  "unit": "kg",
  "quality_grade": "A",
  "market_price": 50.0,
  "storage_location": "Main Warehouse"
}

Example response:

{
  "id": 19,
  "crop_id": 40,
  "harvest_date": "2026-08-10",
  "quantity": 100.0,
  "unit": "kg",
  "quality_grade": "A",
  "market_price": 50.0,
  "total_revenue": 5000.0,
  "remarks": null,
  "storage_location": "Main Warehouse"
}

Harvest management includes:

Harvest Creation
Harvest Retrieval
Quantity Management
Quality Grade
Market Price
Total Revenue Calculation
Storage Location
Harvest Validation
Sales Management

Sales are created from harvested crops.

Sales functionality includes:

Create Sale
Get Sales
Search Sales
Payment Status Filtering
Pagination
Sorting
Authentication
Input Validation

Example sale:

{
  "buyer_name": "ABC Traders",
  "harvest_id": 19,
  "price_per_unit": 100.0,
  "sale_date": "2026-08-12",
  "quantity": 20.0
}

Example response:

{
  "buyer_name": "ABC Traders",
  "harvest_id": 19,
  "price_per_unit": 100.0,
  "sale_date": "2026-08-12",
  "quantity": 20.0,
  "id": 8,
  "total_amount": 2000.0,
  "payment_status": "Paid"
}
Sales Search

Sales can be searched and filtered by payment status.

Example response:

{
  "total": 1,
  "page": 1,
  "limit": 10,
  "data": [
    {
      "buyer_name": "ABC Traders",
      "harvest_id": 19,
      "price_per_unit": 100.0,
      "sale_date": "2026-08-12",
      "quantity": 20.0,
      "id": 8,
      "total_amount": 2000.0,
      "payment_status": "Paid"
    }
  ]
}
Sales Pagination

Sales support pagination using page and limit parameters.

Example:

page=1
limit=1

Example response:

{
  "total": 2,
  "page": 1,
  "limit": 1,
  "data": [
    {
      "buyer_name": "Buyer Two",
      "harvest_id": 20,
      "price_per_unit": 100.0,
      "sale_date": "2026-08-12",
      "quantity": 10.0,
      "id": 10,
      "total_amount": 1000.0,
      "payment_status": "Paid"
    }
  ]
}
Sales Validation

Invalid page values are rejected.

Example:

page=0

Response:

400 Bad Request
{
  "detail": "page must be greater than 0"
}

Invalid limit values are rejected.

Example:

limit=101

Response:

400 Bad Request
{
  "detail": "limit must be between 1 and 100"
}
Sales Sorting

Supported sort fields:

buyer_name
harvest_id
id
payment_status
price_per_unit
quantity
sale_date
total_amount

Supported sort orders:

asc
desc

Invalid sort field returns:

400 Bad Request

Invalid sort order returns:

400 Bad Request

Example:

{
  "detail": "sort_order must be asc or desc"
}
Treatment Management

Treatments are associated with crops.

Treatment information includes:

Crop
Product Name
Product Type
Quantity
Applied Date
Cost
Remarks

Example fertilizer treatment:

{
  "crop_id": 50,
  "product_name": "NPK 20-20-20",
  "product_type": "Fertilizer",
  "quantity": 30.0,
  "applied_date": "2026-08-13",
  "cost": 2500.0,
  "remarks": "Balanced fertilizer"
}

Example pesticide treatment:

{
  "crop_id": 51,
  "product_name": "Neem Oil",
  "product_type": "Pesticide",
  "quantity": 5.0,
  "applied_date": "2026-08-13",
  "cost": 800.0,
  "remarks": "Organic pest control"
}
Treatment Validation

Treatment quantity must be greater than zero.

quantity > 0

Treatment cost must also be greater than zero.

cost > 0

Zero quantity returns:

422 Unprocessable Entity

Negative quantity returns:

422 Unprocessable Entity

Zero cost returns:

422 Unprocessable Entity

Negative cost returns:

422 Unprocessable Entity
Crop Treatment History

The system provides treatment history for individual crops.

Example response:

[
  {
    "id": 4,
    "crop_id": 45,
    "product_name": "Neem Oil",
    "product_type": "Pesticide",
    "quantity": 5.0,
    "applied_date": "2026-08-12",
    "cost": 700.0,
    "remarks": "Pest control"
  },
  {
    "id": 3,
    "crop_id": 45,
    "product_name": "Urea",
    "product_type": "Fertilizer",
    "quantity": 10.0,
    "applied_date": "2026-08-10",
    "cost": 500.0,
    "remarks": "First application"
  }
]

If the crop does not exist:

404 Not Found
{
  "detail": "Crop not found"
}
Error Handling

The application uses standard HTTP status codes:

200 OK
201 Created
204 No Content
400 Bad Request
401 Unauthorized
404 Not Found
409 Conflict
422 Unprocessable Entity

The API validates invalid input and returns appropriate error responses.

Testing

The project uses Pytest for automated testing.

Run all tests:

pytest -v

Run sales tests:

pytest tests/test_sales.py -v

Run treatment tests:

pytest tests/test_treatments.py -v
Test Results

All automated tests passed successfully.

123 passed, 2 warnings in 77.88s

Test summary:

Total Tests : 123
Passed      : 123
Failed      : 0
Warnings    : 2
Status      : PASSED
Test Coverage

The automated test suite covers:

Authentication
Farm Management
Field Management
Crop Management
Harvest Management
Sales Management
Irrigation Management
Treatment Management

Sales tests include:

Create Sale
Get Sales
Search Sales
Payment Status Search
Sales Pagination
Invalid Page
Invalid Limit
Invalid Sort Field
Invalid Sort Order
Ascending Sort
Unauthorized Get Sales
Unauthorized Create Sale

Treatment tests include:

Create Treatment
Get Treatments
Crop Treatment History
Zero Quantity Validation
Negative Quantity Validation
Zero Cost Validation
Negative Cost Validation
Non-existing Crop Validation
Fertilizer Treatment
Pesticide Treatment
Unauthorized Get Treatments
Unauthorized Create Treatment
Security

The application uses JWT authentication for protected APIs.

Sensitive information should be stored in environment variables.

The following files should not be committed to GitHub:

.env
venv/
__pycache__/
*.pyc
.pytest_cache/
Useful Commands

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

Start application:

uvicorn main:app --reload

Run all tests:

pytest -v
API Access

Application:

http://127.0.0.1:8000

Swagger:

http://127.0.0.1:8000/docs

ReDoc:

http://127.0.0.1:8000/redoc
Completed
✅ Authentication
✅ JWT Authorization
✅ Farm Management
✅ Field Management
✅ Crop Management
✅ Harvest Management
✅ Sales Management
✅ Sales Search and Filtering
✅ Sales Pagination
✅ Sales Sorting
✅ Irrigation Management
✅ Treatment Management
✅ Input Validation
✅ Error Handling
✅ PostgreSQL Database
✅ SQLAlchemy ORM
✅ Alembic Migrations
✅ Swagger API Documentation
✅ Automated Testing
✅ 123/123 Tests Passing

Author

Srikanth Bethamcharla

Smart Agriculture Farm Management System


