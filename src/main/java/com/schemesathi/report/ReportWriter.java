package com.schemesathi.report;

import com.schemesathi.model.Scheme;
import com.schemesathi.model.Student;

import java.io.IOException;
import java.nio.file.Path;
import java.util.List;

/**
 * Interface defining the contract for writing eligibility evaluation reports.
 * Demonstrates programming to an interface rather than a concrete implementation.
 */
public interface ReportWriter {
    /**
     * Writes the student criteria and eligible schemes report to the destination file.
     *
     * @param destination File path where report will be saved
     * @param student The student profile
     * @param schemes The matching eligible schemes
     * @throws IOException if destination cannot be written
     */
    void write(Path destination, Student student, List<Scheme> schemes) throws IOException;
}
