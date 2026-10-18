package com.schemesathi.report;

import com.schemesathi.model.MeritScheme;
import com.schemesathi.model.Scheme;
import com.schemesathi.model.Student;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class EligibilityReportWriterTest {

    private final EligibilityReportWriter writer = new EligibilityReportWriter();

    @Test
    @DisplayName("Write valid report with eligible schemes")
    void testWriteReportWithEligible(@TempDir Path tempDir) throws IOException {
        Path reportFile = tempDir.resolve("output").resolve("report.txt");
        Student student = new Student(92.0, 180000.0, "OBC");
        Scheme scheme = new MeritScheme("M1", "National Merit Award", List.of("Marksheet", "ID Proof"), 85.0);

        writer.write(reportFile, student, List.of(scheme));

        assertTrue(Files.exists(reportFile));
        String content = Files.readString(reportFile);
        assertTrue(content.contains("SchemeSathi Eligibility Report"));
        assertTrue(content.contains("92.00%"));
        assertTrue(content.contains("National Merit Award"));
        assertTrue(content.contains("Marksheet"));
    }

    @Test
    @DisplayName("Write report when no schemes match")
    void testWriteReportWithNone(@TempDir Path tempDir) throws IOException {
        Path reportFile = tempDir.resolve("none_report.txt");
        Student student = new Student(40.0, 900000.0, "General");

        writer.write(reportFile, student, List.of());

        assertTrue(Files.exists(reportFile));
        String content = Files.readString(reportFile);
        assertTrue(content.contains("No matching schemes were found for this profile."));
    }
}
