import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_success():
    # Test successful signup
    response = client.post("/activities/Chess%20Club/signup?email=test@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "Signed up test@mergington.edu for Chess Club" in data["message"]

    # Verify participant was added
    response = client.get("/activities")
    data = response.json()
    assert "test@mergington.edu" in data["Chess Club"]["participants"]


def test_signup_duplicate():
    # Try to sign up the same student again
    response = client.post("/activities/Chess%20Club/signup?email=test@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert "Student already signed up" in data["detail"]


def test_signup_invalid_activity():
    response = client.post("/activities/Invalid%20Activity/signup?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_unregister_success():
    # First sign up
    client.post("/activities/Programming%20Class/signup?email=remove@mergington.edu")
    
    # Then unregister
    response = client.delete("/activities/Programming%20Class/signup?email=remove@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered remove@mergington.edu from Programming Class" in data["message"]

    # Verify participant was removed
    response = client.get("/activities")
    data = response.json()
    assert "remove@mergington.edu" not in data["Programming Class"]["participants"]


def test_unregister_not_signed_up():
    response = client.delete("/activities/Gym%20Class/signup?email=notsigned@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert "Student not signed up for this activity" in data["detail"]


def test_unregister_invalid_activity():
    response = client.delete("/activities/Invalid%20Activity/signup?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]