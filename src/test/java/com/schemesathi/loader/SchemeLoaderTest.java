package com.schemesathi.loader;

import com.schemesathi.model.Scheme;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class SchemeLoaderTest {

    private final SchemeLoader loader = new SchemeLoader();

    @Test
    @DisplayName("Load valid schemes.json file from data directory")
    void testLoadExistingSchemes() throws IOException {
        Path path = Path.of("data", "schemes.json");
        List<Scheme> schemes = loader.load(path);
        assertNotNull(schemes);
        assertFalse(schemes.isEmpty());
        assertEquals(9, schemes.size());
    }

    @Test
    @DisplayName("Throws IOException when file does not exist")
    void testNonExistentFile() {
        Path invalid = Path.of("data", "does_not_exist.json");
        assertThrows(IOException.class, () -> loader.load(invalid));
    }

    @Test
    @DisplayName("Throws IllegalArgumentException for malformed rule schema")
    void testMalformedRuleSchema(@TempDir Path tempDir) throws IOException {
        Path malformedFile = tempDir.resolve("bad_schemes.json");
        // Missing required documents
        String badJson = "[{\"id\":\"M1\",\"name\":\"Bad Scheme\",\"type\":\"MERIT\",\"minimumMarks\":80.0,\"requiredDocuments\":[]}]";
        Files.writeString(malformedFile, badJson);

        assertThrows(IllegalArgumentException.class, () -> loader.load(malformedFile));
    }
}
