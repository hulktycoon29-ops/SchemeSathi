package com.schemesathi.loader;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import java.util.List;

/**
 * Data Transfer Object (DTO) for deserializing scheme configuration from JSON.
 */
@JsonIgnoreProperties(ignoreUnknown = true)
public class SchemeRule {
    private String id;
    private String name;
    private String type;
    private Double minimumMarks;
    private Double maximumAnnualIncome;
    private List<String> allowedCategories;
    private List<String> requiredDocuments;

    public SchemeRule() {
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public Double getMinimumMarks() {
        return minimumMarks;
    }

    public void setMinimumMarks(Double minimumMarks) {
        this.minimumMarks = minimumMarks;
    }

    public Double getMaximumAnnualIncome() {
        return maximumAnnualIncome;
    }

    public void setMaximumAnnualIncome(Double maximumAnnualIncome) {
        this.maximumAnnualIncome = maximumAnnualIncome;
    }

    public List<String> getAllowedCategories() {
        return allowedCategories;
    }

    public void setAllowedCategories(List<String> allowedCategories) {
        this.allowedCategories = allowedCategories;
    }

    public List<String> getRequiredDocuments() {
        return requiredDocuments;
    }

    public void setRequiredDocuments(List<String> requiredDocuments) {
        this.requiredDocuments = requiredDocuments;
    }
}
