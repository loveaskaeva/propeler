from fastapi.testclient import TestClient


def test_create_contact_request(client: TestClient):
    service_resp = client.post("/services", json={"name": "Консультация", "price": 5000})
    service_id = service_resp.json()["id"]

    payload = {
        "client_name": "Иван Петров",
        "email": "ivan@example.com",
        "phone": "+7 (900) 000-00-00",
        "message": "Хочу заказать сайт",
        "service_id": service_id,
    }
    resp = client.post("/contact-requests", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["client_name"] == "Иван Петров"
    assert data["email"] == "ivan@example.com"
    assert data["service_id"] == service_id
    assert data["service"]["name"] == "Консультация"


def test_invalid_email_rejected(client: TestClient):
    payload = {"client_name": "Иван Петров", "email": "не-почта"}
    resp = client.post("/contact-requests", json=payload)
    assert resp.status_code == 422
