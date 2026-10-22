# SchemeSathi — Scholarship Eligibility Navigator 🎓⚡

**SchemeSathi** is an educational scholarship navigator built with a **Java Object-Oriented Programming (OOP) Backend** and a modern **React Web UI** featuring **WebGL2 canvas animations** (`CursorGrid`).

---

## 🌟 Key Features

1. **Robust Java OOP Architecture**:
   - **Encapsulation**: Private immutable state & validation in [`Student`](file:///c:/Users/hp/OneDrive/Desktop/JAVA%20PROJECT/src/main/java/com/schemesathi/model/Student.java).
   - **Abstraction**: Abstract base class [`Scheme`](file:///c:/Users/hp/OneDrive/Desktop/JAVA%20PROJECT/src/main/java/com/schemesathi/model/Scheme.java) defining shared attributes and the polymorphic `isEligible(Student)` contract.
   - **Inheritance & Polymorphism**: Specialized concrete subclasses:
     - [`MeritScheme`](file:///c:/Users/hp/OneDrive/Desktop/JAVA%20PROJECT/src/main/java/com/schemesathi/model/MeritScheme.java): Minimum academic percentage threshold.
     - [`IncomeScheme`](file:///c:/Users/hp/OneDrive/Desktop/JAVA%20PROJECT/src/main/java/com/schemesathi/model/IncomeScheme.java): Maximum annual family income ceiling.
     - [`CategoryScheme`](file:///c:/Users/hp/OneDrive/Desktop/JAVA%20PROJECT/src/main/java/com/schemesathi/model/CategoryScheme.java): Case-insensitive social category matching.
   - **Service Layer**: [`EligibilityService`](file:///c:/Users/hp/OneDrive/Desktop/JAVA%20PROJECT/src/main/java/com/schemesathi/service/EligibilityService.java) polymorphically evaluates qualifying schemes.
   - **File I/O & Error Handling**:
     - [`SchemeLoader`](file:///c:/Users/hp/OneDrive/Desktop/JAVA%20PROJECT/src/main/java/com/schemesathi/loader/SchemeLoader.java): JSON loading & strict rule validation from [`data/schemes.json`](file:///c:/Users/hp/OneDrive/Desktop/JAVA%20PROJECT/data/schemes.json).
     - [`EligibilityReportWriter`](file:///c:/Users/hp/OneDrive/Desktop/JAVA%20PROJECT/src/main/java/com/schemesathi/report/EligibilityReportWriter.java): Generates formatted plain-text reports to [`output/eligibility-report.txt`](file:///c:/Users/hp/OneDrive/Desktop/JAVA%20PROJECT/output/eligibility-report.txt).
2. **Dual Execution Modes**:
   - **Interactive Console CLI**: User-friendly terminal interface as requested in `ProjectPRD_OPPS.md`.
   - **Built-in REST API Server**: High-performance HTTP server (`com.sun.net.httpserver`) providing `/api/health`, `/api/schemes`, `/api/evaluate`, and `/api/report`.
3. **Modern Web UI with Dynamic Animations**:
   - Interactive WebGL2 **`CursorGrid`** background from React Bits.
   - Instant criteria slider/inputs, quick test presets, catalog explorer, and 1-click official report download.

---

## 🚀 Quick Start Guide

### 1. Run the Interactive Java Console Application (CLI)

```bash
# Using pre-built standalone executable JAR:
java -jar target/schemesathi-1.0.0-jar-with-dependencies.jar --cli

# Or using Maven:
mvn compile exec:java -Dexec.args="--cli"
```

### 2. Run the Java REST API Backend Server

```bash
# Start backend server on port 8080:
java -jar target/schemesathi-1.0.0-jar-with-dependencies.jar --server --port 8080
```
> The API server exposes:
> - `GET  http://localhost:8080/api/health`
> - `GET  http://localhost:8080/api/schemes`
> - `POST http://localhost:8080/api/evaluate`
> - `POST http://localhost:8080/api/report`
> - `POST http://localhost:8080/api/auth/register` (New user registration)
> - `POST http://localhost:8080/api/auth/login` (Authentication & session token issuance)
> - `GET  http://localhost:8080/api/admin/logins` (Audit log of all user logins)
> - `GET  http://localhost:8080/api/admin/logins/csv` (Downloadable CSV audit log)

### 3. Run the React Web UI

```bash
cd frontend
npm run dev
```

- **User Portal (Default)**: **`http://localhost:5173/`**
  - Users **must sign in or create an account** before accessing the scholarship navigator.
  - Contains **no admin controls or buttons**.
- **Admin Console (Isolated URL)**: **`http://localhost:5173/#/admin`** (or `/admin`)
  - Dedicated administrative gateway.
  - Accessible strictly to administrators (`admin` / `Admin@123`).
  - View real-time user login audit logs and export to `.csv`.

---

## 🧪 Running Unit Tests

Run the full JUnit 5 test suite with:

```bash
mvn test
```
All 19 tests test boundary values, invalid inputs, case-insensitivity, multiple polymorphic matches, schema validation, and report file generation.

---

## 📁 Project Structure

```
JAVA PROJECT/
├── data/
│   └── schemes.json                   # Configurable scholarship rules
├── src/
│   ├── main/java/com/schemesathi/
│   │   ├── Main.java                  # Application coordinator (CLI + REST Server)
│   │   ├── model/                     # Domain models (Student, Scheme, Merit, Income, Category)
│   │   ├── service/                   # EligibilityService
│   │   ├── loader/                    # SchemeLoader & SchemeRule DTO
│   │   ├── report/                    # ReportWriter & EligibilityReportWriter
│   │   ├── server/                    # ApiServer (REST HTTP server)
│   │   └── ui/                        # ConsoleUI
│   └── test/java/com/schemesathi/     # Comprehensive JUnit 5 test suite
├── frontend/                          # Modern React + Vite application
│   ├── src/
│   │   ├── components/animations/     # CursorGrid (WebGL2)
│   │   ├── App.jsx                    # Reactive UI with live evaluation & presets
│   │   └── index.css                  # Modern dark theme design system
├── target/
│   └── schemesathi-1.0.0-jar-with-dependencies.jar # Standalone executable JAR
└── pom.xml                            # Maven project build configuration
```
