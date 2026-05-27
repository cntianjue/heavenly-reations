package com.example.library.controller;

import com.example.library.entity.Book;
import com.example.library.service.BorrowService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/borrow")
public class BorrowController {

    private final BorrowService borrowService;

    public BorrowController(BorrowService borrowService) {
        this.borrowService = borrowService;
    }

    @PostMapping
    public ResponseEntity<Book> borrowBook(@RequestParam Long bookId) {
        Book book = borrowService.borrowBook(bookId);
        return ResponseEntity.ok(book);
    }

    @PostMapping("/return")
    public ResponseEntity<Book> returnBook(@RequestParam Long bookId) {
        Book book = borrowService.returnBook(bookId);
        return ResponseEntity.ok(book);
    }
}
