# tests/test_fields.py


# ============================================================
# HELPER - REGISTER / LOGIN FARM MANAGER
# ============================================================

def get_auth_headers(client):

    register_response = client.post(
        "/auth/register",
        json={
            "username": "fieldmanager",
            "email": "fieldmanager@example.com",
            "password": "Test@12345",
            "role": "Farm Manager"
        }
    )

    assert register_response.status_code in [200, 201, 400]

    login_response = client.post(
        "/auth/login",
        json={
            "username": "fieldmanager",
            "password": "Test@12345"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


# ============================================================
# HELPER - CREATE FARM
# ============================================================

def create_farm(client, headers, farm_name="Field Test Farm", area=100):

    response = client.post(
        "/farms",
        headers=headers,
        json={
            "farm_name": farm_name,
            "location": "Andhra Pradesh",
            "total_area": area,
            "owner_name": "Test Owner",
            "status": "Active"
        }
    )

    assert response.status_code in [200, 201]

    return response.json()["id"]


# ============================================================
# TEST 1 - CREATE FIELD
# ============================================================

def test_create_field(client):

    headers = get_auth_headers(client)

    farm_id = create_farm(
        client,
        headers,
        farm_name="Create Field Farm",
        area=100
    )

    response = client.post(
        f"/farms/{farm_id}/fields",
        headers=headers,
        json={
            "field_name": "Field A",
            "area": 40,
            "soil_type": "Black Soil",
            "irrigation_type": "Drip",
            "status": "Active"
        }
    )

    print("\nCREATE FIELD STATUS:", response.status_code)
    print("CREATE FIELD RESPONSE:", response.text)

    assert response.status_code in [200, 201]

    data = response.json()

    assert "id" in data
    assert data["farm_id"] == farm_id
    assert data["field_name"] == "Field A"
    assert data["area"] == 40
    assert data["soil_type"] == "Black Soil"
    assert data["irrigation_type"] == "Drip"
    assert data["status"] == "Active"


# ============================================================
# TEST 2 - GET FIELDS FOR FARM
# ============================================================

def test_get_farm_fields(client):

    headers = get_auth_headers(client)

    farm_id = create_farm(
        client,
        headers,
        farm_name="Get Fields Farm",
        area=100
    )

    create_response = client.post(
        f"/farms/{farm_id}/fields",
        headers=headers,
        json={
            "field_name": "Field B",
            "area": 30,
            "soil_type": "Red Soil",
            "irrigation_type": "Sprinkler",
            "status": "Active"
        }
    )

    assert create_response.status_code in [200, 201]

    response = client.get(
        f"/farms/{farm_id}/fields",
        headers=headers
    )

    print("\nGET FIELDS STATUS:", response.status_code)
    print("GET FIELDS RESPONSE:", response.text)

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["farm_id"] == farm_id


# ============================================================
# TEST 3 - FIELD AREA CANNOT EXCEED FARM AVAILABLE AREA
# ============================================================

def test_field_area_exceeds_farm_area(client):

    headers = get_auth_headers(client)

    farm_id = create_farm(
        client,
        headers,
        farm_name="Area Validation Farm",
        area=100
    )

    response = client.post(
        f"/farms/{farm_id}/fields",
        headers=headers,
        json={
            "field_name": "Too Large Field",
            "area": 150,
            "soil_type": "Black Soil",
            "irrigation_type": "Drip",
            "status": "Active"
        }
    )

    print(
        "\nFIELD AREA EXCEEDS FARM STATUS:",
        response.status_code
    )

    print(
        "FIELD AREA EXCEEDS FARM RESPONSE:",
        response.text
    )

    assert response.status_code in [400, 409, 422]


# ============================================================
# TEST 4 - FIELD AREA CANNOT EXCEED AVAILABLE AREA
# ============================================================

def test_field_area_exceeds_remaining_available_area(client):

    headers = get_auth_headers(client)

    farm_id = create_farm(
        client,
        headers,
        farm_name="Available Area Farm",
        area=100
    )

    # First field uses 70
    first_response = client.post(
        f"/farms/{farm_id}/fields",
        headers=headers,
        json={
            "field_name": "First Field",
            "area": 70,
            "soil_type": "Black Soil",
            "irrigation_type": "Drip",
            "status": "Active"
        }
    )

    assert first_response.status_code in [200, 201]

    # Only 30 area remains
    second_response = client.post(
        f"/farms/{farm_id}/fields",
        headers=headers,
        json={
            "field_name": "Second Field",
            "area": 40,
            "soil_type": "Red Soil",
            "irrigation_type": "Sprinkler",
            "status": "Active"
        }
    )

    print(
        "\nREMAINING AREA STATUS:",
        second_response.status_code
    )

    print(
        "REMAINING AREA RESPONSE:",
        second_response.text
    )

    assert second_response.status_code in [400, 409, 422]


# ============================================================
# TEST 5 - NEGATIVE FIELD AREA
# ============================================================

def test_negative_field_area(client):

    headers = get_auth_headers(client)

    farm_id = create_farm(
        client,
        headers,
        farm_name="Negative Field Area Farm",
        area=100
    )

    response = client.post(
        f"/farms/{farm_id}/fields",
        headers=headers,
        json={
            "field_name": "Negative Field",
            "area": -10,
            "soil_type": "Black Soil",
            "irrigation_type": "Drip",
            "status": "Active"
        }
    )

    print(
        "\nNEGATIVE FIELD AREA STATUS:",
        response.status_code
    )

    print(
        "NEGATIVE FIELD AREA RESPONSE:",
        response.text
    )

    assert response.status_code == 422


# ============================================================
# TEST 6 - ZERO FIELD AREA
# ============================================================

def test_zero_field_area(client):

    headers = get_auth_headers(client)

    farm_id = create_farm(
        client,
        headers,
        farm_name="Zero Field Area Farm",
        area=100
    )

    response = client.post(
        f"/farms/{farm_id}/fields",
        headers=headers,
        json={
            "field_name": "Zero Field",
            "area": 0,
            "soil_type": "Black Soil",
            "irrigation_type": "Drip",
            "status": "Active"
        }
    )

    assert response.status_code == 422


# ============================================================
# TEST 7 - DUPLICATE FIELD NAME
# ============================================================

def test_duplicate_field(client):

    headers = get_auth_headers(client)

    farm_id = create_farm(
        client,
        headers,
        farm_name="Duplicate Field Farm",
        area=100
    )

    field_data = {
        "field_name": "Duplicate Field",
        "area": 20,
        "soil_type": "Black Soil",
        "irrigation_type": "Drip",
        "status": "Active"
    }

    first_response = client.post(
        f"/farms/{farm_id}/fields",
        headers=headers,
        json=field_data
    )

    assert first_response.status_code in [200, 201]

    second_response = client.post(
        f"/farms/{farm_id}/fields",
        headers=headers,
        json=field_data
    )

    print(
        "\nDUPLICATE FIELD STATUS:",
        second_response.status_code
    )

    print(
        "DUPLICATE FIELD RESPONSE:",
        second_response.text
    )

    assert second_response.status_code in [400, 409]


# ============================================================
# TEST 8 - INVALID FIELD STATUS
# ============================================================

def test_invalid_field_status(client):

    headers = get_auth_headers(client)

    farm_id = create_farm(
        client,
        headers,
        farm_name="Invalid Field Status Farm",
        area=100
    )

    response = client.post(
        f"/farms/{farm_id}/fields",
        headers=headers,
        json={
            "field_name": "Invalid Status Field",
            "area": 20,
            "soil_type": "Black Soil",
            "irrigation_type": "Drip",
            "status": "Invalid"
        }
    )

    print(
        "\nINVALID FIELD STATUS:",
        response.status_code
    )

    print(
        "INVALID FIELD STATUS RESPONSE:",
        response.text
    )

    assert response.status_code == 422


# ============================================================
# TEST 9 - NON-EXISTING FARM
# ============================================================

def test_create_field_for_non_existing_farm(client):

    headers = get_auth_headers(client)

    response = client.post(
        "/farms/999999/fields",
        headers=headers,
        json={
            "field_name": "Orphan Field",
            "area": 20,
            "soil_type": "Black Soil",
            "irrigation_type": "Drip",
            "status": "Active"
        }
    )

    print(
        "\nNON-EXISTING FARM STATUS:",
        response.status_code
    )

    print(
        "NON-EXISTING FARM RESPONSE:",
        response.text
    )

    assert response.status_code == 404


# ============================================================
# TEST 10 - GET FIELDS FOR NON-EXISTING FARM
# ============================================================

def test_get_fields_for_non_existing_farm(client):

    headers = get_auth_headers(client)

    response = client.get(
        "/farms/999999/fields",
        headers=headers
    )

    print(
        "\nGET NON-EXISTING FARM FIELDS:",
        response.status_code
    )

    print(
        "RESPONSE:",
        response.text
    )

    assert response.status_code == 404


# ============================================================
# TEST 11 - INACTIVE FIELD CAN BE CREATED
# ============================================================

def test_create_inactive_field(client):

    headers = get_auth_headers(client)

    farm_id = create_farm(
        client,
        headers,
        farm_name="Inactive Field Farm",
        area=100
    )

    response = client.post(
        f"/farms/{farm_id}/fields",
        headers=headers,
        json={
            "field_name": "Inactive Field",
            "area": 20,
            "soil_type": "Black Soil",
            "irrigation_type": "None",
            "status": "Inactive"
        }
    )

    print(
        "\nINACTIVE FIELD STATUS:",
        response.status_code
    )

    print(
        "INACTIVE FIELD RESPONSE:",
        response.text
    )

    assert response.status_code in [200, 201]


# ============================================================
# TEST 12 - UNDER MAINTENANCE FIELD
# ============================================================

def test_create_maintenance_field(client):

    headers = get_auth_headers(client)

    farm_id = create_farm(
        client,
        headers,
        farm_name="Maintenance Field Farm",
        area=100
    )

    response = client.post(
        f"/farms/{farm_id}/fields",
        headers=headers,
        json={
            "field_name": "Maintenance Field",
            "area": 20,
            "soil_type": "Red Soil",
            "irrigation_type": "Canal",
            "status": "Under Maintenance"
        }
    )

    print(
        "\nMAINTENANCE FIELD STATUS:",
        response.status_code
    )

    print(
        "MAINTENANCE FIELD RESPONSE:",
        response.text
    )

    assert response.status_code in [200, 201]