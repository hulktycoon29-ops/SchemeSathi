package com.schemesathi.service;

import com.schemesathi.model.*;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Set;

import static org.junit.jupiter.api.Assertions.*;

class EligibilityServiceTest {

    @Test
    @DisplayName("EligibilityService finds all qualifying schemes polymorphically")
    void testFindEligibleMultiple() {
        EligibilityService service = new EligibilityService();

        Scheme merit = new MeritScheme("M1", "Merit", List.of("Marksheet"), 80.0);
        Scheme income = new IncomeScheme("I1", "Income", List.of("Income Cert"), 300000.0);
        Scheme category = new CategoryScheme("C1", "Category", List.of("Caste Cert"), Set.of("SC", "ST"));

        List<Scheme> allSchemes = List.of(merit, income, category);

        // Student qualifies for merit and income, but not category
        Student student = new Student(85.0, 200000.0, "General");
        List<Scheme> eligible = service.findEligible(student, allSchemes);

        assertEquals(2, eligible.size());
        assertTrue(eligible.contains(merit));
        assertTrue(eligible.contains(income));
        assertFalse(eligible.contains(category));
    }

    @Test
    @DisplayName("EligibilityService returns empty list when no schemes match")
    void testFindEligibleNone() {
        EligibilityService service = new EligibilityService();

        Scheme merit = new MeritScheme("M1", "High Merit", List.of("Marksheet"), 95.0);
        Scheme income = new IncomeScheme("I1", "Strict Income", List.of("Income Cert"), 100000.0);

        Student student = new Student(70.0, 500000.0, "General");
        List<Scheme> eligible = service.findEligible(student, List.of(merit, income));

        assertTrue(eligible.isEmpty());
    }
}
