from conftest import get_auth_headers


# ============================================================
# HELPER: CREATE FARM
# ============================================================

def create_farm(client, headers, farm_name):

    response = client.post(
        "/farms",
        headers=headers,
        json={
            "farm_name": farm_name,
            "location": "Andhra Pradesh",
            "total_area": 100,
            "owner_name": "Harvest Owner",
            "status": "Active"
        }
    )

    assert response.status_code == 201, (
        f"Farm creation failed: "
        f"{response.status_code} - {response.text}"
    )

    return response.json()


# ============================================================
# HELPER: CREATE FIELD
# ============================================================

def create_field(client, headers, farm_id, field_name):

    response = client.post(
        "/fields",
        headers=headers,
        json={
            "farm_id": farm_id,
            "field_name": field_name,
            "area": 50,
            "soil_type": "Black Soil",
            "irrigation_type": "Drip",
            "status": "Active"
        }
    )

    assert response.status_code == 201, (
        f"Field creation failed: "
        f"{response.status_code} - {response.text}"
    )

    return response.json()


# ============================================================
# HELPER: CREATE CROP
# ============================================================

def create_crop(client, headers, field_id, crop_name):

    response = client.post(
        "/crops",
        headers=headers,
        json={
            "field_id": field_id,
            "crop_name": crop_name,
            "crop_type": "Cereal",
            "planting_date": "2026-01-01",
            "expected_harvest_date": "2026-12-01",
            "seed_quantity": 50,
            "status": "Ready for Harvest"
        }
    )

    assert response.status_code == 201, (
        f"Crop creation failed: "
        f"{response.status_code} - {response.text}"
    )

    return response.json()


# ============================================================
# HELPER: SETUP HARVEST DATA
# ============================================================

def setup_harvest_data(client, prefix):

    headers = get_auth_headers(
        client,
        f"{prefix}_admin",
        role="Admin"
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
        field["id"],
        f"{prefix} Crop"
    )

    return headers, farm, field, crop


# ============================================================
# HELPER: CREATE HARVEST
# ============================================================

def create_harvest(client, headers, crop_id, **overrides):

    payload = {
        "crop_id": crop_id,
        "harvest_date": "2026-08-10",
        "quantity": 100,
        "unit": "kg",
        "quality_grade": "A",
        "market_price": 2000,
        "total_revenue": 200000,
        "storage_location": "Warehouse A"
    }

    payload.update(overrides)

    response = client.post(
        "/harvests",
        headers=headers,
        json=payload
    )

    return response


# ============================================================
# CREATE HARVEST
# ============================================================

def test_create_harvest(client):

    headers, farm, field, crop = setup_harvest_data(
        client,
        "createharvest"
    )

    response = create_harvest(
        client,
        headers,
        crop["id"]
    )

    print("\nCREATE HARVEST STATUS:", response.status_code)
    print("CREATE HARVEST RESPONSE:", response.text)

    assert response.status_code == 201, (
        f"Harvest creation failed: "
        f"{response.status_code} - {response.text}"
    )

    data = response.json()

    assert data["crop_id"] == crop["id"]
    assert data["quantity"] == 100
    assert data["unit"] == "kg"
    assert data["quality_grade"] == "A"
    assert data["storage_location"] == "Warehouse A"


# ============================================================
# GET ALL HARVESTS
# ============================================================

def test_get_harvests(client):

    headers, farm, field, crop = setup_harvest_data(
        client,
        "getharvest"
    )

    create_response = create_harvest(
        client,
        headers,
        crop["id"]
    )

    assert create_response.status_code == 201, (
        f"Harvest creation failed: "
        f"{create_response.status_code} - "
        f"{create_response.text}"
    )

    response = client.get(
        "/harvests",
        headers=headers
    )

    print("\nGET HARVESTS STATUS:", response.status_code)
    print("GET HARVESTS RESPONSE:", response.text)

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ============================================================
# GET CROP HARVEST
# ============================================================

def test_get_crop_harvest(client):

    headers, farm, field, crop = setup_harvest_data(
        client,
        "cropharvest"
    )

    create_response = create_harvest(
        client,
        headers,
        crop["id"]
    )

    assert create_response.status_code == 201, (
        f"Harvest creation failed: "
        f"{create_response.status_code} - "
        f"{create_response.text}"
    )

    response = client.get(
        f"/crops/{crop['id']}/harvest",
        headers=headers
    )

    print("\nGET CROP HARVEST STATUS:", response.status_code)
    print("GET CROP HARVEST RESPONSE:", response.text)

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["crop_id"] == crop["id"]


# ============================================================
# ZERO HARVEST QUANTITY
# ============================================================

def test_zero_harvest_quantity(client):

    headers, farm, field, crop = setup_harvest_data(
        client,
        "zeroharvest"
    )

    response = create_harvest(
        client,
        headers,
        crop["id"],
        quantity=0,
        total_revenue=0
    )

    print("\nZERO HARVEST QUANTITY STATUS:", response.status_code)
    print("ZERO HARVEST QUANTITY RESPONSE:", response.text)

    assert response.status_code == 422


# ============================================================
# NEGATIVE HARVEST QUANTITY
# ============================================================

def test_negative_harvest_quantity(client):

    headers, farm, field, crop = setup_harvest_data(
        client,
        "negativeharvest"
    )

    response = create_harvest(
        client,
        headers,
        crop["id"],
        quantity=-10,
        total_revenue=-20000
    )

    print("\nNEGATIVE HARVEST QUANTITY STATUS:", response.status_code)
    print("NEGATIVE HARVEST QUANTITY RESPONSE:", response.text)

    assert response.status_code == 422


# ============================================================
# ZERO MARKET PRICE
# ============================================================

def test_zero_market_price(client):

    headers, farm, field, crop = setup_harvest_data(
        client,
        "zeroprice"
    )

    response = create_harvest(
        client,
        headers,
        crop["id"],
        market_price=0,
        total_revenue=0
    )

    print("\nZERO MARKET PRICE STATUS:", response.status_code)
    print("ZERO MARKET PRICE RESPONSE:", response.text)

    assert response.status_code == 422


# ============================================================
# NEGATIVE MARKET PRICE
# ============================================================

def test_negative_market_price(client):

    headers, farm, field, crop = setup_harvest_data(
        client,
        "negativeprice"
    )

    response = create_harvest(
        client,
        headers,
        crop["id"],
        market_price=-500,
        total_revenue=-50000
    )

    print("\nNEGATIVE MARKET PRICE STATUS:", response.status_code)
    print("NEGATIVE MARKET PRICE RESPONSE:", response.text)

    assert response.status_code == 422


# ============================================================
# NON-EXISTING CROP
# ============================================================

def test_harvest_non_existing_crop(client):

    headers = get_auth_headers(
        client,
        "harvestnonexistingcrop",
        role="Admin"
    )

    response = create_harvest(
        client,
        headers,
        999999
    )

    print("\nNON-EXISTING CROP STATUS:", response.status_code)
    print("NON-EXISTING CROP RESPONSE:", response.text)

    assert response.status_code == 404


# ============================================================
# INVALID HARVEST DATE
# ============================================================

def test_invalid_harvest_date(client):

    headers, farm, field, crop = setup_harvest_data(
        client,
        "invaliddate"
    )

    response = create_harvest(
        client,
        headers,
        crop["id"],
        harvest_date="2025-01-01"
    )

    print("\nINVALID HARVEST DATE STATUS:", response.status_code)
    print("INVALID HARVEST DATE RESPONSE:", response.text)

    assert response.status_code == 400


# ============================================================
# QUALITY GRADE A
# ============================================================

def test_quality_grade_a(client):

    headers, farm, field, crop = setup_harvest_data(
        client,
        "qualitya"
    )

    response = create_harvest(
        client,
        headers,
        crop["id"],
        quality_grade="A",
        market_price=2500,
        total_revenue=250000
    )

    print("\nQUALITY GRADE A STATUS:", response.status_code)
    print("QUALITY GRADE A RESPONSE:", response.text)

    assert response.status_code == 201

    data = response.json()

    assert data["quality_grade"] == "A"
    assert data["storage_location"] == "Warehouse A"


# ============================================================
# SEARCH BY QUALITY GRADE
# ============================================================

def test_search_harvests_by_quality_grade(client):

    headers, farm, field, crop = setup_harvest_data(
        client,
        "searchquality"
    )

    create_response = create_harvest(
        client,
        headers,
        crop["id"],
        quality_grade="A"
    )

    assert create_response.status_code == 201, (
        f"Harvest creation failed: "
        f"{create_response.status_code} - "
        f"{create_response.text}"
    )

    response = client.get(
        "/harvests/search",
        headers=headers,
        params={
            "quality_grade": "A"
        }
    )

    print("\nSEARCH HARVEST STATUS:", response.status_code)
    print("SEARCH HARVEST RESPONSE:", response.text)

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)
    assert "total" in data
    assert "page" in data
    assert "limit" in data
    assert "data" in data

    assert isinstance(data["data"], list)


# ============================================================
# PAGINATION
# ============================================================

def test_harvest_pagination(client):

    headers, farm, field, crop = setup_harvest_data(
        client,
        "pagination"
    )

    create_response = create_harvest(
        client,
        headers,
        crop["id"]
    )

    assert create_response.status_code == 201, (
        f"Harvest creation failed: "
        f"{create_response.status_code} - "
        f"{create_response.text}"
    )

    response = client.get(
        "/harvests/search",
        headers=headers,
        params={
            "page": 1,
            "limit": 10
        }
    )

    print("\nHARVEST PAGINATION STATUS:", response.status_code)
    print("HARVEST PAGINATION RESPONSE:", response.text)

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)
    assert data["page"] == 1
    assert data["limit"] == 10
    assert "total" in data
    assert "data" in data
    assert isinstance(data["data"], list)


# ============================================================
# INVALID PAGE
# ============================================================

def test_invalid_harvest_page(client):

    headers = get_auth_headers(
        client,
        "invalidpage",
        role="Admin"
    )

    response = client.get(
        "/harvests/search",
        headers=headers,
        params={
            "page": 0
        }
    )

    print("\nINVALID PAGE STATUS:", response.status_code)
    print("INVALID PAGE RESPONSE:", response.text)

    assert response.status_code == 400


# ============================================================
# INVALID LIMIT
# ============================================================

def test_invalid_harvest_limit(client):

    headers = get_auth_headers(
        client,
        "invalidlimit",
        role="Admin"
    )

    response = client.get(
        "/harvests/search",
        headers=headers,
        params={
            "limit": 101
        }
    )

    print("\nINVALID LIMIT STATUS:", response.status_code)
    print("INVALID LIMIT RESPONSE:", response.text)

    assert response.status_code == 400


# ============================================================
# NON-EXISTING CROP HARVEST HISTORY
# ============================================================

def test_get_harvest_for_non_existing_crop(client):

    headers = get_auth_headers(
        client,
        "nonexistingcrophistory",
        role="Admin"
    )

    response = client.get(
        "/crops/999999/harvest",
        headers=headers
    )

    print(
        "\nNON-EXISTING CROP HARVEST STATUS:",
        response.status_code
    )

    print(
        "NON-EXISTING CROP HARVEST RESPONSE:",
        response.text
    )

    assert response.status_code == 404


# ============================================================
# GET WITHOUT TOKEN
# ============================================================

def test_get_harvests_without_token(client):

    response = client.get(
        "/harvests"
    )

    print(
        "\nUNAUTHENTICATED GET HARVEST STATUS:",
        response.status_code
    )

    print(
        "UNAUTHENTICATED GET HARVEST RESPONSE:",
        response.text
    )

    assert response.status_code == 401


# ============================================================
# CREATE WITHOUT TOKEN
# ============================================================

def test_create_harvest_without_token(client):

    response = client.post(
        "/harvests",
        json={
            "crop_id": 1,
            "harvest_date": "2026-08-10",
            "quantity": 100,
            "unit": "kg",
            "quality_grade": "A",
            "market_price": 2000,
            "total_revenue": 200000,
            "storage_location": "Warehouse A"
        }
    )

    print(
        "\nUNAUTHENTICATED CREATE HARVEST STATUS:",
        response.status_code
    )

    print(
        "UNAUTHENTICATED CREATE HARVEST RESPONSE:",
        response.text
    )

    assert response.status_code == 401