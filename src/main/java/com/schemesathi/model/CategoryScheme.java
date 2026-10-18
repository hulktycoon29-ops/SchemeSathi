package com.schemesathi.model;

import java.util.Collections;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

/**
 * Concrete scheme specialization based on social category reservation/eligibility.
 * Demonstrates Inheritance and Polymorphism by extending {@link Scheme}
 * and implementing {@link #isEligible(Student)}.
 */
public class CategoryScheme extends Scheme {
    private final Set<String> allowedCategories;

    public CategoryScheme(String id, String name, List<String> requiredDocuments, Set<String> allowedCategories) {
        super(id, name, requiredDocuments);
        if (allowedCategories == null || allowedCategories.isEmpty()) {
            throw new IllegalArgumentException("Allowed categories cannot be empty for CategoryScheme.");
        }
        // Store normalized upper-case set for consistent case-insensitive comparison
        this.allowedCategories = allowedCategories.stream()
                .filter(cat -> cat != null && !cat.trim().isEmpty())
                .map(String::trim)
                .map(String::toUpperCase)
                .collect(Collectors.toUnmodifiableSet());

        if (this.allowedCategories.isEmpty()) {
            throw new IllegalArgumentException("Allowed categories cannot contain only blank strings.");
        }
    }

    public Set<String> getAllowedCategories() {
        return allowedCategories;
    }

    @Override
    public boolean isEligible(Student student) {
        if (student == null || student.getCategory() == null) {
            return false;
        }
        return allowedCategories.contains(student.getCategory().trim().toUpperCase());
    }

    @Override
    public String getType() {
        return "CATEGORY";
    }

    @Override
    public String getCriteriaSummary() {
        return "Allowed Categories: " + String.join(", ", allowedCategories);
    }
}
