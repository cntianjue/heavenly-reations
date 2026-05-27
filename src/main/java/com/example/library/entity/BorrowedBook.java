package com.example.library.entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "borrowed_books")
public class BorrowedBook {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "book_id", nullable = false)
    private Book book;

    @Column(name = "borrowed_date", nullable = false)
    private LocalDateTime borrowedDate;

    @Column(name = "returned_date")
    private LocalDateTime returnedDate;

    public BorrowedBook() {}

    public BorrowedBook(Book book) {
        this.book = book;
        this.borrowedDate = LocalDateTime.now();
    }

    // Getters and setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public Book getBook() { return book; }
    public void setBook(Book book) { this.book = book; }

    public LocalDateTime getBorrowedDate() { return borrowedDate; }
    public void setBorrowedDate(LocalDateTime borrowedDate) { this.borrowedDate = borrowedDate; }

    public LocalDateTime getReturnedDate() { return returnedDate; }
    public void setReturnedDate(LocalDateTime returnedDate) { this.returnedDate = returnedDate; }
}
