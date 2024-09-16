import pytest
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_enroll_user():
    response = client.post("/api/v1/users/enroll", json={
        "email": "test@example.com",
        "firstname": "John",
        "lastname": "Doe"
    })
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"

def test_list_books():
    response = client.get("/api/v1/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_book_by_id():
    response = client.get("/api/v1/books/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_filter_books_by_publisher():
    response = client.get("/api/v1/books?publisher=Wiley")
    assert response.status_code == 200
    assert all(book['publisher'] == 'Wiley' for book in response.json())

def test_filter_books_by_category():
    response = client.get("/api/v1/books?category=fiction")
    assert response.status_code == 200
    assert all(book['category'] == 'fiction' for book in response.json())

def test_borrow_book():
    response = client.post("/api/v1/books/borrow/1", json={"days": 7})
    assert response.status_code == 200
    assert response.json()["message"] == "Book borrowed successfully"
