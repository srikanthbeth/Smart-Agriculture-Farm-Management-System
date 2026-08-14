from datetime import date

from fastapi.testclient import TestClient


# ============================================================
# AUTHENTICATION
# ============================================================

def create_user_and_login(client: TestClient, username: str):
    register_response = client.post(
        "/auth/register",
        json={
            "username": username,
            "email": f"{username}@example.com",
            "password": "Test@12345",
            "role": "Farm Manager",
        },
    )

    # User may already exist in some test database situations.
    assert register_response.status_code in [201, 400, 409], (
        f"Register failed: "
        f"{register_response.status_code} - {register_response.text}"
    )

    login_response = client.post(
        "/auth/login",
        json={
            "username": username,
            "password": "Test@12345",
        },
    )

    # If your login API uses email instead of username, try email.
    if login_response.status_code == 422:
        login_response = client.post(
            "/auth/login",
            json={
                "email": f"{username}@example.com",
                "password": "Test@12345",
            },
        )

    assert login_response.status_code == 200, (
        f"Login failed: "
        f"{login_response.status_code} - {login_response.text}"
    )

    return login_response.json()["access_token"]


def get_auth_headers(token):
    return {
        "Authorization": f"Bearer {token}"
    }


# ============================================================
# FARM
# ============================================================

def create_farm(client, token, farm_name):
    response = client.post(
        "/farms",
        headers=get_auth_headers(token),
        json={
            "farm_name": farm_name,
            "location": "Andhra Pradesh",
            "total_area": 100,
            "owner_name": "Test Owner",
            "status": "Active",
        },
    )

    assert response.status_code == 201, (
        f"Create farm failed: "
        f"{response.status_code} - {response.text}"
    )

    return response.json()


# ============================================================
# FIELD
# ============================================================

def create_field(client, token, farm_id, field_name, status="Active"):
    response = client.post(
        f"/farms/{farm_id}/fields",
        headers=get_auth_headers(token),
        json={
            "field_name": field_name,
            "area": 40,
            "soil_type": "Black Soil",
            "irrigation_type": "Drip",
            "status": status,
        },
    )

    assert response.status_code == 201, (
        f"Create field failed: "
        f"{response.status_code} - {response.text}"
    )

    return response.json()


# ============================================================
# CROP
# ============================================================

def create_crop(client, token, field_id, crop_name):
    response = client.post(
        "/crops",
        headers=get_auth_headers(token),
        json={
            "field_id": field_id,
            "crop_name": crop_name,
            "crop_type": "Cereal",
            "planting_date": "2026-08-01",
            "expected_harvest_date": "2026-12-01",
            "seed_quantity": 50,
            "status": "Growing",
        },
    )

    assert response.status_code == 201, (
        f"Create crop failed: "
        f"{response.status_code} - {response.text}"
    )

    return response.json()


# ============================================================
# COMPLETE IRRIGATION SETUP
# ============================================================

def setup_irrigation_data(client, prefix):
    token = create_user_and_login(
        client,
        f"irrigation_{prefix}"
    )

    farm = create_farm(
        client,
        token,
        f"{prefix} Farm"
    )

    field = create_field(
        client,
        token,
        farm["id"],
        f"{prefix} Field"
    )

    crop = create_crop(
        client,
        token,
        field["id"],
        f"{prefix} Crop"
    )

    return token, farm, field, crop


# ============================================================
# TEST 1 - CREATE IRRIGATION
# ============================================================

def test_create_irrigation(client):

    token, farm, field, crop = setup_irrigation_data(
        client,
        "createirrigation"
    )

    response = client.post(
        "/irrigation",
        headers=get_auth_headers(token),
        json={
            "field_id": field["id"],
            "irrigation_date": "2026-08-13",
            "water_quantity": 100,
            "duration_minutes": 30,
            "irrigation_status": "Completed",
            "remarks": "Morning irrigation",
        },
    )

    print("\nCREATE IRRIGATION STATUS:", response.status_code)
    print("CREATE IRRIGATION RESPONSE:", response.text)

    assert response.status_code == 201
    data = response.json()

    assert data["field_id"] == field["id"]
    assert data["water_quantity"] == 100
    assert data["duration_minutes"] == 30


# ============================================================
# TEST 2 - GET ALL IRRIGATION
# ============================================================

def test_get_irrigation(client):

    token, farm, field, crop = setup_irrigation_data(
        client,
        "getirrigation"
    )

    create_response = client.post(
        "/irrigation",
        headers=get_auth_headers(token),
        json={
            "field_id": field["id"],
            "irrigation_date": "2026-08-13",
            "water_quantity": 150,
            "duration_minutes": 45,
            "irrigation_status": "Completed",
            "remarks": "Regular irrigation",
        },
    )

    assert create_response.status_code == 201

    response = client.get(
        "/irrigation",
        headers=get_auth_headers(token)
    )

    print("\nGET IRRIGATION STATUS:", response.status_code)
    print("GET IRRIGATION RESPONSE:", response.text)

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ============================================================
# TEST 3 - FIELD IRRIGATION HISTORY
# ============================================================

def test_get_field_irrigation_history(client):

    token, farm, field, crop = setup_irrigation_data(
        client,
        "fieldhistory"
    )

    client.post(
        "/irrigation",
        headers=get_auth_headers(token),
        json={
            "field_id": field["id"],
            "irrigation_date": "2026-08-10",
            "water_quantity": 100,
            "duration_minutes": 30,
            "irrigation_status": "Completed",
            "remarks": "First irrigation",
        },
    )

    client.post(
        "/irrigation",
        headers=get_auth_headers(token),
        json={
            "field_id": field["id"],
            "irrigation_date": "2026-08-12",
            "water_quantity": 120,
            "duration_minutes": 35,
            "irrigation_status": "Completed",
            "remarks": "Second irrigation",
        },
    )

    response = client.get(
        f"/fields/{field['id']}/irrigation",
        headers=get_auth_headers(token)
    )

    print(
        "\nFIELD IRRIGATION HISTORY STATUS:",
        response.status_code
    )
    print(
        "FIELD IRRIGATION HISTORY RESPONSE:",
        response.text
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 2


# ============================================================
# TEST 4 - ZERO WATER
# ============================================================

def test_zero_water_quantity(client):

    token, farm, field, crop = setup_irrigation_data(
        client,
        "zerowater"
    )

    response = client.post(
        "/irrigation",
        headers=get_auth_headers(token),
        json={
            "field_id": field["id"],
            "irrigation_date": "2026-08-13",
            "water_quantity": 0,
            "duration_minutes": 30,
            "irrigation_status": "Completed",
            "remarks": "Invalid water quantity",
        },
    )

    print("\nZERO WATER STATUS:", response.status_code)
    print("ZERO WATER RESPONSE:", response.text)

    assert response.status_code == 422


# ============================================================
# TEST 5 - NEGATIVE WATER
# ============================================================

def test_negative_water_quantity(client):

    token, farm, field, crop = setup_irrigation_data(
        client,
        "negativewater"
    )

    response = client.post(
        "/irrigation",
        headers=get_auth_headers(token),
        json={
            "field_id": field["id"],
            "irrigation_date": "2026-08-13",
            "water_quantity": -10,
            "duration_minutes": 30,
            "irrigation_status": "Completed",
            "remarks": "Invalid water quantity",
        },
    )

    print("\nNEGATIVE WATER STATUS:", response.status_code)
    print("NEGATIVE WATER RESPONSE:", response.text)

    assert response.status_code == 422


# ============================================================
# TEST 6 - ZERO DURATION
# ============================================================

def test_zero_duration(client):

    token, farm, field, crop = setup_irrigation_data(
        client,
        "zeroduration"
    )

    response = client.post(
        "/irrigation",
        headers=get_auth_headers(token),
        json={
            "field_id": field["id"],
            "irrigation_date": "2026-08-13",
            "water_quantity": 100,
            "duration_minutes": 0,
            "irrigation_status": "Completed",
            "remarks": "Invalid duration",
        },
    )

    print("\nZERO DURATION STATUS:", response.status_code)
    print("ZERO DURATION RESPONSE:", response.text)

    assert response.status_code == 422


# ============================================================
# TEST 7 - NEGATIVE DURATION
# ============================================================

def test_negative_duration(client):

    token, farm, field, crop = setup_irrigation_data(
        client,
        "negativeduration"
    )

    response = client.post(
        "/irrigation",
        headers=get_auth_headers(token),
        json={
            "field_id": field["id"],
            "irrigation_date": "2026-08-13",
            "water_quantity": 100,
            "duration_minutes": -20,
            "irrigation_status": "Completed",
            "remarks": "Invalid duration",
        },
    )

    print("\nNEGATIVE DURATION STATUS:", response.status_code)
    print("NEGATIVE DURATION RESPONSE:", response.text)

    assert response.status_code == 422


# ============================================================
# TEST 8 - NON-EXISTING FIELD
# ============================================================

def test_irrigation_non_existing_field(client):

    token = create_user_and_login(
        client,
        "irrigation_nonexisting"
    )

    response = client.post(
        "/irrigation",
        headers=get_auth_headers(token),
        json={
            "field_id": 999999,
            "irrigation_date": "2026-08-13",
            "water_quantity": 100,
            "duration_minutes": 30,
            "irrigation_status": "Completed",
            "remarks": "Invalid field",
        },
    )

    print(
        "\nNON-EXISTING FIELD STATUS:",
        response.status_code
    )
    print(
        "NON-EXISTING FIELD RESPONSE:",
        response.text
    )

    assert response.status_code == 404


# ============================================================
# TEST 9 - INACTIVE FIELD
# ============================================================

def test_irrigation_inactive_field(client):

    token = create_user_and_login(
        client,
        "irrigationinactive"
    )

    farm = create_farm(
        client,
        token,
        "Inactive Irrigation Farm"
    )

    field = create_field(
        client,
        token,
        farm["id"],
        "Inactive Irrigation Field",
        "Inactive"
    )

    response = client.post(
        "/irrigation",
        headers=get_auth_headers(token),
        json={
            "field_id": field["id"],
            "irrigation_date": "2026-08-13",
            "water_quantity": 100,
            "duration_minutes": 30,
            "irrigation_status": "Completed",
            "remarks": "Inactive field irrigation",
        },
    )

    print(
        "\nINACTIVE FIELD IRRIGATION STATUS:",
        response.status_code
    )
    print(
        "INACTIVE FIELD IRRIGATION RESPONSE:",
        response.text
    )

    assert response.status_code in [400, 404]


# ============================================================
# TEST 10 - MAINTENANCE FIELD
# ============================================================

def test_irrigation_maintenance_field(client):

    token = create_user_and_login(
        client,
        "irrigationmaintenance"
    )

    farm = create_farm(
        client,
        token,
        "Maintenance Irrigation Farm"
    )

    field = create_field(
        client,
        token,
        farm["id"],
        "Maintenance Irrigation Field",
        "Under Maintenance"
    )

    response = client.post(
        "/irrigation",
        headers=get_auth_headers(token),
        json={
            "field_id": field["id"],
            "irrigation_date": "2026-08-13",
            "water_quantity": 100,
            "duration_minutes": 30,
            "irrigation_status": "Completed",
            "remarks": "Maintenance field irrigation",
        },
    )

    print(
        "\nMAINTENANCE FIELD IRRIGATION STATUS:",
        response.status_code
    )
    print(
        "MAINTENANCE FIELD IRRIGATION RESPONSE:",
        response.text
    )

    assert response.status_code in [400, 404]


# ============================================================
# TEST 11 - HISTORY FOR NON-EXISTING FIELD
# ============================================================

def test_get_irrigation_for_non_existing_field(client):

    token = create_user_and_login(
        client,
        "irrigationhistorymissing"
    )

    response = client.get(
        "/fields/999999/irrigation",
        headers=get_auth_headers(token)
    )

    print(
        "\nNON-EXISTING FIELD HISTORY STATUS:",
        response.status_code
    )
    print(
        "NON-EXISTING FIELD HISTORY RESPONSE:",
        response.text
    )

    assert response.status_code == 404


# ============================================================
# TEST 12 - WITHOUT TOKEN
# ============================================================

def test_irrigation_without_token(client):

    response = client.post(
        "/irrigation",
        json={
            "field_id": 1,
            "irrigation_date": "2026-08-13",
            "water_quantity": 100,
            "duration_minutes": 30,
            "irrigation_status": "Completed",
            "remarks": "No authentication",
        },
    )

    print(
        "\nUNAUTHENTICATED IRRIGATION STATUS:",
        response.status_code
    )
    print(
        "UNAUTHENTICATED IRRIGATION RESPONSE:",
        response.text
    )

    assert response.status_code == 401