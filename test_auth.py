# tests/test_auth.py


# ============================================================
# TEST 1 - REGISTER USER
# ============================================================

def test_register_user(client):

    response = client.post(
        "/auth/register",
        json={
            "username": "testfarmer",
            "email": "testfarmer@example.com",
            "password": "Test@12345",
            "role": "Farmer"
        }
    )

    print("\nREGISTER STATUS:", response.status_code)
    print("REGISTER RESPONSE:", response.text)

    assert response.status_code in [200, 201]

    data = response.json()

    assert "id" in data
    assert data["email"] == "testfarmer@example.com"


# ============================================================
# TEST 2 - LOGIN USER
# ============================================================

def test_login_user(client):

    # First register the user
    register_response = client.post(
        "/auth/register",
        json={
            "username": "loginfarmer",
            "email": "loginfarmer@example.com",
            "password": "Test@12345",
            "role": "Farmer"
        }
    )

    print(
        "\nREGISTER STATUS:",
        register_response.status_code
    )

    assert register_response.status_code in [200, 201]

    # Login using username
    response = client.post(
        "/auth/login",
        json={
            "username": "loginfarmer",
            "password": "Test@12345"
        }
    )

    print("\nLOGIN STATUS:", response.status_code)
    print("LOGIN RESPONSE:", response.text)

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


# ============================================================
# TEST 3 - GET CURRENT USER
# ============================================================

def test_get_current_user(client):

    # Register user
    register_response = client.post(
        "/auth/register",
        json={
            "username": "mefarmer",
            "email": "mefarmer@example.com",
            "password": "Test@12345",
            "role": "Farmer"
        }
    )

    print(
        "\nREGISTER STATUS:",
        register_response.status_code
    )

    assert register_response.status_code in [200, 201]

    # Login
    login_response = client.post(
        "/auth/login",
        json={
            "username": "mefarmer",
            "password": "Test@12345"
        }
    )

    print(
        "\nLOGIN STATUS:",
        login_response.status_code
    )

    print(
        "LOGIN RESPONSE:",
        login_response.text
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    # Get current user
    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    print(
        "\nCURRENT USER STATUS:",
        response.status_code
    )

    print(
        "CURRENT USER RESPONSE:",
        response.text
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == "mefarmer@example.com"


# ============================================================
# TEST 4 - PROTECTED ENDPOINT WITHOUT TOKEN
# ============================================================

def test_protected_endpoint_without_token(client):

    response = client.get(
        "/farms"
    )

    print(
        "\nPROTECTED ENDPOINT STATUS:",
        response.status_code
    )

    print(
        "PROTECTED ENDPOINT RESPONSE:",
        response.text
    )

    assert response.status_code == 401