# PRD

## Background
The user wants to create a simple library management system to manage basic book information and inventory status. The initial version should be minimalistic, allowing for subsequent testing of AI-generated code, interfaces, databases, and test cases.

## Goals
- Support adding, querying, modifying, and deleting books.
- Implement basic borrowing and returning operations.

## Users
The primary user is an administrator or librarian responsible for managing the library's book inventory.

## User Stories
1. As a librarian, I want to add new books so that they can be made available in the library.
2. As a librarian, I want to query all books so that I can manage them effectively.
3. As a librarian, I want to query a specific book by its ID so that I can access detailed information about it.
4. As a librarian, I want to modify existing book information so that the data remains accurate.
5. As a librarian, I want to delete books that are no longer needed or available.
6. As a librarian, I want to borrow books so that they can be checked out to library members.
7. As a librarian, I want to return books so that their inventory status is updated correctly.

## Functional Scope
### Must Have
- Add new books with unique ISBNs.
- Query all books and retrieve book details by ID.
- Modify existing book information.
- Delete books from the inventory.
- Borrow books, reducing the inventory count by 1.
- Return books, increasing the inventory count by 1.
- Prevent borrowing when the inventory is zero.

### Should Have
- Basic testing for each functionality.

### Could Have
- User login and permission control (not required initially).

### Won't Have
- Frontend interface.
- Advanced features like user management or advanced reporting.

## Non-functional Requirements
- Backend developed using Java Spring Boot.
- Database to be MySQL.
- Provide REST API endpoints.
- ISBN uniqueness constraint.
- Inventory count cannot go below zero.

## Acceptance Criteria
1. The system should allow adding new books with unique ISBNs.
2. The system should provide an endpoint to query all books and retrieve details by ID.
3. The system should support modifying existing book information.
4. The system should enable deleting books from the inventory.
5. The system should allow borrowing books, reducing the inventory count by 1.
6. The system should prevent borrowing when the inventory is zero.
7. The system should allow returning books, increasing the inventory count by 1.
8. The system should have basic testing for each functionality.

## Open Questions
- Should user login and permission control be included in the initial release?
- Are there any specific performance requirements or constraints?