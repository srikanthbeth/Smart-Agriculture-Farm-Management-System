from conftest import get_auth_headers


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def create_farm(client, headers, farm_name):

    response = client.post(
        "/farms",
        headers=headers,
        json={
            "farm_name": farm_name,
            "location": "Andhra Pradesh",
            "total_area": 100,
            "owner_name": "Sales Owner",
            "status": "Active"
        }
    )

    assert response.status_code == 201, (
        f"Farm creation failed: "
        f"{response.status_code} - {response.text}"
    )

    return response.json()


def create_field(client, headers, farm_id, field_name):

    response = client.post(
        f"/farms/{farm_id}/fields",
        headers=headers,
        json={
            "field_name": field_name,
            "area": 20,
            "soil_type": "Loamy",
            "irrigation_type": "Drip",
            "status": "Active"
        }
    )

    print("\nCREATE FIELD STATUS:", response.status_code)
    print("CREATE FIELD RESPONSE:", response.text)

    assert response.status_code in [200, 201], (
        f"Field creation failed: "
        f"{response.status_code} - {response.text}"
    )

    return response.json()
def create_crop(client, headers, field_id):

    response = client.post(
        "/crops",
        headers=headers,
        json={
            "field_id": field_id,
            "crop_name": "Rice",
            "crop_type": "Cereal",
            "planting_date": "2026-06-01",
            "expected_harvest_date": "2026-08-10",
            "seed_quantity": 50,
            "status": "Ready for Harvest"
        }
    )

    print("\nCREATE CROP STATUS:", response.status_code)
    print("CREATE CROP RESPONSE:", response.text)

    assert response.status_code == 201, (
        f"Crop creation failed: "
        f"{response.status_code} - {response.text}"
    )

    return response.json()


def create_harvest(client, headers, crop_id):
    response = client.post(
        "/harvests",
        headers=headers,
        json={
            "crop_id": crop_id,
            "harvest_date": "2026-08-10",
            "quantity": 100,
            "unit": "kg",
            "quality_grade": "A",
            "market_price": 50,
            "total_revenue": 5000,
            "storage_location": "Main Warehouse"
        }
    )

    print("\nCREATE HARVEST STATUS:", response.status_code)
    print("CREATE HARVEST RESPONSE:", response.text)

    assert response.status_code == 201, (
        f"Harvest creation failed: "
        f"{response.status_code} - {response.text}"
    )

    return response.json()


def setup_sales_data(client, prefix):

    headers = get_auth_headers(
        client,
        f"{prefix}_sales"
    )

    farm = create_farm(
        client,
        headers,
        f"{prefix} Farm"
    )

    field = create_field(
    client,
    headers,
    farm["id"],
    f"{prefix} Field"
)

    crop = create_crop(
        client,
        headers,
        field["id"]
    )

    harvest = create_harvest(
        client,
        headers,
        crop["id"]
    )

    return headers, farm, field, crop, harvest


def create_sale(
    client,
    headers,
    harvest_id,
    buyer_name="ABC Traders",
    quantity=20,
    price_per_unit=100,
    sale_date="2026-08-12",
    payment_status="Paid"
):

    response = client.post(
        "/sales",
        headers=headers,
        json={
            "harvest_id": harvest_id,
            "buyer_name": buyer_name,
            "quantity": quantity,
            "price_per_unit": price_per_unit,
            "sale_date": sale_date,
            "payment_status": payment_status
        }
    )

    return response


# ============================================================
# CREATE SALE
# ============================================================

def test_create_sale(client):

    headers, farm, field, crop, harvest = setup_sales_data(
        client,
        "createsale"
    )

    response = create_sale(
        client,
        headers,
        harvest["id"],
        buyer_name="ABC Traders",
        quantity=20,
        price_per_unit=100
    )

    print("\nCREATE SALE STATUS:", response.status_code)
    print("CREATE SALE RESPONSE:", response.text)

    assert response.status_code == 201

    data = response.json()

    assert data["harvest_id"] == harvest["id"]
    assert data["buyer_name"] == "ABC Traders"
    assert data["quantity"] == 20
    assert data["price_per_unit"] == 100
    assert data["total_amount"] == 2000


# ============================================================
# GET ALL SALES
# ============================================================

def test_get_sales(client):

    headers, farm, field, crop, harvest = setup_sales_data(
        client,
        "getsales"
    )

    create_sale(
        client,
        headers,
        harvest["id"]
    )

    response = client.get(
        "/sales",
        headers=headers
    )

    print("\nGET SALES STATUS:", response.status_code)
    print("GET SALES RESPONSE:", response.text)

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 1


# ============================================================
# GET SALE BY ID
# ============================================================

def test_get_sale_by_id(client):

    headers, farm, field, crop, harvest = setup_sales_data(
        client,
        "getsalebyid"
    )

    sale_response = create_sale(
        client,
        headers,
        harvest["id"]
    )

    assert sale_response.status_code == 201

    sale = sale_response.json()

    response = client.get(
        f"/sales/{sale['id']}",
        headers=headers
    )

    print("\nGET SALE BY ID STATUS:", response.status_code)
    print("GET SALE BY ID RESPONSE:", response.text)

    assert response.status_code == 200
    assert response.json()["id"] == sale["id"]


# ============================================================
# NON-EXISTING SALE
# ============================================================

def test_sale_non_existing():

    # This test is intentionally skipped from setup because
    # it only needs authentication.
    pass


def test_get_non_existing_sale(client):

    headers = get_auth_headers(
        client,
        "nonexistingsale"
    )

    response = client.get(
        "/sales/999999",
        headers=headers
    )

    print("\nNON-EXISTING SALE STATUS:", response.status_code)
    print("NON-EXISTING SALE RESPONSE:", response.text)

    assert response.status_code == 404
    assert response.json()["detail"] == "Sale not found"


# ============================================================
# NON-EXISTING HARVEST
# ============================================================

def test_sale_non_existing_harvest(client):

    headers = get_auth_headers(
        client,
        "nonexistingharvestsale"
    )

    response = create_sale(
        client,
        headers,
        999999
    )

    print("\nNON-EXISTING HARVEST STATUS:", response.status_code)
    print("NON-EXISTING HARVEST RESPONSE:", response.text)

    assert response.status_code == 404
    assert response.json()["detail"] == "Harvest not found"


# ============================================================
# SALE DATE BEFORE HARVEST DATE
# ============================================================

def test_sale_date_before_harvest(client):

    headers, farm, field, crop, harvest = setup_sales_data(
        client,
        "invalidsaledate"
    )

    response = create_sale(
        client,
        headers,
        harvest["id"],
        sale_date="2026-08-09"
    )

    print("\nINVALID SALE DATE STATUS:", response.status_code)
    print("INVALID SALE DATE RESPONSE:", response.text)

    assert response.status_code == 400

    assert response.json()["detail"] == (
        "Sale date cannot be before harvest date"
    )


# ============================================================
# ZERO QUANTITY
# ============================================================

def test_zero_sale_quantity(client):

    headers, farm, field, crop, harvest = setup_sales_data(
        client,
        "zerosalequantity"
    )

    response = create_sale(
        client,
        headers,
        harvest["id"],
        quantity=0
    )

    print("\nZERO SALE QUANTITY STATUS:", response.status_code)
    print("ZERO SALE QUANTITY RESPONSE:", response.text)

    assert response.status_code == 422


# ============================================================
# NEGATIVE QUANTITY
# ============================================================

def test_negative_sale_quantity(client):

    headers, farm, field, crop, harvest = setup_sales_data(
        client,
        "negativesalequantity"
    )

    response = create_sale(
        client,
        headers,
        harvest["id"],
        quantity=-10
    )

    print("\nNEGATIVE SALE QUANTITY STATUS:", response.status_code)
    print("NEGATIVE SALE QUANTITY RESPONSE:", response.text)

    assert response.status_code == 422


# ============================================================
# ZERO PRICE
# ============================================================

def test_zero_price_per_unit(client):

    headers, farm, field, crop, harvest = setup_sales_data(
        client,
        "zeroprice"
    )

    response = create_sale(
        client,
        headers,
        harvest["id"],
        price_per_unit=0
    )

    print("\nZERO PRICE STATUS:", response.status_code)
    print("ZERO PRICE RESPONSE:", response.text)

    assert response.status_code == 422


# ============================================================
# NEGATIVE PRICE
# ============================================================

def test_negative_price_per_unit(client):

    headers, farm, field, crop, harvest = setup_sales_data(
        client,
        "negativeprice"
    )

    response = create_sale(
        client,
        headers,
        harvest["id"],
        price_per_unit=-50
    )

    print("\nNEGATIVE PRICE STATUS:", response.status_code)
    print("NEGATIVE PRICE RESPONSE:", response.text)

    assert response.status_code == 422


# ============================================================
# OVER SELLING
# ============================================================

def test_overselling_harvest(client):

    headers, farm, field, crop, harvest = setup_sales_data(
        client,
        "overselling"
    )

    response = create_sale(
        client,
        headers,
        harvest["id"],
        quantity=101
    )

    print("\nOVERSELLING STATUS:", response.status_code)
    print("OVERSELLING RESPONSE:", response.text)

    assert response.status_code == 400

    assert "Insufficient harvested quantity" in (
        response.json()["detail"]
    )


# ============================================================
# SOLD QUANTITY CANNOT EXCEED REMAINING QUANTITY
# ============================================================

def test_multiple_sales_remaining_quantity(client):

    headers, farm, field, crop, harvest = setup_sales_data(
        client,
        "remainingsales"
    )

    first_sale = create_sale(
        client,
        headers,
        harvest["id"],
        buyer_name="Buyer One",
        quantity=60,
        price_per_unit=100
    )

    assert first_sale.status_code == 201

    second_sale = create_sale(
        client,
        headers,
        harvest["id"],
        buyer_name="Buyer Two",
        quantity=40,
        price_per_unit=120
    )

    assert second_sale.status_code == 201

    third_sale = create_sale(
        client,
        headers,
        harvest["id"],
        buyer_name="Buyer Three",
        quantity=1,
        price_per_unit=100
    )

    print("\nREMAINING QUANTITY STATUS:", third_sale.status_code)
    print("REMAINING QUANTITY RESPONSE:", third_sale.text)

    assert third_sale.status_code == 400

    assert "Insufficient harvested quantity" in (
        third_sale.json()["detail"]
    )


# ============================================================
# PAYMENT STATUS
# ============================================================

def test_payment_status(client):

    headers, farm, field, crop, harvest = setup_sales_data(
        client,
        "paymentstatus"
    )

    response = create_sale(
        client,
        headers,
        harvest["id"],
        payment_status="Pending"
    )

    print("\nPAYMENT STATUS:", response.status_code)
    print("PAYMENT RESPONSE:", response.text)

    assert response.status_code == 201
    assert response.json()["payment_status"] == "Pending"


# ============================================================
# BUYER SEARCH
# ============================================================

def test_search_sales_by_buyer(client):

    headers, farm, field, crop, harvest = setup_sales_data(
        client,
        "buyersearch"
    )

    create_sale(
        client,
        headers,
        harvest["id"],
        buyer_name="ABC Traders"
    )

    response = client.get(
        "/sales/search",
        headers=headers,
        params={
            "buyer": "ABC"
        }
    )

    print("\nBUYER SEARCH STATUS:", response.status_code)
    print("BUYER SEARCH RESPONSE:", response.text)

    assert response.status_code == 200

    data = response.json()

    assert "data" in data
    assert data["total"] >= 1


# ============================================================
# PAYMENT STATUS SEARCH
# ============================================================

def test_search_sales_by_payment_status(client):

    headers, farm, field, crop, harvest = setup_sales_data(
        client,
        "paymentsearch"
    )

    create_sale(
        client,
        headers,
        harvest["id"],
        payment_status="Paid"
    )

    response = client.get(
        "/sales/search",
        headers=headers,
        params={
            "payment_status": "Paid"
        }
    )

    print("\nPAYMENT SEARCH STATUS:", response.status_code)
    print("PAYMENT SEARCH RESPONSE:", response.text)

    assert response.status_code == 200

    data = response.json()

    assert "data" in data
    assert data["total"] >= 1


# ============================================================
# PAGINATION
# ============================================================

def test_sales_pagination(client):

    headers, farm, field, crop, harvest = setup_sales_data(
        client,
        "pagination"
    )

    create_sale(
        client,
        headers,
        harvest["id"],
        buyer_name="Buyer One",
        quantity=10
    )

    create_sale(
        client,
        headers,
        harvest["id"],
        buyer_name="Buyer Two",
        quantity=10
    )

    response = client.get(
        "/sales/search",
        headers=headers,
        params={
            "page": 1,
            "limit": 1
        }
    )

    print("\nSALES PAGINATION STATUS:", response.status_code)
    print("SALES PAGINATION RESPONSE:", response.text)

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 1
    assert data["limit"] == 1
    assert data["total"] >= 2
    assert len(data["data"]) == 1


# ============================================================
# INVALID PAGE
# ============================================================

def test_invalid_sales_page(client):

    headers = get_auth_headers(
        client,
        "invalidsalespage"
    )

    response = client.get(
        "/sales/search",
        headers=headers,
        params={
            "page": 0
        }
    )

    print("\nINVALID PAGE STATUS:", response.status_code)
    print("INVALID PAGE RESPONSE:", response.text)

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "page must be greater than 0"
    )


# ============================================================
# INVALID LIMIT
# ============================================================

def test_invalid_sales_limit(client):

    headers = get_auth_headers(
        client,
        "invalidsaleslimit"
    )

    response = client.get(
        "/sales/search",
        headers=headers,
        params={
            "limit": 101
        }
    )

    print("\nINVALID LIMIT STATUS:", response.status_code)
    print("INVALID LIMIT RESPONSE:", response.text)

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "limit must be between 1 and 100"
    )


# ============================================================
# INVALID SORT FIELD
# ============================================================

def test_invalid_sales_sort_field(client):

    headers = get_auth_headers(
        client,
        "invalidsortfield"
    )

    response = client.get(
        "/sales/search",
        headers=headers,
        params={
            "sort_by": "invalid_field"
        }
    )

    print("\nINVALID SORT FIELD STATUS:", response.status_code)
    print("INVALID SORT FIELD RESPONSE:", response.text)

    assert response.status_code == 400

    assert "Invalid sort_by" in (
        response.json()["detail"]
    )


# ============================================================
# INVALID SORT ORDER
# ============================================================

def test_invalid_sales_sort_order(client):

    headers = get_auth_headers(
        client,
        "invalidsortorder"
    )

    response = client.get(
        "/sales/search",
        headers=headers,
        params={
            "sort_order": "invalid"
        }
    )

    print("\nINVALID SORT ORDER STATUS:", response.status_code)
    print("INVALID SORT ORDER RESPONSE:", response.text)

    assert response.status_code == 400

    assert response.json()["detail"] == (
        "sort_order must be asc or desc"
    )


# ============================================================
# SORT ASCENDING
# ============================================================

def test_sales_sort_ascending(client):

    headers, farm, field, crop, harvest = setup_sales_data(
        client,
        "sortasc"
    )

    create_sale(
        client,
        headers,
        harvest["id"],
        buyer_name="Buyer B",
        quantity=20
    )

    create_sale(
        client,
        headers,
        harvest["id"],
        buyer_name="Buyer A",
        quantity=10
    )

    response = client.get(
        "/sales/search",
        headers=headers,
        params={
            "sort_by": "buyer_name",
            "sort_order": "asc"
        }
    )

    print("\nSORT ASC STATUS:", response.status_code)
    print("SORT ASC RESPONSE:", response.text)

    assert response.status_code == 200

    data = response.json()

    assert "data" in data


# ============================================================
# UNAUTHENTICATED GET
# ============================================================

def test_get_sales_without_token(client):

    response = client.get(
        "/sales"
    )

    print("\nUNAUTHENTICATED GET SALES STATUS:", response.status_code)
    print(
        "UNAUTHENTICATED GET SALES RESPONSE:",
        response.text
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


# ============================================================
# UNAUTHENTICATED CREATE
# ============================================================

def test_create_sale_without_token(client):

    response = client.post(
        "/sales",
        json={
            "harvest_id": 1,
            "buyer_name": "Unauthorized Buyer",
            "quantity": 10,
            "price_per_unit": 100,
            "sale_date": "2026-08-12",
            "payment_status": "Paid"
        }
    )

    print(
        "\nUNAUTHENTICATED CREATE SALE STATUS:",
        response.status_code
    )

    print(
        "UNAUTHENTICATED CREATE SALE RESPONSE:",
        response.text
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"