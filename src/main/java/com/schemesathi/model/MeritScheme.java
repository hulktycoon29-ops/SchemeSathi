package com.schemesathi.model;

import java.util.List;

/**
 * Concrete scheme specialization based on academic marks threshold.
 * Demonstrates Inheritance and Polymorphism by extending {@link Scheme}
 * and implementing {@link #isEligible(Student)}.
 */
public class MeritScheme extends Scheme {
    private final double minimumMarks;

    public MeritScheme(String id, String name, List<String> requiredDocuments, double minimumMarks) {
        super(id, name, requiredDocuments);
        if (minimumMarks < 0.0 || minimumMarks > 100.0) {
            throw new IllegalArgumentException("Minimum marks must be between 0 and 100. Received: " + minimumMarks);
        }
        this.minimumMarks = minimumMarks;
    }

    public double getMinimumMarks() {
        return minimumMarks;
    }

    @Override
    public boolean isEligible(Student student) {
        if (student == null) {
            return false;
        }
        return student.getMarks() >= minimumMarks;
    }

    @Override
    public String getType() {
        return "MERIT";
    }

    @Override
    public String getCriteriaSummary() {
        return String.format("Minimum Marks: %.1f%%", minimumMarks);
    }
}
