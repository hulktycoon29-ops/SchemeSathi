package com.schemesathi.ui;

import com.schemesathi.loader.SchemeLoader;
import com.schemesathi.model.Scheme;
import com.schemesathi.model.Student;
import com.schemesathi.report.EligibilityReportWriter;
import com.schemesathi.report.ReportWriter;
import com.schemesathi.service.EligibilityService;

import java.io.IOException;
import java.nio.file.Path;
import java.util.List;
import java.util.Scanner;

/**
 * Handles the console interaction workflow as specified in the PRD and Architecture guide.
 */
public class ConsoleUI {
    private final SchemeLoader schemeLoader;
    private final EligibilityService eligibilityService;
    private final ReportWriter reportWriter;
    private final Scanner scanner;

    public ConsoleUI() {
        this(new SchemeLoader(), new EligibilityService(), new EligibilityReportWriter(), new Scanner(System.in));
    }

    public ConsoleUI(SchemeLoader schemeLoader, EligibilityService eligibilityService,
                     ReportWriter reportWriter, Scanner scanner) {
        this.schemeLoader = schemeLoader;
        this.eligibilityService = eligibilityService;
        this.reportWriter = reportWriter;
        this.scanner = scanner;
    }

    public void run() {
        printBanner();

        // 1. Collect student details
        Student student = promptForStudent();
        if (student == null) {
            System.out.println("\n[!] Operation cancelled by user.");
            return;
        }

        // 2. Load scheme rules
        Path rulesPath = Path.of("data", "schemes.json");
        List<Scheme> loadedSchemes;
        try {
            System.out.println("\n[*] Loading scholarship scheme definitions from " + rulesPath + "...");
            loadedSchemes = schemeLoader.load(rulesPath);
            System.out.printf("[✓] Successfully loaded %d scholarship scheme(s).\n", loadedSchemes.size());
        } catch (IOException | IllegalArgumentException ex) {
            System.err.println("\n[X] ERROR: Could not load scholarship schemes:");
            System.err.println("    " + ex.getMessage());
            System.err.println("    Evaluation halted to prevent inaccurate or incomplete results.");
            return;
        }

        // 3. Evaluate eligibility
        System.out.println("[*] Evaluating eligibility against student profile...");
        List<Scheme> eligibleSchemes = eligibilityService.findEligible(student, loadedSchemes);

        // 4. Display results
        displayResults(student, eligibleSchemes);

        // 5. Prompt for saving report
        promptSaveReport(student, eligibleSchemes);

        System.out.println("\nThank you for using SchemeSathi!");
    }

    private void printBanner() {
        System.out.println("==================================================================");
        System.out.println("               SCHEMESATHI — Scholarship Navigator               ");
        System.out.println("==================================================================");
        System.out.println("Disclaimer: Results are indicative based on configured rules.");
        System.out.println("This is an educational navigator, not an official government grant.");
        System.out.println("------------------------------------------------------------------");
    }

    private Student promptForStudent() {
        double marks = -1;
        while (true) {
            System.out.print("Enter your academic marks (percentage 0.0 - 100.0): ");
            String input = scanner.nextLine().trim();
            if (input.equalsIgnoreCase("q") || input.equalsIgnoreCase("exit")) return null;
            try {
                marks = Double.parseDouble(input);
                if (marks < 0.0 || marks > 100.0) {
                    System.out.println(" [!] Invalid input: Marks must be between 0 and 100. Try again.");
                    continue;
                }
                break;
            } catch (NumberFormatException e) {
                System.out.println(" [!] Invalid input: Please enter a valid decimal number. Try again.");
            }
        }

        double income = -1;
        while (true) {
            System.out.print("Enter annual family income (in INR ₹, non-negative): ");
            String input = scanner.nextLine().trim();
            if (input.equalsIgnoreCase("q") || input.equalsIgnoreCase("exit")) return null;
            try {
                income = Double.parseDouble(input);
                if (income < 0.0) {
                    System.out.println(" [!] Invalid input: Income cannot be negative. Try again.");
                    continue;
                }
                break;
            } catch (NumberFormatException e) {
                System.out.println(" [!] Invalid input: Please enter a valid monetary amount. Try again.");
            }
        }

        String category = "";
        while (true) {
            System.out.print("Enter category (e.g. General, OBC, SC, ST, EWS): ");
            category = scanner.nextLine().trim();
            if (category.equalsIgnoreCase("q") || category.equalsIgnoreCase("exit")) return null;
            if (category.isEmpty()) {
                System.out.println(" [!] Invalid input: Category cannot be blank. Try again.");
                continue;
            }
            break;
        }

        try {
            return new Student(marks, income, category);
        } catch (IllegalArgumentException e) {
            System.err.println(" [X] Validation failed: " + e.getMessage());
            return null;
        }
    }

    private void displayResults(Student student, List<Scheme> eligibleSchemes) {
        System.out.println("\n==================================================================");
        System.out.println("                       ELIGIBILITY RESULTS                        ");
        System.out.println("==================================================================");
        System.out.printf("Profile: Marks: %.2f%% | Family Income: ₹%,.2f | Category: %s\n",
                student.getMarks(), student.getAnnualFamilyIncome(), student.getCategory());
        System.out.println("------------------------------------------------------------------");

        if (eligibleSchemes.isEmpty()) {
            System.out.println("\n[-] No matching scholarship schemes were found for your profile.");
            System.out.println("    You may check if relaxing category, marks, or income criteria matches");
            System.out.println("    other available regional or state programs.");
        } else {
            System.out.printf("\n[+] Congratulations! You appear ELIGIBLE for %d scholarship scheme(s):\n\n",
                    eligibleSchemes.size());

            int count = 1;
            for (Scheme scheme : eligibleSchemes) {
                System.out.printf("  %d. %s [%s]\n", count++, scheme.getName(), scheme.getId());
                System.out.printf("     Category/Type: %s\n", scheme.getType());
                System.out.printf("     Criteria:      %s\n", scheme.getCriteriaSummary());
                System.out.println("     Required Documents:");
                for (String doc : scheme.getRequiredDocuments()) {
                    System.out.printf("       • %s\n", doc);
                }
                System.out.println();
            }
        }
        System.out.println("==================================================================");
    }

    private void promptSaveReport(Student student, List<Scheme> eligibleSchemes) {
        System.out.print("\nWould you like to save this report to a text file? (y/n): ");
        String answer = scanner.nextLine().trim().toLowerCase();
        if (answer.startsWith("y")) {
            Path reportPath = Path.of("output", "eligibility-report.txt");
            try {
                reportWriter.write(reportPath, student, eligibleSchemes);
                System.out.println("[✓] Report successfully saved to: " + reportPath.toAbsolutePath());
            } catch (IOException e) {
                System.err.println("[X] ERROR: Could not save report to " + reportPath.toAbsolutePath());
                System.err.println("    Reason: " + e.getMessage());
            }
        }
    }
}
