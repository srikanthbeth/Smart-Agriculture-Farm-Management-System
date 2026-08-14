# tests/test_crops.py


# ============================================================
# HELPER - GET AUTHENTICATION HEADERS
# ============================================================

def get_auth_headers(client):

    register_response = client.post(
        "/auth/register",
        json={
            "username": "cropmanager",
            "email": "cropmanager@example.com",
            "password": "Test@12345",
            "role": "Farm Manager"
        }
    )

    assert register_response.status_code in [200, 201, 400]

    login_response = client.post(
        "/auth/login",
        json={
            "username": "cropmanager",
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

def create_farm(client, headers, farm_name="Crop Test Farm", area=100):

    response = client.post(
        "/farms",
        headers=headers,
        json={
            "farm_name": farm_name,
            "location": "Andhra Pradesh",
            "total_area": area,
            "owner_name": "Crop Test Owner",
            "status": "Active"
        }
    )

    assert response.status_code in [200, 201]

    return response.json()["id"]


# ============================================================
# HELPER - CREATE FIELD
# ============================================================

def create_field(
    client,
    headers,
    farm_id,
    field_name="Crop Test Field",
    area=40,
    status="Active"
):

    response = client.post(
        f"/farms/{farm_id}/fields",
        headers=headers,
        json={
            "field_name": field_name,
            "area": area,
            "soil_type": "Black Soil",
            "irrigation_type": "Drip",
            "status": status
        }
    )

    assert response.status_code in [200, 201]

    return response.json()["id"]


# ============================================================
# TEST 1 - CREATE CROP
# ============================================================

def test_create_crop(client):

    headers = get_auth_headers(client)

    farm_id = create_farm(
        client,
        headers,
        farm_name="Create Crop Farm"
    )

    field_id = create_field(
        client,
        headers,
        farm_id,
        field_name="Crop Field A"
    )

    response = client.post(
        "/crops",
        headers=headers,
        json={
            "field_id": field_id,
            "crop_name": "Rice",
            "crop_type": "Cereal",
            "planting_date": "2026-08-01",
            "expected_harvest_date": "2026-12-01",
            "seed_quantity": 50,
            "status": "Planned"
        }
    )

    print("\nCREATE CROP STATUS:", response.status_code)
    print("CREATE CROP RESPONSE:", response.text)

    assert response.status_code in [200, 201]

    data = response.json()

    assert "id" in data
    assert data["field_id"] == field_id
    assert data["crop_name"] == "Rice"
    assert data["crop_type"] == "Cereal"
    assert data["status"] == "Planned"


# ============================================================
# TEST 2 - GET ALL CROPS
# ============================================================

def test_get_crops(client):

    headers = get_auth_headers(client)

    farm_id = create_farm(
        client,
        headers,
        farm_name="Get Crops Farm"
    )

    field_id = create_field(
        client,
        headers,
        farm_id,
        field_name="Get Crops Field"
    )

    create_response = client.post(
        "/crops",
        headers=headers,
        json={
            "field_id": field_id,
            "crop_name": "Wheat",
            "crop_type": "Cereal",
            "planting_date": "2026-08-01",
            "expected_harvest_date": "2026-12-01",
            "seed_quantity": 40,
            "status": "Growing"
        }
    )

    assert create_response.status_code in [200, 201]

    response = client.get(
        "/crops",
        headers=headers
    )

    print("\nGET CROPS STATUS:", response.status_code)
    print("GET CROPS RESPONSE:", response.text)

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, (list, dict))


# ============================================================
# TEST 3 - GET CROP BY ID
# ============================================================

def test_get_crop_by_id(client):

    headers = get_auth_headers(client)

    farm_id = create_farm(
        client,
        headers,
        farm_name="Get Crop ID Farm"
    )

    field_id = create_field(
        client,
        headers,
        farm_id,
        field_name="Get Crop ID Field"
    )

    create_response = client.post(
        "/crops",
        headers=headers,
        json={
            "field_id": field_id,
            "crop_name": "Maize",
            "crop_type": "Cereal",
            "planting_date": "2026-08-05",
            "expected_harvest_date": "2026-12-05",
            "seed_quantity": 30,
            "status": "Planned"
        }
    )

    assert create_response.status_code in [200, 201]

    crop_id = create_response.json()["id"]

    response = client.get(
        f"/crops/{crop_id}",
        headers=headers
    )

    print("\nGET CROP STATUS:", response.status_code)
    print("GET CROP RESPONSE:", response.text)

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == crop_id
    assert data["crop_name"] == "Maize"


# ============================================================
# TEST 4 - GET NON-EXISTING CROP
# ============================================================

def test_get_non_existing_crop(client):

    headers = get_auth_headers(client)

    response = client.get(
        "/crops/999999",
        headers=headers
    )

    print("\nNON-EXISTING CROP:", response.status_code)
    print("RESPONSE:", response.text)

    assert response.status_code == 404


# ============================================================
# TEST 5 - UPDATE CROP
# ============================================================

def test_update_crop(client):

    headers = get_auth_headers(client)

    farm_id = create_farm(
        client,
        headers,
        farm_name="Update Crop Farm"
    )

    field_id = create_field(
        client,
        headers,
        farm_id,
        field_name="Update Crop Field"
    )

    create_response = client.post(
        "/crops",
        headers=headers,
        json={
            "field_id": field_id,
            "crop_name": "Cotton",
            "crop_type": "Cash Crop",
            "planting_date": "2026-08-01",
            "expected_harvest_date": "2027-01-01",
            "seed_quantity": 25,
            "status": "Planned"
        }
    )

    assert create_response.status_code in [200, 201]

    crop_id = create_response.json()["id"]

    response = client.put(
        f"/crops/{crop_id}",
        headers=headers,
        json={
            "crop_name": "Updated Cotton",
            "crop_type": "Cash Crop",
            "planting_date": "2026-08-01",
            "expected_harvest_date": "2027-01-01",
            "seed_quantity": 30,
            "status": "Growing"
        }
    )

    print("\nUPDATE CROP STATUS:", response.status_code)
    print("UPDATE CROP RESPONSE:", response.text)

    assert response.status_code == 200

    data = response.json()

    assert data["crop_name"] == "Updated Cotton"
    assert data["status"] == "Growing"


# ============================================================
# TEST 6 - PLANTING DATE AFTER HARVEST DATE
# ============================================================

def test_invalid_crop_dates(client):

    headers = get_auth_headers(client)

    farm_id = create_farm(
        client,
        headers,
        farm_name="Invalid Date Farm"
    )

    field_id = create_field(
        client,
        headers,
        farm_id,
        field_name="Invalid Date Field"
    )

    response = client.post(
        "/crops",
        headers=headers,
        json={
            "field_id": field_id,
            "crop_name": "Invalid Crop",
            "crop_type": "Cereal",
            "planting_date": "2026-12-01",
            "expected_harvest_date": "2026-08-01",
            "seed_quantity": 20,
            "status": "Planned"
        }
    )

    print("\nINVALID DATE STATUS:", response.status_code)
    print("INVALID DATE RESPONSE:", response.text)

    assert response.status_code in [400, 422]


# ============================================================
# TEST 7 - ZERO SEED QUANTITY
# ============================================================

def test_zero_seed_quantity(client):

    headers = get_auth_headers(client)

    farm_id = create_farm(
        client,
        headers,
        farm_name="Zero Seed Farm"
    )

    field_id = create_field(
        client,
        headers,
        farm_id,
        field_name="Zero Seed Field"
    )

    response = client.post(
        "/crops",
        headers=headers,
        json={
            "field_id": field_id,
            "crop_name": "Rice",
            "crop_type": "Cereal",
            "planting_date": "2026-08-01",
            "expected_harvest_date": "2026-12-01",
            "seed_quantity": 0,
            "status": "Planned"
        }
    )

    print("\nZERO SEED STATUS:", response.status_code)
    print("ZERO SEED RESPONSE:", response.text)

    assert response.status_code == 422


# ============================================================
# TEST 8 - NEGATIVE SEED QUANTITY
# ============================================================

def test_negative_seed_quantity(client):

    headers = get_auth_headers(client)

    farm_id = create_farm(
        client,
        headers,
        farm_name="Negative Seed Farm"
    )

    field_id = create_field(
        client,
        headers,
        farm_id,
        field_name="Negative Seed Field"
    )

    response = client.post(
        "/crops",
        headers=headers,
        json={
            "field_id": field_id,
            "crop_name": "Rice",
            "crop_type": "Cereal",
            "planting_date": "2026-08-01",
            "expected_harvest_date": "2026-12-01",
            "seed_quantity": -10,
            "status": "Planned"
        }
    )

    assert response.status_code == 422


# ============================================================
# TEST 9 - INVALID CROP STATUS
# ============================================================

def test_invalid_crop_status(client):

    headers = get_auth_headers(client)

    farm_id = create_farm(
        client,
        headers,
        farm_name="Invalid Crop Status Farm"
    )

    field_id = create_field(
        client,
        headers,
        farm_id,
        field_name="Invalid Crop Status Field"
    )

    response = client.post(
        "/crops",
        headers=headers,
        json={
            "field_id": field_id,
            "crop_name": "Rice",
            "crop_type": "Cereal",
            "planting_date": "2026-08-01",
            "expected_harvest_date": "2026-12-01",
            "seed_quantity": 20,
            "status": "Invalid"
        }
    )

    print("\nINVALID CROP STATUS:", response.status_code)
    print("RESPONSE:", response.text)

    assert response.status_code == 422


# ============================================================
# TEST 10 - NON-EXISTING FIELD
# ============================================================

def test_create_crop_for_non_existing_field(client):

    headers = get_auth_headers(client)

    response = client.post(
        "/crops",
        headers=headers,
        json={
            "field_id": 999999,
            "crop_name": "Orphan Crop",
            "crop_type": "Cereal",
            "planting_date": "2026-08-01",
            "expected_harvest_date": "2026-12-01",
            "seed_quantity": 20,
            "status": "Planned"
        }
    )

    print("\nNON-EXISTING FIELD:", response.status_code)
    print("RESPONSE:", response.text)

    assert response.status_code == 404


# ============================================================
# TEST 11 - INACTIVE FIELD CANNOT HAVE NEW CROP
# ============================================================

def test_crop_on_inactive_field(client):

    headers = get_auth_headers(client)

    farm_id = create_farm(
        client,
        headers,
        farm_name="Inactive Crop Farm"
    )

    field_id = create_field(
        client,
        headers,
        farm_id,
        field_name="Inactive Crop Field",
        status="Inactive"
    )

    response = client.post(
        "/crops",
        headers=headers,
        json={
            "field_id": field_id,
            "crop_name": "Rice",
            "crop_type": "Cereal",
            "planting_date": "2026-08-01",
            "expected_harvest_date": "2026-12-01",
            "seed_quantity": 20,
            "status": "Planned"
        }
    )

    print("\nINACTIVE FIELD CROP:", response.status_code)
    print("RESPONSE:", response.text)

    assert response.status_code in [400, 409]


# ============================================================
# TEST 12 - MAINTENANCE FIELD CANNOT HAVE NEW CROP
# ============================================================

def test_crop_on_maintenance_field(client):

    headers = get_auth_headers(client)

    farm_id = create_farm(
        client,
        headers,
        farm_name="Maintenance Crop Farm"
    )

    field_id = create_field(
        client,
        headers,
        farm_id,
        field_name="Maintenance Crop Field",
        status="Under Maintenance"
    )

    response = client.post(
        "/crops",
        headers=headers,
        json={
            "field_id": field_id,
            "crop_name": "Wheat",
            "crop_type": "Cereal",
            "planting_date": "2026-08-01",
            "expected_harvest_date": "2026-12-01",
            "seed_quantity": 20,
            "status": "Planned"
        }
    )

    print("\nMAINTENANCE FIELD CROP:", response.status_code)
    print("RESPONSE:", response.text)

    assert response.status_code in [400, 409]


# ============================================================
# TEST 13 - OVERLAPPING ACTIVE CROPS
# ============================================================

def test_overlapping_active_crops(client):

    headers = get_auth_headers(client)

    farm_id = create_farm(
        client,
        headers,
        farm_name="Overlap Crop Farm"
    )

    field_id = create_field(
        client,
        headers,
        farm_id,
        field_name="Overlap Crop Field"
    )

    first_response = client.post(
        "/crops",
        headers=headers,
        json={
            "field_id": field_id,
            "crop_name": "Rice",
            "crop_type": "Cereal",
            "planting_date": "2026-08-01",
            "expected_harvest_date": "2026-12-01",
            "seed_quantity": 20,
            "status": "Growing"
        }
    )

    assert first_response.status_code in [200, 201]

    second_response = client.post(
        "/crops",
        headers=headers,
        json={
            "field_id": field_id,
            "crop_name": "Wheat",
            "crop_type": "Cereal",
            "planting_date": "2026-09-01",
            "expected_harvest_date": "2027-01-01",
            "seed_quantity": 20,
            "status": "Planned"
        }
    )

    print("\nOVERLAPPING CROP STATUS:", second_response.status_code)
    print("OVERLAPPING CROP RESPONSE:", second_response.text)

    assert second_response.status_code in [400, 409]


# ============================================================
# TEST 14 - NON-OVERLAPPING CROPS
# ============================================================

def test_non_overlapping_crops(client):

    headers = get_auth_headers(client)

    farm_id = create_farm(
        client,
        headers,
        farm_name="Non Overlap Farm"
    )

    field_id = create_field(
        client,
        headers,
        farm_id,
        field_name="Non Overlap Field"
    )

    first_response = client.post(
        "/crops",
        headers=headers,
        json={
            "field_id": field_id,
            "crop_name": "Rice",
            "crop_type": "Cereal",
            "planting_date": "2026-01-01",
            "expected_harvest_date": "2026-05-01",
            "seed_quantity": 20,
            "status": "Harvested"
        }
    )

    assert first_response.status_code in [200, 201]

    second_response = client.post(
        "/crops",
        headers=headers,
        json={
            "field_id": field_id,
            "crop_name": "Wheat",
            "crop_type": "Cereal",
            "planting_date": "2026-06-01",
            "expected_harvest_date": "2026-10-01",
            "seed_quantity": 20,
            "status": "Growing"
        }
    )

    print("\nNON-OVERLAPPING CROP:", second_response.status_code)
    print("RESPONSE:", second_response.text)

    assert second_response.status_code in [200, 201]


# ============================================================
# TEST 15 - HARVESTED CROP CANNOT BE MODIFIED
# ============================================================

def test_harvested_crop_cannot_be_modified(client):

    headers = get_auth_headers(client)

    farm_id = create_farm(
        client,
        headers,
        farm_name="Harvested Crop Farm"
    )

    field_id = create_field(
        client,
        headers,
        farm_id,
        field_name="Harvested Crop Field"
    )

    create_response = client.post(
        "/crops",
        headers=headers,
        json={
            "field_id": field_id,
            "crop_name": "Rice",
            "crop_type": "Cereal",
            "planting_date": "2026-01-01",
            "expected_harvest_date": "2026-05-01",
            "seed_quantity": 20,
            "status": "Harvested"
        }
    )

    assert create_response.status_code in [200, 201]

    crop_id = create_response.json()["id"]

    response = client.put(
        f"/crops/{crop_id}",
        headers=headers,
        json={
            "crop_name": "Modified Rice",
            "crop_type": "Cereal",
            "planting_date": "2026-01-01",
            "expected_harvest_date": "2026-05-01",
            "seed_quantity": 30,
            "status": "Harvested"
        }
    )

    print("\nHARVESTED CROP UPDATE:", response.status_code)
    print("RESPONSE:", response.text)

    assert response.status_code in [400, 409]


# ============================================================
# TEST 16 - CROP SEARCH
# ============================================================

def test_crop_search(client):

    headers = get_auth_headers(client)

    farm_id = create_farm(
        client,
        headers,
        farm_name="Crop Search Farm"
    )

    field_id = create_field(
        client,
        headers,
        farm_id,
        field_name="Crop Search Field"
    )

    response = client.post(
        "/crops",
        headers=headers,
        json={
            "field_id": field_id,
            "crop_name": "Tomato",
            "crop_type": "Vegetable",
            "planting_date": "2026-08-01",
            "expected_harvest_date": "2026-11-01",
            "seed_quantity": 10,
            "status": "Growing"
        }
    )

    assert response.status_code in [200, 201]

    response = client.get(
        "/crops",
        headers=headers,
        params={
            "crop_name": "Tomato"
        }
    )

    print("\nCROP SEARCH STATUS:", response.status_code)
    print("CROP SEARCH RESPONSE:", response.text)

    assert response.status_code == 200


# ============================================================
# TEST 17 - CROP STATUS FILTER
# ============================================================

def test_crop_status_filter(client):

    headers = get_auth_headers(client)

    response = client.get(
        "/crops",
        headers=headers,
        params={
            "status": "Growing"
        }
    )

    print("\nCROP STATUS FILTER:", response.status_code)
    print("RESPONSE:", response.text)

    assert response.status_code == 200


# ============================================================
# TEST 18 - CROP PAGINATION
# ============================================================

def test_crop_pagination(client):

    headers = get_auth_headers(client)

    response = client.get(
        "/crops",
        headers=headers,
        params={
            "page": 1,
            "limit": 10
        }
    )

    print("\nCROP PAGINATION:", response.status_code)
    print("RESPONSE:", response.text)

    assert response.status_code == 200