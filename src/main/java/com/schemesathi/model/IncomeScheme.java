package com.schemesathi.model;

import java.util.List;

/**
 * Concrete scheme specialization based on annual family income ceiling.
 * Demonstrates Inheritance and Polymorphism by extending {@link Scheme}
 * and implementing {@link #isEligible(Student)}.
 */
public class IncomeScheme extends Scheme {
    private final double maximumAnnualIncome;

    public IncomeScheme(String id, String name, List<String> requiredDocuments, double maximumAnnualIncome) {
        super(id, name, requiredDocuments);
        if (maximumAnnualIncome < 0.0) {
            throw new IllegalArgumentException("Maximum annual income cannot be negative. Received: " + maximumAnnualIncome);
        }
        this.maximumAnnualIncome = maximumAnnualIncome;
    }

    public double getMaximumAnnualIncome() {
        return maximumAnnualIncome;
    }

    @Override
    public boolean isEligible(Student student) {
        if (student == null) {
            return false;
        }
        return student.getAnnualFamilyIncome() <= maximumAnnualIncome;
    }

    @Override
    public String getType() {
        return "INCOME";
    }

    @Override
    public String getCriteriaSummary() {
        return String.format("Maximum Family Income: ₹%,.2f per annum", maximumAnnualIncome);
    }
}
