package com.schemesathi.service;

import com.schemesathi.model.Scheme;
import com.schemesathi.model.Student;

import java.util.Collections;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;

/**
 * Service orchestrating scholarship eligibility evaluations.
 * Demonstrates Polymorphism by executing {@link Scheme#isEligible(Student)}
 * through base Scheme references without knowing their concrete subclasses.
 */
public class EligibilityService {

    /**
     * Finds and returns all schemes for which the given student is eligible.
     *
     * @param student The validated student profile
     * @param schemes The collection of loaded scholarship schemes
     * @return List of schemes meeting eligibility criteria (may be empty if no matches)
     * @throws IllegalArgumentException if student or schemes collection is null
     */
    public List<Scheme> findEligible(Student student, List<Scheme> schemes) {
        if (student == null) {
            throw new IllegalArgumentException("Student profile cannot be null for eligibility evaluation.");
        }
        if (schemes == null) {
            throw new IllegalArgumentException("Schemes list cannot be null for eligibility evaluation.");
        }

        return schemes.stream()
                .filter(Objects::nonNull)
                .filter(scheme -> scheme.isEligible(student))
                .collect(Collectors.toList());
    }
}
