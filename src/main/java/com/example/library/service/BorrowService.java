package com.example.library.service;

import com.example.library.entity.Book;
import com.example.library.entity.BorrowedBook;
import com.example.library.repository.BorrowedBookRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Transactional
public class BorrowService {

    private final BorrowedBookRepository borrowedBookRepository;
    private final BookService bookService;

    public BorrowService(BorrowedBookRepository borrowedBookRepository, BookService bookService) {
        this.borrowedBookRepository = borrowedBookRepository;
        this.bookService = bookService;
    }

    public Book borrowBook(Long bookId) {
        Book book = bookService.getBookById(bookId);
        bookService.decreaseInventory(book);
        BorrowedBook borrowedBook = new BorrowedBook(book);
        borrowedBookRepository.save(borrowedBook);
        return book;
    }

    public Book returnBook(Long bookId) {
        Book book = bookService.getBookById(bookId);
        // We don't require a specific borrow record; just increase inventory
        bookService.increaseInventory(book);
        // Mark the latest unreturned borrow record as returned (optional)
        return book;
    }
}
