# Library Management System

This application manages books in a library, allowing users to browse and borrow books, and administrators to manage the library’s catalog and users. The application is divided into two independent API services: a **Frontend API** for users and a **Backend/Admin API** for administrators.

## Table of Contents

- [API Endpoints](#api-endpoints)
  - [Frontend API Endpoints (User-Facing)](#frontend-api-endpoints-user-facing)
  - [Backend/Admin API Endpoints (Admin-Facing)](#backendadmin-api-endpoints-admin-facing)

---

# API Endpoints

## Frontend API Endpoints (User-Facing)

Port:8001
| HTTP Method | Endpoint | Description |
|-------------|-------------------------------------|---------------------------------------------------------------------------------------|
| `POST` | `/api/v1/users/enroll` | Enroll a new user into the library using their email, first name, and last name. |
| `GET` | `/api/v1/books` | List all available books in the library. |
| `GET` | `/api/v1/books/{id}` | Get details of a single book by its ID. |
| `GET` | `/api/v1/books?publisher={name}` | Filter books by publisher (e.g., Wiley, Apress, Manning). |
| `GET` | `/api/v1/books?category={name}` | Filter books by category (e.g., fiction, technology, science). |
| `POST` | `/api/v1/books/borrow/{id}` | Borrow a book by its ID, specifying how many days the user wants to borrow it for. |

## Backend/Admin API Endpoints (Admin-Facing)

Port 8000
| HTTP Method | Endpoint | Description |
|-------------|-------------------------------------|---------------------------------------------------------------------------------------|
| `POST` | `/api/v1/books` | Add a new book to the catalog. |
| `DELETE` | `/api/v1/books/{id}` | Remove a book from the catalog by its ID. |
| `GET` | `/api/v1/users` | Fetch a list of all users enrolled in the library. |
| `GET` | `/api/v1/users/borrowed-books` | Fetch a list of users and the books they have borrowed. |
| `GET` | `/api/v1/books/unavailable` | List books that are not available for borrowing and when they will be available again. |
