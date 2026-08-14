# ============================================================
# tests/test_dashboard.py
# ============================================================

from fastapi.testclient import TestClient


# ============================================================
# AUTH HELPER
# ============================================================

def get_auth_headers(
    client: TestClient,
    username: str,
    role: str = "Admin"
):
    # --------------------------------------------------------
    # REGISTER USER
    # --------------------------------------------------------

    register_data = {
        "username": username,
        "email": f"{username}@example.com",
        "password": "Password@123",
        "role": role
    }

    register_response = client.post(
        "/auth/register",
        json=register_data
    )

    print("\nREGISTER STATUS:", register_response.status_code)
    print("REGISTER RESPONSE:", register_response.text)

    assert register_response.status_code == 201, (
        f"Registration failed: "
        f"{register_response.status_code} - "
        f"{register_response.text}"
    )

    # --------------------------------------------------------
    # LOGIN
    # Your auth router uses:
    # POST /auth/login
    # JSON body
    # --------------------------------------------------------

    login_data = {
        "username": username,
        "password": "Password@123"
    }

    login_response = client.post(
        "/auth/login",
        json=login_data
    )

    print("LOGIN STATUS:", login_response.status_code)
    print("LOGIN RESPONSE:", login_response.text)

    assert login_response.status_code == 200, (
        f"Login failed: "
        f"{login_response.status_code} - "
        f"{login_response.text}"
    )

    token = login_response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


# ============================================================
# TEST 1 - MAIN DASHBOARD
# ============================================================

def test_get_dashboard(client):

    headers = get_auth_headers(
        client,
        "dashboard_admin_1",
        role="Admin"
    )

    response = client.get(
        "/dashboard",
        headers=headers
    )

    print("\nDASHBOARD STATUS:", response.status_code)
    print("DASHBOARD RESPONSE:", response.text)

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)

    assert "total_farms" in data
    assert "total_fields" in data
    assert "active_crops" in data
    assert "crops_ready_for_harvest" in data
    assert "critical_crop_alerts" in data
    assert "total_harvest_quantity" in data
    assert "total_sales" in data
    assert "total_revenue" in data
    assert "total_treatment_cost" in data


# ============================================================
# TEST 2 - DASHBOARD VALUES ARE NON-NEGATIVE
# ============================================================

def test_dashboard_values(client):

    headers = get_auth_headers(
        client,
        "dashboard_admin_2",
        role="Admin"
    )

    response = client.get(
        "/dashboard",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    print("\nDASHBOARD VALUES:", data)

    assert data["total_farms"] >= 0
    assert data["total_fields"] >= 0
    assert data["active_crops"] >= 0
    assert data["crops_ready_for_harvest"] >= 0
    assert data["critical_crop_alerts"] >= 0
    assert data["total_harvest_quantity"] >= 0
    assert data["total_sales"] >= 0
    assert data["total_revenue"] >= 0
    assert data["total_treatment_cost"] >= 0


# ============================================================
# TEST 3 - FARM-WISE REVENUE
# ============================================================

def test_farm_wise_revenue(client):

    headers = get_auth_headers(
        client,
        "dashboard_revenue_1",
        role="Admin"
    )

    response = client.get(
        "/dashboard/farm-wise-revenue",
        headers=headers
    )

    print(
        "\nFARM-WISE REVENUE STATUS:",
        response.status_code
    )

    print(
        "FARM-WISE REVENUE RESPONSE:",
        response.text
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


# ============================================================
# TEST 4 - FARM-WISE REVENUE RESPONSE STRUCTURE
# ============================================================

def test_farm_wise_revenue_structure(client):

    headers = get_auth_headers(
        client,
        "dashboard_revenue_2",
        role="Admin"
    )

    response = client.get(
        "/dashboard/farm-wise-revenue",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    print("\nFARM REVENUE DATA:", data)

    for item in data:

        assert "farm_id" in item
        assert "farm_name" in item
        assert "total_revenue" in item

        assert item["farm_id"] > 0
        assert item["farm_name"]
        assert item["total_revenue"] >= 0


# ============================================================
# TEST 5 - CROP-WISE PRODUCTION
# ============================================================

def test_crop_wise_production(client):

    headers = get_auth_headers(
        client,
        "dashboard_production_1",
        role="Admin"
    )

    response = client.get(
        "/dashboard/crop-wise-production",
        headers=headers
    )

    print(
        "\nCROP-WISE PRODUCTION STATUS:",
        response.status_code
    )

    print(
        "CROP-WISE PRODUCTION RESPONSE:",
        response.text
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


# ============================================================
# TEST 6 - CROP-WISE PRODUCTION RESPONSE STRUCTURE
# ============================================================

def test_crop_wise_production_structure(client):

    headers = get_auth_headers(
        client,
        "dashboard_production_2",
        role="Admin"
    )

    response = client.get(
        "/dashboard/crop-wise-production",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    print("\nCROP PRODUCTION DATA:", data)

    for item in data:

        assert "crop_id" in item
        assert "crop_name" in item
        assert "total_production" in item

        assert item["crop_id"] > 0
        assert item["crop_name"]
        assert item["total_production"] >= 0


# ============================================================
# TEST 7 - DASHBOARD WITHOUT TOKEN
# ============================================================

def test_dashboard_without_token(client):

    response = client.get(
        "/dashboard"
    )

    print(
        "\nUNAUTHENTICATED DASHBOARD STATUS:",
        response.status_code
    )

    print(
        "UNAUTHENTICATED DASHBOARD RESPONSE:",
        response.text
    )

    assert response.status_code == 401


# ============================================================
# TEST 8 - FARM REVENUE WITHOUT TOKEN
# ============================================================

def test_farm_wise_revenue_without_token(client):

    response = client.get(
        "/dashboard/farm-wise-revenue"
    )

    print(
        "\nUNAUTHENTICATED FARM REVENUE STATUS:",
        response.status_code
    )

    print(
        "UNAUTHENTICATED FARM REVENUE RESPONSE:",
        response.text
    )

    assert response.status_code == 401


# ============================================================
# TEST 9 - CROP PRODUCTION WITHOUT TOKEN
# ============================================================

def test_crop_wise_production_without_token(client):

    response = client.get(
        "/dashboard/crop-wise-production"
    )

    print(
        "\nUNAUTHENTICATED CROP PRODUCTION STATUS:",
        response.status_code
    )

    print(
        "UNAUTHENTICATED CROP PRODUCTION RESPONSE:",
        response.text
    )

    assert response.status_code == 401


# ============================================================
# TEST 10 - FARM MANAGER DASHBOARD
# ============================================================

def test_dashboard_farm_manager(client):

    headers = get_auth_headers(
        client,
        "dashboard_manager",
        role="Farm Manager"
    )

    response = client.get(
        "/dashboard",
        headers=headers
    )

    print(
        "\nFARM MANAGER DASHBOARD STATUS:",
        response.status_code
    )

    print(
        "FARM MANAGER DASHBOARD RESPONSE:",
        response.text
    )

    assert response.status_code == 200


# ============================================================
# TEST 11 - FARMER DASHBOARD
# ============================================================

def test_dashboard_farmer(client):

    headers = get_auth_headers(
        client,
        "dashboard_farmer",
        role="Farmer"
    )

    response = client.get(
        "/dashboard",
        headers=headers
    )

    print(
        "\nFARMER DASHBOARD STATUS:",
        response.status_code
    )

    print(
        "FARMER DASHBOARD RESPONSE:",
        response.text
    )

    assert response.status_code == 200