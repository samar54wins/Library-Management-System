# Library Management API

This project is a Library Management API built using **FastAPI**, **MySQL**, and **SQLAlchemy**. The API provides functionality to manage books, authors, and users in a library system with JWT token-based authentication.

## Features
- **User Authentication**: Users can register and log in to receive a JWT access token.
- **Books Management**: Perform CRUD operations on books (create, read, update, delete).
- **Authors Management**: Perform CRUD operations on authors (create, read, update, delete).
- **Search Functionality**: Search books by title or author name.
- **Token-Based Authentication**: All routes except the registration/login require a valid JWT token.

## Technology Stack
- **Backend**: FastAPI (Python Web Framework)
- **Database**: MySQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT (JSON Web Tokens)
- **Hashing Algorithm**: bcrypt
- **Security**: OAuth2 Password Flow with Bearer Token

## Requirements

- Python 3.8+
- MySQL server running locally or remotely
- Required Python packages (listed in `requirements.txt`)

## Setup

### 1. Clone the repository

git clone https://github.com/your-username/library-management-api.git
cd library-management-api



2. Install dependencies
You can install the required Python dependencies using pip.

pip install -r requirements.tx

3. Set up the database
Create a MySQL database and update the DATABASE_URL in app/database.py with the correct credentials and database name.

Example:

DATABASE_URL = "mysql+pymysql://root:password@localhost/library_management"

4. Run the application
To start the application, use Uvicorn (ASGI server) to run the FastAPI app.

python run.py 

5. Access the API documentation
Once the application is running, you can access the auto-generated Swagger UI for the API at:



http://localhost:8000/docs
Alternatively, you can view the ReDoc documentation at:


http://localhost:8000/redoc
Authentication
Register a New User
To register a new user, send a POST request to /users/ with the following body:

json
{
    "username": "john_doe",
    "email": "john.doe@example.com",
    "password": "password123"
}
Login to Get JWT Token
After registering, you can log in by sending a POST request to /auth/login with the following form data:

username: your username
password: your password
You will receive a JWT token in the response. Example:

json

{
    "access_token": "your-jwt-token",
    "token_type": "bearer"
}
Use the JWT Token
For protected routes, you must include the JWT token in the Authorization header using the Bearer scheme.

Example:

Authorization: Bearer your-jwt-token
Available Endpoints
Users
POST /users/: Create a new user
GET /users/me: Get current logged-in user
Authentication
POST /auth/login: Login to receive a JWT token
Books
POST /books/: Create a new book
GET /books/search: Search books by title or author name
DELETE /books/: Delete books
PUT /books/: Update book details
Authors
POST /authors/: Create a new author
GET /authors/: Get a list of authors
PUT /authors/: Update author details
DELETE /authors/: Delete an author
Database Schema
Tables
Users:

id (Primary Key)
username (Unique)
email (Unique)
hashed_password

Books:
book_id (Primary Key)
title
author_id (Foreign Key to author.author_id)
isbn
published_year
genre

Authors:
author_id (Primary Key)
author_name
bio
date_of_birth
Contributing
Feel free to fork this project and create pull requests for new features or bug fixes. Ensure that you add appropriate tests for new functionality.


Acknowledgments
FastAPI - The web framework used for building the API.
SQLAlchemy - ORM for interacting with the MySQL database.
JWT - Token-based authentication.


