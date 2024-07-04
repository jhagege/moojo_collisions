import pytest
from fastapi.testclient import TestClient

from app import ResourceLockAPI


@pytest.fixture(scope="module")
def test_client():
    # Create the ResourceLockAPI instance
    test_resource_lock_api = ResourceLockAPI()

    # Create a TestClient using the initialized app
    client = TestClient(test_resource_lock_api.app)

    # Initialize the resource lock state using API calls
    client.post("/add_lock", json={"resource_id": "a", "start_time": 1500, "end_time": 1600})
    client.post("/add_lock", json={"resource_id": "a", "start_time": 1800, "end_time": 1900})
    client.post("/add_lock", json={"resource_id": "b", "start_time": 1700, "end_time": 3000})
    client.post("/add_lock",
                json={"resource_id": "a", "start_time": 1550, "end_time": 1650})  # Adding a collision for testing

    yield client


def test_add_lock(test_client):
    response = test_client.post("/add_lock", json={"resource_id": "c", "start_time": 2000, "end_time": 2100})
    assert response.status_code == 200
    assert response.json() == {"message": "Lock added successfully"}


def test_first_collision(test_client):
    response = test_client.get("/first_collision/a")
    assert response.status_code == 200
    assert response.json() == {"collision": [[1500, 1600], [1550, 1650]]}


def test_is_locked(test_client):
    response = test_client.get("/is_locked", params={"resource_id": "a", "t": 1550})
    assert response.status_code == 200
    assert response.json() == {"is_locked": True}

    response = test_client.get("/is_locked", params={"resource_id": "a", "t": 1750})
    assert response.status_code == 200
    assert response.json() == {"is_locked": False}


def test_has_collision(test_client):
    response = test_client.get("/has_collision", params={"resource_id": "a", "t": 1550})
    assert response.status_code == 200
    assert response.json() == {"has_collision": True}

    response = test_client.get("/has_collision", params={"resource_id": "a", "t": 1750})
    assert response.status_code == 200
    assert response.json() == {"has_collision": False}


def test_all_collisions(test_client):
    response = test_client.get("/all_collisions/a")
    assert response.status_code == 200
    assert response.json() == {"collisions": [[[1500, 1600], [1550, 1650]]]}
