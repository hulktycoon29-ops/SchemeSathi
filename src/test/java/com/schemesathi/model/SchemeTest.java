package com.schemesathi.model;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Set;

import static org.junit.jupiter.api.Assertions.*;

class SchemeTest {

    @Test
    @DisplayName("MeritScheme threshold boundary evaluation")
    void testMeritScheme() {
        MeritScheme scheme = new MeritScheme("M1", "Merit Award", List.of("Marksheet"), 75.0);
        
        Student eligibleExact = new Student(75.0, 500000, "General");
        Student eligibleHigher = new Student(90.0, 500000, "General");
        Student ineligible = new Student(74.9, 500000, "General");

        assertTrue(scheme.isEligible(eligibleExact));
        assertTrue(scheme.isEligible(eligibleHigher));
        assertFalse(scheme.isEligible(ineligible));
    }

    @Test
    @DisplayName("IncomeScheme ceiling boundary evaluation")
    void testIncomeScheme() {
        IncomeScheme scheme = new IncomeScheme("I1", "Need Award", List.of("Income Cert"), 250000.0);

        Student eligibleExact = new Student(60.0, 250000.0, "General");
        Student eligibleLower = new Student(60.0, 100000.0, "General");
        Student ineligible = new Student(60.0, 250000.01, "General");

        assertTrue(scheme.isEligible(eligibleExact));
        assertTrue(scheme.isEligible(eligibleLower));
        assertFalse(scheme.isEligible(ineligible));
    }

    @Test
    @DisplayName("CategoryScheme case-insensitive matching")
    void testCategoryScheme() {
        CategoryScheme scheme = new CategoryScheme("C1", "OBC Scheme", List.of("Caste Cert"), Set.of("OBC", "EWS"));

        Student obcLower = new Student(60.0, 400000.0, "obc");
        Student ewsUpper = new Student(60.0, 400000.0, "EWS");
        Student general = new Student(60.0, 400000.0, "General");

        assertTrue(scheme.isEligible(obcLower));
        assertTrue(scheme.isEligible(ewsUpper));
        assertFalse(scheme.isEligible(general));
    }
}
