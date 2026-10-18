# SchemeSathi: Complete OOP Architecture & Project Presentation Guide

> **Author**: Priyanshu Gupta (`hulktycoon29-ops`)  
> **Course / Domain**: Object-Oriented Software Design & Engineering (Java 17)  
> **Generated PDF File**: [`SchemeSathi_OOP_Project_Presentation_Guide.pdf`](./SchemeSathi_OOP_Project_Presentation_Guide.pdf)

---

## 1. Executive Summary & Problem Solved
**SchemeSathi** is an automated scholarship eligibility navigator and security management system designed for Indian students. It eliminates manual, error-prone verification of fragmented educational schemes by providing:
1. **Dynamic Academic & Income Evaluation**: Real-time matching against Merit, Need-Based, and Category schemes.
2. **Polymorphic Rule Engine**: Modular Java OOP architecture allowing new scholarship types to be added without modifying core evaluation logic.
3. **Cryptographic User & Admin Security**: SHA-256 + 16-byte random salt password hashing with real-time audit logging and CSV export.
4. **Modern Web Interface**: Responsive React 19 SPA with light/dark theme toggle, WebGL2 background grids, and isolated admin portal.

---

## 2. The 4 Core OOP Pillars in SchemeSathi

### A. Abstraction
- **Abstract Class `Scheme.java`** ([`src/main/java/com/schemesathi/model/Scheme.java`](./src/main/java/com/schemesathi/model/Scheme.java)):
  Defines the common blueprint for all scholarships. It declares common attributes (`id`, `name`, `type`, `requiredDocuments`) and mandates abstract methods:
  ```java
  public abstract boolean isEligible(Student student);
  public abstract String getCriteriaDescription();
  ```
  The rest of the system does not need to know *how* eligibility is computed, only *that* it can be evaluated.
- **Interface `ReportWriter.java`** ([`src/main/java/com/schemesathi/report/ReportWriter.java`](./src/main/java/com/schemesathi/report/ReportWriter.java)):
  Abstracts file export behavior behind `generateReport(...)`.

### B. Encapsulation
- **Private Fields & Data Validation**:
  In `Student.java` ([`src/main/java/com/schemesathi/model/Student.java`](./src/main/java/com/schemesathi/model/Student.java)), all fields (`id`, `name`, `marksPercentage`, `annualIncome`, `category`) are `private`. Constructing or setting a student validates that marks are between `0.0` and `100.0%` and income is positive.
- **Cryptographic Security in `AuthService.java`** ([`src/main/java/com/schemesathi/auth/AuthService.java`](./src/main/java/com/schemesathi/auth/AuthService.java)):
  User password hashes and salts are encapsulated. Passwords are never stored in plaintext:
  ```java
  String salt = generateSalt(); // 16-byte cryptographically secure random salt
  String hash = hashPassword(password, salt); // SHA-256
  ```

### C. Inheritance
- Concrete subclasses inherit from `Scheme`:
  1. **`MeritScheme extends Scheme`**: Adds `minimumMarks`.
  2. **`IncomeScheme extends Scheme`**: Adds `maximumAnnualIncome`.
  3. **`CategoryScheme extends Scheme`**: Adds `List<String> allowedCategories`.
- Each subclass calls `super(id, name, type, requiredDocuments)` to reuse base constructor logic.

### D. Polymorphism
- **Dynamic Method Dispatch (Runtime Polymorphism)**:
  In `EligibilityService.java` ([`src/main/java/com/schemesathi/service/EligibilityService.java`](./src/main/java/com/schemesathi/service/EligibilityService.java)):
  ```java
  public List<Scheme> findEligibleSchemes(Student student, List<Scheme> schemes) {
      List<Scheme> eligible = new ArrayList<>();
      for (Scheme scheme : schemes) {
          // Dynamic dispatch: resolves to MeritScheme, IncomeScheme, or CategoryScheme at runtime
          if (scheme.isEligible(student)) {
              eligible.add(scheme);
          }
      }
      return eligible;
  }
  ```
  No `instanceof` checks or `switch` statements exist. Adding a new `SportsScheme` requires zero changes to `EligibilityService`.

---

## 3. Project Layered Structure

```
src/main/java/com/schemesathi/
├── model/        -> Domain models (Student, Scheme, MeritScheme, IncomeScheme, CategoryScheme)
├── service/      -> Business rules (EligibilityService)
├── loader/       -> JSON serialization/deserialization (SchemeLoader, SchemeRule)
├── report/       -> Dossier generation (ReportWriter, EligibilityReportWriter)
├── auth/         -> Security, hashing, and audit trails (AuthService, User, LoginRecord)
├── server/       -> Embedded HTTP REST API Server (ApiServer)
└── ui/           -> Headless Terminal Console (ConsoleUI)
```

---

## 4. End-to-End Execution Flow

1. **Student Input**: Student enters marks (`85%`), income (`₹2.4L`), category (`OBC`) in the UI.
2. **REST Dispatch**: React POSTs JSON to `/api/evaluate`.
3. **Encapsulation**: `ApiServer` instantiates a validated `Student` object.
4. **Polymorphic Evaluation**: `EligibilityService` evaluates each scheme polymorphically via `scheme.isEligible(student)`.
5. **Report & Output**: Audit report is written to `output/eligibility-report.txt` and returned as JSON to the UI.
6. **Admin Auditing**: User logins and events are logged into `loginHistory` and exportable as CSV.

---

## 5. Top 5 Viva Questions & Bulletproof Answers

1. **Q: Why use an abstract class instead of an interface for `Scheme`?**  
   *A: Because all scholarships share common fields (`id`, `name`, `requiredDocuments`) and shared getters. Interfaces in Java cannot hold instance state. An abstract class combines code reuse with mandatory abstract method contracts.*

2. **Q: Where does runtime polymorphism take place?**  
   *A: In `EligibilityService.findEligibleSchemes` when `scheme.isEligible(student)` is called on a collection of `List<Scheme>`.*

3. **Q: How is security maintained in the project?**  
   *A: Passwords are salted with a 16-byte random salt using `SecureRandom` and hashed with SHA-256. Admin routes are protected and audited with timestamped session records.*

4. **Q: How does the client-server communication work?**  
   *A: An embedded Java `HttpServer` exposes REST endpoints (`/api/evaluate`, `/api/auth`, `/api/schemes`) with CORS enabled. The React frontend interacts asynchronously via `fetch`.*

5. **Q: How is the project tested?**  
   *A: 24 unit tests built with JUnit 5 test models, polymorphic services, report writing, and security hashing during `mvn test`.*
