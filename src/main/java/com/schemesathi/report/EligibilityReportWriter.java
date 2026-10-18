package com.schemesathi.report;

import com.schemesathi.model.Scheme;
import com.schemesathi.model.Student;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;

/**
 * Concrete report writer that outputs evaluation results into a formatted plain-text report.
 * Implements {@link ReportWriter} and demonstrates robust Java NIO file handling.
 */
public class EligibilityReportWriter implements ReportWriter {

    @Override
    public void write(Path destination, Student student, List<Scheme> schemes) throws IOException {
        if (destination == null) {
            throw new IllegalArgumentException("Destination path cannot be null.");
        }
        if (student == null) {
            throw new IllegalArgumentException("Student profile cannot be null.");
        }
        if (schemes == null) {
            throw new IllegalArgumentException("Schemes list cannot be null.");
        }

        Path parent = destination.getParent();
        if (parent != null && !Files.exists(parent)) {
            Files.createDirectories(parent);
        }

        StringBuilder report = new StringBuilder();
        report.append("=================================================================\n");
        report.append("               SchemeSathi Eligibility Report                     \n");
        report.append("=================================================================\n");
        report.append("Generated on: ").append(LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"))).append('\n');
        report.append("Notice: This is an educational navigator report based on configured rules.\n");
        report.append("-----------------------------------------------------------------\n");
        report.append("STUDENT PROFILE:\n");
        report.append("  • Academic Marks: ").append(String.format("%.2f%%", student.getMarks())).append('\n');
        report.append("  • Annual Family Income: ").append(String.format("₹%,.2f", student.getAnnualFamilyIncome())).append('\n');
        report.append("  • Social Category: ").append(student.getCategory()).append('\n');
        report.append("-----------------------------------------------------------------\n");
        report.append("ELIGIBLE SCHEMES:\n");

        if (schemes.isEmpty()) {
            report.append("\nNo matching schemes were found for this profile.\n");
            report.append("Tip: Verify income thresholds, academic criteria, and category requirements.\n");
        } else {
            report.append(String.format("Found %d matching scholarship scheme(s):\n", schemes.size()));
            for (Scheme scheme : schemes) {
                report.append("\n• ")
                        .append(scheme.getName())
                        .append(" [ID: ").append(scheme.getId()).append("]")
                        .append(" (").append(scheme.getType()).append(")\n");
                report.append("  Criteria: ").append(scheme.getCriteriaSummary()).append('\n');
                report.append("  Required Documents:\n");
                for (String document : scheme.getRequiredDocuments()) {
                    report.append("    - ").append(document).append('\n');
                }
            }
        }
        report.append("\n=================================================================\n");
        report.append("End of SchemeSathi Report\n");

        Files.writeString(
                destination,
                report.toString(),
                StandardCharsets.UTF_8,
                StandardOpenOption.CREATE,
                StandardOpenOption.TRUNCATE_EXISTING,
                StandardOpenOption.WRITE
        );
    }
}
