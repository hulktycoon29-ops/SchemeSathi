# SchemeSathi — Architecture Guide

**Project:** SchemeSathi (Scholarship Eligibility Navigator)  
**Document:** `architecture.md`  
**Purpose:** Implementation-oriented architecture guide for an LLM or developer building the OOP Java project.

## 1. Source of truth and scope

This architecture is based on `ProjectPRD_OPPS.md` and the supplied project description:

> SchemeSathi helps students understand scholarship eligibility. It accepts marks, annual family income, and category, compares them with scheme rules in JSON, and lists matching schemes with their required documents. The core OOP design uses an abstract `Scheme` class and `isEligible()` implementations in `MeritScheme`, `IncomeScheme`, and `CategoryScheme`. New schemes that use a supported rule type can be added through JSON configuration without changing Java code.

The PRD defines a **Java console application**. It explicitly excludes a web/mobile interface, user accounts, authentication, online databases, automatic internet-based scheme discovery, and scholarship submission. Accordingly:

- “Frontend” in this document means the console interaction layer, not a browser UI.
- There is no HTTP server or REST API in the initial scope. The API design below describes internal Java class contracts instead of invented HTTP endpoints.
- Persistence means reading the JSON rules file and optionally writing a plain-text report. No database is required.
- The rules file is configuration, not an official or automatically verified source of scholarship information.
- Eligibility results are indicative and must not be presented as a guarantee of scholarship approval.

### 1.1 Requirements from the PRD

The implementation must:

1. Accept marks (0–100), annual family income in INR, and category.
2. Validate student input before evaluation.
3. Read and validate scheme definitions from a JSON file.
4. Support `MERIT`, `INCOME`, and `CATEGORY` scheme types.
5. Instantiate the appropriate `Scheme` subclass and call `isEligible(Student)` polymorphically.
6. Display every matching loaded scheme and its required documents.
7. Show a clear no-match message when evaluation succeeds but no schemes match.
8. Optionally write a plain-text eligibility report.
9. Handle missing/unreadable files, malformed JSON, invalid rules, unsupported types, invalid student input, and report-write failures clearly.
10. Never treat a failed rule load as a valid empty list or claim an eligibility result when evaluation did not run successfully.

## 2. Architecture overview

Use a small layered architecture with clear separation of concerns. Keep domain rules independent of console input and file I/O, so eligibility logic can be unit-tested without running the whole application.

### 2.1 High-level components

| Layer | Main components | Responsibility |
|---|---|---|
| Presentation / console | `Main`, `ConsoleUI` (recommended helper) | Prompt for student details, display validation and operation errors, show results, ask whether to save the report |
| Application | `EligibilityService` | Evaluate all loaded schemes and return every matching scheme |
| Domain model | `Student`, abstract `Scheme`, `MeritScheme`, `IncomeScheme`, `CategoryScheme` | Encapsulate profile data and represent scheme-specific eligibility behavior |
| Configuration / data access | `SchemeLoader`, JSON parser, optional `SchemeRule` DTO | Read JSON, validate rule definitions, map them to concrete scheme objects |
| Output / file handling | `EligibilityReportWriter` (optionally implements `ReportWriter`) | Format and write the report to a text file |
| Filesystem | `data/schemes.json`, `output/eligibility-report.txt` | Store configurable rules and optional report output |

The PRD's named classes are the core architecture. `ConsoleUI` and `SchemeRule` are optional implementation helpers, not new product features.

### 2.2 Textual data-flow diagram

Successful run:

```text
Student
  -> ConsoleUI / Main: enter marks, annual family income, category
  -> Student constructor: validate values and create immutable Student
  -> SchemeLoader
  -> Java file API reads data/schemes.json
  -> JSON parser parses the file
  -> Rule validation checks common and type-specific fields
  -> SchemeLoader maps each rule to MeritScheme / IncomeScheme / CategoryScheme
  -> List<Scheme>
  -> EligibilityService.findEligible(student, schemes)
  -> scheme.isEligible(student) [runtime dispatch to concrete override]
  -> List<Scheme> eligibleSchemes
  -> ConsoleUI: display each scheme and required documents
  -> [if user chooses to save]
  -> EligibilityReportWriter
  -> Java file API writes output/eligibility-report.txt
```

Failure paths:

```text
Invalid student input -> show validation message -> ask again or stop; do not evaluate
Missing/unreadable schemes.json -> loader error -> explain path/problem -> stop eligibility run
Malformed JSON / invalid rule / unsupported type -> loader error -> stop eligibility run
No matching schemes after successful load and evaluation -> show explicit no-match message
Report write failure -> explain report was not saved and show destination path
```

**Important distinction:** an empty eligible result is valid only when rules loaded and evaluation completed successfully. A failed load must be represented as an error, not as “no scholarships found.”

### 2.3 Design principles

- **Separation of concerns:** console input, domain rules, JSON loading, eligibility orchestration, and report writing belong in different classes.
- **Encapsulation:** use private fields and validate values at object boundaries.
- **Abstraction and polymorphism:** the service calls `isEligible(Student)` through `Scheme` references; concrete subclasses define the rule.
- **Configuration-driven scheme data:** thresholds, allowed categories, and document names live in JSON for supported types.
- **Fail clearly and safely:** malformed or incomplete rules must not silently produce incomplete or misleading results.
- **Testability:** eligibility rules should be unit-testable without filesystem or console dependencies.
- **Portability:** use Java NIO file APIs and relative/configurable paths, not machine-specific absolute paths.
- **Minimal dependencies:** no web framework, database, authentication service, Docker, or external service is needed for the stated scope.

## 3. Frontend design: console interaction layer

The PRD explicitly calls for a console application. Do not build React, Angular, Vue, HTML pages, browser routing, or a frontend server for the initial version.

### 3.1 Console flow

1. Print the SchemeSathi title and a short explanation that results are based on configured rules.
2. Prompt for marks from `0` through `100`.
3. Prompt for annual family income in INR; reject negative values and non-numeric input.
4. Prompt for category; reject blank input.
5. Construct a validated `Student`.
6. Load and validate `data/schemes.json`.
7. Evaluate all loaded schemes.
8. Print each eligible scheme's ID/name and required document list. If the result list is empty, print a clear no-match message.
9. Ask whether to save a report if report saving is configured as optional.
10. If requested, write the report and confirm success or show a clear failure.
11. End without implying official approval.

### 3.2 Suggested component/class hierarchy

```text
Main
└── ConsoleUI (optional helper)
    ├── collects and validates raw console input
    ├── calls Student constructor
    ├── invokes SchemeLoader
    ├── invokes EligibilityService
    ├── displays eligible schemes and documents
    └── optionally invokes EligibilityReportWriter

EligibilityService
└── works with List<Scheme>
    ├── MeritScheme
    ├── IncomeScheme
    └── CategoryScheme
```

Keep `Main` as a coordinator. Avoid placing JSON parsing, eligibility formulas, and report formatting directly inside the main method.

### 3.3 State management and interaction patterns

There is no persistent client-side state manager. Keep the current run's state in ordinary Java objects and local variables:

- `Student student`: validated profile for this run.
- `List<Scheme> schemes`: successfully loaded scheme definitions.
- `List<Scheme> eligibleSchemes`: results of a successful evaluation.
- `Path rulesPath` and `Path reportPath`: configured file locations.

Do not reuse stale results after a failed load or invalid input. If the user retries input, create a new `Student` only after all fields validate.

### 3.4 Console usability

- Use direct, plain-language prompts and errors.
- Identify paths in file errors so the user can locate the problem.
- Show scheme IDs or names for traceability.
- List required documents under each matching scheme.
- Make “no matching schemes” distinct from “could not evaluate.”
- Include a short disclaimer that results depend on the configured rules and do not guarantee funding.
- Do not print stack traces as the only user-facing error. Detailed exception information can be logged or printed during development.

## 4. Backend design: Java application layers

“Backend” here means the internal Java application. The PRD does not require a network server, REST controller, or external persistence service.

### 4.1 Suggested package structure

Use a conventional Maven layout. Package names can be adjusted to course conventions, but keep responsibilities separate.

```text
schemesathi/
├── pom.xml
├── README.md
├── data/
│   └── schemes.json
├── output/
│   └── .gitkeep                 # optional; report is generated at runtime
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/
│   │   │       └── schemesathi/
│   │   │           ├── Main.java
│   │   │           ├── ui/
│   │   │           │   └── ConsoleUI.java
│   │   │           ├── model/
│   │   │           │   ├── Student.java
│   │   │           │   ├── Scheme.java
│   │   │           │   ├── MeritScheme.java
│   │   │           │   ├── IncomeScheme.java
│   │   │           │   └── CategoryScheme.java
│   │   │           ├── service/
│   │   │           │   └── EligibilityService.java
│   │   │           ├── loader/
│   │   │           │   ├── SchemeLoader.java
│   │   │           │   └── SchemeRule.java        # optional DTO
│   │   │           └── report/
│   │   │               ├── ReportWriter.java      # optional interface
│   │   │               └── EligibilityReportWriter.java
│   │   └── resources/
│   │       └── (optional bundled defaults)
│   └── test/
│       └── java/
│           └── com/
│               └── schemesathi/
│                   ├── model/
│                   ├── service/
│                   └── loader/
└── .gitignore
```

The PRD's sample paths use `data/schemes.json` and `output/eligibility-report.txt` relative to the working directory. If the implementation packages a default rules file as a resource instead, document the path behavior and retain a clear way to use an editable JSON file. Do not silently change the expected configuration location.

### 4.2 Domain classes and contracts

#### `Student`

Responsibilities:
- Store marks, annual family income, and category.
- Validate input at construction.
- Expose read-only getters.

Fields should be private and preferably `final`. Validate:
- `0 <= marks <= 100`
- `annualFamilyIncome >= 0`
- category is non-null and non-blank; trim surrounding whitespace.

Illustrative contract:

```java
public final class Student {
    public Student(double marks, double annualFamilyIncome, String category);
    public double getMarks();
    public double getAnnualFamilyIncome();
    public String getCategory();
}
```

#### `Scheme`

Responsibilities:
- Store shared scheme data: `id`, `name`, and `requiredDocuments`.
- Expose read-only accessors.
- Define the common eligibility contract.

```java
public abstract class Scheme {
    public String getId();
    public String getName();
    public List<String> getRequiredDocuments();
    public abstract boolean isEligible(Student student);
}
```

Use defensive copies for document collections, such as `List.copyOf(...)`, so callers cannot mutate the scheme's internal list. Validate nonblank IDs/names and a valid document list when constructing a scheme or validating its rule.

#### `MeritScheme`

- Extends `Scheme`.
- Holds `minimumMarks`.
- `isEligible(student)` returns `student.getMarks() >= minimumMarks`.
- Validate the threshold against the supported marks scale (`0` through `100`).

#### `IncomeScheme`

- Extends `Scheme`.
- Holds `maximumAnnualIncome`.
- `isEligible(student)` returns `student.getAnnualFamilyIncome() <= maximumAnnualIncome`.
- Reject negative thresholds.

#### `CategoryScheme`

- Extends `Scheme`.
- Holds a non-empty set/list of allowed categories.
- `isEligible(student)` checks whether the student's category matches an allowed category.
- Match case-insensitively, as in the PRD example, and trim category strings consistently.

#### `EligibilityService`

Responsibilities:
- Accept a validated `Student` and successfully loaded `List<Scheme>`.
- Evaluate each scheme using `scheme.isEligible(student)`.
- Return every matching scheme, not just the first match.
- Contain no console reads/writes and no JSON/file parsing.

Suggested method:

```java
public List<Scheme> findEligible(Student student, List<Scheme> schemes);
```

For Java 11 compatibility, use `.collect(Collectors.toList())` rather than `Stream.toList()`. If the project selects Java 17, either style is available.

#### `SchemeLoader`

Responsibilities:
- Read `data/schemes.json` with Java file APIs.
- Parse JSON using a real JSON library.
- Validate the full file and all supported rule definitions.
- Convert each valid definition into its concrete subclass.
- Reject missing fields, invalid thresholds, empty allowed categories, malformed document lists, duplicate IDs if treated as invalid by the implementation, and unsupported `type` values.
- Throw a meaningful checked or documented application exception if loading fails.

Recommended fail-safe behavior: reject the configuration and stop evaluation if a rule is invalid, rather than silently skipping it and presenting incomplete results. This follows the safer behavior identified in the PRD.

#### `EligibilityReportWriter`

Responsibilities:
- Write a plain-text report with the submitted criteria, eligible scheme IDs/names, and required documents.
- Create the output directory if needed.
- Use UTF-8.
- Report I/O failures to the caller instead of swallowing them.

The PRD's sample writer overwrites the destination file. Retain this behavior for the initial version unless a new requirement specifies report history.

An optional `ReportWriter` interface can define a `write(Path, Student, List<Scheme>)` contract. It is not mandatory for the smallest implementation.

#### `Main`

Responsibilities:
- Construct or coordinate the console UI, loader, service, and writer.
- Define the run sequence.
- Handle expected errors at the application boundary.
- Ensure a failed rules load never turns into an empty valid scheme list.
- Avoid embedding scheme-specific eligibility logic.

### 4.3 Internal API contracts (not HTTP endpoints)

No REST API is in scope. Use the following internal method-level contracts to make module boundaries explicit:

| Operation | Input | Output | Failure behavior |
|---|---|---|---|
| Collect profile | Console input | Valid `Student` | Invalid values prompt again or stop with a clear message |
| `SchemeLoader.load(Path)` | JSON file path | `List<Scheme>` | Throws/reports parse, validation, or I/O failure; no partial success by default |
| `EligibilityService.findEligible(Student, List<Scheme>)` | Valid student and loaded schemes | List of all eligible schemes | Invalid arguments should be rejected clearly |
| `EligibilityReportWriter.write(Path, Student, List<Scheme>)` | Destination, student, results | Successful write (e.g. `void`) | Propagates/reports I/O failure |
| Display results | Student and eligible list | Console output | Distinguishes no matches from evaluation failure |

Do not add HTTP request/response DTOs, controllers, URL routes, or status codes unless the project scope is explicitly changed to a web application.

### 4.4 JSON rule schema

The JSON file is the configuration source for scheme data. The initial implementation supports these types:

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

These are illustrative examples, not verified real-world scholarship rules.

Common required fields:
- `id`: nonblank string.
- `name`: nonblank string.
- `type`: one of `MERIT`, `INCOME`, `CATEGORY`.
- `requiredDocuments`: valid list of nonblank strings.

Type-specific fields:
- `MERIT`: `minimumMarks`, numeric and between 0 and 100.
- `INCOME`: `maximumAnnualIncome`, numeric and non-negative.
- `CATEGORY`: `allowedCategories`, non-empty list of nonblank strings.

Ignore no invalid value silently. Do not infer a missing threshold or guess what an unknown type means. Parse and validate the entire file before returning the scheme list.

### 4.5 Eligibility semantics

Use the PRD's stated assumptions:

- Marks are percentages from 0 to 100.
- Income is annual family income in Indian rupees (INR).
- Merit comparison is inclusive: marks greater than or equal to the configured minimum.
- Income comparison is inclusive: income less than or equal to the configured maximum.
- Category matching is case-insensitive.
- The initial scheme types are independent rules. Do not assume a single scheme can combine marks, income, and category constraints unless a future requirement defines combined-rule behavior.
- Results apply only to schemes present in the successfully loaded JSON file.

### 4.6 Error-handling strategy

Use exceptions for exceptional failures at the file/configuration boundary and validation messages for expected user input correction.

| Failure | Required behavior |
|---|---|
| Non-numeric marks/income | Explain expected input and reprompt or stop |
| Marks outside 0–100 | Reject before constructing/accepting `Student` |
| Negative income | Reject before evaluation |
| Blank category | Reject before evaluation |
| Missing rules file | Show the attempted path; stop evaluation |
| Unreadable file or I/O failure | Show a clear error; do not claim results |
| Empty or malformed JSON | Report parse/configuration error; stop evaluation |
| Missing/invalid rule field | Identify scheme/rule when possible; reject configuration |
| Unsupported scheme `type` | Reject rather than guessing |
| No eligible schemes | Show “No matching schemes were found” after successful evaluation |
| Report destination cannot be written | Explain that the report was not saved and show the path |

Avoid broad catch-and-ignore blocks. Catch parser-specific exceptions inside `SchemeLoader` and wrap them in a clear loader/configuration exception if useful. At the application boundary, display a human-readable message. Detailed diagnostics can be retained for development.

## 5. Data persistence and transaction behavior

There is no database in the PRD.

- **Read source:** `data/schemes.json`.
- **Write destination:** `output/eligibility-report.txt` when the user chooses to save.
- **In-memory data:** `Student`, loaded `Scheme` objects, and eligible results live for the duration of the run.

File operations are not database transactions. Apply a simple all-or-nothing rule-load strategy: parse and validate all scheme definitions before exposing a `List<Scheme>` to the eligibility service. If any required configuration is invalid, fail the load and do not evaluate a partial list.

For report output, create parent directories if needed, write UTF-8 text, and propagate errors. The initial report writer may overwrite the existing report file, as in the PRD example. Avoid storing unnecessary personal data in the report; include only the profile fields required by the PRD/report format.

## 6. Technology stack

The PRD requires Java and a JSON parser, but it does not mandate a specific JSON library, Java release, or build tool. The following is a **recommended concrete baseline**, not a claim that these choices were mandated by the source document.

### 6.1 Recommended baseline

| Area | Recommendation | Status / rationale |
|---|---|---|
| Language | Java | Required by PRD |
| Runtime / JDK | Java 17 LTS | Recommended baseline; supports modern language/library APIs and avoids Java 11 `Stream.toList()` incompatibility |
| Build tool | Apache Maven | Recommended for repeatable compilation, dependency management, and test execution |
| JSON parsing | Jackson Databind or Gson | Choose one; PRD leaves library open. Do not hand-parse JSON with string splitting |
| Unit testing | JUnit 5 | Recommended for model, eligibility, and loader tests |
| File I/O | `java.nio.file.Files`, `Path`, UTF-8 | Matches PRD's standard Java file API and portability requirements |
| Version control | Git | Recommended for source history; not a runtime dependency |
| IDE | IntelliJ IDEA, Eclipse, or VS Code with Java support | Developer choice |
| API documentation | Not applicable in initial console app | Swagger/OpenAPI is unnecessary unless an HTTP API is added |

Do not add Spring Boot, React, Angular, Vue, an external database, OAuth, Docker, or CI/CD merely because they are common in larger systems. None is required by this PRD.

### 6.2 Maven utilities

A minimal Maven project should include:
- Java compiler release set consistently to `17` if adopting the recommendation above.
- One JSON library dependency (Jackson **or** Gson).
- JUnit Jupiter for tests.
- Maven Surefire Plugin for test execution.
- Optional Maven Compiler Plugin configuration.

Lombok is optional and not necessary for this small project. Prefer explicit constructors/getters where they help demonstrate encapsulation and OOP to the evaluator. No Swagger dependency is needed because there is no REST API.

### 6.3 Runtime requirements

- A JDK matching the configured Maven compiler release.
- The editable `data/schemes.json` file in the documented location.
- Read access to the rules file.
- Write access to the report destination only when report saving is requested.
- No network connection, database server, or external service.

## 7. Testing strategy

Keep the core domain and service logic independent so tests can run without interactive console input.

### 7.1 Unit tests

**`Student`**
- Marks `0` and `100` accepted; values below `0` or above `100` rejected.
- Negative income rejected.
- Null/blank category rejected.
- Input category whitespace trimmed if that behavior is implemented.

**`MeritScheme`**
- Marks at the threshold qualify.
- Marks above threshold qualify.
- Marks below threshold do not qualify.

**`IncomeScheme`**
- Income exactly at maximum qualifies.
- Income below maximum qualifies.
- Income above maximum does not qualify.

**`CategoryScheme`**
- Allowed category qualifies regardless of letter case.
- Disallowed category does not qualify.
- Empty allowed-category configuration is rejected.

**`EligibilityService`**
- Returns every matching scheme.
- Does not return ineligible schemes.
- Returns an empty list for a valid evaluation with no matches.
- Uses polymorphic `isEligible(Student)` calls across the `Scheme` hierarchy.

### 7.2 Loader and file tests

- Valid JSON loads all three supported types.
- Missing file fails with a clear error.
- Malformed JSON fails.
- Missing common fields fail.
- Missing type-specific fields fail.
- Invalid threshold values fail.
- Empty category list or invalid document list fails.
- Unsupported `type` fails.
- Invalid configuration does not yield a partial scheme list.

Use temporary files/directories for tests where practical so tests do not depend on machine-specific paths.

### 7.3 Report tests

- Creates the report file and parent directory as required.
- Includes matching scheme IDs/names and required documents.
- Writes a clear no-match result.
- Reports a write failure when the destination cannot be written.

### 7.4 Acceptance checklist

- [ ] Student profile validates marks, income, and category.
- [ ] Rules load from JSON and are fully validated.
- [ ] `Scheme` is abstract and declares `isEligible(Student)`.
- [ ] `MeritScheme`, `IncomeScheme`, and `CategoryScheme` override the method.
- [ ] `EligibilityService` uses a `List<Scheme>` and runtime polymorphism.
- [ ] All matching schemes and their documents are displayed.
- [ ] No-match output is distinct from a load/evaluation error.
- [ ] Optional report is written as plain text.
- [ ] Missing, unreadable, malformed, and invalid files produce clear errors.
- [ ] New schemes of a supported type can be added by editing JSON only.
- [ ] The application does not imply official scholarship approval.

## 8. Build and run

Assuming Maven and JDK 17 are installed:

```bash
mvn clean test
mvn package
```

Run the compiled application using the project's documented main class and classpath, or configure the Maven Exec Plugin optionally. Because the rules path is relative to the working directory in the PRD example, run the app from the project root unless the implementation explicitly supports a configurable path.

The README should document:
- JDK and Maven versions.
- Which JSON library is used.
- The schema and location of `data/schemes.json`.
- How to run the console application.
- Where `eligibility-report.txt` is written.
- Common configuration/input errors.
- The disclaimer that eligibility is only as reliable as the configured rules.

Do not invent a command that depends on a plugin not configured in `pom.xml`; either provide a direct `java` command using the actual build output or configure/document the optional plugin.

## 9. Deployment

The initial deployment model is a local Java console program:

1. Provide the packaged application and the editable `data/schemes.json`.
2. Ensure the target machine has a compatible JDK, or distribute a runtime in a manner approved by the project owner.
3. Run from a working directory where the rules path is available, or pass a configured path if implemented.
4. Ensure the process can read the rules file and write to the report folder if report saving is used.

No Docker image, hosted web app, database deployment, cloud service, authentication system, or CI/CD pipeline is required.

## 10. Extensibility boundaries

The innovation is configuration-driven rules. New scheme entries can be added in JSON **without changing Java code when they use one of the already supported types**:

- Add a `MERIT` entry with its own `minimumMarks`.
- Add an `INCOME` entry with its own `maximumAnnualIncome`.
- Add a `CATEGORY` entry with its own `allowedCategories`.
- Supply the required documents for each entry.

A genuinely new rule type or combined-condition scheme requires code support or a separately designed composition model. Do not claim arbitrary new eligibility logic can be expressed by JSON alone. The initial scope supports only the three specified types.

## 11. Assumptions and unresolved decisions

The following are either specified by the PRD or remain implementation choices:

**Specified by the PRD**
- Console application, not web/mobile.
- Java OOP implementation.
- Marks on a 0–100 scale; annual family income in INR.
- Three initial scheme types: merit, income, category.
- JSON rules input and optional plain-text report output.
- Clear error handling and no misleading eligibility result on load failure.
- No online service, database, or graphical interface.

**Recommended choices for implementation**
- Java 17 LTS and Maven.
- One JSON library, such as Jackson or Gson.
- JUnit 5 for automated tests.
- Fail the entire rules load if any required rule is invalid.
- Use `data/schemes.json` and `output/eligibility-report.txt` relative to the project root.

**Open questions carried from the PRD**
1. Should report saving always happen or should the user be asked? This guide preserves optional saving.
2. Should the report include ineligible schemes? The initial recommendation is to include only eligible schemes, matching the primary output requirement.
3. Which JSON library and Java version does the course/evaluator require? The recommended baseline is Java 17 and one standard JSON library, but course constraints take precedence.
4. Should category values be restricted to a predefined list? The initial design treats them as configurable strings.
5. Should invalid scheme entries stop the entire load or be skipped? This guide recommends rejecting the configuration to avoid silently incomplete results.
6. Which official source will maintainers use to verify real scholarship criteria and document lists? This remains a project-owner responsibility.

## 12. Instructions for an implementation LLM

When implementing this architecture:

1. Treat the PRD requirements and exclusions in Section 1 as authoritative.
2. Build a Java console application; do not add a browser UI or REST API.
3. Implement the domain model and eligibility rules before the console workflow.
4. Keep `SchemeLoader` responsible for JSON parsing, validation, and mapping only.
5. Keep `EligibilityService` independent of file I/O and console input.
6. Keep report formatting/writing inside `EligibilityReportWriter`.
7. Preserve exact class names `Student`, `Scheme`, `MeritScheme`, `IncomeScheme`, `CategoryScheme`, `SchemeLoader`, `EligibilityService`, `EligibilityReportWriter`, and `Main`.
8. Use clear exceptions/messages; never silently ignore invalid JSON or rules.
9. Ensure a failed load does not become a successful empty result.
10. Add tests for thresholds, case-insensitive category matching, multiple matches, malformed rules, and report failures.
11. Use only supported rule types unless the project requirements are deliberately changed.
12. Keep the rules and documents clearly labeled as configurable sample data, not official guarantees.

## 13. Related requirements document

The source PRD is `ProjectPRD_OPPS.md`. Keep it alongside this architecture guide so implementation decisions can be traced back to the project's stated requirements.
