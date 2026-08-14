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

    assert register_response.status_code in [201, 400, 409], (
        f"Register failed: "
        f"{register_response.status_code} - "
        f"{register_response.text}"
    )

    login_response = client.post(
        "/auth/login",
        json={
            "username": username,
            "password": "Test@12345",
        },
    )

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
        f"{login_response.status_code} - "
        f"{login_response.text}"
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

def create_field(client, token, farm_id, field_name):

    response = client.post(
        f"/farms/{farm_id}/fields",
        headers=get_auth_headers(token),
        json={
            "field_name": field_name,
            "area": 40,
            "soil_type": "Black Soil",
            "irrigation_type": "Drip",
            "status": "Active",
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
# COMPLETE TEST DATA SETUP
# ============================================================

def setup_treatment_data(client, prefix):

    token = create_user_and_login(
        client,
        f"treatment_{prefix}"
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
# 1. CREATE TREATMENT
# ============================================================

def test_create_treatment(client):

    token, farm, field, crop = setup_treatment_data(
        client,
        "create"
    )

    response = client.post(
        "/crop-treatments",
        headers=get_auth_headers(token),
        json={
            "crop_id": crop["id"],
            "product_name": "Urea",
            "product_type": "Fertilizer",
            "quantity": 25,
            "applied_date": "2026-08-13",
            "cost": 1500,
            "remarks": "Nitrogen fertilizer application",
        },
    )

    print("\nCREATE TREATMENT STATUS:", response.status_code)
    print("CREATE TREATMENT RESPONSE:", response.text)

    assert response.status_code == 201

    data = response.json()

    assert data["crop_id"] == crop["id"]
    assert data["product_name"] == "Urea"
    assert data["product_type"] == "Fertilizer"
    assert data["quantity"] == 25
    assert data["cost"] == 1500


# ============================================================
# 2. GET ALL TREATMENTS
# ============================================================

def test_get_treatments(client):

    token, farm, field, crop = setup_treatment_data(
        client,
        "getall"
    )

    create_response = client.post(
        "/crop-treatments",
        headers=get_auth_headers(token),
        json={
            "crop_id": crop["id"],
            "product_name": "DAP",
            "product_type": "Fertilizer",
            "quantity": 20,
            "applied_date": "2026-08-13",
            "cost": 1200,
            "remarks": "DAP application",
        },
    )

    assert create_response.status_code == 201

    response = client.get(
        "/crop-treatments",
        headers=get_auth_headers(token)
    )

    print("\nGET TREATMENTS STATUS:", response.status_code)
    print("GET TREATMENTS RESPONSE:", response.text)

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ============================================================
# 3. CROP TREATMENT HISTORY
# ============================================================

def test_get_crop_treatment_history(client):

    token, farm, field, crop = setup_treatment_data(
        client,
        "history"
    )

    first_response = client.post(
        "/crop-treatments",
        headers=get_auth_headers(token),
        json={
            "crop_id": crop["id"],
            "product_name": "Urea",
            "product_type": "Fertilizer",
            "quantity": 10,
            "applied_date": "2026-08-10",
            "cost": 500,
            "remarks": "First application",
        },
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/crop-treatments",
        headers=get_auth_headers(token),
        json={
            "crop_id": crop["id"],
            "product_name": "Neem Oil",
            "product_type": "Pesticide",
            "quantity": 5,
            "applied_date": "2026-08-12",
            "cost": 700,
            "remarks": "Pest control",
        },
    )

    assert second_response.status_code == 201

    response = client.get(
        f"/crops/{crop['id']}/treatments",
        headers=get_auth_headers(token)
    )

    print(
        "\nCROP TREATMENT HISTORY STATUS:",
        response.status_code
    )
    print(
        "CROP TREATMENT HISTORY RESPONSE:",
        response.text
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 2


# ============================================================
# 4. ZERO QUANTITY
# ============================================================

def test_zero_treatment_quantity(client):

    token, farm, field, crop = setup_treatment_data(
        client,
        "zeroquantity"
    )

    response = client.post(
        "/crop-treatments",
        headers=get_auth_headers(token),
        json={
            "crop_id": crop["id"],
            "product_name": "Urea",
            "product_type": "Fertilizer",
            "quantity": 0,
            "applied_date": "2026-08-13",
            "cost": 500,
            "remarks": "Invalid quantity",
        },
    )

    print("\nZERO QUANTITY STATUS:", response.status_code)
    print("ZERO QUANTITY RESPONSE:", response.text)

    assert response.status_code == 422


# ============================================================
# 5. NEGATIVE QUANTITY
# ============================================================

def test_negative_treatment_quantity(client):

    token, farm, field, crop = setup_treatment_data(
        client,
        "negativequantity"
    )

    response = client.post(
        "/crop-treatments",
        headers=get_auth_headers(token),
        json={
            "crop_id": crop["id"],
            "product_name": "Urea",
            "product_type": "Fertilizer",
            "quantity": -10,
            "applied_date": "2026-08-13",
            "cost": 500,
            "remarks": "Invalid quantity",
        },
    )

    print(
        "\nNEGATIVE QUANTITY STATUS:",
        response.status_code
    )
    print(
        "NEGATIVE QUANTITY RESPONSE:",
        response.text
    )

    assert response.status_code == 422


# ============================================================
# 6. ZERO COST
# ============================================================

def test_zero_treatment_cost(client):

    token, farm, field, crop = setup_treatment_data(
        client,
        "zerocost"
    )

    response = client.post(
        "/crop-treatments",
        headers=get_auth_headers(token),
        json={
            "crop_id": crop["id"],
            "product_name": "Urea",
            "product_type": "Fertilizer",
            "quantity": 10,
            "applied_date": "2026-08-13",
            "cost": 0,
            "remarks": "Invalid cost",
        },
    )

    print("\nZERO COST STATUS:", response.status_code)
    print("ZERO COST RESPONSE:", response.text)

    assert response.status_code == 422


# ============================================================
# 7. NEGATIVE COST
# ============================================================

def test_negative_treatment_cost(client):

    token, farm, field, crop = setup_treatment_data(
        client,
        "negativecost"
    )

    response = client.post(
        "/crop-treatments",
        headers=get_auth_headers(token),
        json={
            "crop_id": crop["id"],
            "product_name": "Urea",
            "product_type": "Fertilizer",
            "quantity": 10,
            "applied_date": "2026-08-13",
            "cost": -500,
            "remarks": "Invalid cost",
        },
    )

    print("\nNEGATIVE COST STATUS:", response.status_code)
    print("NEGATIVE COST RESPONSE:", response.text)

    assert response.status_code == 422


# ============================================================
# 8. NON-EXISTING CROP
# ============================================================

def test_treatment_non_existing_crop(client):

    token = create_user_and_login(
        client,
        "treatment_nonexisting"
    )

    response = client.post(
        "/crop-treatments",
        headers=get_auth_headers(token),
        json={
            "crop_id": 999999,
            "product_name": "Urea",
            "product_type": "Fertilizer",
            "quantity": 10,
            "applied_date": "2026-08-13",
            "cost": 500,
            "remarks": "Invalid crop",
        },
    )

    print(
        "\nNON-EXISTING CROP STATUS:",
        response.status_code
    )
    print(
        "NON-EXISTING CROP RESPONSE:",
        response.text
    )

    assert response.status_code == 404


# ============================================================
# 9. FERTILIZER TREATMENT
# ============================================================

def test_fertilizer_treatment(client):

    token, farm, field, crop = setup_treatment_data(
        client,
        "fertilizer"
    )

    response = client.post(
        "/crop-treatments",
        headers=get_auth_headers(token),
        json={
            "crop_id": crop["id"],
            "product_name": "NPK 20-20-20",
            "product_type": "Fertilizer",
            "quantity": 30,
            "applied_date": "2026-08-13",
            "cost": 2500,
            "remarks": "Balanced fertilizer",
        },
    )

    print(
        "\nFERTILIZER STATUS:",
        response.status_code
    )
    print(
        "FERTILIZER RESPONSE:",
        response.text
    )

    assert response.status_code == 201


# ============================================================
# 10. PESTICIDE TREATMENT
# ============================================================

def test_pesticide_treatment(client):

    token, farm, field, crop = setup_treatment_data(
        client,
        "pesticide"
    )

    response = client.post(
        "/crop-treatments",
        headers=get_auth_headers(token),
        json={
            "crop_id": crop["id"],
            "product_name": "Neem Oil",
            "product_type": "Pesticide",
            "quantity": 5,
            "applied_date": "2026-08-13",
            "cost": 800,
            "remarks": "Organic pest control",
        },
    )

    print(
        "\nPESTICIDE STATUS:",
        response.status_code
    )
    print(
        "PESTICIDE RESPONSE:",
        response.text
    )

    assert response.status_code == 201


# ============================================================
# 11. HISTORY FOR NON-EXISTING CROP
# ============================================================

def test_get_treatments_for_non_existing_crop(client):

    token = create_user_and_login(
        client,
        "treatment_history_missing"
    )

    response = client.get(
        "/crops/999999/treatments",
        headers=get_auth_headers(token)
    )

    print(
        "\nNON-EXISTING CROP HISTORY STATUS:",
        response.status_code
    )
    print(
        "NON-EXISTING CROP HISTORY RESPONSE:",
        response.text
    )

    assert response.status_code == 404


# ============================================================
# 12. GET TREATMENTS WITHOUT TOKEN
# ============================================================

def test_get_treatments_without_token(client):

    response = client.get(
        "/crop-treatments"
    )

    print(
        "\nUNAUTHENTICATED GET STATUS:",
        response.status_code
    )
    print(
        "UNAUTHENTICATED GET RESPONSE:",
        response.text
    )

    assert response.status_code == 401


# ============================================================
# 13. CREATE TREATMENT WITHOUT TOKEN
# ============================================================

def test_create_treatment_without_token(client):

    response = client.post(
        "/crop-treatments",
        json={
            "crop_id": 1,
            "product_name": "Urea",
            "product_type": "Fertilizer",
            "quantity": 10,
            "applied_date": "2026-08-13",
            "cost": 500,
            "remarks": "No authentication",
        },
    )

    print(
        "\nUNAUTHENTICATED CREATE STATUS:",
        response.status_code
    )
    print(
        "UNAUTHENTICATED CREATE RESPONSE:",
        response.text
    )

    assert response.status_code == 401