package com.example.library.service;

import com.example.library.entity.Book;
import com.example.library.exception.BookNotFoundException;
import com.example.library.exception.DuplicateIsbnException;
import com.example.library.repository.BookRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class BookServiceTest {

    @Mock
    private BookRepository bookRepository;

    @InjectMocks
    private BookService bookService;

    private Book book;

    @BeforeEach
    void setUp() {
        book = new Book("Test Title", "Test Author", "123-4567890123", 5);
        book.setId(1L);
    }

    @Test
    void addBookSuccess() {
        when(bookRepository.existsByIsbn(book.getIsbn())).thenReturn(false);
        when(bookRepository.save(any(Book.class))).thenReturn(book);

        Book saved = bookService.addBook(book);

        assertThat(saved).isNotNull();
        assertThat(saved.getIsbn()).isEqualTo(book.getIsbn());
        verify(bookRepository).save(any(Book.class));
    }

    @Test
    void addBookDuplicateIsbnThrows() {
        when(bookRepository.existsByIsbn(book.getIsbn())).thenReturn(true);

        assertThatThrownBy(() -> bookService.addBook(book))
                .isInstanceOf(DuplicateIsbnException.class)
                .hasMessageContaining("ISBN already exists");
    }

    @Test
    void getBookByIdSuccess() {
        when(bookRepository.findById(1L)).thenReturn(Optional.of(book));

        Book found = bookService.getBookById(1L);

        assertThat(found).isEqualTo(book);
    }

    @Test
    void getBookByIdNotFoundThrows() {
        when(bookRepository.findById(1L)).thenReturn(Optional.empty());

        assertThatThrownBy(() -> bookService.getBookById(1L))
                .isInstanceOf(BookNotFoundException.class)
                .hasMessageContaining("Book not found");
    }

    @Test
    void decreaseInventorySuccess() {
        book.setInventoryCount(1);
        when(bookRepository.save(any(Book.class))).thenReturn(book);

        bookService.decreaseInventory(book);

        assertThat(book.getInventoryCount()).isEqualTo(0);
        verify(bookRepository).save(book);
    }

    @Test
    void decreaseInventoryZeroThrows() {
        book.setInventoryCount(0);

        assertThatThrownBy(() -> bookService.decreaseInventory(book))
                .isInstanceOf(IllegalStateException.class)
                .hasMessageContaining("inventory is zero");
    }
}
