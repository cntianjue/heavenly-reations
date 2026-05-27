# Library Management System

A simple Spring Boot REST API for managing library books (CRUD) and performing borrow/return operations.

## Prerequisites

- Java 17+
- Maven 3.8+
- Docker and Docker Compose (for local MySQL)

## Quick Start

1. Clone the repository and navigate to the project root.
2. Start MySQL with Docker Compose:

```bash
docker-compose up -d
```

3. Build and run the application:

```bash
mvn clean package
java -jar target/library-management-0.0.1-SNAPSHOT.jar
```

4. The API is available at `http://localhost:8080`.

## Configuration

- **dev profile** (default): connects to Docker MySQL on localhost:3306 using credentials `libuser`/`libpass`.
- **test profile**: uses H2 in-memory database.

## API Endpoints

| Method | Endpoint         | Description                  |
|--------|------------------|------------------------------|
| POST   | /books           | Add a new book               |
| GET    | /books           | List all books               |
| GET    | /books/{id}      | Get book by ID               |
| PUT    | /books/{id}      | Update book title/author     |
| DELETE | /books/{id}      | Delete a book                |
| POST   | /borrow?bookId=  | Borrow a book (decrease inventory by 1) |
| POST   | /borrow/return?bookId= | Return a book (increase inventory by 1) |

## Testing

Run unit and integration tests:

```bash
mvn test
```

## Database Schema

The database schema is located in `db/schema.sql`. It is automatically applied when the Docker MySQL container starts.
