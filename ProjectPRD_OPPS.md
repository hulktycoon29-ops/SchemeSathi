# SchemeSathi — Product Requirements Document (PRD)

## 1. Project Overview

**Project name:** SchemeSathi (Scholarship Eligibility Navigator)  
**Project type:** Java Object-Oriented Programming (OOP) project  
**Primary goal:** Help students identify scholarship schemes they may qualify for and understand which documents are required for each scheme.

SchemeSathi accepts a student's academic marks, family income, and category. It compares those details with scholarship rules stored in a JSON file, then lists the schemes for which the student appears eligible, along with the required documents.

The project demonstrates core Java OOP concepts and mandatory file handling. Scholarship rules are kept separate from the Java source code so that adding or updating a scheme can usually be done by editing the rules file rather than changing the program.

## 2. Abstract

Students can miss scholarship opportunities when eligibility requirements are difficult to find, interpret, or compare. SchemeSathi is a small Java application designed to make scholarship discovery clearer by evaluating a student's supplied details against a collection of configurable scheme rules. It reports matching schemes and their document requirements.

The project uses an abstract `Scheme` class and specialized scheme types such as `MeritScheme`, `IncomeScheme`, and `CategoryScheme`. Each type overrides `isEligible()` to demonstrate runtime polymorphism. Encapsulation protects student and scheme data, inheritance supports shared behavior, and abstraction defines a common eligibility contract. Composition, interfaces, collections, and exception handling may be used where they make the design clearer.

File handling is central to the application: the program reads scheme definitions from a JSON file and may write the eligibility report to a text file. Invalid or missing files and malformed rules must be handled without silently reporting incorrect eligibility. This is an educational navigator, not an official government eligibility determination; results depend on the accuracy and completeness of the configured rules.

## 3. Goals and Success Criteria

### 3.1 Goals

- Capture a student's marks, annual family income, and category.
- Load scholarship scheme definitions from a JSON rules file.
- Evaluate the student against the configured eligibility requirements.
- Display every configured scheme that matches the student's details.
- Show the documents required for each matching scheme.
- Demonstrate core Java OOP concepts through a coherent implementation.
- Demonstrate file reading, writing, validation, and error handling.

### 3.2 Success criteria

The project is considered successful when:

1. A valid student profile can be entered or constructed.
2. The application reads valid scheme definitions from the configured JSON file.
3. Each supported scheme type evaluates eligibility according to its configured rules.
4. The result includes all matching schemes among the successfully loaded schemes.
5. Each matching scheme displays its required documents.
6. A report can be written to a text file.
7. Missing, unreadable, or malformed input files produce a clear error rather than a misleading eligibility result.
8. The code visibly demonstrates encapsulation, inheritance, polymorphism, abstraction, and file handling.

## 4. Scope

### 4.1 In scope

- A Java console application.
- Student data: marks, annual family income, and category.
- Scheme definitions stored in a JSON file.
- `Scheme`, `MeritScheme`, `IncomeScheme`, and `CategoryScheme` classes.
- Eligibility evaluation and a list of required documents.
- A text-based results display.
- Optional saving of the results to a plain-text report file.
- Input validation and file-related error handling.
- Unit-testable eligibility logic.

### 4.2 Out of scope

- Submitting scholarship applications on a student's behalf.
- Verifying documents or contacting scholarship authorities.
- A web or mobile interface.
- User accounts, authentication, or online databases.
- Automatic discovery or downloading of scholarship rules from the internet.
- Legal or official confirmation that a student will receive funding.

## 5. Intended Users

- **Student:** Supplies the required profile details and reviews matching schemes and documents.
- **Project evaluator:** Reviews the Java implementation to confirm that OOP principles and file handling are demonstrated.

## 6. Functional Requirements

| ID | Requirement | Expected behavior |
|---|---|---|
| FR-01 | Student profile | Accept marks, annual family income, and category. |
| FR-02 | Validate profile | Reject marks outside the configured scale, negative income, and blank category. |
| FR-03 | Load rules | Read scheme definitions from a JSON file. |
| FR-04 | Validate rules | Check required fields, supported scheme type, threshold values, and document lists. |
| FR-05 | Evaluate schemes | Call the appropriate eligibility implementation for every loaded scheme. |
| FR-06 | Display matches | List every loaded scheme that evaluates as eligible. |
| FR-07 | Show documents | Display the document list associated with each eligible scheme. |
| FR-08 | No matches | Show a clear message if no loaded scheme matches. |
| FR-09 | Save report | Write the results to a plain-text report file when requested. |
| FR-10 | Handle failures | Report file and rule errors clearly; do not treat a failed rules load as a valid empty scheme list. |

## 7. Non-Functional Requirements

- **Clarity:** Console prompts, errors, and results should use straightforward language.
- **Maintainability:** Scheme data and eligibility logic should be separated.
- **Extensibility:** New schemes that use a supported rule type should be addable through JSON configuration.
- **Correctness:** Invalid input must not produce a positive eligibility result.
- **Portability:** Use standard Java file APIs and avoid machine-specific absolute paths.
- **Traceability:** Keep scheme identifiers or names in the output so students can identify each result.

## 8. Proposed Design

### 8.1 Main components

| Component | Responsibility |
|---|---|
| `Student` | Stores and validates the student's profile data. |
| `Scheme` | Abstract base class defining shared scheme data and the eligibility contract. |
| `MeritScheme` | Checks the minimum marks requirement. |
| `IncomeScheme` | Checks the maximum income requirement. |
| `CategoryScheme` | Checks whether the student's category is allowed. |
| `SchemeLoader` | Reads the JSON file and creates scheme objects. |
| `EligibilityService` | Evaluates all loaded schemes for a student. |
| `EligibilityReportWriter` | Writes results to a plain-text file. |
| `Main` | Coordinates input, loading, evaluation, display, and optional report saving. |

### 8.2 Example flow

1. Start the application.
2. Collect marks, annual family income, and category.
3. Validate and create a `Student` object.
4. Read and validate the scheme definitions from `schemes.json`.
5. Convert each supported definition into the matching `Scheme` subclass.
6. Call `isEligible(student)` on each scheme.
7. Display matching schemes and their required documents.
8. Optionally save the same results to `eligibility-report.txt`.
9. Finish with a clear message if no schemes match or if an operation fails.

## 9. OOP Concepts

The following snippets are illustrative Java examples. They show the intended design and may need imports, constructors, and supporting methods to compile as a complete application.

### 9.1 Encapsulation

**Purpose:** Keep fields private and control access through constructors and methods. This protects profile data from arbitrary changes and allows validation at the class boundary.

```java
public class Student {
    private final double marks;
    private final double annualFamilyIncome;
    private final String category;

    public Student(double marks, double annualFamilyIncome, String category) {
        if (marks < 0 || marks > 100) {
            throw new IllegalArgumentException("Marks must be between 0 and 100.");
        }
        if (annualFamilyIncome < 0) {
            throw new IllegalArgumentException("Income cannot be negative.");
        }
        if (category == null || category.isBlank()) {
            throw new IllegalArgumentException("Category is required.");
        }

        this.marks = marks;
        this.annualFamilyIncome = annualFamilyIncome;
        this.category = category.trim();
    }

    public double getMarks() {
        return marks;
    }

    public double getAnnualFamilyIncome() {
        return annualFamilyIncome;
    }

    public String getCategory() {
        return category;
    }
}
```

**Requirement:** Student fields must not be publicly mutable. Validation should occur before an object is accepted.

### 9.2 Abstraction

**Purpose:** Define the common properties and required operation for every scholarship scheme without prescribing one universal eligibility formula.

```java
import java.util.List;

public abstract class Scheme {
    private final String id;
    private final String name;
    private final List<String> requiredDocuments;

    protected Scheme(String id, String name, List<String> requiredDocuments) {
        this.id = id;
        this.name = name;
        this.requiredDocuments = List.copyOf(requiredDocuments);
    }

    public String getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public List<String> getRequiredDocuments() {
        return requiredDocuments;
    }

    public abstract boolean isEligible(Student student);
}
```

`Scheme` is abstract because a generic scheme does not have one meaningful eligibility rule. Each concrete subclass supplies its own implementation.

### 9.3 Inheritance

**Purpose:** Reuse shared scheme information and behavior while specializing the eligibility rule.

```java
import java.util.List;

public class MeritScheme extends Scheme {
    private final double minimumMarks;

    public MeritScheme(
            String id, String name, List<String> documents, double minimumMarks) {
        super(id, name, documents);
        this.minimumMarks = minimumMarks;
    }

    @Override
    public boolean isEligible(Student student) {
        return student.getMarks() >= minimumMarks;
    }
}
```

`MeritScheme` inherits the scheme identifier, name, and document list from `Scheme`. It adds a minimum-marks threshold.

`IncomeScheme` and `CategoryScheme` follow the same inheritance pattern and define their own eligibility conditions.

### 9.4 Polymorphism

**Purpose:** Call the same method on different concrete scheme types and let Java select the correct overridden implementation at runtime.

```java
import java.util.List;

public class EligibilityService {
    public List<Scheme> findEligible(
            Student student, List<Scheme> schemes) {
        return schemes.stream()
                .filter(scheme -> scheme.isEligible(student))
                .toList();
    }
}
```

The list contains `Scheme` references, but each object may be a `MeritScheme`, `IncomeScheme`, or `CategoryScheme`. The call to `isEligible(student)` invokes the implementation belonging to the actual object.

### 9.5 Income and category specializations

```java
import java.util.List;

public class IncomeScheme extends Scheme {
    private final double maximumAnnualIncome;

    public IncomeScheme(
            String id, String name, List<String> documents,
            double maximumAnnualIncome) {
        super(id, name, documents);
        this.maximumAnnualIncome = maximumAnnualIncome;
    }

    @Override
    public boolean isEligible(Student student) {
        return student.getAnnualFamilyIncome() <= maximumAnnualIncome;
    }
}
```

```java
import java.util.List;
import java.util.Set;

public class CategoryScheme extends Scheme {
    private final Set<String> allowedCategories;

    public CategoryScheme(
            String id, String name, List<String> documents,
            Set<String> allowedCategories) {
        super(id, name, documents);
        this.allowedCategories = Set.copyOf(allowedCategories);
    }

    @Override
    public boolean isEligible(Student student) {
        return allowedCategories.stream()
                .anyMatch(value ->
                        value.equalsIgnoreCase(student.getCategory()));
    }
}
```

The category comparison is case-insensitive in this example. The JSON loader should validate that the allowed category set is not empty.

### 9.6 Composition

**Purpose:** Build the application from collaborating objects rather than placing all responsibilities in one class.

`EligibilityService` uses a list of `Scheme` objects. `Main` can hold a `SchemeLoader`, an `EligibilityService`, and an `EligibilityReportWriter`. These objects work together, but each retains a focused responsibility.

```java
List<Scheme> schemes = schemeLoader.load("data/schemes.json");
List<Scheme> eligible = eligibilityService.findEligible(student, schemes);
reportWriter.write("output/eligibility-report.txt", student, eligible);
```

This snippet illustrates object collaboration; the named objects must be constructed before use.

### 9.7 Interface (optional but useful)

**Purpose:** Define a small contract for report output so the main application depends on behavior rather than a particular writer.

```java
import java.io.IOException;
import java.nio.file.Path;
import java.util.List;

public interface ReportWriter {
    void write(Path destination, Student student, List<Scheme> schemes)
            throws IOException;
}
```

`EligibilityReportWriter` can implement `ReportWriter`. This interface is optional for the smallest version, but it provides another clear example of programming to a contract.

### 9.8 Overriding and runtime dispatch

`@Override` documents that a subclass is replacing a superclass method. If a new supported scheme class is added, its `isEligible(Student)` method will be selected automatically when the service calls that method through a `Scheme` reference.

Overloading is not required for the core design. If demonstrated, it should be used for a meaningful alternative method signature rather than added only to claim another OOP concept.

## 10. JSON Rules File and File Handling

File handling is mandatory and central to this project. The rules file is the source of scheme configuration, and the output report provides a concrete file-writing operation.

### 10.1 File layout

A simple project layout may be:

```text
SchemeSathi/
├── src/
│   └── ... Java source files ...
├── data/
│   └── schemes.json
└── output/
    └── eligibility-report.txt
```

Use relative paths from the project working directory. The application should explain which path it attempted to read if the file is missing.

### 10.2 Example `schemes.json`

The following is example JSON data. The application should support the three rule types shown here.

```json
[
  {
    "id": "MERIT-001",
    "name": "Academic Merit Scholarship",
    "type": "MERIT",
    "minimumMarks": 80,
    "requiredDocuments": [
      "Previous examination marksheet",
      "Identity proof"
    ]
  },
  {
    "id": "INCOME-001",
    "name": "Need-Based Scholarship",
    "type": "INCOME",
    "maximumAnnualIncome": 250000,
    "requiredDocuments": [
      "Income certificate",
      "Identity proof"
    ]
  },
  {
    "id": "CATEGORY-001",
    "name": "Category-Specific Scholarship",
    "type": "CATEGORY",
    "allowedCategories": ["SC", "ST"],
    "requiredDocuments": [
      "Category certificate",
      "Previous examination marksheet"
    ]
  }
]
```

This is a project example, not a statement of current real-world scholarship rules. Thresholds and documents must be verified before the data is used for real guidance.

### 10.3 Rule-loading requirements

The loader must:

1. Open the configured JSON file using a relative or explicitly configured path.
2. Read and parse the file.
3. Validate required fields such as `id`, `name`, `type`, and `requiredDocuments`.
4. Validate type-specific fields, such as `minimumMarks`, `maximumAnnualIncome`, and `allowedCategories`.
5. Reject unsupported scheme types and malformed values with a useful error.
6. Convert each valid rule to the corresponding concrete `Scheme` subclass.
7. Avoid silently treating a failed load as an empty list of schemes.

The exact JSON parsing library is an implementation choice. A JSON parser should be used rather than attempting to parse arbitrary JSON with simple string splitting.

### 10.4 File reading example

This example demonstrates reading a text file with Java's `Files` API. It returns the raw JSON text; parsing and validation are separate responsibilities.

```java
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;

public class SchemeFileReader {
    public String readRules(Path path) throws IOException {
        if (!Files.exists(path)) {
            throw new IOException("Rules file does not exist: " + path);
        }
        if (!Files.isRegularFile(path) || !Files.isReadable(path)) {
            throw new IOException("Rules file is not a readable regular file: " + path);
        }

        return Files.readString(path, StandardCharsets.UTF_8);
    }
}
```

A JSON parser should then convert the returned text into validated rule definitions and scheme objects. If the file is empty or contains malformed JSON, the loader should report the problem and stop the eligibility run.

### 10.5 File writing example

The report should contain the student's submitted criteria, the matching scheme names, and each scheme's required documents. Avoid writing unnecessary personal information.

```java
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.util.List;

public class EligibilityReportWriter implements ReportWriter {
    @Override
    public void write(
            Path destination, Student student, List<Scheme> schemes)
            throws IOException {

        Path parent = destination.getParent();
        if (parent != null) {
            Files.createDirectories(parent);
        }

        StringBuilder report = new StringBuilder();
        report.append("SchemeSathi Eligibility Report\n");
        report.append("Marks: ").append(student.getMarks()).append('\n');
        report.append("Annual family income: ")
                .append(student.getAnnualFamilyIncome()).append('\n');
        report.append("Category: ").append(student.getCategory()).append('\n');
        report.append("\nEligible schemes:\n");

        if (schemes.isEmpty()) {
            report.append("No matching schemes were found.\n");
        } else {
            for (Scheme scheme : schemes) {
                report.append("\n- ")
                        .append(scheme.getName())
                        .append(" [").append(scheme.getId()).append("]\n");
                report.append("  Required documents:\n");
                for (String document : scheme.getRequiredDocuments()) {
                    report.append("  - ").append(document).append('\n');
                }
            }
        }

        Files.writeString(
                destination,
                report.toString(),
                StandardCharsets.UTF_8,
                StandardOpenOption.CREATE,
                StandardOpenOption.TRUNCATE_EXISTING,
                StandardOpenOption.WRITE);
    }
}
```

This implementation overwrites an existing report file. If preserving prior reports is desired later, a different filename strategy can be considered; it is not required for the initial project.

### 10.6 Error handling

The application must handle at least these cases:

- **File not found:** Show the expected path and explain that rules could not be loaded.
- **Permission or I/O error:** Show a clear message and do not continue as though the operation succeeded.
- **Malformed JSON:** Report a parse error; do not evaluate a partially interpreted rules file.
- **Missing or invalid fields:** Identify the affected scheme where possible and reject invalid configuration.
- **Unsupported `type`:** Reject the rule rather than guessing its meaning.
- **Report write failure:** Tell the user that the report was not saved and provide the destination path.
- **Invalid student input:** Ask for corrected input or stop before eligibility evaluation.

Use specific exception handling where possible. Do not silently catch and ignore exceptions. Detailed diagnostic information may be printed for development, while the user-facing message should remain understandable.

Example orchestration:

```java
try {
    List<Scheme> schemes = schemeLoader.load(Path.of("data/schemes.json"));
    List<Scheme> eligible = eligibilityService.findEligible(student, schemes);
    reportWriter.write(
            Path.of("output/eligibility-report.txt"), student, eligible);
    System.out.println("Report saved successfully.");
} catch (IOException | IllegalArgumentException ex) {
    System.err.println("SchemeSathi could not complete the operation: "
            + ex.getMessage());
}
```

The `SchemeLoader.load(...)` method in this example is expected to read, parse, validate, and construct the scheme list. If a particular JSON library uses a separate parsing exception, the implementation should catch or wrap that exception at the loader boundary and provide a meaningful message.

### 10.7 Adding schemes without changing Java code

A new scheme can be added without changing Java code when it uses an already supported rule type. For example, adding another `MERIT` rule with a different threshold and document list requires only a new JSON object.

A genuinely new rule type, such as a combined marks-and-income condition, requires either a supported composition of existing rules or a new implementation and loader mapping. JSON configuration does not automatically create new executable behavior. The initial scope supports `MERIT`, `INCOME`, and `CATEGORY`.

## 11. Eligibility Rules and Output Behavior

- Marks are assumed to be percentages on a scale from 0 to 100.
- Annual family income is a non-negative amount in Indian rupees (INR).
- Category values are strings and are compared case-insensitively in the category example.
- Threshold comparisons are inclusive in the examples: marks must be greater than or equal to the minimum; income must be less than or equal to the maximum.
- A scheme matches only when its implemented rule returns `true`.
- The first version treats the three scheme types as independent rules. It does not combine multiple conditions unless a future requirement defines how combined conditions should work.
- The results cover only schemes present in the loaded file. The application cannot guarantee that the file contains every scholarship available in reality.

## 12. User Interaction Requirements

The console workflow should request:

1. Marks (0–100).
2. Annual family income in INR.
3. Category.
4. Whether to save the report, if report saving is optional.

The result should display each eligible scheme's name or identifier and required documents. If no schemes match, display a clear no-match message. If scheme rules cannot be loaded, explain that eligibility could not be evaluated.

## 13. Testing and Acceptance Criteria

### 13.1 Functional test cases

| Test | Input or setup | Expected result |
|---|---|---|
| Valid merit match | Marks meet the minimum threshold | Merit scheme is listed. |
| Merit below threshold | Marks are below the minimum | Merit scheme is not listed. |
| Income at limit | Income equals the maximum | Income scheme is listed. |
| Income above limit | Income exceeds the maximum | Income scheme is not listed. |
| Category match | Category matches an allowed category, ignoring case | Category scheme is listed. |
| Category mismatch | Category is not allowed | Category scheme is not listed. |
| Multiple matches | Profile satisfies more than one configured scheme | Every matching scheme is listed. |
| No matches | Profile fails all loaded rules | No-match message is displayed. |
| Missing rules file | Configured file does not exist | Clear error; no eligibility result is claimed. |
| Malformed JSON | Rules file contains invalid JSON | Clear load error; evaluation does not proceed. |
| Invalid rule | A required field or threshold is invalid | Invalid configuration is rejected. |
| Report output | Report destination is writable | Report is created with matches and documents. |
| Report write failure | Destination cannot be written | Clear error indicates the report was not saved. |

### 13.2 OOP review checklist

- [ ] Student data is encapsulated in private fields.
- [ ] `Scheme` is an abstract class with an abstract `isEligible(Student)` method.
- [ ] `MeritScheme`, `IncomeScheme`, and `CategoryScheme` extend `Scheme`.
- [ ] Each concrete scheme overrides `isEligible(Student)`.
- [ ] Eligibility evaluation uses a `List<Scheme>` and dynamic dispatch.
- [ ] Responsibilities are divided among focused classes.
- [ ] The JSON rules file is read using Java file APIs.
- [ ] The report is written using Java file APIs.
- [ ] Missing, malformed, and inaccessible files are handled.
- [ ] Invalid input cannot silently become a positive eligibility result.

## 14. Assumptions

- The application is a console-based Java project.
- Marks are represented as a percentage from 0 to 100.
- Income is annual family income in INR.
- The initial supported scheme types are merit, income, and category.
- Required documents are informational labels supplied by the rules file.
- The rules file is maintained by the project owner and is not automatically verified against official sources.
- A JSON parsing library may be selected during implementation; its dependency and version should be documented in the project setup.
- Java 11 or later is recommended for the file API examples. The use of `Stream.toList()` requires Java 16 or later; for Java 11 compatibility, replace it with `.collect(Collectors.toList())`.

## 15. Constraints

- The project must be implemented in Java.
- Core eligibility logic must demonstrate OOP rather than being concentrated in one procedural method.
- Scheme configuration must be read from a JSON file.
- File handling must include both reading rules and writing a report.
- File and parsing errors must be handled explicitly.
- The first version supports only the three listed scheme types.
- The project must not present sample rules as official or guarantee scholarship approval.
- No online services, database, or graphical interface is required.

## 16. Open Questions

1. Should the application always save a report, or ask the student first?
2. Should the report include all evaluated schemes with eligible/ineligible status, or only eligible schemes?
3. Which JSON parsing library and Java version will the course or evaluator require?
4. Should category values be restricted to a predefined list, or remain configurable as strings?
5. Should invalid scheme entries stop the entire load, as proposed, or be skipped with warnings? The safer initial behavior is to reject the configuration so results are not incomplete without the user's knowledge.
6. Which official source will maintainers use to verify real scholarship criteria and document lists before distributing the application for practical use?

## 17. Deliverable Summary

The completed project should contain Java source files for the student model, abstract scheme and concrete subclasses, scheme loader, eligibility service, report writer, and main program, plus a `schemes.json` configuration file. It should demonstrate encapsulation, inheritance, polymorphism, abstraction, composition, and optionally an interface. It must read scheme definitions from a file, validate them, evaluate eligibility, display required documents, and write a plain-text report with explicit error handling.

SchemeSathi is complete for the initial scope when the acceptance criteria and OOP review checklist pass.
