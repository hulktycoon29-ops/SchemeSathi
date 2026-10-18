package com.schemesathi.model;

import java.util.Collections;
import java.util.List;
import java.util.Objects;

/**
 * Abstract base class for all scholarship schemes.
 * Demonstrates Abstraction by specifying shared attributes and the common
 * eligibility evaluation contract {@link #isEligible(Student)}.
 */
public abstract class Scheme {
    private final String id;
    private final String name;
    private final List<String> requiredDocuments;

    /**
     * Initializes base scheme attributes with validation and defensive copying.
     *
     * @param id Unique non-blank scheme identifier
     * @param name Descriptive non-blank scheme name
     * @param requiredDocuments Non-empty list of required document names
     */
    protected Scheme(String id, String name, List<String> requiredDocuments) {
        if (id == null || id.trim().isEmpty()) {
            throw new IllegalArgumentException("Scheme ID cannot be blank.");
        }
        if (name == null || name.trim().isEmpty()) {
            throw new IllegalArgumentException("Scheme name cannot be blank.");
        }
        if (requiredDocuments == null || requiredDocuments.isEmpty()) {
            throw new IllegalArgumentException("Scheme must specify at least one required document.");
        }

        this.id = id.trim();
        this.name = name.trim();
        this.requiredDocuments = List.copyOf(requiredDocuments);
    }

    public String getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public List<String> getRequiredDocuments() {
        return requiredDocuments;
    }

    /**
     * Evaluates whether the given student qualifies for this scheme.
     * Overridden polymorphically by concrete scheme subclasses.
     *
     * @param student The student profile being evaluated
     * @return true if student meets eligibility requirements, false otherwise
     */
    public abstract boolean isEligible(Student student);

    /**
     * Returns the scheme category/type discriminator (e.g. MERIT, INCOME, CATEGORY).
     */
    public abstract String getType();

    /**
     * Returns a human-readable description of the eligibility requirement.
     */
    public abstract String getCriteriaSummary();

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Scheme scheme)) return false;
        return id.equalsIgnoreCase(scheme.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id.toUpperCase());
    }

    @Override
    public String toString() {
        return String.format("%s [%s] (%s)", name, id, getType());
    }
}
