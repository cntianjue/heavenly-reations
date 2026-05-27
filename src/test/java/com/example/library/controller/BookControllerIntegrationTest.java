package com.example.library.controller;

import com.example.library.entity.Book;
import com.example.library.repository.BookRepository;
import com.fasterxml.jackson.databind.ObjectMapper;
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
@ActiveProfiles("test")
class BookControllerIntegrationTest {

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
    void addBookAndGetById() throws Exception {
        Book book = new Book("Integration Title", "Integration Author", "111-2223334445", 10);

        mockMvc.perform(post("/books")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(book)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id").isNumber())
                .andExpect(jsonPath("$.title").value("Integration Title"));

        // Verify we can get it
        mockMvc.perform(get("/books/1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.isbn").value("111-2223334445"));
    }

    @Test
    void addDuplicateIsbnReturnsBadRequest() throws Exception {
        Book book1 = new Book("One", "Author1", "DUPLICATE-ISBN", 1);
        bookRepository.save(book1);

        Book book2 = new Book("Two", "Author2", "DUPLICATE-ISBN", 1);

        mockMvc.perform(post("/books")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(book2)))
                .andExpect(status().isBadRequest());
    }

    @Test
    void borrowAndReturnIntegration() throws Exception {
        Book book = new Book("Borrowable", "Author B", "ISBN-BORROW-001", 2);
        Book saved = bookRepository.save(book);

        mockMvc.perform(post("/borrow")
                        .param("bookId", saved.getId().toString()))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.inventoryCount").value(1));

        mockMvc.perform(post("/borrow/return")
                        .param("bookId", saved.getId().toString()))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.inventoryCount").value(2));
    }

    @Test
    void borrowWhenInventoryZeroReturnsBadRequest() throws Exception {
        Book book = new Book("OutOfStock", "Author O", "ISBN-OUT-001", 0);
        Book saved = bookRepository.save(book);

        mockMvc.perform(post("/borrow")
                        .param("bookId", saved.getId().toString()))
                .andExpect(status().isBadRequest());
    }
}
