from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)


# -----------------------------
# 1. Login and get JWT token
# -----------------------------
def get_token():
    response = client.post(
        "/users/login",
        json={
            "email": "aysha@gmail.com",
            "password": "Aysha123"
        }
    )

    print(response.json())  # temporary debugging
    assert response.status_code == 200
    return response.json()["access_token"]

# -----------------------------
# 2. GET all events
# -----------------------------
def test_get_events():
    token = get_token()

    response = client.get(
        "/events",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# -----------------------------
# 3. POST - Create Event
# -----------------------------
def test_create_event():
    token = get_token()
    response = client.post(
        "/events",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "title": "Pytest Workshop",
            "description": "Testing FastAPI with Pytest",
            "location": "Madurai",
            "event_date": "2026-10-01",
            "start_time": "10:00:00",
            "end_time": "12:00:00",
            "category": "Technical Workshop",
            "max_attendees": 30
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Pytest Workshop"
    assert "id" in data
# -----------------------------
# 4. POST → PATCH → DELETE
# -----------------------------
def test_crud_event_flow():
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    # CREATE
    create_response = client.post(
        "/events",
        headers=headers,
        json={
            "title": "CRUD Test Event",
            "description": "Testing CRUD operations",
            "location": "Chennai",
            "event_date": "2026-10-10",
            "start_time": "10:00:00",
            "end_time": "12:00:00",
            "category": "Testing",
            "max_attendees": 20
        }
    )
    assert create_response.status_code == 200
    event = create_response.json()
    event_id = event["id"]
    # GET
    get_response = client.get(
        f"/events/{event_id}",
        headers=headers
    )
    assert get_response.status_code == 200
    assert get_response.json()["id"] == event_id
    # PATCH
    patch_response = client.patch(
        f"/events/{event_id}",
        headers=headers,
        json={
            "title": "Updated CRUD Test Event"
        }
    )
    assert patch_response.status_code == 200
    assert patch_response.json()["title"] == "Updated CRUD Test Event"
    # DELETE
    delete_response = client.delete(
        f"/events/{event_id}",
        headers=headers
    )
    assert delete_response.status_code == 200
    # Verify deleted
    get_deleted_response = client.get(
        f"/events/{event_id}",
        headers=headers
    )
    assert get_deleted_response.status_code == 404
def test_create_event_without_token():
    response = client.post(
        "/events",
        json={
            "title": "Unauthorized Test",
            "description": "Testing without JWT",
            "location": "Chennai",
            "event_date": "2026-10-15",
            "start_time": "10:00:00",
            "end_time": "12:00:00",
            "category": "Testing",
            "max_attendees": 20
        }
    )
    assert response.status_code == 401
def test_get_invalid_event():
    token = get_token()

    response = client.get(
        "/events/999999",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    assert response.status_code == 404
def test_update_other_users_event():
    token = get_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.get(
        "/events",
        headers=headers
    )
    assert response.status_code == 200
    events = response.json()
    # Find an event that belongs to another user
    other_user_events = [
        event for event in events
        if event["user_id"] != 1
    ]
    if not other_user_events:
        pytest.skip("No event owned by another user is available")
    event_id = other_user_events[0]["id"]
    response = client.patch(
        f"/events/{event_id}",
        headers=headers,
        json={
            "title": "Trying Unauthorized Update"
        }
    )
    assert response.status_code == 403