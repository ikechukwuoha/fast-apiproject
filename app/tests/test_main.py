from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_items():
    response = client.get("/items/")
    assert response.status_code == 200
    assert "items" in response.json()
