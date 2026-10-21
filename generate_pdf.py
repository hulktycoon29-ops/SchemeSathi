import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(45, 805, "SchemeSathi — Java OOP Architecture & Presentation Defense Guide")
            self.setStrokeColor(colors.HexColor("#e2e8f0"))
            self.setLineWidth(0.5)
            self.line(45, 800, 550, 800)

        # Footer
        text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(550, 30, text)
        self.drawString(45, 30, "Confidential — Prepared for Academic Project Defense & Evaluation")
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(45, 40, 550, 40)
        self.restoreState()

def build_pdf(filename="SchemeSathi_OOP_Project_Presentation_Guide.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=45,
        rightMargin=45,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    # Custom styles
    primary_color = colors.HexColor("#0f172a")
    accent_blue = colors.HexColor("#0284c7")
    text_dark = colors.HexColor("#1e293b")
    text_muted = colors.HexColor("#475569")
    bg_subtle = colors.HexColor("#f8fafc")
    border_color = colors.HexColor("#cbd5e1")

    style_title = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=primary_color,
        spaceAfter=4
    )

    style_subtitle = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=accent_blue,
        spaceAfter=14
    )

    style_h1 = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=primary_color,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    style_h2 = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=accent_blue,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=text_dark,
        spaceAfter=6
    )

    style_code = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#0f172a")
    )

    style_badge = ParagraphStyle(
        'Badge',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#0369a1")
    )

    story = []

    # ================= COVER / HEADER =================
    badge_table = Table([[Paragraph("OBJECT-ORIENTED PROGRAMMING (JAVA) CAPSTONE PROJECT", style_badge)]], colWidths=[505])
    badge_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#e0f2fe")),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(badge_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("SchemeSathi: Scholarship Eligibility Navigator", style_title))
    story.append(Paragraph("Complete Technical Architecture, OOP Implementation Mapping & Defense Guide", style_subtitle))
    story.append(HRFlowable(width="100%", thickness=1.5, color=accent_blue, spaceAfter=10))

    meta_data = [
        [
            Paragraph("<b>Author / Lead Developer:</b> Priyanshu Gupta", style_body),
            Paragraph("<b>Academic Domain:</b> Object-Oriented Software Design", style_body)
        ],
        [
            Paragraph("<b>Backend Architecture:</b> Java 17 + Maven + Embedded HTTP Server", style_body),
            Paragraph("<b>Security & Cryptography:</b> SHA-256 + 16-Byte Secure Salt Hashing", style_body)
        ],
        [
            Paragraph("<b>Frontend Framework:</b> React 19 + Vite (Modern Dark/Light System)", style_body),
            Paragraph("<b>Cloud Deployment:</b> Multi-Stage Docker on Render (HTTPS Enabled)", style_body)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[250, 255])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg_subtle),
        ('BOX', (0,0), (-1,-1), 1, border_color),
        ('INNERGRID', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 14))

    # ================= SECTION 1 =================
    story.append(Paragraph("1. Project Overview & Problem Statement", style_h1))
    story.append(Paragraph(
        "<b>SchemeSathi</b> is an automated scholarship eligibility and navigation system engineered to solve the complex discovery problem faced by Indian students. Instead of manually inspecting numerous disparate portals and government gazettes, students provide their academic performance (marks %), annual family income, and demographic category. The Java OOP rule engine executes polymorphic rule verification to output instant eligibility outcomes, detailed disqualification reasons, mandatory document checklists, and downloadable plain-text audit reports.",
        style_body
    ))
    story.append(Spacer(1, 6))

    # ================= SECTION 2: THE 4 OOP PILLARS =================
    story.append(Paragraph("2. Deep-Dive: The 4 Core OOP Principles in SchemeSathi", style_h1))
    story.append(Paragraph(
        "The project is structured strictly around the four fundamental pillars of Object-Oriented Programming:",
        style_body
    ))

    oop_rows = [
        [
            Paragraph("<b>OOP Pillar</b>", style_body),
            Paragraph("<b>Source Code Location</b>", style_body),
            Paragraph("<b>Implementation & Architectural Purpose</b>", style_body)
        ],
        [
            Paragraph("<b>1. Abstraction</b>", style_body),
            Paragraph("<code>com.schemesathi.model.Scheme</code><br/><code>com.schemesathi.report.ReportWriter</code>", style_code),
            Paragraph("• <code>Scheme</code> is an <b>abstract class</b> defining common attributes (id, name, required documents) and abstract methods <code>isEligible(Student s)</code> and <code>getCriteriaDescription()</code>.<br/>• <code>ReportWriter</code> is an <b>interface</b> hiding underlying File I/O behind an abstract contract.", style_body)
        ],
        [
            Paragraph("<b>2. Encapsulation</b>", style_body),
            Paragraph("<code>com.schemesathi.model.Student</code><br/><code>com.schemesathi.auth.User</code><br/><code>com.schemesathi.auth.AuthService</code>", style_code),
            Paragraph("• All class fields are declared <code>private</code>. Data mutation occurs only through getters/setters with strict defensive validation (e.g., marks between 0-100%, non-negative income).<br/>• Passwords are encrypted with SHA-256 and unique 16-byte random salts before storage.", style_body)
        ],
        [
            Paragraph("<b>3. Inheritance</b>", style_body),
            Paragraph("<code>MeritScheme extends Scheme</code><br/><code>IncomeScheme extends Scheme</code><br/><code>CategoryScheme extends Scheme</code>", style_code),
            Paragraph("• Concrete subclasses inherit shared fields and constructors via <code>super(...)</code> while introducing specialized criteria (e.g. <code>minimumMarks</code> in <code>MeritScheme</code>, <code>maximumAnnualIncome</code> in <code>IncomeScheme</code>).", style_body)
        ],
        [
            Paragraph("<b>4. Polymorphism</b>", style_body),
            Paragraph("<code>com.schemesathi.service.EligibilityService</code>", style_code),
            Paragraph("• <b>Dynamic Method Dispatch</b>: The evaluation engine handles a generic collection <code>List&lt;Scheme&gt;</code> and calls <code>scheme.isEligible(student)</code>. The JVM resolves the concrete implementation at runtime without <code>instanceof</code> checks, adhering to the <b>Open/Closed Principle</b>.", style_body)
        ]
    ]

    oop_table = Table(oop_rows, colWidths=[90, 160, 255])
    oop_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    for i in range(len(oop_rows)):
        if i == 0:
            oop_table.setStyle(TableStyle([('TEXTCOLOR', (0,0), (-1,0), colors.white)]))
        elif i % 2 == 1:
            oop_table.setStyle(TableStyle([('BACKGROUND', (0, i), (-1, i), colors.HexColor("#f8fafc"))]))

    story.append(oop_table)
    story.append(Spacer(1, 14))

    # ================= SECTION 3: CODE SNIPPET HIGHLIGHT =================
    story.append(Paragraph("3. Runtime Polymorphism in Action (Code Proof)", style_h1))
    code_text = (
        "// EligibilityService.java - Polymorphic loop with Dynamic Method Dispatch\n"
        "public List<Scheme> findEligibleSchemes(Student student, List<Scheme> schemes) {\n"
        "    List<Scheme> eligible = new ArrayList<>();\n"
        "    for (Scheme scheme : schemes) {\n"
        "        // Dynamic dispatch: executes MeritScheme, IncomeScheme, or CategoryScheme at runtime\n"
        "        if (scheme.isEligible(student)) {\n"
        "            eligible.add(scheme);\n"
        "        }\n"
        "    }\n"
        "    return eligible;\n"
        "}"
    )
    code_box = Table([[Paragraph(f"<pre>{code_text}</pre>", style_code)]], colWidths=[505])
    code_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0f172a")),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(code_box)
    story.append(Spacer(1, 14))

    # ================= SECTION 4: LAYERED ARCHITECTURE & STRUCTURE =================
    story.append(Paragraph("4. Project Layered Structure & Clean Architecture", style_h1))
    struct_data = [
        [Paragraph("<b>Layer / Package</b>", style_body), Paragraph("<b>Primary Responsibility & Classes</b>", style_body)],
        [Paragraph("<code>com.schemesathi.model</code>", style_code), Paragraph("Domain entities: <code>Student</code>, abstract <code>Scheme</code>, <code>MeritScheme</code>, <code>IncomeScheme</code>, <code>CategoryScheme</code>.", style_body)],
        [Paragraph("<code>com.schemesathi.service</code>", style_code), Paragraph("Business rule evaluation: <code>EligibilityService</code> running polymorphic verification and breakdown analysis.", style_body)],
        [Paragraph("<code>com.schemesathi.loader</code>", style_code), Paragraph("JSON persistence ingestion: <code>SchemeLoader</code> reading scholarship rules from <code>data/schemes.json</code>.", style_body)],
        [Paragraph("<code>com.schemesathi.report</code>", style_code), Paragraph("Export subsystem: <code>ReportWriter</code> (interface) and <code>EligibilityReportWriter</code> generating formatted text dossiers.", style_body)],
        [Paragraph("<code>com.schemesathi.auth</code>", style_code), Paragraph("Security, hashing & auditing: <code>AuthService</code>, <code>User</code>, <code>LoginRecord</code> with SHA-256 + 16-byte random salt.", style_body)],
        [Paragraph("<code>com.schemesathi.server</code>", style_code), Paragraph("Microserver layer: <code>ApiServer</code> exposing REST endpoints (<code>/api/evaluate</code>, <code>/api/auth</code>, <code>/api/admin</code>).", style_body)],
        [Paragraph("<code>frontend/</code>", style_code), Paragraph("Client-side SPA: React 19 + Vite with Light/Dark CSS variables, WebGL2 animations, and isolated Admin Console.", style_body)]
    ]
    struct_table = Table(struct_data, colWidths=[160, 345])
    struct_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(struct_table)
    story.append(Spacer(1, 14))

    # ================= SECTION 5: VIVA & PRESENTATION QUESTIONS =================
    story.append(Paragraph("5. Key Viva & Presentation Defense Questions", style_h1))

    qnas = [
        ("Q1: Why did you use an abstract class instead of an interface for Scheme?",
         "An abstract class allows sharing state (fields like id, name, requiredDocuments) and shared methods (getters/setters) across all schemes via super(...). Interfaces cannot hold instance fields. Abstract methods (isEligible) ensure each subclass provides custom evaluation logic."),
        
        ("Q2: How does the system handle security and passwords?",
         "Passwords are never stored in plaintext. In AuthService.java, every password is combined with a cryptographically secure 16-byte random salt generated via java.security.SecureRandom and hashed with SHA-256. This prevents rainbow table attacks and protects credentials."),

        ("Q3: How does the client communicate with the Java backend?",
         "The Java backend runs an embedded HttpServer on port 8080 (or cloud $PORT) exposing REST endpoints. It implements CORS headers (Access-Control-Allow-Origin: *) allowing the React frontend to asynchronously POST student data and receive structured JSON responses."),

        ("Q4: How was this project tested?",
         "We implemented 24 comprehensive automated unit tests using JUnit 5 in src/test/java. Every test verifies domain constraints, polymorphic evaluations, report generation, and credential hashing. All 24 tests pass cleanly during mvn test."),

        ("Q5: How is the application deployed to production?",
         "We created a production-ready multi-stage Dockerfile compiling the Java Fat-JAR and serving it on Render Cloud with automatic HTTPS. The React frontend is deployed as a high-performance Static Site on Render connected to the cloud backend.")
    ]

    for q, a in qnas:
        q_box = [
            [Paragraph(f"<b>{q}</b>", style_h2)],
            [Paragraph(f"<b>Model Answer:</b> {a}", style_body)]
        ]
        t = Table(q_box, colWidths=[505])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), bg_subtle),
            ('BOX', (0,0), (-1,-1), 1, border_color),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(t)
        story.append(Spacer(1, 6))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] Defense Guide PDF generated: {filename}")

if __name__ == "__main__":
    build_pdf()
    try:
        from generate_presentation_pdf import create_presentation_pdf
        create_presentation_pdf("SchemeSathi_Faculty_Presentation.pdf")
    except Exception as e:
        print(f"[!] Note: Could not auto-trigger presentation PDF: {e}")
