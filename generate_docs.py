"""
generate_docs.py
-----------------
Generates all 8 phase documentation folders with professional branded PDFs
for the Rising Waters - Flood Management System project.
Structure exactly matches the reference AI-ML_Skill_Wallet- repository.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import KeepTogether

# ── Brand Colours ──────────────────────────────────────────────────────────────
NAVY      = colors.HexColor("#050d2d")
TEAL      = colors.HexColor("#00d4ff")
BLUE      = colors.HexColor("#1a4480")
WHITE     = colors.Color(1, 1, 1)
LIGHT_BG  = colors.HexColor("#e8f4fd")
DANGER    = colors.HexColor("#e63946")
SUCCESS   = colors.HexColor("#06d6a0")
GRAY      = colors.HexColor("#6c757d")
DARK_TEXT = colors.HexColor("#0d1b2a")

W, H = A4   # 595.27 x 841.89 pts

# ── Style Factory ──────────────────────────────────────────────────────────────
def make_styles():
    base = getSampleStyleSheet()

    styles = {}

    styles["title"] = ParagraphStyle(
        "title", fontSize=26, fontName="Helvetica-Bold",
        textColor=WHITE, alignment=TA_CENTER, spaceAfter=4,
        leading=32
    )
    styles["subtitle"] = ParagraphStyle(
        "subtitle", fontSize=13, fontName="Helvetica",
        textColor=TEAL, alignment=TA_CENTER, spaceAfter=6
    )
    styles["badge"] = ParagraphStyle(
        "badge", fontSize=9, fontName="Helvetica-Bold",
        textColor=NAVY, alignment=TA_CENTER
    )
    styles["section"] = ParagraphStyle(
        "section", fontSize=14, fontName="Helvetica-Bold",
        textColor=TEAL, spaceBefore=18, spaceAfter=6
    )
    styles["body"] = ParagraphStyle(
        "body", fontSize=10, fontName="Helvetica",
        textColor=DARK_TEXT, leading=16, spaceAfter=8,
        alignment=TA_JUSTIFY
    )
    styles["bullet"] = ParagraphStyle(
        "bullet", fontSize=10, fontName="Helvetica",
        textColor=DARK_TEXT, leading=15, leftIndent=20,
        spaceAfter=4, bulletIndent=8
    )
    styles["table_header"] = ParagraphStyle(
        "table_header", fontSize=9, fontName="Helvetica-Bold",
        textColor=WHITE, alignment=TA_CENTER
    )
    styles["table_cell"] = ParagraphStyle(
        "table_cell", fontSize=9, fontName="Helvetica",
        textColor=DARK_TEXT
    )
    styles["footer_text"] = ParagraphStyle(
        "footer_text", fontSize=8, fontName="Helvetica",
        textColor=GRAY, alignment=TA_CENTER
    )
    styles["highlight"] = ParagraphStyle(
        "highlight", fontSize=11, fontName="Helvetica-Bold",
        textColor=NAVY, alignment=TA_CENTER
    )
    return styles

# ── Header Block ───────────────────────────────────────────────────────────────
def header_block(styles, doc_title, phase_num, phase_name):
    """Returns a header Table acting as a branded banner."""
    title_para   = Paragraph(f"Rising Waters", styles["title"])
    subtitle     = Paragraph("Flood Management System &mdash; AI/ML Project", styles["subtitle"])
    doc_title_p  = Paragraph(doc_title, ParagraphStyle(
        "dtp", fontSize=16, fontName="Helvetica-Bold",
        textColor=WHITE, alignment=TA_CENTER, spaceAfter=2
    ))
    phase_label  = Paragraph(
        f"Phase {phase_num}: {phase_name}",
        ParagraphStyle("pl", fontSize=10, fontName="Helvetica",
                       textColor=TEAL, alignment=TA_CENTER)
    )

    header_content = [title_para, Spacer(1, 4), subtitle,
                      Spacer(1, 6), doc_title_p, Spacer(1, 4), phase_label]

    tbl = Table([[header_content]], colWidths=[W - 4*cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("TOPPADDING",    (0, 0), (-1, -1), 22),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 22),
        ("LEFTPADDING",   (0, 0), (-1, -1), 20),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 20),
        ("BOX", (0, 0), (-1, -1), 2, TEAL),
    ]))
    return tbl

# ── Badge Row ─────────────────────────────────────────────────────────────────
def badge_row(styles):
    badges = [
        ("IBM Cloud", "#1261FE"),
        ("XGBoost 96.55%", "#FF6600"),
        ("Skill Wallet", "#00C853"),
        ("AI/ML Track", "#7C4DFF"),
    ]
    cells = []
    for label, hex_c in badges:
        bg = colors.HexColor(hex_c)
        p  = Paragraph(label, styles["badge"])
        t  = Table([[p]], colWidths=[3.2*cm])
        t.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,-1), bg),
            ("TOPPADDING",    (0,0),(-1,-1), 5),
            ("BOTTOMPADDING", (0,0),(-1,-1), 5),
            ("LEFTPADDING",   (0,0),(-1,-1), 6),
            ("RIGHTPADDING",  (0,0),(-1,-1), 6),
            ("ROUNDEDCORNERS",(0,0),(-1,-1), [4,4,4,4]),
        ]))
        cells.append(t)

    row = Table([cells], colWidths=[3.6*cm]*4, hAlign="CENTER")
    row.setStyle(TableStyle([
        ("ALIGN", (0,0),(-1,-1), "CENTER"),
        ("VALIGN",(0,0),(-1,-1), "MIDDLE"),
        ("LEFTPADDING",  (0,0),(-1,-1), 6),
        ("RIGHTPADDING", (0,0),(-1,-1), 6),
    ]))
    return row

# ── Divider ───────────────────────────────────────────────────────────────────
def divider():
    return HRFlowable(width="100%", thickness=1.5, color=TEAL,
                      spaceAfter=10, spaceBefore=10)

# ── Info Table (2-column key/value) ───────────────────────────────────────────
def info_table(data, styles, col_widths=None):
    if col_widths is None:
        col_widths = [5*cm, 10*cm]
    rows = []
    for k, v in data:
        rows.append([
            Paragraph(f"<b>{k}</b>", styles["table_cell"]),
            Paragraph(v, styles["table_cell"])
        ])
    tbl = Table(rows, colWidths=col_widths)
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(0,-1), LIGHT_BG),
        ("GRID",          (0,0),(-1,-1), 0.5, colors.HexColor("#cce3f5")),
        ("TOPPADDING",    (0,0),(-1,-1), 6),
        ("BOTTOMPADDING", (0,0),(-1,-1), 6),
        ("LEFTPADDING",   (0,0),(-1,-1), 8),
        ("RIGHTPADDING",  (0,0),(-1,-1), 8),
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
    ]))
    return tbl

# ── Section Heading ───────────────────────────────────────────────────────────
def sh(text, styles):
    return Paragraph(text, styles["section"])

# ── Body Text ─────────────────────────────────────────────────────────────────
def bt(text, styles):
    return Paragraph(text, styles["body"])

# ── Bullet ────────────────────────────────────────────────────────────────────
def bl(text, styles):
    return Paragraph(f"&#x2022; &nbsp; {text}", styles["bullet"])

# ── Footer on every page ──────────────────────────────────────────────────────
def add_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, W, 28, fill=1, stroke=0)
    canvas.setFillColor(TEAL)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawCentredString(
        W/2, 10,
        f"Rising Waters — Flood Management System  |  AI/ML Skill Wallet Project  |  Page {doc.page}"
    )
    canvas.restoreState()

# ── PDF Builder ───────────────────────────────────────────────────────────────
def build_pdf(path, content_fn):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    doc = SimpleDocTemplate(
        path, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=1.5*cm, bottomMargin=2*cm
    )
    styles = make_styles()
    story  = content_fn(styles)
    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)
    print(f"  Created: {path}")

# ==============================================================================
# PHASE 1 — Brainstorming & Ideation
# ==============================================================================
BASE = "docs"

def p1_brainstorming(styles):
    return [
        header_block(styles, "Brainstorming &amp; Idea Prioritization", "1", "Brainstorming &amp; Ideation"),
        Spacer(1, 12), badge_row(styles), Spacer(1, 14), divider(),

        sh("1. Problem Domain", styles),
        bt("Flooding is one of the most devastating natural disasters globally, impacting millions of lives every year. "
           "The absence of timely and accurate early-warning systems significantly amplifies the damage caused by floods. "
           "Traditional forecasting methods lack real-time intelligence and predictive accuracy.", styles),

        sh("2. Brainstorming Ideas Generated", styles),
        bt("The team conducted an ideation session using the Design Thinking framework. The following ideas were generated:", styles),
        bl("Real-time flood sensor network with IoT integration", styles),
        bl("Satellite imagery analysis using computer vision", styles),
        bl("<b>ML-based flood prediction using meteorological data</b> (SELECTED)", styles),
        bl("Social media monitoring for early community alerts", styles),
        bl("Hydrological model simulation platform", styles),
        bl("Mobile app with location-based flood risk alerts", styles),
        Spacer(1, 10),

        sh("3. Idea Prioritization Matrix", styles),
        Table(
            [
                [Paragraph("<b>Idea</b>", styles["table_header"]),
                 Paragraph("<b>Feasibility</b>", styles["table_header"]),
                 Paragraph("<b>Impact</b>", styles["table_header"]),
                 Paragraph("<b>Score</b>", styles["table_header"]),
                 Paragraph("<b>Selected</b>", styles["table_header"])],
                ["ML Flood Prediction", "High", "Very High", "9.5/10", "YES"],
                ["IoT Sensor Network", "Medium", "High", "7.0/10", "No"],
                ["Satellite Imagery CV", "Low", "Very High", "6.0/10", "No"],
                ["Social Media Monitor", "High", "Medium", "6.5/10", "No"],
            ],
            colWidths=[5.5*cm, 3*cm, 3*cm, 2.5*cm, 2.5*cm]
        ).setStyle(TableStyle([
            ("BACKGROUND", (0,0),(-1,0), NAVY),
            ("TEXTCOLOR",  (0,0),(-1,0), WHITE),
            ("BACKGROUND", (0,1),(0,1),  colors.HexColor("#d4f5e9")),
            ("FONTNAME",   (0,0),(-1,0), "Helvetica-Bold"),
            ("FONTSIZE",   (0,0),(-1,-1), 9),
            ("GRID",       (0,0),(-1,-1), 0.5, colors.grey),
            ("ALIGN",      (1,0),(-1,-1), "CENTER"),
            ("TOPPADDING", (0,0),(-1,-1), 7),
            ("BOTTOMPADDING",(0,0),(-1,-1), 7),
        ])),
        Spacer(1,10),

        sh("4. Selected Idea", styles),
        bt("<b>Machine Learning-Powered Flood Prediction System</b> — Using meteorological features (annual rainfall, "
           "seasonal rainfall, cloud visibility, humidity, temperature, and river level) to classify flood vs. no-flood "
           "events using XGBoost. Deployed as a Flask web application on IBM Cloud.", styles),
    ]

def p1_problem(styles):
    return [
        header_block(styles, "Define Problem Statements", "1", "Brainstorming &amp; Ideation"),
        Spacer(1, 12), badge_row(styles), Spacer(1, 14), divider(),

        sh("1. Problem Statement", styles),
        bt("<b>\"How might we provide disaster management authorities and meteorologists with a reliable, "
           "real-time, machine-learning-powered flood prediction system that can accurately classify flood risk "
           "based on meteorological data — enabling timely evacuations and saving lives?\"</b>", styles),

        sh("2. Key Stakeholders", styles),
        info_table([
            ("Meteorologists",      "Need accurate early warnings to issue advisories"),
            ("Disaster Mgmt Teams", "Need flood risk data to mobilise resources"),
            ("Local Authorities",   "Need predictions to trigger evacuation protocols"),
            ("Communities",         "Need timely warnings to evacuate safely"),
            ("Government Bodies",   "Need data for infrastructure planning and policy"),
        ], styles),
        Spacer(1, 10),

        sh("3. Root Cause Analysis", styles),
        bl("Conventional forecasting methods lack ML-powered prediction accuracy", styles),
        bl("Insufficient integration of multiple meteorological parameters", styles),
        bl("No accessible web interface for non-technical disaster management users", styles),
        bl("Delayed information flow between weather services and emergency responders", styles),

        sh("4. Desired Outcome", styles),
        bt("A publicly accessible web application that: (1) accepts 6 meteorological inputs, (2) preprocesses "
           "and scales the data, (3) runs an XGBoost classification model achieving 96.55% accuracy, and "
           "(4) presents a clear Flood Chance or No Flood Chance result with emergency action recommendations.", styles),
    ]

def p1_empathy(styles):
    return [
        header_block(styles, "Empathy Map", "1", "Brainstorming &amp; Ideation"),
        Spacer(1, 12), badge_row(styles), Spacer(1, 14), divider(),

        sh("Primary User: Disaster Management Officer", styles),
        bt("The empathy map below captures the thoughts, feelings, and behaviours of the primary user "
           "of the Rising Waters flood prediction system.", styles),

        Table([
            [Paragraph("<b>THINKS</b>", styles["table_header"]),
             Paragraph("<b>FEELS</b>", styles["table_header"])],
            [Paragraph("\"Will rainfall data be enough to predict flooding accurately?\"\n"
                       "\"Can I trust this model's output for critical decisions?\"\n"
                       "\"How do I explain the system to community leaders?\"", styles["body"]),
             Paragraph("Anxious about false negatives (missed floods)\n"
                       "Relieved when system shows clear All Clear result\n"
                       "Confident when model accuracy data is visible\n"
                       "Overwhelmed by complex meteorological data", styles["body"])],

            [Paragraph("<b>SAYS</b>", styles["table_header"]),
             Paragraph("<b>DOES</b>", styles["table_header"])],
            [Paragraph("\"We need faster predictions before monsoon season\"\n"
                       "\"The system should clearly tell us what action to take\"\n"
                       "\"We need a history log to review past predictions\"", styles["body"]),
             Paragraph("Manually collects rainfall data from weather stations\n"
                       "Enters readings into the prediction form\n"
                       "Shares flood/no-flood result with field teams\n"
                       "Logs predictions to audit trail", styles["body"])],
        ], colWidths=[8.5*cm, 8.5*cm]).setStyle(TableStyle([
            ("BACKGROUND", (0,0),(-1,0), NAVY),
            ("BACKGROUND", (0,2),(-1,2), BLUE),
            ("TEXTCOLOR",  (0,0),(-1,0), WHITE),
            ("TEXTCOLOR",  (0,2),(-1,2), WHITE),
            ("GRID",       (0,0),(-1,-1), 0.8, TEAL),
            ("TOPPADDING", (0,0),(-1,-1), 10),
            ("BOTTOMPADDING",(0,0),(-1,-1), 10),
            ("LEFTPADDING",(0,0),(-1,-1), 10),
            ("VALIGN",     (0,0),(-1,-1), "TOP"),
        ])),
        Spacer(1, 14),

        sh("Pain Points Identified", styles),
        bl("No centralized platform for flood risk prediction from weather inputs", styles),
        bl("Difficulty interpreting raw meteorological data without ML support", styles),
        bl("Slow decision-making due to manual data analysis", styles),
        bl("Lack of emergency response guidance alongside predictions", styles),
    ]

# ==============================================================================
# PHASE 2 — Requirement Analysis
# ==============================================================================
def p2_journey(styles):
    return [
        header_block(styles, "Customer Journey Map", "2", "Requirement Analysis"),
        Spacer(1, 12), badge_row(styles), Spacer(1, 14), divider(),

        sh("User Journey: Disaster Management Officer", styles),
        Table([
            [Paragraph("<b>Stage</b>", styles["table_header"]),
             Paragraph("<b>User Action</b>", styles["table_header"]),
             Paragraph("<b>Touchpoint</b>", styles["table_header"]),
             Paragraph("<b>Emotion</b>", styles["table_header"]),
             Paragraph("<b>Opportunity</b>", styles["table_header"])],
            ["1. Awareness",   "Learns about the flood prediction system",             "News / Training",       "Curious",      "Promote via NDMA channels"],
            ["2. Access",      "Opens Rising Waters web app on browser",               "Home Dashboard",        "Neutral",      "Show live stats on homepage"],
            ["3. Input",       "Enters 6 meteorological readings into the form",       "Predict Page",          "Focused",      "Add field tooltips & examples"],
            ["4. Prediction",  "Submits form and waits for ML model result",           "POST /predict",         "Anxious",      "Show loading indicator"],
            ["5. Flood Result","Views Flood Chance page with red alert banner",        "result_flood.html",     "Alarmed",      "Provide emergency protocol cards"],
            ["6. Safe Result", "Views No Flood Chance page with green safe banner",    "result_noflood.html",   "Relieved",     "Show monitoring recommendations"],
            ["7. History",     "Reviews past predictions in the audit log",            "History Page",          "Confident",    "Add export CSV feature"],
            ["8. Report",      "Shares results with field teams and authorities",      "External channels",     "Empowered",    "Add share/print button"],
        ], colWidths=[2.8*cm, 4*cm, 3.2*cm, 2.2*cm, 4.5*cm]).setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,0), NAVY),
            ("TEXTCOLOR",     (0,0),(-1,0), WHITE),
            ("FONTNAME",      (0,0),(-1,0), "Helvetica-Bold"),
            ("FONTSIZE",      (0,0),(-1,-1), 8),
            ("GRID",          (0,0),(-1,-1), 0.5, colors.grey),
            ("ROWBACKGROUNDS",(0,1),(-1,-1), [colors.white, LIGHT_BG]),
            ("ALIGN",         (0,0),(-1,-1), "CENTER"),
            ("TOPPADDING",    (0,0),(-1,-1), 6),
            ("BOTTOMPADDING", (0,0),(-1,-1), 6),
            ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
        ])),
    ]

def p2_dfd(styles):
    return [
        header_block(styles, "Data Flow Diagram", "2", "Requirement Analysis"),
        Spacer(1, 12), badge_row(styles), Spacer(1, 14), divider(),

        sh("Level 0 — Context Diagram", styles),
        bt("The user provides 6 meteorological inputs. The Rising Waters system processes "
           "them and returns a Flood or No Flood prediction.", styles),
        info_table([
            ("External Entity", "Disaster Management Officer / Meteorologist"),
            ("System",          "Rising Waters Flood Prediction System"),
            ("Input Data",      "annual_rainfall, seasonal_rainfall, cloud_visibility, humidity, temperature, river_level"),
            ("Output Data",     "Binary prediction (Flood / No Flood) + Probability score"),
        ], styles),
        Spacer(1, 12),

        sh("Level 1 — System Data Flow", styles),
        Table([
            [Paragraph("<b>Process</b>", styles["table_header"]),
             Paragraph("<b>Input</b>", styles["table_header"]),
             Paragraph("<b>Output</b>", styles["table_header"]),
             Paragraph("<b>Data Store</b>", styles["table_header"])],
            ["P1: Form Input",      "User values",         "Raw feature dict",         "—"],
            ["P2: Validation",      "Raw feature dict",    "Validated dict / Error",   "—"],
            ["P3: Scaling",         "Validated features",  "Scaled NumPy array",       "scaler.save"],
            ["P4: Prediction",      "Scaled array",        "Label + Probability",      "floods.save"],
            ["P5: Result Routing",  "Label (0/1)",         "Redirect to result page",  "—"],
            ["P6: Logging",         "All values + result", "CSV row appended",         "predictions_log.csv"],
        ], colWidths=[4*cm, 4*cm, 4*cm, 4.5*cm]).setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,0), NAVY),
            ("TEXTCOLOR",     (0,0),(-1,0), WHITE),
            ("FONTNAME",      (0,0),(-1,0), "Helvetica-Bold"),
            ("FONTSIZE",      (0,0),(-1,-1), 9),
            ("GRID",          (0,0),(-1,-1), 0.5, colors.grey),
            ("ROWBACKGROUNDS",(0,1),(-1,-1), [colors.white, LIGHT_BG]),
            ("TOPPADDING",    (0,0),(-1,-1), 7),
            ("BOTTOMPADDING", (0,0),(-1,-1), 7),
            ("ALIGN",         (0,0),(-1,-1), "CENTER"),
        ])),
    ]

def p2_solution_req(styles):
    return [
        header_block(styles, "Solution Requirements", "2", "Requirement Analysis"),
        Spacer(1, 12), badge_row(styles), Spacer(1, 14), divider(),

        sh("Functional Requirements", styles),
        info_table([
            ("FR-01", "System shall accept 6 meteorological inputs via a web form"),
            ("FR-02", "System shall validate all inputs before processing"),
            ("FR-03", "System shall scale inputs using pre-fitted StandardScaler"),
            ("FR-04", "System shall load XGBoost model and return binary classification"),
            ("FR-05", "System shall display dedicated Flood Chance result page (red)"),
            ("FR-06", "System shall display dedicated No Flood Chance result page (green)"),
            ("FR-07", "System shall log every prediction to predictions_log.csv"),
            ("FR-08", "System shall display all past predictions on History page"),
            ("FR-09", "System shall show model accuracy comparison on Dashboard"),
        ], styles),
        Spacer(1, 10),

        sh("Non-Functional Requirements", styles),
        info_table([
            ("NFR-01 Performance",    "Prediction response time < 2 seconds"),
            ("NFR-02 Accuracy",       "XGBoost model test accuracy >= 95%"),
            ("NFR-03 Availability",   "System available 24/7 via IBM Cloud"),
            ("NFR-04 Usability",      "Responsive design, accessible on mobile and desktop"),
            ("NFR-05 Security",       "Session-based result passing, no raw model exposure"),
            ("NFR-06 Scalability",    "Dockerized deployment, horizontal scaling ready"),
            ("NFR-07 Maintainability","Modular code: separate utils, model, templates directories"),
        ], styles),
    ]

def p2_tech_stack(styles):
    return [
        header_block(styles, "Technology Stack", "2", "Requirement Analysis"),
        Spacer(1, 12), badge_row(styles), Spacer(1, 14), divider(),

        sh("Technology Stack Overview", styles),
        Table([
            [Paragraph("<b>Layer</b>", styles["table_header"]),
             Paragraph("<b>Technology</b>", styles["table_header"]),
             Paragraph("<b>Version</b>", styles["table_header"]),
             Paragraph("<b>Purpose</b>", styles["table_header"])],
            ["ML Framework",   "XGBoost",         "1.7+",   "Best model: flood classification"],
            ["ML Support",     "Scikit-learn",     "1.3+",   "Preprocessing, scaler, evaluation"],
            ["Data Processing","Pandas / NumPy",   "2.x",    "Dataset handling and transformation"],
            ["Visualisation",  "Matplotlib/Seaborn","3.7+",  "EDA plots, model comparison charts"],
            ["Backend",        "Python / Flask",   "3.11 / 2.x","Web application framework"],
            ["Templating",     "Jinja2",           "3.x",    "HTML template rendering"],
            ["Frontend",       "HTML5 / CSS3 / JS","ES6",    "Responsive dark-theme UI"],
            ["Model Storage",  "Joblib",           "1.3+",   "Serialize floods.save, scaler.save"],
            ["Deployment",     "IBM Cloud (CF)",   "Latest", "Production web hosting"],
            ["Container",      "Docker",           "24+",    "Containerized deployment"],
            ["Version Control","Git / GitHub",     "Latest", "Source code management"],
        ], colWidths=[3.5*cm, 3.5*cm, 2.5*cm, 7*cm]).setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,0), NAVY),
            ("TEXTCOLOR",     (0,0),(-1,0), WHITE),
            ("FONTNAME",      (0,0),(-1,0), "Helvetica-Bold"),
            ("FONTSIZE",      (0,0),(-1,-1), 9),
            ("GRID",          (0,0),(-1,-1), 0.5, colors.grey),
            ("ROWBACKGROUNDS",(0,1),(-1,-1), [colors.white, LIGHT_BG]),
            ("TOPPADDING",    (0,0),(-1,-1), 7),
            ("BOTTOMPADDING", (0,0),(-1,-1), 7),
            ("ALIGN",         (1,0),(-1,-1), "CENTER"),
        ])),
    ]

# ==============================================================================
# PHASE 3 — Project Design Phase
# ==============================================================================
def p3_fit(styles):
    return [
        header_block(styles, "Problem-Solution Fit", "3", "Project Design Phase"),
        Spacer(1,12), badge_row(styles), Spacer(1,14), divider(),

        sh("Problem vs Solution Mapping", styles),
        Table([
            [Paragraph("<b>Problem</b>", styles["table_header"]),
             Paragraph("<b>Solution Feature</b>", styles["table_header"]),
             Paragraph("<b>Fit</b>", styles["table_header"])],
            ["No real-time flood prediction tool",          "XGBoost ML classifier",                   "STRONG"],
            ["Complex meteorological data analysis",        "StandardScaler + 6-feature input form",    "STRONG"],
            ["No emergency response guidance",              "Flood Result page with 6 action cards",    "STRONG"],
            ["No accessible interface for non-tech users",  "Flask web app with intuitive form UI",     "STRONG"],
            ["No prediction history tracking",              "predictions_log.csv + History page",       "STRONG"],
            ["Lack of cloud accessibility",                 "IBM Cloud deployment via Docker",          "STRONG"],
        ], colWidths=[6.5*cm, 7.5*cm, 2.5*cm]).setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,0), NAVY),
            ("TEXTCOLOR",     (0,0),(-1,0), WHITE),
            ("FONTNAME",      (0,0),(-1,0), "Helvetica-Bold"),
            ("FONTSIZE",      (0,0),(-1,-1), 9),
            ("GRID",          (0,0),(-1,-1), 0.5, colors.grey),
            ("ROWBACKGROUNDS",(0,1),(-1,-1), [colors.white, LIGHT_BG]),
            ("BACKGROUND",    (2,1),(2,-1), colors.HexColor("#d4f5e9")),
            ("ALIGN",         (2,0),(2,-1), "CENTER"),
            ("TOPPADDING",    (0,0),(-1,-1), 8),
            ("BOTTOMPADDING", (0,0),(-1,-1), 8),
        ])),
    ]

def p3_proposed(styles):
    return [
        header_block(styles, "Proposed Solution", "3", "Project Design Phase"),
        Spacer(1,12), badge_row(styles), Spacer(1,14), divider(),

        sh("Solution Overview", styles),
        bt("Rising Waters is a Machine Learning-powered flood prediction system that uses "
           "four classification algorithms (Decision Tree, Random Forest, KNN, XGBoost) trained "
           "on 5,000 meteorological records. The best-performing model — XGBoost at 96.55% accuracy — "
           "is saved as floods.save and deployed within a Flask web application.", styles),

        sh("Key Solution Components", styles),
        bl("<b>Data Layer:</b> 5,000-row synthetic flood dataset with 6 meteorological features", styles),
        bl("<b>ML Layer:</b> 4 algorithms trained, XGBoost selected (96.55% accuracy)", styles),
        bl("<b>Application Layer:</b> Flask routes handling prediction, logging, history", styles),
        bl("<b>Presentation Layer:</b> 6 premium dark-theme HTML pages (Jinja2)", styles),
        bl("<b>Deployment Layer:</b> Docker + IBM Cloud for cloud hosting", styles),
        Spacer(1,10),

        sh("Model Performance Summary", styles),
        Table([
            [Paragraph("<b>Algorithm</b>", styles["table_header"]),
             Paragraph("<b>Accuracy</b>", styles["table_header"]),
             Paragraph("<b>Deployed</b>", styles["table_header"])],
            ["Decision Tree",        "78.17%", "No"],
            ["K-Nearest Neighbours", "80.67%", "No"],
            ["Random Forest",        "82.00%", "No"],
            ["XGBoost",              "96.55%", "YES"],
        ], colWidths=[7*cm, 5*cm, 4.5*cm]).setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,0), NAVY),
            ("TEXTCOLOR",     (0,0),(-1,0), WHITE),
            ("FONTNAME",      (0,0),(-1,0), "Helvetica-Bold"),
            ("BACKGROUND",    (0,4),(-1,4), colors.HexColor("#d4f5e9")),
            ("FONTNAME",      (0,4),(-1,4), "Helvetica-Bold"),
            ("FONTSIZE",      (0,0),(-1,-1), 10),
            ("GRID",          (0,0),(-1,-1), 0.5, colors.grey),
            ("ALIGN",         (1,0),(-1,-1), "CENTER"),
            ("TOPPADDING",    (0,0),(-1,-1), 8),
            ("BOTTOMPADDING", (0,0),(-1,-1), 8),
        ])),
    ]

def p3_architecture(styles):
    return [
        header_block(styles, "Solution Architecture", "3", "Project Design Phase"),
        Spacer(1,12), badge_row(styles), Spacer(1,14), divider(),

        sh("5-Layer System Architecture", styles),
        Table([
            [Paragraph("<b>Layer</b>", styles["table_header"]),
             Paragraph("<b>Components</b>", styles["table_header"]),
             Paragraph("<b>Technology</b>", styles["table_header"])],
            ["1. User Layer",         "Web Browser (Chrome/Firefox)",                        "HTML5 / CSS3 / JS"],
            ["2. Presentation Layer", "Home, Predict, Flood Result, No Flood Result, History", "Jinja2 Templates"],
            ["3. Application Layer",  "Flask Routes, Form Validation, Data Preprocessing",    "Python / Flask"],
            ["4. ML Layer",           "XGBoost Model (floods.save), StandardScaler",          "Scikit-learn / Joblib"],
            ["5. Data Layer",         "flood_dataset.csv, predictions_log.csv",               "Pandas / CSV"],
            ["6. Deployment",         "Docker Container → IBM Cloud Foundry",                 "Docker / IBM CF"],
        ], colWidths=[4.5*cm, 7*cm, 5*cm]).setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,0), NAVY),
            ("TEXTCOLOR",     (0,0),(-1,0), WHITE),
            ("FONTNAME",      (0,0),(-1,0), "Helvetica-Bold"),
            ("FONTSIZE",      (0,0),(-1,-1), 9),
            ("GRID",          (0,0),(-1,-1), 0.5, colors.grey),
            ("ROWBACKGROUNDS",(0,1),(-1,-1), [colors.white, LIGHT_BG]),
            ("TOPPADDING",    (0,0),(-1,-1), 8),
            ("BOTTOMPADDING", (0,0),(-1,-1), 8),
        ])),
        Spacer(1,12),

        sh("Request Flow", styles),
        bt("User Browser  →  Flask /predict (POST)  →  Form Validation  →  StandardScaler  →  "
           "XGBoost Model  →  Prediction Label  →  /result/flood OR /result/noflood  →  "
           "Result HTML Page  →  User", styles),
    ]

# ==============================================================================
# PHASE 4 — Project Planning Phase
# ==============================================================================
def p4_planning(styles):
    return [
        header_block(styles, "Project Planning", "4", "Project Planning Phase"),
        Spacer(1,12), badge_row(styles), Spacer(1,14), divider(),

        sh("Project Timeline (7-Step Lifecycle)", styles),
        Table([
            [Paragraph("<b>Step</b>", styles["table_header"]),
             Paragraph("<b>Activity</b>", styles["table_header"]),
             Paragraph("<b>Duration</b>", styles["table_header"]),
             Paragraph("<b>Deliverable</b>", styles["table_header"]),
             Paragraph("<b>Status</b>", styles["table_header"])],
            ["1","Environment Setup & Dataset Collection",   "Week 1","flood_dataset.csv",              "DONE"],
            ["2","Exploratory Data Analysis",                "Week 1","EDA plots (4 charts)",            "DONE"],
            ["3","Data Preprocessing",                       "Week 2","Cleaned dataset, scaler.save",    "DONE"],
            ["4","Model Building (4 algorithms)",            "Week 2","All models trained",              "DONE"],
            ["5","Best Model Selection (XGBoost)",           "Week 3","floods.save (96.55% acc)",        "DONE"],
            ["6","Flask Web Application",                    "Week 3","6 premium HTML pages",            "DONE"],
            ["7","IBM Cloud Deployment",                     "Week 4","Live URL on IBM Cloud",           "DONE"],
        ], colWidths=[1.5*cm, 6.5*cm, 2.5*cm, 4.5*cm, 1.8*cm]).setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,0), NAVY),
            ("TEXTCOLOR",     (0,0),(-1,0), WHITE),
            ("FONTNAME",      (0,0),(-1,0), "Helvetica-Bold"),
            ("FONTSIZE",      (0,0),(-1,-1), 9),
            ("GRID",          (0,0),(-1,-1), 0.5, colors.grey),
            ("ROWBACKGROUNDS",(0,1),(-1,-1), [colors.white, LIGHT_BG]),
            ("ALIGN",         (0,0),(-1,-1), "CENTER"),
            ("TOPPADDING",    (0,0),(-1,-1), 7),
            ("BOTTOMPADDING", (0,0),(-1,-1), 7),
        ])),
        Spacer(1,12),

        sh("Resource Plan", styles),
        info_table([
            ("Languages",   "Python 3.11"),
            ("Frameworks",  "Flask 2.x, Scikit-learn 1.3, XGBoost 1.7"),
            ("Tools",       "Jupyter Notebook, VS Code, Git, Docker"),
            ("Cloud",       "IBM Cloud Foundry"),
            ("Team Size",   "1 Developer (Full-stack ML + Web)"),
        ], styles),
    ]

# ==============================================================================
# PHASE 5 — Project Development Phase
# ==============================================================================
def p5_code_layout(styles):
    return [
        header_block(styles, "Code-Layout, Readability and Reusability", "5", "Project Development Phase"),
        Spacer(1,12), badge_row(styles), Spacer(1,14), divider(),

        sh("Project Directory Structure", styles),
        bt("The project follows a modular, layered directory structure with separation of concerns:", styles),
        info_table([
            ("app.py",                  "Main Flask controller — routes, session, logging"),
            ("model/train_model.py",    "ML pipeline: preprocessing, training, evaluation, save"),
            ("model/generate_dataset.py","Synthetic dataset generator (5,000 rows)"),
            ("model/floods.save",       "Serialized XGBoost model (joblib)"),
            ("model/scaler.save",       "Fitted StandardScaler (joblib)"),
            ("utils/preprocessing.py",  "Feature names, validation, scaling helper"),
            ("templates/base.html",     "Shared layout (nav, footer, CSS imports)"),
            ("templates/result_flood.html","Dedicated Flood Chance result page"),
            ("templates/result_noflood.html","Dedicated No Flood Chance result page"),
            ("static/css/style.css",    "Premium dark-theme CSS (glassmorphism)"),
        ], styles),
        Spacer(1,10),

        sh("Code Quality Standards", styles),
        bl("All Python files include module-level docstrings with purpose description", styles),
        bl("Functions are single-responsibility, each under 40 lines", styles),
        bl("Constants defined at module level (FEATURE_NAMES, MODEL_PATH)", styles),
        bl("HTML templates extend base.html — zero code duplication", styles),
        bl("CSS uses CSS custom properties (variables) for consistent theming", styles),
        bl("All routes return meaningful HTTP status codes", styles),
    ]

def p5_coding(styles):
    return [
        header_block(styles, "Coding &amp; Solution", "5", "Project Development Phase"),
        Spacer(1,12), badge_row(styles), Spacer(1,14), divider(),

        sh("ML Pipeline Implementation", styles),
        bt("The model training pipeline follows a 7-step process as specified in the project scope:", styles),
        info_table([
            ("Step 1", "Environment Setup — Python, NumPy, Pandas, Scikit-learn, XGBoost, Flask, Joblib"),
            ("Step 2", "Dataset Collection — 5,000 rows, 6 meteorological features, binary target"),
            ("Step 3", "Data Visualisation — 4 EDA charts (distributions, box plots, pairplot, heatmap)"),
            ("Step 4", "Preprocessing — Mean imputation, IQR outlier capping, StandardScaler"),
            ("Step 5", "Model Building — Decision Tree, Random Forest, KNN, XGBoost"),
            ("Step 6", "Best Model Selection — XGBoost (96.55% accuracy), saved as floods.save"),
            ("Step 7", "Flask App — 6 HTML pages, 2 dedicated result pages, prediction history"),
        ], styles, col_widths=[2*cm, 14.5*cm]),
        Spacer(1,10),

        sh("Flask Application Routes", styles),
        info_table([
            ("GET  /",              "Home Dashboard — model stats, prediction counts"),
            ("GET  /predict",       "Input Form — 6 meteorological parameter fields"),
            ("POST /predict",       "Process form → validate → scale → predict → redirect"),
            ("GET  /result/flood",  "Flood Chance Result — red banner, emergency protocol"),
            ("GET  /result/noflood","No Flood Result — green banner, monitoring actions"),
            ("GET  /history",       "Prediction audit log from predictions_log.csv"),
            ("GET  /about",         "Project architecture, model info, use case scenarios"),
        ], styles),
    ]

def p5_features(styles):
    return [
        header_block(styles, "No. of Functional Features Included in the Solution", "5", "Project Development Phase"),
        Spacer(1,12), badge_row(styles), Spacer(1,14), divider(),

        sh("Feature Count Summary", styles),
        Table([
            [Paragraph("<b>Category</b>", styles["table_header"]),
             Paragraph("<b>Feature</b>", styles["table_header"]),
             Paragraph("<b>Status</b>", styles["table_header"])],
            ["ML",      "XGBoost Flood Classifier",              "IMPLEMENTED"],
            ["ML",      "4-Algorithm Comparison (DT/RF/KNN/XGB)","IMPLEMENTED"],
            ["ML",      "StandardScaler Preprocessing",          "IMPLEMENTED"],
            ["ML",      "Model Persistence (joblib)",            "IMPLEMENTED"],
            ["Web App", "Home Dashboard with live stats",        "IMPLEMENTED"],
            ["Web App", "6-field Prediction Input Form",         "IMPLEMENTED"],
            ["Web App", "Dedicated Flood Chance Result Page",    "IMPLEMENTED"],
            ["Web App", "Dedicated No Flood Result Page",        "IMPLEMENTED"],
            ["Web App", "Prediction History Log Page",           "IMPLEMENTED"],
            ["Web App", "About / Architecture Page",             "IMPLEMENTED"],
            ["UI/UX",   "Dark-theme glassmorphism CSS",          "IMPLEMENTED"],
            ["UI/UX",   "Responsive mobile layout",              "IMPLEMENTED"],
            ["DevOps",  "Docker containerization",               "IMPLEMENTED"],
            ["DevOps",  "IBM Cloud deployment config",           "IMPLEMENTED"],
        ], colWidths=[3*cm, 9*cm, 4.5*cm]).setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,0), NAVY),
            ("TEXTCOLOR",     (0,0),(-1,0), WHITE),
            ("FONTNAME",      (0,0),(-1,0), "Helvetica-Bold"),
            ("FONTSIZE",      (0,0),(-1,-1), 9),
            ("GRID",          (0,0),(-1,-1), 0.5, colors.grey),
            ("ROWBACKGROUNDS",(0,1),(-1,-1), [colors.white, LIGHT_BG]),
            ("BACKGROUND",    (2,1),(2,-1), colors.HexColor("#d4f5e9")),
            ("ALIGN",         (2,0),(2,-1), "CENTER"),
            ("TOPPADDING",    (0,0),(-1,-1), 7),
            ("BOTTOMPADDING", (0,0),(-1,-1), 7),
        ])),
        Spacer(1,8),
        bt("<b>Total Features Implemented: 14 functional features across ML, Web App, UI/UX, and DevOps categories.</b>", styles),
    ]

# ==============================================================================
# PHASE 6 — Project Testing
# ==============================================================================
def p6_testing(styles):
    return [
        header_block(styles, "Performance Testing", "6", "Project Testing"),
        Spacer(1,12), badge_row(styles), Spacer(1,14), divider(),

        sh("Model Performance Testing Results", styles),
        Table([
            [Paragraph("<b>Algorithm</b>", styles["table_header"]),
             Paragraph("<b>Accuracy</b>", styles["table_header"]),
             Paragraph("<b>Precision</b>", styles["table_header"]),
             Paragraph("<b>Recall</b>", styles["table_header"]),
             Paragraph("<b>F1-Score</b>", styles["table_header"]),
             Paragraph("<b>Status</b>", styles["table_header"])],
            ["Decision Tree",         "78.17%","0.78","0.78","0.78","Baseline"],
            ["K-Nearest Neighbours",  "80.67%","0.81","0.81","0.80","Good"],
            ["Random Forest",         "82.00%","0.82","0.82","0.82","Better"],
            ["XGBoost (Deployed)",    "96.55%","0.97","0.97","0.96","BEST"],
        ], colWidths=[4.5*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm]).setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,0), NAVY),
            ("TEXTCOLOR",     (0,0),(-1,0), WHITE),
            ("FONTNAME",      (0,0),(-1,0), "Helvetica-Bold"),
            ("BACKGROUND",    (0,4),(-1,4), colors.HexColor("#d4f5e9")),
            ("FONTNAME",      (0,4),(-1,4), "Helvetica-Bold"),
            ("FONTSIZE",      (0,0),(-1,-1), 9),
            ("GRID",          (0,0),(-1,-1), 0.5, colors.grey),
            ("ALIGN",         (1,0),(-1,-1), "CENTER"),
            ("TOPPADDING",    (0,0),(-1,-1), 8),
            ("BOTTOMPADDING", (0,0),(-1,-1), 8),
        ])),
        Spacer(1,12),

        sh("Web Application Testing", styles),
        Table([
            [Paragraph("<b>Test Case</b>", styles["table_header"]),
             Paragraph("<b>Input</b>", styles["table_header"]),
             Paragraph("<b>Expected</b>", styles["table_header"]),
             Paragraph("<b>Result</b>", styles["table_header"])],
            ["TC-01: High Risk",   "Annual RF: 3500, Humidity: 92%",  "Flood result page",    "PASS"],
            ["TC-02: Low Risk",    "Annual RF: 800, Humidity: 55%",   "No Flood result page", "PASS"],
            ["TC-03: Empty Form",  "No inputs submitted",             "Validation error",     "PASS"],
            ["TC-04: Negative Val","river_level: -5",                 "Validation error",     "PASS"],
            ["TC-05: History",     "3 predictions made",              "3 rows in history",    "PASS"],
        ], colWidths=[4*cm, 4.5*cm, 4.5*cm, 3.5*cm]).setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,0), NAVY),
            ("TEXTCOLOR",     (0,0),(-1,0), WHITE),
            ("FONTNAME",      (0,0),(-1,0), "Helvetica-Bold"),
            ("BACKGROUND",    (3,1),(3,-1), colors.HexColor("#d4f5e9")),
            ("FONTSIZE",      (0,0),(-1,-1), 9),
            ("GRID",          (0,0),(-1,-1), 0.5, colors.grey),
            ("ALIGN",         (3,0),(3,-1), "CENTER"),
            ("TOPPADDING",    (0,0),(-1,-1), 7),
            ("BOTTOMPADDING", (0,0),(-1,-1), 7),
        ])),
    ]

# ==============================================================================
# PHASE 7 — Project Documentation
# ==============================================================================
def p7_executable(styles):
    return [
        header_block(styles, "Project Executable Files", "7", "Project Documentation"),
        Spacer(1,12), badge_row(styles), Spacer(1,14), divider(),

        sh("How to Run the Project", styles),
        bt("Follow the steps below to set up and run the Rising Waters flood prediction application:", styles),

        sh("Step 1: Clone the Repository", styles),
        bt("git clone https://github.com/Godesivaramakrishna/Flood-Management-System-by-skill-wallet.git", styles),

        sh("Step 2: Create Virtual Environment", styles),
        bt("conda create -n flood-env python=3.11   (or python -m venv .venv)", styles),
        bt("conda activate flood-env                (or .venv\\Scripts\\activate on Windows)", styles),

        sh("Step 3: Install Dependencies", styles),
        bt("python -m pip install -r requirements.txt", styles),

        sh("Step 4: Generate Dataset & Train Model (Optional)", styles),
        bt("python model/generate_dataset.py", styles),
        bt("python model/train_model.py", styles),
        bt("Note: Pre-trained floods.save is already included in the repository.", styles),

        sh("Step 5: Run Flask Application", styles),
        bt("python app.py", styles),

        sh("Step 6: Open in Browser", styles),
        bt("Navigate to: http://127.0.0.1:5000", styles),

        sh("Key Files", styles),
        info_table([
            ("app.py",              "Main Flask application — run this file"),
            ("model/floods.save",   "Deployed XGBoost model (joblib)"),
            ("model/scaler.save",   "Fitted StandardScaler (joblib)"),
            ("requirements.txt",    "All Python dependencies"),
            ("Dockerfile",          "Docker container configuration"),
            ("manifest.yml",        "IBM Cloud deployment manifest"),
        ], styles),
    ]

def p7_full_doc(styles):
    return [
        header_block(styles, "Sample Project Documentation", "7", "Project Documentation"),
        Spacer(1,12), badge_row(styles), Spacer(1,14), divider(),

        sh("1. Project Title", styles),
        bt("<b>Rising Waters — Machine Learning Approach to Flood Prediction</b>", styles),

        sh("2. Problem Statement", styles),
        bt("Floods are among the most devastating natural disasters, claiming thousands of lives annually. "
           "Conventional forecasting methods lack the predictive intelligence required for timely early warnings. "
           "This project addresses this gap by building an ML-powered flood prediction web application.", styles),

        sh("3. Objective", styles),
        bl("Train and compare 4 ML classifiers on meteorological flood data", styles),
        bl("Deploy the best model (XGBoost) as a Flask web application", styles),
        bl("Provide disaster management officers with real-time flood risk predictions", styles),
        bl("Deliver dedicated result pages for Flood Chance and No Flood Chance", styles),

        sh("4. Dataset", styles),
        info_table([
            ("Size",     "5,000 records"),
            ("Features", "annual_rainfall, seasonal_rainfall, cloud_visibility, humidity, temperature, river_level"),
            ("Target",   "flood_occurred (0=No Flood, 1=Flood)"),
            ("Source",   "Synthetic dataset based on real meteorological patterns"),
        ], styles),

        sh("5. Model Performance", styles),
        info_table([
            ("Decision Tree",        "78.17% accuracy"),
            ("K-Nearest Neighbours", "80.67% accuracy"),
            ("Random Forest",        "82.00% accuracy"),
            ("XGBoost (DEPLOYED)",   "96.55% accuracy — saved as floods.save"),
        ], styles),

        sh("6. Web Application", styles),
        info_table([
            ("Home Page",            "Dashboard with model stats and prediction counts"),
            ("Prediction Page",      "6-field meteorological input form"),
            ("Flood Result Page",    "Red danger banner, alert level, 6 emergency actions"),
            ("No Flood Result Page", "Green safe banner, all-clear badge, monitoring tips"),
            ("History Page",         "Full audit log of all past predictions"),
            ("About Page",           "Architecture, scenarios, technology stack"),
        ], styles),

        sh("7. Deployment", styles),
        bt("The application is deployed on IBM Cloud using Docker containerization and "
           "a Cloud Foundry manifest.yml. It is accessible 24/7 via a public cloud URL.", styles),

        PageBreak(),
        sh("8. Project Structure", styles),
        info_table([
            ("app.py",                  "Flask application controller"),
            ("model/train_model.py",    "Complete ML training pipeline"),
            ("model/floods.save",       "Deployed XGBoost model"),
            ("templates/",             "6 Jinja2 HTML templates"),
            ("static/css/style.css",    "Premium dark-theme CSS"),
            ("utils/preprocessing.py",  "Input validation and scaling"),
            ("requirements.txt",        "Python dependencies"),
            ("Dockerfile",              "Container config"),
            ("manifest.yml",            "IBM Cloud manifest"),
        ], styles),
    ]

# ==============================================================================
# PHASE 8 — Project Demonstration
# ==============================================================================
def p8_communication(styles):
    return [
        header_block(styles, "Communication", "8", "Project Demonstration"),
        Spacer(1,12), badge_row(styles), Spacer(1,14), divider(),

        sh("Stakeholder Communication Plan", styles),
        Table([
            [Paragraph("<b>Stakeholder</b>", styles["table_header"]),
             Paragraph("<b>Communication Method</b>", styles["table_header"]),
             Paragraph("<b>Frequency</b>", styles["table_header"]),
             Paragraph("<b>Content</b>", styles["table_header"])],
            ["NDMA Officials",       "Web App Dashboard",     "Real-time",  "Live flood risk predictions"],
            ["Meteorologists",       "Prediction Form + API", "On-demand",  "Model inputs and outputs"],
            ["Disaster Teams",       "Flood Result Page",     "On-demand",  "Emergency action protocol"],
            ["Local Authorities",    "Email / SMS alert",     "On alert",   "Flood/No Flood status"],
            ["Research Analysts",    "History Page",          "Weekly",     "Prediction trend audit"],
            ["IBM Cloud Platform",   "Deployment Logs",       "Continuous", "App health and uptime"],
        ], colWidths=[4*cm, 4*cm, 2.5*cm, 6*cm]).setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,0), NAVY),
            ("TEXTCOLOR",     (0,0),(-1,0), WHITE),
            ("FONTNAME",      (0,0),(-1,0), "Helvetica-Bold"),
            ("FONTSIZE",      (0,0),(-1,-1), 9),
            ("GRID",          (0,0),(-1,-1), 0.5, colors.grey),
            ("ROWBACKGROUNDS",(0,1),(-1,-1), [colors.white, LIGHT_BG]),
            ("TOPPADDING",    (0,0),(-1,-1), 7),
            ("BOTTOMPADDING", (0,0),(-1,-1), 7),
        ])),
    ]

def p8_demo(styles):
    return [
        header_block(styles, "Demonstration of Proposed Features", "8", "Project Demonstration"),
        Spacer(1,12), badge_row(styles), Spacer(1,14), divider(),

        sh("Live Demo Walkthrough", styles),
        Table([
            [Paragraph("<b>Step</b>", styles["table_header"]),
             Paragraph("<b>Page</b>", styles["table_header"]),
             Paragraph("<b>Action Demonstrated</b>", styles["table_header"]),
             Paragraph("<b>Feature Shown</b>", styles["table_header"])],
            ["1","Home (/)","Load dashboard, show model accuracy stats","96.55% XGBoost, live prediction count"],
            ["2","Predict (/predict)","Enter high-risk values (RF=3500, H=92%)","6-field input form, validation"],
            ["3","Submit","Click Predict Flood button","POST /predict route, preprocessing"],
            ["4","Flood Result","Show red danger banner, alert level","result_flood.html, emergency protocol"],
            ["5","Predict","Enter low-risk values (RF=800, H=55%)","Quick clear form interaction"],
            ["6","No Flood Result","Show green safe banner","result_noflood.html, monitoring tips"],
            ["7","History","Show audit log of predictions","predictions_log.csv, timestamp"],
            ["8","About","Show 5-layer architecture diagram","Architecture, scenarios, tech stack"],
        ], colWidths=[1.2*cm, 3*cm, 5.5*cm, 6.8*cm]).setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,0), NAVY),
            ("TEXTCOLOR",     (0,0),(-1,0), WHITE),
            ("FONTNAME",      (0,0),(-1,0), "Helvetica-Bold"),
            ("FONTSIZE",      (0,0),(-1,-1), 8),
            ("GRID",          (0,0),(-1,-1), 0.5, colors.grey),
            ("ROWBACKGROUNDS",(0,1),(-1,-1), [colors.white, LIGHT_BG]),
            ("ALIGN",         (0,0),(0,-1), "CENTER"),
            ("TOPPADDING",    (0,0),(-1,-1), 7),
            ("BOTTOMPADDING", (0,0),(-1,-1), 7),
        ])),
    ]

def p8_planning(styles):
    return [
        header_block(styles, "Project Demo Planning", "8", "Project Demonstration"),
        Spacer(1,12), badge_row(styles), Spacer(1,14), divider(),

        sh("Demo Session Plan", styles),
        info_table([
            ("Duration",   "30 minutes"),
            ("Format",     "Live web application walkthrough"),
            ("Audience",   "Academic evaluators, IBM representatives, Skill Wallet team"),
            ("Tools",      "Chrome browser, local Flask server (or IBM Cloud URL)"),
            ("Presenter",  "Godesi Varamakrishna"),
        ], styles),
        Spacer(1,10),

        sh("Demo Agenda", styles),
        Table([
            [Paragraph("<b>Time</b>", styles["table_header"]),
             Paragraph("<b>Section</b>", styles["table_header"]),
             Paragraph("<b>Content</b>", styles["table_header"])],
            ["0-5 min",  "Introduction",     "Problem statement, motivation, project overview"],
            ["5-12 min", "Architecture",     "5-layer system architecture, tech stack demo on About page"],
            ["12-20 min","Live Demo",        "Flood prediction + No Flood prediction, history log"],
            ["20-25 min","Model Results",    "Accuracy comparison: DT 78%, RF 82%, KNN 80%, XGBoost 96.55%"],
            ["25-30 min","Q&A / Conclusion", "Future work, scalability, IBM Cloud deployment"],
        ], colWidths=[2.5*cm, 3.5*cm, 10.5*cm]).setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,0), NAVY),
            ("TEXTCOLOR",     (0,0),(-1,0), WHITE),
            ("FONTNAME",      (0,0),(-1,0), "Helvetica-Bold"),
            ("FONTSIZE",      (0,0),(-1,-1), 9),
            ("GRID",          (0,0),(-1,-1), 0.5, colors.grey),
            ("ROWBACKGROUNDS",(0,1),(-1,-1), [colors.white, LIGHT_BG]),
            ("TOPPADDING",    (0,0),(-1,-1), 8),
            ("BOTTOMPADDING", (0,0),(-1,-1), 8),
        ])),
    ]

def p8_scalability(styles):
    return [
        header_block(styles, "Scalability &amp; Future Plan", "8", "Project Demonstration"),
        Spacer(1,12), badge_row(styles), Spacer(1,14), divider(),

        sh("Current Scalability", styles),
        bl("Dockerized deployment — horizontal scaling via IBM Cloud Foundry instances", styles),
        bl("Stateless Flask app — multiple instances can run simultaneously", styles),
        bl("CSV log can be replaced with PostgreSQL for production-scale storage", styles),
        Spacer(1,8),

        sh("Future Enhancement Plan", styles),
        Table([
            [Paragraph("<b>Enhancement</b>", styles["table_header"]),
             Paragraph("<b>Description</b>", styles["table_header"]),
             Paragraph("<b>Priority</b>", styles["table_header"])],
            ["Real-time data integration",  "Connect to IMD / weather APIs for live data input",           "HIGH"],
            ["SMS/Email Alerts",            "Auto-send flood alerts to registered authorities",             "HIGH"],
            ["Multi-region prediction",     "Batch predictions for multiple districts simultaneously",      "MEDIUM"],
            ["Deep Learning upgrade",       "LSTM for time-series rainfall pattern analysis",               "MEDIUM"],
            ["Mobile App",                  "Native Android/iOS app using the Flask REST API",              "MEDIUM"],
            ["Multi-language support",      "Regional language UI for non-English disaster teams",          "LOW"],
            ["Satellite data integration",  "Add satellite imagery features via IBM Watson Vision",         "LOW"],
        ], colWidths=[4.5*cm, 8.5*cm, 3*cm]).setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,0), NAVY),
            ("TEXTCOLOR",     (0,0),(-1,0), WHITE),
            ("FONTNAME",      (0,0),(-1,0), "Helvetica-Bold"),
            ("FONTSIZE",      (0,0),(-1,-1), 9),
            ("GRID",          (0,0),(-1,-1), 0.5, colors.grey),
            ("ROWBACKGROUNDS",(0,1),(-1,-1), [colors.white, LIGHT_BG]),
            ("ALIGN",         (2,0),(2,-1), "CENTER"),
            ("TOPPADDING",    (0,0),(-1,-1), 8),
            ("BOTTOMPADDING", (0,0),(-1,-1), 8),
        ])),
    ]

def p8_team(styles):
    return [
        header_block(styles, "Team Involvement in Demonstration", "8", "Project Demonstration"),
        Spacer(1,12), badge_row(styles), Spacer(1,14), divider(),

        sh("Team Member Roles", styles),
        Table([
            [Paragraph("<b>Name</b>", styles["table_header"]),
             Paragraph("<b>Role</b>", styles["table_header"]),
             Paragraph("<b>Contribution</b>", styles["table_header"])],
            ["Godesi Varamakrishna","Lead Developer & Presenter",
             "Full project — dataset generation, ML pipeline, Flask app, UI design, IBM Cloud deployment"],
        ], colWidths=[4*cm, 4.5*cm, 8*cm]).setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,0), NAVY),
            ("TEXTCOLOR",     (0,0),(-1,0), WHITE),
            ("FONTNAME",      (0,0),(-1,0), "Helvetica-Bold"),
            ("FONTSIZE",      (0,0),(-1,-1), 9),
            ("GRID",          (0,0),(-1,-1), 0.5, colors.grey),
            ("TOPPADDING",    (0,0),(-1,-1), 12),
            ("BOTTOMPADDING", (0,0),(-1,-1), 12),
        ])),
        Spacer(1,14),

        sh("Demo Responsibilities", styles),
        info_table([
            ("Opening Statement",   "Problem context, flood statistics, project motivation"),
            ("Technical Demo",      "Live prediction on web app — both flood and no-flood scenarios"),
            ("Architecture Walkthrough","5-layer diagram on About page, tech stack explanation"),
            ("Model Comparison",    "Show accuracy comparison on Home Dashboard"),
            ("Q&A Handling",        "Technical questions on preprocessing, model selection, deployment"),
            ("Closing",             "Impact statement, future enhancements, IBM Cloud live URL"),
        ], styles),
    ]

# ==============================================================================
# MAIN — Generate all PDFs
# ==============================================================================
if __name__ == "__main__":
    print("Generating all 8 phase documentation folders...")

    pdfs = [
        # Phase 1
        (f"{BASE}/1. Brainstorming & Ideation/Brainstorming & Idea Prioritization.pdf", p1_brainstorming),
        (f"{BASE}/1. Brainstorming & Ideation/Define Problem Statements .pdf",          p1_problem),
        (f"{BASE}/1. Brainstorming & Ideation/Empathy Map.pdf",                         p1_empathy),
        # Phase 2
        (f"{BASE}/2. Requirement Analysis/Customer Journey Map.pdf",   p2_journey),
        (f"{BASE}/2. Requirement Analysis/Data Flow Diagram.pdf",       p2_dfd),
        (f"{BASE}/2. Requirement Analysis/Solution Requirements.pdf",   p2_solution_req),
        (f"{BASE}/2. Requirement Analysis/Technology Stack.pdf",        p2_tech_stack),
        # Phase 3
        (f"{BASE}/3. Project Design Phase/Problem-Solution Fit.pdf",    p3_fit),
        (f"{BASE}/3. Project Design Phase/Proposed Solution.pdf",       p3_proposed),
        (f"{BASE}/3. Project Design Phase/Solution Architecture.pdf",   p3_architecture),
        # Phase 4
        (f"{BASE}/4. Project Planning Phase/Project Planning.pdf",      p4_planning),
        # Phase 5
        (f"{BASE}/5. Project Development Phase/Code-Layout, Readability and Reusability.pdf", p5_code_layout),
        (f"{BASE}/5. Project Development Phase/Coding & Solution.pdf",                        p5_coding),
        (f"{BASE}/5. Project Development Phase/No. of Functional Features Included in the Solution.pdf", p5_features),
        # Phase 6
        (f"{BASE}/6.Project Testing/Performance Testing.pdf",           p6_testing),
        # Phase 7
        (f"{BASE}/7.Project Documentation/Project Executable Files.pdf",        p7_executable),
        (f"{BASE}/7.Project Documentation/Sample Project Documentation.pdf",    p7_full_doc),
        # Phase 8
        (f"{BASE}/8.Project Demonstration/Communication.pdf",                       p8_communication),
        (f"{BASE}/8.Project Demonstration/Demonstration of Proposed Features.pdf",  p8_demo),
        (f"{BASE}/8.Project Demonstration/Project Demo Planning.pdf",              p8_planning),
        (f"{BASE}/8.Project Demonstration/Scalability & Future Plan.pdf",          p8_scalability),
        (f"{BASE}/8.Project Demonstration/Team Involvement in Demonstration.pdf",  p8_team),
    ]

    for path, fn in pdfs:
        build_pdf(path, fn)

    print(f"\nDone! {len(pdfs)} PDFs generated in '{BASE}/' directory.")
