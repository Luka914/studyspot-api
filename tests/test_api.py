import pytest
import main
from fastapi.testclient import TestClient

@pytest.fixture
def client(tmp_path, monkeypatch):
    database = tmp_path / "test.db"
    monkeypatch.setattr(main, "DATABASE", str(database))
    main.setup_database()
    return TestClient(main.app)

def test_home_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to StudySpot API!"

def test_create_study_spot(client):
    response = client.post(
        "/spots",
        json={
            "name": "Test Library",
            "location": "Durham",
            "noise_level": 2,
            "busy_level": 3,
            "has_wifi": True,
            "tags": ["quiet"]
        }
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Test Library"

def test_invalid_noise_level(client):
    response = client.post(
        "/spots",
        json={
            "name": "Test Library",
            "location": "Durham",
            "noise_level": 10,
            "busy_level": 3,
            "has_wifi": True,
            "tags": []
        }
    )
    assert response.status_code == 422

def test_missing_study_spot(client):
    response = client.get("/spots/999")
    assert response.status_code == 404