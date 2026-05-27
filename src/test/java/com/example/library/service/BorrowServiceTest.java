package com.example.library.service;

import com.example.library.entity.Book;
import com.example.library.exception.BookNotFoundException;
import com.example.library.repository.BorrowedBookRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class BorrowServiceTest {

    @Mock
    private BorrowedBookRepository borrowedBookRepository;

    @Mock
    private BookService bookService;

    @InjectMocks
    private BorrowService borrowService;

    private Book book;

    @BeforeEach
    void setUp() {
        book = new Book("Borrow Test", "Author", "321-0987654321", 3);
        book.setId(1L);
    }

    @Test
    void borrowBookSuccess() {
        when(bookService.getBookById(1L)).thenReturn(book);
        doAnswer(invocation -> {
            book.setInventoryCount(book.getInventoryCount() - 1);
            return null;
        }).when(bookService).decreaseInventory(book);

        Book borrowed = borrowService.borrowBook(1L);

        assertThat(borrowed.getInventoryCount()).isEqualTo(2);
        verify(borrowedBookRepository).save(any());
    }

    @Test
    void borrowBookNotFoundThrows() {
        when(bookService.getBookById(1L)).thenThrow(new BookNotFoundException("Book not found"));

        assertThatThrownBy(() -> borrowService.borrowBook(1L))
                .isInstanceOf(BookNotFoundException.class);
    }

    @Test
    void returnBookSuccess() {
        when(bookService.getBookById(1L)).thenReturn(book);
        doAnswer(invocation -> {
            book.setInventoryCount(book.getInventoryCount() + 1);
            return null;
        }).when(bookService).increaseInventory(book);

        Book returned = borrowService.returnBook(1L);

        assertThat(returned.getInventoryCount()).isEqualTo(4);
    }
}
