# SchemeSathi: Faculty Presentation & OOP Defense Guide

> **Project Title**: SchemeSathi — Automated Scholarship Eligibility Navigator  
> **Course / Domain**: Object-Oriented Software Design & Engineering (Java 17)  
> **Target Audience**: Academic Faculty & Project Evaluation Committee  
> **Ready-to-Run Presentation Slide Deck**: [`SchemeSathi_Faculty_Presentation.pdf`](./SchemeSathi_Faculty_Presentation.pdf) (16:9 Landscape Widescreen)  
> **Comprehensive Architecture Guide**: [`SchemeSathi_OOP_Project_Presentation_Guide.pdf`](./SchemeSathi_OOP_Project_Presentation_Guide.pdf)  

---

## 1. Team Work Division & 15-Minute Defense Schedule

The project presentation is systematically partitioned among three team members. Each member presents for **5 minutes**, covering their core technical domain with slide hand-offs.

```
========================================================================================
TIMELINE         MEMBER / ROLE                       SLIDES COVERED & CORE DOMAIN
========================================================================================
00:00 - 05:00    Member 1: Priyanshu Gupta           Slides 1 - 6
                 (System Architect & OOP Core)       • Problem Solved & Executive Vision
                                                     • 4 OOP Pillars (Abstraction, Encapsulation,
                                                       Inheritance, Dynamic Polymorphism)
                                                     • Open/Closed Principle (OCP) Proof
----------------------------------------------------------------------------------------
05:00 - 10:00    Member 2: Team Member 2             Slides 7 - 9
                 (Backend & File-Handling Lead)      • SPECIAL FOCUS: Java File Handling Architecture
                                                     • SchemeLoader Java NIO Input Ingestion
                                                     • EligibilityReportWriter Output Dossiers
                                                     • RFC-4180 CSV Export & REST Microserver
----------------------------------------------------------------------------------------
10:00 - 15:00    Member 3: Team Member 3             Slides 10 - 12
                 (UI/UX & Integration Lead)          • React 19 Frontend UI/UX Design System
                                                     • Dual Theme Accessibility (Dark/Light)
                                                     • 24 JUnit 5 Automated Unit Tests (100% Pass)
                                                     • End-to-End Live Demo & Faculty Viva Q&A
========================================================================================
```

---

## 2. Speaker Cue Cards & Presentation Script

### Speaker 1: Priyanshu Gupta (System Architect & OOP Core Lead)
- **Time**: 0:00 – 5:00 min | **Slides**: 1 – 6
- **Opening Cue**:
  > *"Respected faculty members and evaluators, welcome to our capstone defense of **SchemeSathi**. I am Priyanshu Gupta, lead architect. SchemeSathi solves the fragmented scholarship discovery crisis faced by Indian students. Millions of eligible students miss out on scholarships due to disparate portals and opaque eligibility rules. We engineered an automated, rule-based evaluation engine in pure Java 17 adhering strictly to the four pillars of Object-Oriented Programming."*
- **Slide 2 (Overview)**: Outline academic marks (%), annual family income (₹), and social category evaluation. Emphasize multi-channel delivery (Console CLI and React 19 SPA).
- **Slide 3 (Abstraction)**: Explain `Scheme.java` as an abstract class holding common state (`id`, `name`, `requiredDocuments`) and abstract methods `isEligible()` and `getCriteriaSummary()`. Contrast with `ReportWriter.java` interface.
- **Slide 4 (Encapsulation)**: Walk through defensive field protection in `Student.java` (0–100% marks, positive income) and cryptographic security in `AuthService.java` (SHA-256 with 16-byte random salt).
- **Slide 5 (Inheritance)**: Highlight `MeritScheme`, `IncomeScheme`, and `CategoryScheme` extending `Scheme`, calling `super(...)` to reuse base construction logic.
- **Slide 6 (Polymorphism)**: Explain dynamic method dispatch in `EligibilityService.java` where `scheme.isEligible(student)` executes the correct subclass logic at runtime without any `instanceof` checks.
- **Hand-off to Speaker 2**:
  > *"Now, my colleague will walk you through the centerpiece of our data pipeline — Java File Handling Architecture, JSON Ingestion, and CSV Streaming."*

---

### Speaker 2: Team Member 2 (Backend & File-Handling Lead)
- **Time**: 5:00 – 10:00 min | **Slides**: 7 – 9
- **Opening Cue**:
  > *"Thank you, Priyanshu. Respected faculty, I will now focus on our enterprise Java File Handling architecture and backend server design. File handling in SchemeSathi is split into two robust pipelines: configuration ingestion and audit dossier persistence."*
- **Slide 7 (Input File Handling - SchemeLoader)**:
  - Explain modern Java NIO.2 (`java.nio.file.Path` and `Files`).
  - Walk through 3-tier pre-flight verification: `Files.exists()`, `Files.isRegularFile()`, and `Files.isReadable()`.
  - Detail `Files.readString(path, StandardCharsets.UTF_8)` ensuring platform-independent encoding.
  - Explain Jackson deserialization into `SchemeRule` records and duplicate ID rejection via `Set<String> seenIds`.
- **Slide 8 (Output File Handling & CSV Export)**:
  - Walk through `EligibilityReportWriter.java` implementing `ReportWriter`.
  - Emphasize directory self-healing: `destination.getParent()` with `Files.createDirectories(parent)` preventing missing folder crashes.
  - Detail atomic file writing with `Files.writeString(...)` and `StandardOpenOption.CREATE`, `TRUNCATE_EXISTING`, `WRITE`.
  - Highlight RFC-4180 compliant CSV export in `AuthService.java` with UTF-8 BOM (`\ufeff`) for Excel compatibility and quotes escaping.
- **Slide 9 (Backend Architecture & REST Microserver)**:
  - Explain embedded `com.sun.net.httpserver.HttpServer` on port 8080 (zero Spring container bloat).
  - Walk through layered separation of concerns (`model`, `service`, `loader`, `report`, `auth`, `server`).
  - Detail REST endpoints: `/api/evaluate`, `/api/schemes`, `/api/report`, `/api/admin/logins/csv`.
- **Hand-off to Speaker 3**:
  > *"Next, my teammate will demonstrate our modern React 19 Frontend, testing suite, and faculty defense preparation."*

---

### Speaker 3: Team Member 3 (UI/UX & Integration Lead)
- **Time**: 10:00 – 15:00 min | **Slides**: 10 – 12
- **Opening Cue**:
  > *"Thank you. Respected faculty, I will now present the user interface and client integration of SchemeSathi."*
- **Slide 10 (UI/UX Design System)**:
  - Explain React 19 + Vite architecture.
  - Highlight dual-theme system (Dark/Light mode) driven by CSS custom properties.
  - Explain 1-click demographic presets (High Merit 92%, Need-Based ₹2.2L, OBC, SC/ST, EWS).
  - Explain removal of distracting background animations to maintain high contrast, professional focus, and accessibility.
  - Detail isolated Administrator Portal (`/admin`) for session tracking and 1-click CSV download.
- **Slide 11 (Team Work Division)**: Reiterate team collaboration, accountability, and module partitioning.
- **Slide 12 (Testing & Viva Defense)**:
  - Highlight 24/24 passing automated tests in JUnit 5 (`StudentTest`, `SchemeTest`, `EligibilityServiceTest`, `SchemeLoaderTest`, `EligibilityReportWriterTest`, `AuthServiceTest`).
  - Coordinate the viva defense session and invite questions from the panel.

---

## 3. Deep-Dive: The 4 Core OOP Pillars in SchemeSathi

### A. Abstraction
- **Abstract Base Class `Scheme.java`** ([`src/main/java/com/schemesathi/model/Scheme.java`](./src/main/java/com/schemesathi/model/Scheme.java)):
  ```java
  public abstract class Scheme {
      private final String id;
      private final String name;
      private final String type;
      private final List<String> requiredDocuments;

      public abstract boolean isEligible(Student student);
      public abstract String getCriteriaSummary();
  }
  ```
  - **Why an abstract class instead of an interface?**  
    All scholarships share persistent instance state (`id`, `name`, `type`, `requiredDocuments`) and shared getters. Java interfaces cannot hold instance variables. An abstract class provides **state reuse + mandatory polymorphic contracts**.
- **Interface `ReportWriter.java`** ([`src/main/java/com/schemesathi/report/ReportWriter.java`](./src/main/java/com/schemesathi/report/ReportWriter.java)):
  ```java
  public interface ReportWriter {
      void write(Path destination, Student student, List<Scheme> schemes) throws IOException;
  }
  ```
  Decouples report generation logic from file I/O or storage mechanisms.

---

### B. Encapsulation
- **Defensive Invariant Validation** ([`src/main/java/com/schemesathi/model/Student.java`](./src/main/java/com/schemesathi/model/Student.java)):
  ```java
  public Student(double marks, double annualFamilyIncome, String category) {
      if (marks < 0.0 || marks > 100.0) {
          throw new IllegalArgumentException("Marks must be between 0.0 and 100.0%.");
      }
      if (annualFamilyIncome < 0.0) {
          throw new IllegalArgumentException("Income cannot be negative.");
      }
      if (category == null || category.trim().isEmpty()) {
          throw new IllegalArgumentException("Category cannot be blank.");
      }
      this.marks = marks;
      this.annualFamilyIncome = annualFamilyIncome;
      this.category = category.trim().toUpperCase();
  }
  ```
- **Cryptographic Security Encapsulation** ([`src/main/java/com/schemesathi/auth/AuthService.java`](./src/main/java/com/schemesathi/auth/AuthService.java)):
  Passwords are never stored in plaintext. Passwords receive a 16-byte random salt generated via `SecureRandom` and are hashed using `SHA-256`.

---

### C. Inheritance
- **Concrete Subclasses**:
  - `MeritScheme extends Scheme`: Specializes with `minimumMarks`.
  - `IncomeScheme extends Scheme`: Specializes with `maximumAnnualIncome`.
  - `CategoryScheme extends Scheme`: Specializes with `List<String> allowedCategories`.
- **Constructor Chaining**:
  ```java
  public MeritScheme(String id, String name, List<String> docs, double minMarks) {
      super(id, name, "MERIT", docs); // Reuses base constructor
      this.minimumMarks = minMarks;
  }
  ```

---

### D. Polymorphism (Dynamic Method Dispatch)
- **Runtime Binding** ([`src/main/java/com/schemesathi/service/EligibilityService.java`](./src/main/java/com/schemesathi/service/EligibilityService.java)):
  ```java
  public List<Scheme> findEligible(Student student, List<Scheme> schemes) {
      List<Scheme> eligible = new ArrayList<>();
      for (Scheme scheme : schemes) {
          // Dynamic dispatch: resolves at runtime based on the actual concrete type
          if (scheme.isEligible(student)) {
              eligible.add(scheme);
          }
      }
      return eligible;
  }
  ```
- **Open/Closed Principle (OCP)**: Adding a new scholarship subclass (e.g. `SportsScheme`) requires zero changes to `EligibilityService`.

---

## 4. Special Focus: Java File Handling Architecture

File handling in SchemeSathi demonstrates enterprise-level Java NIO.2 best practices:

### 1. Robust Input File Ingestion (`SchemeLoader.java`)
- **Path Abstraction**: Uses `java.nio.file.Path` rather than legacy `java.io.File`.
- **3-Tier Pre-Flight File Checks**:
  ```java
  if (!Files.exists(path)) throw new IOException("Rules file does not exist: " + path);
  if (!Files.isRegularFile(path)) throw new IOException("Rules file is not a regular file: " + path);
  if (!Files.isReadable(path)) throw new IOException("Rules file is not readable: " + path);
  ```
- **Explicit Character Encoding**: `Files.readString(path, StandardCharsets.UTF_8)` prevents character corruption across Windows and Linux.
- **Defensive JSON Ingestion**: Malformed syntax and duplicate scheme IDs throw detailed `IOException` or `IllegalArgumentException`.

### 2. Output Dossier Generation (`EligibilityReportWriter.java`)
- **Automatic Directory Provisioning**:
  ```java
  Path parent = destination.getParent();
  if (parent != null && !Files.exists(parent)) {
      Files.createDirectories(parent);
  }
  ```
- **Atomic Writing Options**:
  ```java
  Files.writeString(
      destination,
      report.toString(),
      StandardCharsets.UTF_8,
      StandardOpenOption.CREATE,
      StandardOpenOption.TRUNCATE_EXISTING,
      StandardOpenOption.WRITE
  );
  ```

### 3. RFC-4180 CSV Export & HTTP Streaming (`AuthService.java` & `ApiServer.java`)
- **Excel Compatibility**: Prepends UTF-8 Byte Order Mark (`\ufeff`) to ensure Microsoft Excel renders the CSV correctly.
- **Field Escaping**: `escapeCsv()` wraps fields with commas or quotes in double-quotes (`""`).
- **HTTP Streaming**: Served via `Content-Type: text/csv; charset=UTF-8` and `Content-Disposition: attachment; filename="schemesathi-logins.csv"`.

---

## 5. UI/UX Design System Overview

- **Modern React 19 SPA**: Powered by Vite with ultra-fast sub-2-second production builds.
- **Dual Theme System**: Seamless toggle between Dark Mode and Light Mode via CSS variables.
- **Clean Visual Focus**: Background canvas animation removed to maintain sharp visual contrast and zero cognitive distraction for academic evaluators.
- **One-Click Presets**: Immediate testing of student profiles (High Merit 92%, Need-Based ₹2.2L, OBC, SC/ST, EWS).
- **Dedicated Admin Console**: Real-time audit session monitoring with 1-click CSV download.

---

## 6. Top 5 Faculty Viva Questions & Model Answers

1. **Q: Why use an abstract class instead of an interface for `Scheme`?**  
   *A: All scholarships share common fields (`id`, `name`, `type`, `requiredDocuments`) and concrete getters. Java interfaces cannot hold instance variables. An abstract class enables instance state reuse while enforcing mandatory polymorphic contracts via abstract `isEligible()`.*

2. **Q: Where exactly does dynamic method dispatch occur?**  
   *A: In `EligibilityService.findEligible()` when invoking `scheme.isEligible(student)`. The JVM resolves the concrete implementation (`MeritScheme`, `IncomeScheme`, or `CategoryScheme`) at runtime via the virtual method table (vtable).*

3. **Q: How does the file handling prevent runtime application crashes?**  
   *A: `SchemeLoader` runs pre-flight checks (`Files.exists`, `isRegularFile`, `isReadable`) before reading. `EligibilityReportWriter` automatically creates parent directories with `Files.createDirectories(parent)`, preventing `NoSuchFileException`.*

4. **Q: How are user passwords secured?**  
   *A: Passwords are salted with a 16-byte random salt using `java.security.SecureRandom` and hashed with SHA-256. Passwords are never stored in plaintext, preventing dictionary and rainbow table attacks.*

5. **Q: How does the client communicate with the Java backend?**  
   *A: An embedded lightweight Java `HttpServer` runs on port 8080 exposing REST endpoints with CORS headers (`Access-Control-Allow-Origin: *`). The React frontend communicates asynchronously via JSON `fetch`.*

---

## 7. Automated Test Suite (JUnit 5)

All 24 automated unit tests execute and pass cleanly:
```bash
mvn test
```
- `StudentTest`: 9 tests (Boundary conditions, negative income, 0–100% marks).
- `SchemeTest`: 3 tests (Concrete subclass rule evaluation).
- `EligibilityServiceTest`: 2 tests (Dynamic dispatch matching).
- `SchemeLoaderTest`: 3 tests (File validation, malformed JSON handling).
- `EligibilityReportWriterTest`: 2 tests (File generation, directory creation).
- `AuthServiceTest`: 5 tests (SHA-256 hashing, session tokens, CSV formatting).
