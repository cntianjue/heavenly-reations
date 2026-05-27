package com.library.controller;

import com.library.entity.Book;
import com.library.repository.BookRepository;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/books")
public class BookController {

    private final BookRepository bookRepository;

    public BookController(BookRepository bookRepository) {
        this.bookRepository = bookRepository;
    }

    // Add a new book
    @PostMapping
    public ResponseEntity<Book> addBook(@RequestBody Book book) {
        if (book.getIsbn() == null || book.getIsbn().trim().isEmpty()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "ISBN is required");
        }
        if (bookRepository.existsByIsbn(book.getIsbn())) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "ISBN already exists");
        }
        Book savedBook = bookRepository.save(book);
        return ResponseEntity.status(HttpStatus.CREATED).body(savedBook);
    }

    // Get all books
    @GetMapping
    public List<Book> getAllBooks() {
        return bookRepository.findAll();
    }

    // Get book by id
    @GetMapping("/{id}")
    public ResponseEntity<Book> getBookById(@PathVariable Long id) {
        Book book = bookRepository.findById(id)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Book not found"));
        return ResponseEntity.ok(book);
    }

    // Modify book info
    @PutMapping("/{id}")
    public ResponseEntity<Book> updateBook(@PathVariable Long id, @RequestBody Book updatedBook) {
        Book existingBook = bookRepository.findById(id)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Book not found"));

        if (updatedBook.getTitle() != null) {
            existingBook.setTitle(updatedBook.getTitle());
        }
        if (updatedBook.getAuthor() != null) {
            existingBook.setAuthor(updatedBook.getAuthor());
        }
        // ISBN change could be supported with additional validation, but skip for simplicity
        if (updatedBook.getIsbn() != null && !updatedBook.getIsbn().equals(existingBook.getIsbn())) {
            if (bookRepository.existsByIsbn(updatedBook.getIsbn())) {
                throw new ResponseStatusException(HttpStatus.CONFLICT, "ISBN already exists");
            }
            existingBook.setIsbn(updatedBook.getIsbn());
        }

        bookRepository.save(existingBook);
        return ResponseEntity.ok(existingBook);
    }

    // Delete book
    @DeleteMapping("/{id}")
    public ResponseEntity<Map<String, String>> deleteBook(@PathVariable Long id) {
        if (!bookRepository.existsById(id)) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Book not found");
        }
        bookRepository.deleteById(id);
        return ResponseEntity.ok(Map.of("message", "Book deleted successfully"));
    }

    // Borrow book
    @PostMapping("/{id}/borrow")
    public ResponseEntity<Map<String, String>> borrowBook(@PathVariable Long id) {
        Book book = bookRepository.findById(id)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Book not found"));
        if (book.getInventoryCount() <= 0) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Inventory is zero");
        }
        book.setInventoryCount(book.getInventoryCount() - 1);
        bookRepository.save(book);
        return ResponseEntity.ok(Map.of("message", "Book borrowed successfully"));
    }

    // Return book
    @PostMapping("/{id}/return")
    public ResponseEntity<Map<String, String>> returnBook(@PathVariable Long id) {
        Book book = bookRepository.findById(id)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Book not found"));
        book.setInventoryCount(book.getInventoryCount() + 1);
        bookRepository.save(book);
        return ResponseEntity.ok(Map.of("message", "Book returned successfully"));
    }
}
