import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

# GET /books testi (başlangıçta boş)
def test_get_books_empty():
    response = client.get("/books")
    assert response.status_code == 200
    assert response.json() == []

# POST /books testi
def test_post_and_delete_book():
    book_data = {"isbn": "9999999999999"}
    
    # Kitap ekleme (POST)
    response = client.post("/books", json=book_data)
    assert response.status_code == 200
    assert "book" in response.json()
    assert response.json()["book"]["ISBN"] == book_data["isbn"]

    # Kitap silme (DELETE)
    response = client.delete(f"/books/{book_data['isbn']}")
    assert response.status_code == 200
    assert response.json()["deleted"]["ISBN"] == book_data["isbn"]
