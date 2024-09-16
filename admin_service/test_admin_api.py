# tests/test_backend_api.py
import pytest
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_add_book():
    response = client.post("/api/v1/books", json={
        "title": "New Book",
        "author": "Author Name",
        "publisher": "Publisher Name",
        "category": "Fiction",
        "available": True
    })
    assert response.status_code == 201
    assert response.json()["title"] == "New Book"

def test_remove_book():
    response = client.delete("/api/v1/books/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Book removed successfully"

def test_list_users():
    response = client.get("/api/v1/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_list_users_and_borrowed_books():
    response = client.get("/api/v1/users/borrowed-books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_list_unavailable_books():
    response = client.get("/api/v1/books/unavailable")
    assert response.status_code == 200
    assert all(book['available'] == False for book in response.json())
