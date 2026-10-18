package com.schemesathi.model;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

import static org.junit.jupiter.api.Assertions.*;

class StudentTest {

    @Test
    @DisplayName("Valid student creation succeeds")
    void testValidStudent() {
        Student s = new Student(85.5, 250000.0, "OBC");
        assertEquals(85.5, s.getMarks());
        assertEquals(250000.0, s.getAnnualFamilyIncome());
        assertEquals("OBC", s.getCategory());
    }

    @ParameterizedTest
    @ValueSource(doubles = {-1.0, -0.01, 100.01, 120.0})
    @DisplayName("Invalid marks throw IllegalArgumentException")
    void testInvalidMarks(double invalidMarks) {
        assertThrows(IllegalArgumentException.class, () -> new Student(invalidMarks, 200000, "General"));
    }

    @Test
    @DisplayName("Negative income throws IllegalArgumentException")
    void testNegativeIncome() {
        assertThrows(IllegalArgumentException.class, () -> new Student(75, -500, "General"));
    }

    @ParameterizedTest
    @ValueSource(strings = {"", "   "})
    @DisplayName("Blank category throws IllegalArgumentException")
    void testBlankCategory(String invalidCategory) {
        assertThrows(IllegalArgumentException.class, () -> new Student(75, 200000, invalidCategory));
    }

    @Test
    @DisplayName("Null category throws IllegalArgumentException")
    void testNullCategory() {
        assertThrows(IllegalArgumentException.class, () -> new Student(75, 200000, null));
    }
}
