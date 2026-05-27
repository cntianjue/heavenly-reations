# Architecture Design

## Goals
- Support adding, querying, modifying, and deleting books.
- Implement basic operations such as borrowing and returning books.

## Current Project Analysis
The project requires a backend system to manage book inventory. The initial version should be minimalistic, focusing on core functionalities without advanced features like user login or frontend interfaces.

## Module Design
### Core Modules
1. **Book Management Module**: Handles adding, querying, modifying, and deleting books.
2. **Inventory Management Module**: Manages the borrowing and returning of books.
3. **Database Access Module**: Interacts with the MySQL database to store and retrieve book information.

### Supporting Modules
1. **Validation Module**: Ensures data integrity by validating ISBNs and inventory counts.
2. **Logging Module**: Logs all operations for auditing and debugging purposes.

## Technology Choices
- **Backend**: Java Spring Boot
- **Database**: MySQL
- **API**: RESTful API

## Data Model
### Book Entity
```java
@Entity
public class Book {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(unique = true, nullable = false)
    private String isbn;
    
    private String title;
    private String author;
    private int inventoryCount;
    
    // Getters and Setters
}
```

## API or UI Design
### RESTful API Endpoints
1. **Add Book**
   - `POST /books`
   - Request Body: `{ "isbn": "1234567890", "title": "Book Title", "author": "Author Name", "inventoryCount": 10 }`

2. **Query All Books**
   - `GET /books`

3. **Query Book by ID**
   - `GET /books/{id}`

4. **Modify Book Information**
   - `PUT /books/{id}`
   - Request Body: `{ "title": "New Title", "author": "New Author" }`

5. **Delete Book**
   - `DELETE /books/{id}`

6. **Borrow Book**
   - `POST /books/{id}/borrow`
   - Response: `{ "message": "Book borrowed successfully" }` or `{ "error": "Inventory is zero" }`

7. **Return Book**
   - `POST /books/{id}/return`
   - Response: `{ "message": "Book returned successfully" }`

## Core Flow
1. **Add Book**: 
   - User sends a POST request with book details.
   - Validation module checks ISBN uniqueness and inventory count.
   - Database access module saves the new book.

2. **Query All Books**:
   - User sends a GET request to retrieve all books.
   - Database access module fetches all books from the database.

3. **Borrow Book**:
   - User sends a POST request to borrow a book by ID.
   - Validation module checks if inventory count is greater than zero.
   - Inventory management module decreases the inventory count.
   - Database access module updates the book's inventory count.

## Error Handling
- Custom exceptions for validation errors (e.g., ISBN already exists, inventory is zero).
- Global exception handler to return standardized error responses.

## Security Considerations
- Basic security measures such as input validation and data encryption.
- No user login or permission control initially.

## Test Strategy
- Unit tests for each module using JUnit.
- Integration tests to ensure modules work together correctly.
- Mock database for testing without affecting the actual database.

## Deployment Considerations
- Docker containerization for easy deployment.
- Kubernetes for orchestration (optional, can be added later).

## Risks
- Potential issues with ISBN uniqueness validation.
- Inventory count management errors during borrowing and returning operations.

## Out of Scope
- Frontend interface.
- Advanced user permissions or roles.