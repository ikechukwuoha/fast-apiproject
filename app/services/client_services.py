from app.models.client import Client

def get_client(client_id: int) -> Client:
    # Placeholder for actual database call
    return Client(id=client_id, name="Test Client", email="test@example.com")
