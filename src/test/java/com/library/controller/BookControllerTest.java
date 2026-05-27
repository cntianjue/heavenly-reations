package com.library.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.library.entity.Book;
import com.library.repository.BookRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;

import static org.hamcrest.Matchers.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")  // Use application-test.properties for in-memory database
public class BookControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private BookRepository bookRepository;

    @Autowired
    private ObjectMapper objectMapper;

    @BeforeEach
    void setUp() {
        bookRepository.deleteAll();
    }

    @Test
    void shouldAddBook() throws Exception {
        Book book = new Book("1234567890", "Test Title", "Test Author", 10);

        mockMvc.perform(post("/books")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(book)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.isbn", is("1234567890")));
    }

    @Test
    void shouldFailAddingDuplicateIsbn() throws Exception {
        Book book1 = new Book("1111111111", "Book One", "Author1", 5);
        bookRepository.save(book1);

        Book book2 = new Book("1111111111", "Book Two", "Author2", 3);

        mockMvc.perform(post("/books")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(book2)))
                .andExpect(status().isConflict());
    }

    @Test
    void shouldGetAllBooks() throws Exception {
        bookRepository.save(new Book("2222222222", "Book1", "Auth1", 1));

        mockMvc.perform(get("/books"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(1)));
    }

    @Test
    void shouldGetBookById() throws Exception {
        Book saved = bookRepository.save(new Book("3333333333", "Single", "Auth", 2));

        mockMvc.perform(get("/books/" + saved.getId()))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.title", is("Single")));
    }

    @Test
    void shouldReturn404ForNonExistingBook() throws Exception {
        mockMvc.perform(get("/books/9999"))
                .andExpect(status().isNotFound());
    }

    @Test
    void shouldUpdateBook() throws Exception {
        Book saved = bookRepository.save(new Book("4444444444", "Old Title", "Old Author", 7));
        Book update = new Book();
        update.setTitle("New Title");

        mockMvc.perform(put("/books/" + saved.getId())
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(update)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.title", is("New Title")))
                .andExpect(jsonPath("$.author", is("Old Author")));
    }

    @Test
    void shouldDeleteBook() throws Exception {
        Book saved = bookRepository.save(new Book("5555555555", "Delete Me", "Auth", 0));

        mockMvc.perform(delete("/books/" + saved.getId()))
                .andExpect(status().isOk());

        mockMvc.perform(get("/books/" + saved.getId()))
                .andExpect(status().isNotFound());
    }

    @Test
    void shouldBorrowBookSuccessfully() throws Exception {
        Book book = new Book("6666666666", "Borrowable", "Auth", 3);
        Book saved = bookRepository.save(book);

        mockMvc.perform(post("/books/" + saved.getId() + "/borrow"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.message", is("Book borrowed successfully")));

        mockMvc.perform(get("/books/" + saved.getId()))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.inventoryCount", is(2)));
    }

    @Test
    void shouldFailBorrowWhenInventoryZero() throws Exception {
        Book book = new Book("7777777777", "No Stock", "Auth", 0);
        Book saved = bookRepository.save(book);

        mockMvc.perform(post("/books/" + saved.getId() + "/borrow"))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.error", is("Inventory is zero")));
    }

    @Test
    void shouldReturnBookSuccessfully() throws Exception {
        Book book = new Book("8888888888", "Returnable", "Auth", 1);
        Book saved = bookRepository.save(book);

        mockMvc.perform(post("/books/" + saved.getId() + "/return"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.message", is("Book returned successfully")));

        mockMvc.perform(get("/books/" + saved.getId()))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.inventoryCount", is(2)));
    }
}
