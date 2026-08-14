# tests/test_farms.py


# ============================================================
# HELPER - GET AUTHENTICATION TOKEN
# ============================================================

def get_auth_headers(client):

    register_response = client.post(
        "/auth/register",
        json={
            "username": "farmmanager",
            "email": "farmmanager@example.com",
            "password": "Test@12345",
            "role": "Farm Manager"
        }
    )

    # Registration may already exist in some test environments.
    assert register_response.status_code in [200, 201, 400]

    login_response = client.post(
        "/auth/login",
        json={
            "username": "farmmanager",
            "password": "Test@12345"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


# ============================================================
# TEST 1 - CREATE FARM
# ============================================================

def test_create_farm(client):

    headers = get_auth_headers(client)

    response = client.post(
        "/farms",
        headers=headers,
        json={
            "farm_name": "Green Valley Farm",
            "location": "Andhra Pradesh",
            "total_area": 100,
            "owner_name": "John Farmer",
            "status": "Active"
        }
    )

    print("\nCREATE FARM STATUS:", response.status_code)
    print("CREATE FARM RESPONSE:", response.text)

    assert response.status_code in [200, 201]

    data = response.json()

    assert "id" in data
    assert data["farm_name"] == "Green Valley Farm"
    assert data["location"] == "Andhra Pradesh"
    assert data["total_area"] == 100
    assert data["owner_name"] == "John Farmer"
    assert data["status"] == "Active"


# ============================================================
# TEST 2 - GET ALL FARMS
# ============================================================

def test_get_farms(client):

    headers = get_auth_headers(client)

    # Create farm first
    create_response = client.post(
        "/farms",
        headers=headers,
        json={
            "farm_name": "Sunrise Farm",
            "location": "Tirupati",
            "total_area": 50,
            "owner_name": "Farmer One",
            "status": "Active"
        }
    )

    assert create_response.status_code in [200, 201]

    # Get farms
    response = client.get(
        "/farms",
        headers=headers
    )

    print("\nGET FARMS STATUS:", response.status_code)
    print("GET FARMS RESPONSE:", response.text)

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, (list, dict))


# ============================================================
# TEST 3 - GET FARM BY ID
# ============================================================

def test_get_farm_by_id(client):

    headers = get_auth_headers(client)

    create_response = client.post(
        "/farms",
        headers=headers,
        json={
            "farm_name": "Farm By ID",
            "location": "Kadapa",
            "total_area": 75,
            "owner_name": "Test Owner",
            "status": "Active"
        }
    )

    assert create_response.status_code in [200, 201]

    farm_id = create_response.json()["id"]

    response = client.get(
        f"/farms/{farm_id}",
        headers=headers
    )

    print("\nGET FARM STATUS:", response.status_code)
    print("GET FARM RESPONSE:", response.text)

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == farm_id
    assert data["farm_name"] == "Farm By ID"


# ============================================================
# TEST 4 - GET NON-EXISTING FARM
# ============================================================

def test_get_non_existing_farm(client):

    headers = get_auth_headers(client)

    response = client.get(
        "/farms/999999",
        headers=headers
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
# TEST 5 - UPDATE FARM
# ============================================================

def test_update_farm(client):

    headers = get_auth_headers(client)

    create_response = client.post(
        "/farms",
        headers=headers,
        json={
            "farm_name": "Old Farm Name",
            "location": "Nellore",
            "total_area": 100,
            "owner_name": "Old Owner",
            "status": "Active"
        }
    )

    assert create_response.status_code in [200, 201]

    farm_id = create_response.json()["id"]

    response = client.put(
        f"/farms/{farm_id}",
        headers=headers,
        json={
            "farm_name": "Updated Farm Name",
            "location": "Nellore",
            "total_area": 120,
            "owner_name": "Updated Owner",
            "status": "Active"
        }
    )

    print("\nUPDATE FARM STATUS:", response.status_code)
    print("UPDATE FARM RESPONSE:", response.text)

    assert response.status_code == 200

    data = response.json()

    assert data["farm_name"] == "Updated Farm Name"
    assert data["total_area"] == 120


# ============================================================
# TEST 6 - NEGATIVE FARM AREA
# ============================================================

def test_negative_farm_area(client):

    headers = get_auth_headers(client)

    response = client.post(
        "/farms",
        headers=headers,
        json={
            "farm_name": "Invalid Area Farm",
            "location": "Chittoor",
            "total_area": -10,
            "owner_name": "Test Owner",
            "status": "Active"
        }
    )

    print(
        "\nNEGATIVE AREA STATUS:",
        response.status_code
    )

    print(
        "NEGATIVE AREA RESPONSE:",
        response.text
    )

    assert response.status_code == 422


# ============================================================
# TEST 7 - ZERO FARM AREA
# ============================================================

def test_zero_farm_area(client):

    headers = get_auth_headers(client)

    response = client.post(
        "/farms",
        headers=headers,
        json={
            "farm_name": "Zero Area Farm",
            "location": "Chittoor",
            "total_area": 0,
            "owner_name": "Test Owner",
            "status": "Active"
        }
    )

    assert response.status_code == 422


# ============================================================
# TEST 8 - INVALID FARM STATUS
# ============================================================

def test_invalid_farm_status(client):

    headers = get_auth_headers(client)

    response = client.post(
        "/farms",
        headers=headers,
        json={
            "farm_name": "Invalid Status Farm",
            "location": "Chittoor",
            "total_area": 100,
            "owner_name": "Test Owner",
            "status": "Invalid"
        }
    )

    print(
        "\nINVALID STATUS:",
        response.status_code
    )

    print(
        "INVALID STATUS RESPONSE:",
        response.text
    )

    assert response.status_code == 422


# ============================================================
# TEST 9 - DUPLICATE FARM
# ============================================================

def test_duplicate_farm(client):

    headers = get_auth_headers(client)

    farm_data = {
        "farm_name": "Duplicate Farm",
        "location": "Kurnool",
        "total_area": 100,
        "owner_name": "Test Owner",
        "status": "Active"
    }

    first_response = client.post(
        "/farms",
        headers=headers,
        json=farm_data
    )

    assert first_response.status_code in [200, 201]

    second_response = client.post(
        "/farms",
        headers=headers,
        json=farm_data
    )

    print(
        "\nDUPLICATE FARM STATUS:",
        second_response.status_code
    )

    print(
        "DUPLICATE FARM RESPONSE:",
        second_response.text
    )

    assert second_response.status_code in [400, 409]


# ============================================================
# TEST 10 - FARM SEARCH BY LOCATION
# ============================================================

def test_search_farms_by_location(client):

    headers = get_auth_headers(client)

    client.post(
        "/farms",
        headers=headers,
        json={
            "farm_name": "Search Farm",
            "location": "Anantapur",
            "total_area": 100,
            "owner_name": "Search Owner",
            "status": "Active"
        }
    )

    response = client.get(
        "/farms",
        headers=headers,
        params={
            "location": "Anantapur"
        }
    )

    print(
        "\nLOCATION SEARCH STATUS:",
        response.status_code
    )

    print(
        "LOCATION SEARCH RESPONSE:",
        response.text
    )

    assert response.status_code == 200


# ============================================================
# TEST 11 - FILTER FARMS BY STATUS
# ============================================================

def test_filter_farms_by_status(client):

    headers = get_auth_headers(client)

    response = client.get(
        "/farms",
        headers=headers,
        params={
            "status": "Active"
        }
    )

    print(
        "\nSTATUS FILTER:",
        response.status_code
    )

    print(
        "STATUS FILTER RESPONSE:",
        response.text
    )

    assert response.status_code == 200


# ============================================================
# TEST 12 - FARM PAGINATION
# ============================================================

def test_farm_pagination(client):

    headers = get_auth_headers(client)

    response = client.get(
        "/farms",
        headers=headers,
        params={
            "page": 1,
            "limit": 10
        }
    )

    print(
        "\nPAGINATION STATUS:",
        response.status_code
    )

    print(
        "PAGINATION RESPONSE:",
        response.text
    )

    assert response.status_code == 200