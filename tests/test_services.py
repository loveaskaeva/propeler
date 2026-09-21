from fastapi.testclient import TestClient


def test_create_service(client: TestClient):
    payload = {"name": "Разработка лендинга", "description": "Современный адаптивный лендинг", "price": 25000.00, "is_active": True}
    resp = client.post("/services", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Разработка лендинга"
    assert data["price"] == "25000.00"
    assert data["is_active"] is True
    assert "id" in data


def test_list_services(client: TestClient):
    payload = {"name": "Дизайн", "price": 15000.00}
    client.post("/services", json=payload)
    resp = client.get("/services")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
    assert len(resp.json()) >= 1


def test_get_service_not_found(client: TestClient):
    resp = client.get("/services/999999")
    assert resp.status_code == 404
    assert "не найдена" in resp.json()["detail"].lower()
