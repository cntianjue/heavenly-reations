# Architecture Design

## Goals
- Support adding, querying, modifying, and deleting books.
- Implement basic borrowing and returning operations.

## Current Project Analysis
The project requires a simple library management system with minimalistic features. The initial version should focus on backend development using Java Spring Boot and MySQL database. The system will provide REST API endpoints for managing book inventory and performing borrowing/returning operations.

## Module Design
### Modules
1. **Book Management Module**: Handles adding, querying, modifying, and deleting books.
2. **Inventory Management Module**: Manages the inventory count of books.
3. **Borrowing/Returning Module**: Handles the borrowing and returning of books.

### Dependencies
- Book Management Module depends on Inventory Management Module for inventory updates.
- Borrowing/Returning Module depends on both Book Management Module and Inventory Management Module for book details and inventory status.

## Technology Choices
- **Backend**: Java Spring Boot
- **Database**: MySQL
- **API Framework**: Spring Web
- **ORM**: Hibernate
- **Testing Framework**: JUnit, Mockito

## Data Model
### Tables
1. **Books**
   - id (Primary Key)
   - title
   - author
   - isbn (Unique)
   - inventory_count

2. **BorrowedBooks**
   - id (Primary Key)
   - book_id (Foreign Key to Books.id)
   - borrowed_date
   - returned_date

## API or UI Design
### REST API Endpoints
1. **Add Book**
   - POST /books
   - Request Body: { "title": "string", "author": "string", "isbn": "string" }
   - Response: 201 Created with book details

2. **Query All Books**
   - GET /books
   - Response: 200 OK with list of books

3. **Query Book by ID**
   - GET /books/{id}
   - Response: 200 OK with book details or 404 Not Found if not found

4. **Modify Book**
   - PUT /books/{id}
   - Request Body: { "title": "string", "author": "string" }
   - Response: 200 OK with updated book details or 404 Not Found if not found

5. **Delete Book**
   - DELETE /books/{id}
   - Response: 204 No Content or 404 Not Found if not found

6. **Borrow Book**
   - POST /borrow
   - Request Body: { "book_id": "string" }
   - Response: 200 OK with book details or 400 Bad Request if inventory is zero

7. **Return Book**
   - POST /return
   - Request Body: { "book_id": "string" }
   - Response: 200 OK with book details or 404 Not Found if not found

## Import Flow
- No initial import flow required for this MVP.

## Error Handling
- Custom exception handling to return appropriate HTTP status codes and error messages.
- Validation for ISBN uniqueness and inventory count constraints.

## Security Considerations
- Basic security measures such as input validation and preventing SQL injection using ORM.
- No user login and permission control initially.

## Test Strategy
- Unit tests for each service layer.
- Integration tests for API endpoints.
- Mocking dependencies to isolate unit tests.

## Deployment Considerations
- Dockerize the application for easy deployment.
- Use a local MySQL instance with Docker Compose.

## Delivery Standard
- Code should be well-documented and follow Java coding standards.
- Unit tests should cover at least 80% of the codebase.
- Documentation for API endpoints and usage.

## Risks
- Potential issues with ISBN uniqueness constraint enforcement.
- Inventory count validation during borrowing/returning operations.

## Out of Scope
- Frontend interface.
- Advanced features like user management or advanced reporting.