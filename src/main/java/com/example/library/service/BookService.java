package com.example.library.service;

import com.example.library.entity.Book;
import com.example.library.exception.BookNotFoundException;
import com.example.library.exception.DuplicateIsbnException;
import com.example.library.repository.BookRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@Transactional
public class BookService {

    private final BookRepository bookRepository;

    public BookService(BookRepository bookRepository) {
        this.bookRepository = bookRepository;
    }

    public Book addBook(Book book) {
        if (bookRepository.existsByIsbn(book.getIsbn())) {
            throw new DuplicateIsbnException("ISBN already exists: " + book.getIsbn());
        }
        if (book.getInventoryCount() < 0) {
            throw new IllegalArgumentException("Inventory count cannot be negative");
        }
        return bookRepository.save(book);
    }

    @Transactional(readOnly = true)
    public List<Book> getAllBooks() {
        return bookRepository.findAll();
    }

    @Transactional(readOnly = true)
    public Book getBookById(Long id) {
        return bookRepository.findById(id)
                .orElseThrow(() -> new BookNotFoundException("Book not found with id: " + id));
    }

    public Book updateBook(Long id, Book bookDetails) {
        Book book = getBookById(id);
        book.setTitle(bookDetails.getTitle());
        book.setAuthor(bookDetails.getAuthor());
        // ISBN is not updatable to maintain uniqueness; if needed, separate endpoint can be added
        return bookRepository.save(book);
    }

    public void deleteBook(Long id) {
        Book book = getBookById(id);
        bookRepository.delete(book);
    }

    public void decreaseInventory(Book book) {
        if (book.getInventoryCount() <= 0) {
            throw new IllegalStateException("Book inventory is zero, cannot borrow");
        }
        book.setInventoryCount(book.getInventoryCount() - 1);
        bookRepository.save(book);
    }

    public void increaseInventory(Book book) {
        book.setInventoryCount(book.getInventoryCount() + 1);
        bookRepository.save(book);
    }
}
