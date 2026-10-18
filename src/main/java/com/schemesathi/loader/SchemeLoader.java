package com.schemesathi.loader;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.schemesathi.model.CategoryScheme;
import com.schemesathi.model.IncomeScheme;
import com.schemesathi.model.MeritScheme;
import com.schemesathi.model.Scheme;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

/**
 * Loads and validates scholarship scheme definitions from a JSON file.
 * Handles missing files, malformed JSON, and rule schema validation.
 */
public class SchemeLoader {
    private final ObjectMapper objectMapper;

    public SchemeLoader() {
        this.objectMapper = new ObjectMapper();
    }

    /**
     * Reads and parses schemes from the given file path.
     *
     * @param path Path to the schemes JSON file
     * @return List of validated concrete Scheme instances
     * @throws IOException if file reading or parsing fails
     * @throws IllegalArgumentException if rules violate schema constraints
     */
    public List<Scheme> load(Path path) throws IOException {
        if (path == null) {
            throw new IllegalArgumentException("Path cannot be null.");
        }
        if (!Files.exists(path)) {
            throw new IOException("Rules file does not exist at path: " + path.toAbsolutePath());
        }
        if (!Files.isRegularFile(path)) {
            throw new IOException("Rules file is not a regular file: " + path.toAbsolutePath());
        }
        if (!Files.isReadable(path)) {
            throw new IOException("Rules file is not readable: " + path.toAbsolutePath());
        }

        String jsonContent = Files.readString(path, StandardCharsets.UTF_8).trim();
        if (jsonContent.isEmpty()) {
            throw new IOException("Rules file is empty: " + path.toAbsolutePath());
        }

        return parseJson(jsonContent);
    }

    /**
     * Parses raw JSON string into a list of Scheme instances.
     *
     * @param jsonContent Valid JSON string
     * @return List of validated Scheme instances
     * @throws IOException on JSON syntax error
     */
    public List<Scheme> parseJson(String jsonContent) throws IOException {
        List<SchemeRule> rules;
        try {
            rules = objectMapper.readValue(jsonContent, new TypeReference<List<SchemeRule>>() {});
        } catch (Exception e) {
            throw new IOException("Malformed JSON in rules configuration: " + e.getMessage(), e);
        }

        if (rules == null || rules.isEmpty()) {
            throw new IllegalArgumentException("Rules configuration must contain at least one scholarship scheme.");
        }

        List<Scheme> schemes = new ArrayList<>();
        Set<String> seenIds = new HashSet<>();

        for (int i = 0; i < rules.size(); i++) {
            SchemeRule rule = rules.get(i);
            int ruleIndex = i + 1;

            if (rule == null) {
                throw new IllegalArgumentException(String.format("Rule #%d is null.", ruleIndex));
            }
            if (rule.getId() == null || rule.getId().trim().isEmpty()) {
                throw new IllegalArgumentException(String.format("Rule #%d is missing required field 'id'.", ruleIndex));
            }

            String id = rule.getId().trim();
            if (!seenIds.add(id.toUpperCase())) {
                throw new IllegalArgumentException(String.format("Duplicate scheme ID '%s' found in rules.", id));
            }

            if (rule.getName() == null || rule.getName().trim().isEmpty()) {
                throw new IllegalArgumentException(String.format("Scheme '%s' is missing required field 'name'.", id));
            }
            if (rule.getType() == null || rule.getType().trim().isEmpty()) {
                throw new IllegalArgumentException(String.format("Scheme '%s' is missing required field 'type'.", id));
            }
            if (rule.getRequiredDocuments() == null || rule.getRequiredDocuments().isEmpty()) {
                throw new IllegalArgumentException(String.format("Scheme '%s' must specify at least one required document.", id));
            }

            String type = rule.getType().trim().toUpperCase();
            switch (type) {
                case "MERIT":
                    if (rule.getMinimumMarks() == null) {
                        throw new IllegalArgumentException(String.format("MERIT scheme '%s' is missing 'minimumMarks'.", id));
                    }
                    if (rule.getMinimumMarks() < 0.0 || rule.getMinimumMarks() > 100.0) {
                        throw new IllegalArgumentException(String.format("MERIT scheme '%s' has invalid 'minimumMarks' (must be 0-100): %s", id, rule.getMinimumMarks()));
                    }
                    schemes.add(new MeritScheme(id, rule.getName(), rule.getRequiredDocuments(), rule.getMinimumMarks()));
                    break;

                case "INCOME":
                    if (rule.getMaximumAnnualIncome() == null) {
                        throw new IllegalArgumentException(String.format("INCOME scheme '%s' is missing 'maximumAnnualIncome'.", id));
                    }
                    if (rule.getMaximumAnnualIncome() < 0.0) {
                        throw new IllegalArgumentException(String.format("INCOME scheme '%s' has negative 'maximumAnnualIncome': %s", id, rule.getMaximumAnnualIncome()));
                    }
                    schemes.add(new IncomeScheme(id, rule.getName(), rule.getRequiredDocuments(), rule.getMaximumAnnualIncome()));
                    break;

                case "CATEGORY":
                    if (rule.getAllowedCategories() == null || rule.getAllowedCategories().isEmpty()) {
                        throw new IllegalArgumentException(String.format("CATEGORY scheme '%s' is missing or has empty 'allowedCategories'.", id));
                    }
                    Set<String> categories = new HashSet<>(rule.getAllowedCategories());
                    schemes.add(new CategoryScheme(id, rule.getName(), rule.getRequiredDocuments(), categories));
                    break;

                default:
                    throw new IllegalArgumentException(String.format("Unsupported scheme type '%s' in scheme '%s'. Supported types: MERIT, INCOME, CATEGORY.", type, id));
            }
        }

        return schemes;
    }
}
