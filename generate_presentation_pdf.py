import os
import sys
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

# 16:9 Presentation Slide Dimensions (960 x 540 pt)
SLIDE_WIDTH = 960
SLIDE_HEIGHT = 540

class PresentationCanvas(canvas.Canvas):
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
            self.draw_slide_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_slide_decorations(self, total_slides):
        self.saveState()
        
        # Top accent gradient/bar
        self.setFillColor(colors.HexColor("#0284c7")) # primary cyan/blue
        self.rect(0, SLIDE_HEIGHT - 6, SLIDE_WIDTH, 6, fill=1, stroke=0)
        
        # Subtle top accent secondary line
        self.setFillColor(colors.HexColor("#38bdf8"))
        self.rect(0, SLIDE_HEIGHT - 8, 220, 2, fill=1, stroke=0)

        # Footer styling
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#0284c7"))
        self.drawString(40, 22, "SCHEMESATHI")
        
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        self.drawString(110, 22, "|   Java OOP Architecture & Academic Faculty Project Defense")
        
        # Center presenter note
        self.drawCentredString(SLIDE_WIDTH / 2.0, 22, "Confidential — Evaluated for B.Tech / Academic Project Defense")

        # Slide Number
        page_str = f"Slide {self._pageNumber} of {total_slides}"
        self.drawRightString(SLIDE_WIDTH - 40, 22, page_str)
        
        # Footer dividing line
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.75)
        self.line(40, 32, SLIDE_WIDTH - 40, 32)
        
        self.restoreState()

def create_presentation_pdf(filename="SchemeSathi_Faculty_Presentation.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=(SLIDE_WIDTH, SLIDE_HEIGHT),
        leftMargin=40,
        rightMargin=40,
        topMargin=28,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Color Palette
    c_primary = colors.HexColor("#0f172a")       # Slate 900
    c_accent = colors.HexColor("#0284c7")        # Sky 600
    c_accent_dark = colors.HexColor("#0369a1")   # Sky 700
    c_teal = colors.HexColor("#0d9488")          # Teal 600
    c_amber = colors.HexColor("#d97706")         # Amber 600
    c_text_dark = colors.HexColor("#1e293b")     # Slate 800
    c_text_muted = colors.HexColor("#475569")    # Slate 600
    c_bg_subtle = colors.HexColor("#f8fafc")     # Slate 50
    c_border = colors.HexColor("#cbd5e1")        # Slate 300
    c_card_border = colors.HexColor("#e2e8f0")   # Slate 200

    # Custom Typography Styles
    title_main = ParagraphStyle(
        'SlideTitleMain',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=c_primary
    )

    title_sub = ParagraphStyle(
        'SlideTitleSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=c_accent
    )

    slide_heading = ParagraphStyle(
        'SlideHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=c_primary
    )

    slide_subheading = ParagraphStyle(
        'SlideSubHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=c_accent
    )

    speaker_badge = ParagraphStyle(
        'SpeakerBadge',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
        alignment=2 # Right align
    )

    card_header = ParagraphStyle(
        'CardHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=c_primary
    )

    card_body = ParagraphStyle(
        'CardBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12.5,
        textColor=c_text_dark
    )

    card_body_bold = ParagraphStyle(
        'CardBodyBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12.5,
        textColor=c_text_dark
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.2,
        leading=11,
        textColor=colors.HexColor("#0f172a")
    )

    code_style_white = ParagraphStyle(
        'CodeStyleWhite',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#f8fafc")
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.white
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=11,
        textColor=c_text_dark
    )

    table_cell_code = ParagraphStyle(
        'TableCellCode',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.8,
        leading=10.5,
        textColor=c_text_dark
    )

    def make_slide_header(title, subtitle, speaker_text, speaker_color="#0284c7"):
        header_table = Table([
            [
                Paragraph(f"<b>{title}</b>", slide_heading),
                Paragraph(f"<font color='{speaker_color}'>●</font> <b>{speaker_text}</b>", speaker_badge)
            ],
            [
                Paragraph(subtitle, slide_subheading),
                Paragraph("", slide_subheading)
            ]
        ], colWidths=[660, 220])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 1),
            ('BOTTOMPADDING', (0,0), (-1,-1), 1),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('ALIGN', (1,0), (1,-1), 'RIGHT'),
        ]))
        return [header_table, HRFlowable(width="100%", thickness=1, color=c_card_border, spaceBefore=4, spaceAfter=8)]

    slides = []

    # =========================================================================
    # SLIDE 1: TITLE & PRESENTATION OVERVIEW
    # =========================================================================
    badge_title = Table([[
        Paragraph("<font color='#0284c7'><b>OBJECT-ORIENTED SOFTWARE DESIGN & ENGINEERING — CAPSTONE DEFENSE</b></font>", card_header),
        Paragraph("<b>Java 17 &nbsp;|&nbsp; React 19 &nbsp;|&nbsp; Maven &nbsp;|&nbsp; Docker</b>", card_body_bold)
    ]], colWidths=[580, 300])
    badge_title.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#e0f2fe")),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ALIGN', (1,0), (1,-1), 'RIGHT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#bae6fd"))
    ]))
    slides.append(badge_title)
    slides.append(Spacer(1, 10))

    slides.append(Paragraph("SchemeSathi: Automated Scholarship Eligibility Navigator", title_main))
    slides.append(Spacer(1, 3))
    slides.append(Paragraph("Comprehensive Java OOP Architecture, Enterprise File Handling & Faculty Defense Presentation", title_sub))
    slides.append(HRFlowable(width="100%", thickness=2, color=c_accent, spaceBefore=6, spaceAfter=12))

    # 3 Team Members Presentation Team Cards
    team_data = [
        [
            Paragraph("<font color='#0369a1'><b>PRESENTER 1 (Lead Architect)</b></font><br/><b>Priyanshu Gupta</b>", card_header),
            Paragraph("<font color='#0d9488'><b>PRESENTER 2 (Backend & File I/O)</b></font><br/><b>Team Member 2</b>", card_header),
            Paragraph("<font color='#d97706'><b>PRESENTER 3 (UI/UX & Integration)</b></font><br/><b>Team Member 3</b>", card_header)
        ],
        [
            Paragraph(
                "• Project Vision & Problem Statement<br/>"
                "• 4 Fundamental OOP Pillars Mapping<br/>"
                "• Abstraction & Polymorphic Rules<br/>"
                "• Domain Model Encapsulation",
                card_body
            ),
            Paragraph(
                "• <b>Special Focus: Java File Handling</b><br/>"
                "• NIO <code>SchemeLoader</code> JSON Ingestion<br/>"
                "• Dossier Export (<code>ReportWriter</code>)<br/>"
                "• CSV Audit Streaming & HTTP Server",
                card_body
            ),
            Paragraph(
                "• React 19 Frontend UI/UX Architecture<br/>"
                "• Dark/Light Theme System Design<br/>"
                "• End-to-End System Integration<br/>"
                "• 24 JUnit 5 Tests & Faculty Q&A",
                card_body
            )
        ],
        [
            Paragraph("<font color='#0284c7'><b>Allotment: Slides 1 – 6 (5 Mins)</b></font>", card_body_bold),
            Paragraph("<font color='#0d9488'><b>Allotment: Slides 7 – 9 (5 Mins)</b></font>", card_body_bold),
            Paragraph("<font color='#d97706'><b>Allotment: Slides 10 – 12 (5 Mins)</b></font>", card_body_bold)
        ]
    ]
    team_table = Table(team_data, colWidths=[286, 286, 288])
    team_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_subtle),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_card_border),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    slides.append(team_table)
    slides.append(Spacer(1, 10))

    meta_bar = Table([[
        Paragraph("<b>Target Faculty Audience:</b> Object-Oriented Software Evaluation Committee", card_body),
        Paragraph("<b>Total Time:</b> 15 Minutes (5 Mins/Member + Viva Q&A)", card_body),
        Paragraph("<b>Format:</b> Ready-to-Run Presentation Slide Deck", card_body)
    ]], colWidths=[350, 270, 260])
    meta_bar.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f1f5f9")),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ALIGN', (2,0), (2,-1), 'RIGHT')
    ]))
    slides.append(meta_bar)
    slides.append(PageBreak())

    # =========================================================================
    # SLIDE 2: EXECUTIVE PROJECT OVERVIEW & PROBLEM STATEMENT
    # =========================================================================
    slides.extend(make_slide_header(
        "Project Overview & Problem Statement",
        "Automated Scholarship Discovery & Verification Engine for Higher Education",
        "Presenter 1: Priyanshu Gupta",
        "#0369a1"
    ))

    overview_cols = [
        [
            Paragraph("<b>The Real-World Academic Challenge</b>", card_header),
            Paragraph("<b>The SchemeSathi Solution</b>", card_header)
        ],
        [
            Paragraph(
                "• <b>Fragmented Scholarship Landscape:</b> Indian students miss over 65% of available central, state, and private schemes due to opaque guidelines.<br/><br/>"
                "• <b>Complex Multi-Variable Criteria:</b> Eligibility hinges on interconnected conditions: Academic Marks (%), Annual Family Income (₹), and Social/Demographic Categories (General, OBC, SC, ST, EWS).<br/><br/>"
                "• <b>High Manual Error Rate:</b> Students spend weeks filing invalid applications only to be rejected due to missing mandatory documents or income limits.",
                card_body
            ),
            Paragraph(
                "• <b>Automated Evaluation Engine:</b> Single consolidated interface taking student credentials and polymorphically evaluating every scheme in milliseconds.<br/><br/>"
                "• <b>Transparent Reasoning & Checklists:</b> Outputs exact eligibility status, specific disqualification reasons, and personalized required document checklists.<br/><br/>"
                "• <b>Multi-Channel Delivery:</b> Fully accessible as an interactive Terminal CLI (per PRD) and an enterprise React 19 Web SPA with embedded REST backend.",
                card_body
            )
        ]
    ]
    t_over = Table(overview_cols, colWidths=[435, 445])
    t_over.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_subtle),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_card_border),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    slides.append(t_over)
    slides.append(Spacer(1, 10))

    # Architecture Highlights bar
    feat_data = [
        [
            Paragraph("<b>Pure Java OOP Core</b><br/>Abstraction, Encapsulation, Inheritance, Polymorphism", card_body),
            Paragraph("<b>Dual File Handling</b><br/>NIO JSON Ingestion & Text Report Dossier Generation", card_body),
            Paragraph("<b>Enterprise Security</b><br/>SHA-256 + 16-byte random salt authentication & CSV audit", card_body),
            Paragraph("<b>100% Test Verified</b><br/>24/24 JUnit 5 tests passing in continuous integration", card_body)
        ]
    ]
    t_feat = Table(feat_data, colWidths=[220, 220, 220, 220])
    t_feat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#e0f2fe")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#bae6fd")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#bae6fd")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    slides.append(t_feat)
    slides.append(PageBreak())

    # =========================================================================
    # SLIDE 3: OOP PILLAR 1 — ABSTRACTION & CONTRACTS
    # =========================================================================
    slides.extend(make_slide_header(
        "OOP Pillar 1: Abstraction & Contract-Driven Design",
        "Hiding Internal Implementation Details Behind Abstract Blueprints and Interfaces",
        "Presenter 1: Priyanshu Gupta",
        "#0369a1"
    ))

    abs_data = [
        [
            Paragraph("<b>1. Abstract Class: <code>Scheme.java</code></b>", card_header),
            Paragraph("<b>2. Interface: <code>ReportWriter.java</code></b>", card_header)
        ],
        [
            Paragraph(
                "• <b>Architectural Purpose:</b> Defines the root contract for all scholarship types. It encapsulates common fields (<code>id</code>, <code>name</code>, <code>type</code>, <code>requiredDocuments</code>) while deferring rule execution to subclasses.<br/><br/>"
                "• <b>Mandated Abstract Methods:</b><br/>"
                "&nbsp;&nbsp;<code>public abstract boolean isEligible(Student student);</code><br/>"
                "&nbsp;&nbsp;<code>public abstract String getCriteriaSummary();</code><br/><br/>"
                "• <b>Why Abstract Class vs. Interface?</b><br/>"
                "All schemes share persistent state (IDs, Names, Document lists) and concrete getters/toString. Java interfaces cannot hold instance variables. An abstract class enables <b>state reuse + strict polymorphism</b>.",
                card_body
            ),
            Paragraph(
                "• <b>Architectural Purpose:</b> Decouples the reporting subsystem from concrete storage devices. The business logic only knows about the contract, not file systems.<br/><br/>"
                "• <b>Interface Definition:</b><br/>"
                "&nbsp;&nbsp;<code>public interface ReportWriter {</code><br/>"
                "&nbsp;&nbsp;&nbsp;&nbsp;<code>void write(Path dest, Student s, List&lt;Scheme&gt; sc)</code><br/>"
                "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<code>throws IOException;</code><br/>"
                "&nbsp;&nbsp;<code>}</code><br/><br/>"
                "• <b>Extensibility Benefit:</b> SchemeSathi currently implements <code>EligibilityReportWriter</code> (text file), but can seamlessly swap to <code>PdfReportWriter</code> or <code>DatabaseReportWriter</code> without modifying calling code.",
                card_body
            )
        ]
    ]
    t_abs = Table(abs_data, colWidths=[440, 440])
    t_abs.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_subtle),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_card_border),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    slides.append(t_abs)
    slides.append(Spacer(1, 8))

    # Code callout box
    code_abs_box = Table([[
        Paragraph(
            "<b>Key Faculty Takeaway:</b> Abstraction in SchemeSathi establishes clean boundaries. The evaluation service never inspects concrete scheme internals; it simply invokes the abstract <code>isEligible()</code> contract.",
            card_body_bold
        )
    ]], colWidths=[880])
    code_abs_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f0fdf4")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#86efac")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    slides.append(code_abs_box)
    slides.append(PageBreak())

    # =========================================================================
    # SLIDE 4: OOP PILLAR 2 — ENCAPSULATION & DEFENSIVE SECURITY
    # =========================================================================
    slides.extend(make_slide_header(
        "OOP Pillar 2: Encapsulation & Defensive Security",
        "Data Hiding, Class Invariants, and Cryptographic Security Bounds",
        "Presenter 1: Priyanshu Gupta",
        "#0369a1"
    ))

    encap_data = [
        [
            Paragraph("<b>Domain Invariant Encapsulation (<code>Student.java</code>)</b>", card_header),
            Paragraph("<b>Cryptographic Security Encapsulation (<code>AuthService.java</code>)</b>", card_header)
        ],
        [
            Paragraph(
                "• <b>Strict <code>private</code> Visibility:</b> All mutable instance variables (<code>marksPercentage</code>, <code>annualFamilyIncome</code>, <code>category</code>) are private.<br/><br/>"
                "• <b>Constructor Validation (Defensive Programming):</b><br/>"
                "&nbsp;&nbsp;Marks must be within <code>[0.0, 100.0]</code>.<br/>"
                "&nbsp;&nbsp;Income must be <code>&gt;= 0.0</code> (no negative financial figures).<br/>"
                "&nbsp;&nbsp;Social category cannot be null or blank.<br/><br/>"
                "• <b>Immutability Principle:</b> State modifications throw explicit <code>IllegalArgumentException</code> before any corrupted object can enter the system runtime.",
                card_body
            ),
            Paragraph(
                "• <b>Zero Plaintext Password Exposure:</b> Passwords are never stored in memory or data files in plaintext.<br/><br/>"
                "• <b>SHA-256 + 16-Byte Cryptographic Salt:</b><br/>"
                "&nbsp;&nbsp;Generates a unique 16-byte random salt per user using <code>java.security.SecureRandom</code>.<br/>"
                "&nbsp;&nbsp;Hashes password + salt via <code>MessageDigest.getInstance(\"SHA-256\")</code>.<br/>"
                "&nbsp;&nbsp;Prevents rainbow table attacks and dictionary exploits.<br/><br/>"
                "• <b>Session Token Isolation:</b> Generates cryptographically isolated Bearer tokens (<code>STOK-...</code>) stored in concurrent thread-safe maps.",
                card_body
            )
        ]
    ]
    t_encap = Table(encap_data, colWidths=[440, 440])
    t_encap.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_subtle),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_card_border),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    slides.append(t_encap)
    slides.append(Spacer(1, 8))

    # Code representation snippet
    code_encap = Table([[
        Paragraph(
            "<code>// AuthService.java - Cryptographically Encapsulated Hashing\n"
            "private String hashPassword(String password, String salt) {\n"
            "    MessageDigest md = MessageDigest.getInstance(\"SHA-256\");\n"
            "    md.update(salt.getBytes(StandardCharsets.UTF_8));\n"
            "    return HexFormat.of().formatHex(md.digest(password.getBytes(StandardCharsets.UTF_8)));\n"
            "}</code>",
            code_style
        )
    ]], colWidths=[880])
    code_encap.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f1f5f9")),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    slides.append(code_encap)
    slides.append(PageBreak())

    # =========================================================================
    # SLIDE 5: OOP PILLAR 3 — INHERITANCE & SPECIALIZATION
    # =========================================================================
    slides.extend(make_slide_header(
        "OOP Pillar 3: Inheritance & Subclass Specialization",
        "Code Reusability, Constructor Chaining via super(), and Domain Hierarchy",
        "Presenter 1: Priyanshu Gupta",
        "#0369a1"
    ))

    # Class hierarchy table
    inh_data = [
        [
            Paragraph("<b>Class Name</b>", table_header),
            Paragraph("<b>Parent & Inheritance Chain</b>", table_header),
            Paragraph("<b>Specialized Attributes</b>", table_header),
            Paragraph("<b>Eligibility Rule Implementation</b>", table_header)
        ],
        [
            Paragraph("<b><code>Scheme</code></b><br/>(Abstract Base)", table_cell),
            Paragraph("<code>java.lang.Object</code>", table_cell_code),
            Paragraph("<code>id, name, type, requiredDocuments</code>", table_cell_code),
            Paragraph("Defines abstract <code>isEligible(Student)</code> blueprint.", table_cell)
        ],
        [
            Paragraph("<b><code>MeritScheme</code></b>", table_cell),
            Paragraph("<code>extends Scheme</code>", table_cell_code),
            Paragraph("<code>double minimumMarks</code>", table_cell_code),
            Paragraph("Evaluates: <code>student.getMarks() &gt;= this.minimumMarks</code>", table_cell)
        ],
        [
            Paragraph("<b><code>IncomeScheme</code></b>", table_cell),
            Paragraph("<code>extends Scheme</code>", table_cell_code),
            Paragraph("<code>double maximumAnnualIncome</code>", table_cell_code),
            Paragraph("Evaluates: <code>student.getAnnualFamilyIncome() &lt;= this.maxIncome</code>", table_cell)
        ],
        [
            Paragraph("<b><code>CategoryScheme</code></b>", table_cell),
            Paragraph("<code>extends Scheme</code>", table_cell_code),
            Paragraph("<code>List&lt;String&gt; allowedCategories</code>", table_cell_code),
            Paragraph("Evaluates: <code>allowedCategories.contains(student.getCategory())</code>", table_cell)
        ]
    ]
    t_inh = Table(inh_data, colWidths=[140, 160, 240, 340])
    t_inh.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#f8fafc")),
        ('BACKGROUND', (0,3), (-1,3), colors.HexColor("#f8fafc")),
    ]))
    slides.append(t_inh)
    slides.append(Spacer(1, 10))

    # Architecture Card on super()
    chain_data = [
        [
            Paragraph("<b>Constructor Chaining with <code>super(...)</code>:</b>", card_header),
            Paragraph("<b>Eliminating Redundancy:</b>", card_header)
        ],
        [
            Paragraph(
                "<code>public MeritScheme(String id, String name, List&lt;String&gt; docs, double minMarks) {\n"
                "    super(id, name, \"MERIT\", docs); // Reuses parent constructor logic\n"
                "    this.minimumMarks = minMarks;\n"
                "}</code>",
                code_style
            ),
            Paragraph(
                "• Avoids repeating field assignments, null checks, and defensive copies across each subclass.<br/>"
                "• Guarantees that any state invariant enforced by <code>Scheme</code> is universally applied to all derived scholarships.<br/>"
                "• Keeps subclass code strictly focused on criteria-specific business logic.",
                card_body
            )
        ]
    ]
    t_chain = Table(chain_data, colWidths=[440, 440])
    t_chain.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_subtle),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_card_border),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    slides.append(t_chain)
    slides.append(PageBreak())

    # =========================================================================
    # SLIDE 6: OOP PILLAR 4 — POLYMORPHISM & DYNAMIC METHOD DISPATCH
    # =========================================================================
    slides.extend(make_slide_header(
        "OOP Pillar 4: Polymorphism & Dynamic Method Dispatch",
        "Runtime Binding and the Open/Closed Principle (OCP)",
        "Presenter 1: Priyanshu Gupta",
        "#0369a1"
    ))

    poly_code_text = (
        "// EligibilityService.java — Polymorphic Evaluation Engine\n"
        "public List<Scheme> findEligible(Student student, List<Scheme> schemes) {\n"
        "    List<Scheme> eligible = new ArrayList<>();\n"
        "    for (Scheme scheme : schemes) {\n"
        "        // RUNTIME POLYMORPHISM (Dynamic Method Dispatch):\n"
        "        // JVM inspects the exact object instance at runtime\n"
        "        // and dispatches to MeritScheme, IncomeScheme, or CategoryScheme.\n"
        "        if (scheme.isEligible(student)) {\n"
        "            eligible.add(scheme);\n"
        "        }\n"
        "    }\n"
        "    return eligible;\n"
        "}"
    )

    poly_data = [
        [
            Paragraph("<b>Source Code: Dynamic Method Dispatch in Action</b>", card_header),
            Paragraph("<b>Architectural & Academic Significance</b>", card_header)
        ],
        [
            Paragraph(f"<pre>{poly_code_text}</pre>", code_style_white),
            Paragraph(
                "• <b>What is Dynamic Dispatch?</b><br/>"
                "The compile-time reference is generic (<code>Scheme</code>), but at runtime the Java Virtual Machine dynamically resolves the virtual method table (vtable) to execute the subclass's overridden <code>isEligible()</code> method.<br/><br/>"
                "• <b>Adherence to Open/Closed Principle (OCP):</b><br/>"
                "Software entities should be <i>open for extension, closed for modification</i>. Adding a brand-new <code>SportsQuotaScheme</code> or <code>DisabilityScheme</code> requires <b>zero edits</b> to <code>EligibilityService</code>!<br/><br/>"
                "• <b>Zero Code Smells:</b><br/>"
                "Eliminates clumsy <code>if (s instanceof MeritScheme)</code> or type-casting ladders.",
                card_body
            )
        ]
    ]
    t_poly = Table(poly_data, colWidths=[450, 430])
    t_poly.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), c_bg_subtle),
        ('BACKGROUND', (0,1), (0,1), c_primary),
        ('BACKGROUND', (1,0), (1,1), c_bg_subtle),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_card_border),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    slides.append(t_poly)
    slides.append(Spacer(1, 8))

    handoff_1 = Table([[
        Paragraph("<b>Handoff to Presenter 2:</b> <i>\"Now, my colleague will delve into the critical technical centerpiece of our project — Java File Handling Architecture, JSON Ingestion, and CSV Streaming.\"</i>", card_body_bold)
    ]], colWidths=[880])
    handoff_1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#eff6ff")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#bfdbfe")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    slides.append(handoff_1)
    slides.append(PageBreak())

    # =========================================================================
    # SLIDE 7: SPECIAL FOCUS — JAVA FILE HANDLING (INPUT INGESTION)
    # =========================================================================
    slides.extend(make_slide_header(
        "Special Focus: Java File Handling Architecture (Input)",
        "Robust File I/O, Defensive Path Validation, and JSON Schema Deserialization",
        "Presenter 2: Backend & File Lead",
        "#0d9488"
    ))

    file_in_code = (
        "// SchemeLoader.java — Defensive Java NIO File Reading\n"
        "public List<Scheme> load(Path path) throws IOException {\n"
        "    if (path == null) throw new IllegalArgumentException(\"Path cannot be null.\");\n"
        "    if (!Files.exists(path))\n"
        "        throw new IOException(\"Rules file does not exist: \" + path.toAbsolutePath());\n"
        "    if (!Files.isRegularFile(path))\n"
        "        throw new IOException(\"Rules file is not a regular file: \" + path.toAbsolutePath());\n"
        "    if (!Files.isReadable(path))\n"
        "        throw new IOException(\"Rules file is not readable: \" + path.toAbsolutePath());\n\n"
        "    // UTF-8 NIO Stream Ingestion\n"
        "    String jsonContent = Files.readString(path, StandardCharsets.UTF_8).trim();\n"
        "    if (jsonContent.isEmpty()) throw new IOException(\"Rules file is empty\");\n"
        "    return parseJson(jsonContent);\n"
        "}"
    )

    file_in_data = [
        [
            Paragraph("<b>Java NIO <code>SchemeLoader.java</code> Implementation</b>", card_header),
            Paragraph("<b>Defensive File-Handling Principles Applied</b>", card_header)
        ],
        [
            Paragraph(f"<pre>{file_in_code}</pre>", code_style),
            Paragraph(
                "• <b>Modern Java NIO.2 API (<code>java.nio.file</code>):</b><br/>"
                "Uses immutable <code>Path</code> and <code>Files</code> utility methods instead of legacy <code>java.io.File</code> for cross-platform file system compatibility.<br/><br/>"
                "• <b>3-Tier Pre-Flight File Checks:</b><br/>"
                "&nbsp;&nbsp;1. <code>Files.exists()</code>: Checks file presence.<br/>"
                "&nbsp;&nbsp;2. <code>Files.isRegularFile()</code>: Protects against directory paths or corrupt symlinks.<br/>"
                "&nbsp;&nbsp;3. <code>Files.isReadable()</code>: Prevents OS permission denials.<br/><br/>"
                "• <b>Explicit Character Encoding (<code>UTF-8</code>):</b><br/>"
                "Mandates <code>StandardCharsets.UTF_8</code> to eliminate platform-dependent encoding bugs on Windows vs. Linux servers.<br/><br/>"
                "• <b>Schema Validation & Duplicate Detection:</b><br/>"
                "Deserializes into intermediate <code>SchemeRule</code> records, rejects malformed schemas, and verifies uniqueness via <code>Set&lt;String&gt; seenIds</code>.",
                card_body
            )
        ]
    ]
    t_file_in = Table(file_in_data, colWidths=[450, 430])
    t_file_in.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_subtle),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_card_border),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    slides.append(t_file_in)
    slides.append(Spacer(1, 6))

    file_badge = Table([[
        Paragraph("<b>Academic Defense Note:</b> Unlike naive projects that crash with unhandled <code>FileNotFoundException</code>, SchemeSathi defensively catches, wraps, and reports actionable error diagnostics.", card_body_bold)
    ]], colWidths=[880])
    file_badge.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#ccfbf1")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#99f6e4")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    slides.append(file_badge)
    slides.append(PageBreak())

    # =========================================================================
    # SLIDE 8: SPECIAL FOCUS — FILE HANDLING (DOSSIER & CSV EXPORT)
    # =========================================================================
    slides.extend(make_slide_header(
        "Special Focus: Java File Handling (Dossiers & CSV Export)",
        "Deterministic File Writing, Directory Creation, and RFC-4180 CSV Streaming",
        "Presenter 2: Backend & File Lead",
        "#0d9488"
    ))

    file_out_code = (
        "// EligibilityReportWriter.java — Safe Disk Dossier Writing\n"
        "Path parent = destination.getParent();\n"
        "if (parent != null && !Files.exists(parent)) {\n"
        "    Files.createDirectories(parent); // Auto-creates 'output/' dir\n"
        "}\n"
        "Files.writeString(\n"
        "    destination,\n"
        "    report.toString(),\n"
        "    StandardCharsets.UTF_8,\n"
        "    StandardOpenOption.CREATE,\n"
        "    StandardOpenOption.TRUNCATE_EXISTING,\n"
        "    StandardOpenOption.WRITE\n"
        ");"
    )

    csv_code = (
        "// AuthService.java — RFC-4180 Compliant CSV Generation\n"
        "StringBuilder sb = new StringBuilder();\n"
        "sb.append('\\ufeff'); // UTF-8 BOM for Microsoft Excel!\n"
        "sb.append(\"Log ID,Username,Email,Role,Timestamp,IP,Status\\r\\n\");\n"
        "for (LoginRecord r : records) {\n"
        "    sb.append(escapeCsv(r.getId())).append(',')\n"
        "      .append(escapeCsv(r.getUsername())).append(',')\n"
        "      .append(escapeCsv(r.getStatus())).append(\"\\r\\n\");\n"
        "}\n"
        "return sb.toString();"
    )

    file_out_data = [
        [
            Paragraph("<b>1. Audit Report Writing (<code>EligibilityReportWriter</code>)</b>", card_header),
            Paragraph("<b>2. RFC-4180 CSV Audit Streaming (<code>AuthService</code>)</b>", card_header)
        ],
        [
            Paragraph(f"<pre>{file_out_code}</pre>", code_style),
            Paragraph(f"<pre>{csv_code}</pre>", code_style)
        ],
        [
            Paragraph(
                "• <b>Automated Directory Provisioning:</b> Invokes <code>Files.createDirectories(parent)</code> so the app never throws <code>NoSuchFileException</code> on fresh machines.<br/>"
                "• <b>Atomic StandardOpenOptions:</b> Uses <code>CREATE</code>, <code>TRUNCATE_EXISTING</code>, and <code>WRITE</code> to ensure clean overwrites without stale byte remnants.",
                card_body
            ),
            Paragraph(
                "• <b>Excel Compatibility:</b> Prepends UTF-8 Byte Order Mark (<code>\\ufeff</code>) to prevent character corruption when opened in Microsoft Excel.<br/>"
                "• <b>CSV Injection & Quoting Escaping:</b> Custom <code>escapeCsv()</code> wraps commas and doubles quotation marks (<code>\"\"</code>) per RFC-4180.",
                card_body
            )
        ]
    ]
    t_file_out = Table(file_out_data, colWidths=[440, 440])
    t_file_out.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_subtle),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_card_border),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    slides.append(t_file_out)
    slides.append(PageBreak())

    # =========================================================================
    # SLIDE 9: BACKEND ARCHITECTURE & REST API MICROSERVER
    # =========================================================================
    slides.extend(make_slide_header(
        "Backend Architecture & REST Microserver Layer",
        "Lightweight Embedded HttpServer, Clean Separation of Concerns, and Endpoints",
        "Presenter 2: Backend & File Lead",
        "#0d9488"
    ))

    # Architecture layered map
    layer_data = [
        [
            Paragraph("<b>Layer / Package</b>", table_header),
            Paragraph("<b>Primary Classes</b>", table_header),
            Paragraph("<b>Responsibilities & Engineering Value</b>", table_header)
        ],
        [
            Paragraph("<b>Domain Model</b>", table_cell),
            Paragraph("<code>Student, Scheme, MeritScheme, IncomeScheme, CategoryScheme</code>", table_cell_code),
            Paragraph("Core business models, inheritance hierarchies, and polymorphic contracts.", table_cell)
        ],
        [
            Paragraph("<b>Service Layer</b>", table_cell),
            Paragraph("<code>EligibilityService</code>", table_cell_code),
            Paragraph("Polymorphic scheme matching and disqualification criteria breakdowns.", table_cell)
        ],
        [
            Paragraph("<b>Persistence & I/O</b>", table_cell),
            Paragraph("<code>SchemeLoader, ReportWriter, EligibilityReportWriter</code>", table_cell_code),
            Paragraph("Java NIO JSON ingestion, rule parsing, and formatted dossier file output.", table_cell)
        ],
        [
            Paragraph("<b>Security & Auth</b>", table_cell),
            Paragraph("<code>AuthService, User, LoginRecord</code>", table_cell_code),
            Paragraph("SHA-256 + 16B salt hashing, session token store, and CSV audit logs.", table_cell)
        ],
        [
            Paragraph("<b>REST Server</b>", table_cell),
            Paragraph("<code>ApiServer, EvaluateHandler, ReportHandler, AdminCsvHandler</code>", table_cell_code),
            Paragraph("Embedded Java <code>HttpServer</code> on port 8080 with CORS headers & JSON responses.", table_cell)
        ]
    ]
    t_layer = Table(layer_data, colWidths=[120, 280, 480])
    t_layer.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#f8fafc")),
        ('BACKGROUND', (0,3), (-1,3), colors.HexColor("#f8fafc")),
        ('BACKGROUND', (0,5), (-1,5), colors.HexColor("#f8fafc")),
    ]))
    slides.append(t_layer)
    slides.append(Spacer(1, 8))

    handoff_2 = Table([[
        Paragraph("<b>Handoff to Presenter 3:</b> <i>\"Next, my colleague will demonstrate the modern React 19 Frontend UI/UX, system integration, automated test verification, and faculty viva preparation.\"</i>", card_body_bold)
    ]], colWidths=[880])
    handoff_2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#fef3c7")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#fde68a")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    slides.append(handoff_2)
    slides.append(PageBreak())

    # =========================================================================
    # SLIDE 10: FRONTEND UI/UX DESIGN SYSTEM
    # =========================================================================
    slides.extend(make_slide_header(
        "Frontend UI/UX Design System & Interface",
        "Modern React 19 SPA, Clean Typography, Dual Themes, and Admin Portal",
        "Presenter 3: UI/UX & Integration Lead",
        "#d97706"
    ))

    ui_data = [
        [
            Paragraph("<b>Modern UI/UX Ergonomics</b>", card_header),
            Paragraph("<b>Enterprise Admin & System Features</b>", card_header)
        ],
        [
            Paragraph(
                "• <b>Dual Theme Design System (Dark & Light Mode):</b><br/>"
                "Engineered with semantic CSS Custom Properties (<code>--bg-main</code>, <code>--text-primary</code>, <code>--accent-cyan</code>) for instant, seamless theme transitions.<br/><br/>"
                "• <b>1-Click Evaluation Demographic Presets:</b><br/>"
                "Interactive presets allow instant evaluation of realistic student archetypes (<i>High Merit 92%, Need-Based ₹2.2L, OBC Candidate, SC/ST Special, EWS Scholar</i>).<br/><br/>"
                "• <b>Clean, Uncluttered Visual Focus:</b><br/>"
                "Refined layout with background animation removed, ensuring maximum visual accessibility, fast render performance, and zero cognitive distraction for evaluators.",
                card_body
            ),
            Paragraph(
                "• <b>Dedicated Administrator Portal (<code>/admin</code>):</b><br/>"
                "Isolated administrative route with real-time audit logs, tracking login timestamps, user roles, IP addresses, and authentication outcomes.<br/><br/>"
                "• <b>1-Click CSV Audit Trail Download:</b><br/>"
                "Directly streams the generated CSV file from the Java backend for institutional compliance and record keeping.<br/><br/>"
                "• <b>Instant Dossier Generation:</b><br/>"
                "Students can click <i>'Download Audit Dossier'</i> to trigger <code>ReportHandler</code> and download the formatted plain-text report onto their local machine.",
                card_body
            )
        ]
    ]
    t_ui = Table(ui_data, colWidths=[440, 440])
    t_ui.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_subtle),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_card_border),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    slides.append(t_ui)
    slides.append(PageBreak())

    # =========================================================================
    # SLIDE 11: TEAM WORK DIVISION & DEFENSE SCHEDULE
    # =========================================================================
    slides.extend(make_slide_header(
        "Team Work Division & Defense Presentation Plan",
        "Clear Responsibility Mapping, Presentation Timing, and Speaker Hand-Offs",
        "Presenter 3: UI/UX & Integration Lead",
        "#d97706"
    ))

    division_data = [
        [
            Paragraph("<b>Member & Role</b>", table_header),
            Paragraph("<b>Assigned Presentation Scope</b>", table_header),
            Paragraph("<b>Key Slide Range & Speaking Time</b>", table_header),
            Paragraph("<b>Defense Hand-Off Responsibilities</b>", table_header)
        ],
        [
            Paragraph("<b>Member 1: Priyanshu Gupta</b><br/><i>System Architect & OOP Core Lead</i>", table_cell),
            Paragraph(
                "• Project Vision & Problem Solved<br/>"
                "• 4 Fundamental OOP Pillars (Abstraction, Encapsulation, Inheritance, Polymorphism)<br/>"
                "• Dynamic Method Dispatch Proof",
                table_cell
            ),
            Paragraph("<b>Slides 1 – 6</b><br/>0:00 – 5:00 min (5 Mins)", table_cell_code),
            Paragraph("Sets up architectural context; introduces domain problem and passes baton to Member 2.", table_cell)
        ],
        [
            Paragraph("<b>Member 2: Team Member 2</b><br/><i>Backend & File-Handling Lead</i>", table_cell),
            Paragraph(
                "• <b>Special Focus: Java File Handling</b><br/>"
                "• NIO <code>SchemeLoader</code> JSON Ingestion<br/>"
                "• Dossier Report Writing to Disk<br/>"
                "• CSV Log Streaming & REST Microserver",
                table_cell
            ),
            Paragraph("<b>Slides 7 – 9</b><br/>5:00 – 10:00 min (5 Mins)", table_cell_code),
            Paragraph("Explains file I/O safety, error handling, try-with-resources; passes baton to Member 3.", table_cell)
        ],
        [
            Paragraph("<b>Member 3: Team Member 3</b><br/><i>UI/UX & Integration Lead</i>", table_cell),
            Paragraph(
                "• React 19 Frontend UI/UX Design<br/>"
                "• Dual-Theme Accessibility System<br/>"
                "• 24 JUnit 5 Automated Tests<br/>"
                "• Cloud Deployment & Viva Defense",
                table_cell
            ),
            Paragraph("<b>Slides 10 – 12</b><br/>10:00 – 15:00 min (5 Mins)", table_cell_code),
            Paragraph("Demonstrates end-to-end integration and opens the floor for faculty viva questions.", table_cell)
        ]
    ]
    t_div = Table(division_data, colWidths=[180, 280, 160, 260])
    t_div.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#f8fafc")),
        ('BACKGROUND', (0,3), (-1,3), colors.HexColor("#f8fafc")),
    ]))
    slides.append(t_div)
    slides.append(PageBreak())

    # =========================================================================
    # SLIDE 12: TESTING, VERIFICATION & FACULTY VIVA Q&A
    # =========================================================================
    slides.extend(make_slide_header(
        "Verification Suite & Faculty Viva Defense Q&A",
        "24 JUnit 5 Automated Tests & Top Faculty Defense Questions with Model Answers",
        "All Team Members (Coordinated Defense)",
        "#0284c7"
    ))

    test_box = Table([[
        Paragraph(
            "<b>Automated Test Suite Status:</b> <font color='#16a34a'><b>✓ 24 / 24 Tests Passing (100% Success)</b></font> &nbsp;|&nbsp; "
            "<code>StudentTest</code> (9) &nbsp;•&nbsp; <code>SchemeTest</code> (3) &nbsp;•&nbsp; <code>EligibilityServiceTest</code> (2) &nbsp;•&nbsp; <code>SchemeLoaderTest</code> (3) &nbsp;•&nbsp; <code>EligibilityReportWriterTest</code> (2) &nbsp;•&nbsp; <code>AuthServiceTest</code> (5)",
            card_body_bold
        )
    ]], colWidths=[880])
    test_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f0fdf4")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#86efac")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    slides.append(test_box)
    slides.append(Spacer(1, 6))

    viva_data = [
        [
            Paragraph("<b>Faculty Viva Question</b>", table_header),
            Paragraph("<b>Bulletproof Model Answer (Defended by Assigned Member)</b>", table_header)
        ],
        [
            Paragraph("<b>Q1: Why use an abstract class instead of an interface for <code>Scheme</code>?</b>", table_cell),
            Paragraph("<i>(Presenter 1)</i> All schemes share common state variables (<code>id, name, requiredDocuments</code>) and shared getters. Interfaces cannot hold instance state. An abstract class maximizes code reuse while guaranteeing mandatory polymorphic behavior via abstract <code>isEligible()</code>.", table_cell)
        ],
        [
            Paragraph("<b>Q2: Where exactly does dynamic method dispatch occur?</b>", table_cell),
            Paragraph("<i>(Presenter 1)</i> In <code>EligibilityService.findEligible()</code> inside the loop <code>scheme.isEligible(student)</code>. The JVM resolves the concrete implementation (<code>MeritScheme</code>, <code>IncomeScheme</code>, or <code>CategoryScheme</code>) at runtime via the vtable.", table_cell)
        ],
        [
            Paragraph("<b>Q3: How does file handling prevent application crashes on invalid input?</b>", table_cell),
            Paragraph("<i>(Presenter 2)</i> <code>SchemeLoader</code> performs 3-tier pre-flight checks (<code>Files.exists</code>, <code>isRegularFile</code>, <code>isReadable</code>) and wraps parsing exceptions into detailed <code>IOException</code>. <code>EligibilityReportWriter</code> auto-creates missing parent directories.", table_cell)
        ],
        [
            Paragraph("<b>Q4: How are passwords protected against dictionary and rainbow table attacks?</b>", table_cell),
            Paragraph("<i>(Presenter 2)</i> We use <code>java.security.SecureRandom</code> to generate a cryptographically secure 16-byte random salt per user. Passwords are never stored in plaintext; only the SHA-256 hashed digest is persisted.", table_cell)
        ],
        [
            Paragraph("<b>Q5: How does the client communicate with the Java server?</b>", table_cell),
            Paragraph("<i>(Presenter 3)</i> Through an embedded lightweight Java <code>HttpServer</code> listening on port 8080. It exposes REST endpoints with CORS headers (<code>Access-Control-Allow-Origin: *</code>) exchanging JSON payloads with the React 19 SPA.", table_cell)
        ]
    ]
    t_viva = Table(viva_data, colWidths=[280, 600])
    t_viva.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#f8fafc")),
        ('BACKGROUND', (0,3), (-1,3), colors.HexColor("#f8fafc")),
        ('BACKGROUND', (0,5), (-1,5), colors.HexColor("#f8fafc")),
    ]))
    slides.append(t_viva)

    doc.build(slides, canvasmaker=PresentationCanvas)
    print(f"[SUCCESS] Presentation PDF generated: {filename}")

if __name__ == "__main__":
    out_pdf = "SchemeSathi_Faculty_Presentation.pdf"
    if len(sys.argv) > 1:
        out_pdf = sys.argv[1]
    create_presentation_pdf(out_pdf)
