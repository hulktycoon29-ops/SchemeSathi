package com.schemesathi.model;

import java.util.Objects;

/**
 * Encapsulates a student profile containing academic marks, annual family income,
 * and social category. Demonstrates encapsulation by maintaining private, final
 * fields and enforcing validation rules at construction.
 */
public final class Student {
    private final double marks;
    private final double annualFamilyIncome;
    private final String category;

    /**
     * Constructs and validates a Student profile.
     *
     * @param marks Percentage score between 0 and 100
     * @param annualFamilyIncome Annual family income in INR (non-negative)
     * @param category Non-empty category name (e.g. General, OBC, SC, ST, EWS)
     * @throws IllegalArgumentException if any field fails validation
     */
    public Student(double marks, double annualFamilyIncome, String category) {
        if (marks < 0.0 || marks > 100.0) {
            throw new IllegalArgumentException("Marks must be between 0 and 100. Received: " + marks);
        }
        if (annualFamilyIncome < 0.0) {
            throw new IllegalArgumentException("Annual family income cannot be negative. Received: " + annualFamilyIncome);
        }
        if (category == null || category.trim().isEmpty()) {
            throw new IllegalArgumentException("Category is required and cannot be blank.");
        }

        this.marks = marks;
        this.annualFamilyIncome = annualFamilyIncome;
        this.category = category.trim();
    }

    public double getMarks() {
        return marks;
    }

    public double getAnnualFamilyIncome() {
        return annualFamilyIncome;
    }

    public String getCategory() {
        return category;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Student student)) return false;
        return Double.compare(student.marks, marks) == 0 &&
               Double.compare(student.annualFamilyIncome, annualFamilyIncome) == 0 &&
               category.equalsIgnoreCase(student.category);
    }

    @Override
    public int hashCode() {
        return Objects.hash(marks, annualFamilyIncome, category.toUpperCase());
    }

    @Override
    public String toString() {
        return String.format("Student[marks=%.2f%%, income=₹%.2f, category='%s']",
                marks, annualFamilyIncome, category);
    }
}
