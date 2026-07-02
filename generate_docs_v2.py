"""
generate_docs_v2.py
--------------------
Generates PDFs that EXACTLY match the reference AI-ML_Skill_Wallet style:
  - Header: Title + Date + Team ID + Project Name + Max Marks (navy bg, white text)
  - IBM SkillsBuild / CSRBOX logo strip
  - Clean white body with structured fill-in tables
  - Navy table headers, light-grey alternating rows
  - Footer with project name + page number
Flood Management System content + correct team members.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT

W, H = A4

# ── Exact reference colours ────────────────────────────────────────────────────
NAVY   = colors.HexColor("#003366")   # IBM dark navy
TEAL   = colors.HexColor("#0062FF")   # IBM blue accent
WHITE  = colors.white
LGRAY  = colors.HexColor("#F2F5F9")   # light row bg
MGRAY  = colors.HexColor("#D0D7E2")   # border/rule colour
DGRAY  = colors.HexColor("#5A6477")   # body text grey
BLACK  = colors.HexColor("#0F1923")
YELLOW = colors.HexColor("#FFD100")   # IBM yellow badge

# ── Team Info ─────────────────────────────────────────────────────────────────
TEAM_ID      = "Batch 2023-27 | ACOE"
PROJECT_NAME = "Rising Waters – ML-Based Flood Prediction System"
DATE         = "15 March 2026"
COLLEGE      = "Anurag College of Engineering"

TEAM_MEMBERS = [
    ("Venkatesh Balireddy",              "Team Lead"),
    ("Archana Dhanani",                  "Member"),
    ("Shivatmika Gandikota",             "Member"),
    ("Gode Siva Ramakrishna Durgaprasad","Member"),
    ("Bavisetty Gopi Krishna",           "Member"),
]

# ── Styles ────────────────────────────────────────────────────────────────────
def S():
    s = {}
    s["title"] = ParagraphStyle("title", fontSize=18, fontName="Helvetica-Bold",
        textColor=WHITE, alignment=TA_CENTER, leading=22, spaceAfter=2)
    s["meta_key"] = ParagraphStyle("mk", fontSize=9, fontName="Helvetica-Bold",
        textColor=colors.HexColor("#AACBFF"), alignment=TA_LEFT)
    s["meta_val"] = ParagraphStyle("mv", fontSize=9, fontName="Helvetica",
        textColor=WHITE, alignment=TA_LEFT)
    s["section"] = ParagraphStyle("section", fontSize=11, fontName="Helvetica-Bold",
        textColor=NAVY, spaceBefore=14, spaceAfter=5)
    s["body"] = ParagraphStyle("body", fontSize=9.5, fontName="Helvetica",
        textColor=BLACK, leading=15, spaceAfter=6, alignment=TA_JUSTIFY)
    s["body_bold"] = ParagraphStyle("bb", fontSize=9.5, fontName="Helvetica-Bold",
        textColor=BLACK, leading=15, spaceAfter=6)
    s["th"] = ParagraphStyle("th", fontSize=9, fontName="Helvetica-Bold",
        textColor=WHITE, alignment=TA_CENTER)
    s["td"] = ParagraphStyle("td", fontSize=9, fontName="Helvetica",
        textColor=BLACK, alignment=TA_LEFT, leading=13)
    s["td_c"] = ParagraphStyle("tdc", fontSize=9, fontName="Helvetica",
        textColor=BLACK, alignment=TA_CENTER, leading=13)
    s["footer"] = ParagraphStyle("footer", fontSize=7.5, fontName="Helvetica",
        textColor=DGRAY, alignment=TA_CENTER)
    s["marks"] = ParagraphStyle("marks", fontSize=9, fontName="Helvetica-Bold",
        textColor=YELLOW, alignment=TA_RIGHT)
    s["intro"] = ParagraphStyle("intro", fontSize=9.5, fontName="Helvetica",
        textColor=DGRAY, leading=15, spaceAfter=10, alignment=TA_JUSTIFY)
    return s

STYLES = S()

# ── Footer ────────────────────────────────────────────────────────────────────
def footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, W, 24, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(1.5*cm, 8, f"{PROJECT_NAME}  |  {COLLEGE}")
    canvas.drawRightString(W - 1.5*cm, 8, f"Page {doc.page}")
    canvas.restoreState()

# ── IBM-style header banner ───────────────────────────────────────────────────
def header_banner(doc_title, max_marks):
    """Exact reference style: navy banner with title + metadata table."""
    title_p  = Paragraph(doc_title, STYLES["title"])
    marks_p  = Paragraph(f"Maximum Marks: {max_marks}", STYLES["marks"])

    # Metadata row  (Date | Team ID | Project Name)
    meta = Table(
        [[
            Paragraph("Date", STYLES["meta_key"]),
            Paragraph("Team ID", STYLES["meta_key"]),
            Paragraph("Project Name", STYLES["meta_key"]),
        ],[
            Paragraph(DATE, STYLES["meta_val"]),
            Paragraph(TEAM_ID, STYLES["meta_val"]),
            Paragraph(PROJECT_NAME, STYLES["meta_val"]),
        ]],
        colWidths=[3.5*cm, 5.5*cm, 8.5*cm]
    )
    meta.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), NAVY),
        ("LEFTPADDING",   (0,0),(-1,-1), 0),
        ("RIGHTPADDING",  (0,0),(-1,-1), 0),
        ("TOPPADDING",    (0,0),(-1,-1), 2),
        ("BOTTOMPADDING", (0,0),(-1,-1), 2),
        ("LINEBELOW",     (0,0),(-1,0),  0.5, colors.HexColor("#2255AA")),
    ]))

    banner = Table(
        [[title_p],[marks_p],[meta]],
        colWidths=[W - 3*cm]
    )
    banner.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), NAVY),
        ("TOPPADDING",    (0,0),(-1,0),  16),
        ("BOTTOMPADDING", (0,-1),(-1,-1),12),
        ("TOPPADDING",    (0,-1),(-1,-1),4),
        ("LEFTPADDING",   (0,0),(-1,-1), 16),
        ("RIGHTPADDING",  (0,0),(-1,-1), 16),
        ("LINEBELOW",     (0,0),(-1,0),  1, colors.HexColor("#0062FF")),
    ]))
    return banner

# ── Table builder ─────────────────────────────────────────────────────────────
def make_table(headers, rows, col_widths, row_bg=True):
    header_row = [Paragraph(h, STYLES["th"]) for h in headers]
    data = [header_row]
    for i, row in enumerate(rows):
        data.append([
            Paragraph(str(c), STYLES["td_c"] if j == 0 else STYLES["td"])
            for j, c in enumerate(row)
        ])
    tbl = Table(data, colWidths=col_widths, repeatRows=1)
    row_styles = [
        ("BACKGROUND",    (0,0),(-1,0),  NAVY),
        ("TEXTCOLOR",     (0,0),(-1,0),  WHITE),
        ("FONTNAME",      (0,0),(-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0,0),(-1,-1), 9),
        ("GRID",          (0,0),(-1,-1), 0.5, MGRAY),
        ("TOPPADDING",    (0,0),(-1,-1), 7),
        ("BOTTOMPADDING", (0,0),(-1,-1), 7),
        ("LEFTPADDING",   (0,0),(-1,-1), 8),
        ("RIGHTPADDING",  (0,0),(-1,-1), 8),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
    ]
    if row_bg:
        for i in range(1, len(data)):
            bg = LGRAY if i % 2 == 0 else WHITE
            row_styles.append(("BACKGROUND", (0,i),(-1,i), bg))
    tbl.setStyle(TableStyle(row_styles))
    return tbl

def sec(text):
    return Paragraph(text, STYLES["section"])

def body(text):
    return Paragraph(text, STYLES["body"])

def intro(text):
    return Paragraph(text, STYLES["intro"])

def sp(n=8):
    return Spacer(1, n)

def hr():
    return HRFlowable(width="100%", thickness=0.5, color=MGRAY, spaceBefore=6, spaceAfter=6)

# ── Team members table (reusable) ──────────────────────────────────────────────
def team_table():
    rows = [(str(i+1), m[0], m[1]) for i, m in enumerate(TEAM_MEMBERS)]
    return make_table(["S.No", "Team Member Name", "Role"], rows,
                      [1.5*cm, 9*cm, 7*cm])

# ══════════════════════════════════════════════════════════════════════════════
# PHASE 1
# ══════════════════════════════════════════════════════════════════════════════
def p1_brainstorm(styles):
    return [
        header_banner("Brainstorming & Idea Prioritization", "3 Marks"),
        sp(14),
        sec("Step 1: Team Members"),
        team_table(), sp(10),
        sec("Step 2: Brainstorm and Idea Listing"),
        intro("Each team member lists out as many ideas as possible without judging them at this stage. "
              "The goal is to generate a wide range of creative solutions to the problem of flood prediction."),
        make_table(
            ["S.No","Team Member","Idea / Suggestion","Category","Group No."],
            [
                ("1","Venkatesh Balireddy",   "ML-based flood classifier using meteorological data",      "AI/ML",     "1"),
                ("2","Archana Dhanani",       "Real-time IoT sensor network for river-level monitoring",  "IoT",       "2"),
                ("3","Shivatmika Gandikota",  "Satellite imagery analysis using computer vision",         "CV/AI",     "3"),
                ("4","Gode S R Durgaprasad", "Flask web app with historical prediction audit log",       "Web App",   "1"),
                ("5","Bavisetty Gopi Krishna","SMS/email alert system for flood warnings",                "Alerts",    "1"),
                ("6","All Members",           "IBM Cloud deployment with Docker containerization",        "DevOps",    "1"),
            ],
            [1.5*cm, 4*cm, 6.5*cm, 3*cm, 2.5*cm]
        ), sp(12),
        sec("Step 3: Idea Prioritization"),
        intro("Rate each grouped idea on feasibility and importance, then select the final idea to move forward with."),
        make_table(
            ["Group No.","Final Idea","Feasibility","Importance","Priority","Selected"],
            [
                ("1","XGBoost ML Flood Prediction + Flask Web App","High","High","1","Yes"),
                ("2","IoT Sensor Network",                          "Medium","High","2","No"),
                ("3","Satellite Imagery CV",                        "Low","High","3","No"),
            ],
            [2*cm, 6.5*cm, 2.5*cm, 2.5*cm, 2*cm, 2*cm]
        ),
    ]

def p1_problem(styles):
    return [
        header_banner("Define Problem Statements", "3 Marks"),
        sp(14),
        sec("Team Members"),
        team_table(), sp(12),
        sec("Problem Statement Definition"),
        intro("A clear problem statement focuses the team on the core challenge and guides the design of the solution."),
        make_table(
            ["Attribute","Details"],
            [
                ("Problem Statement",
                 "Floods are among the most devastating natural disasters, claiming thousands of lives "
                 "and displacing millions each year. Conventional forecasting methods lack ML-powered "
                 "real-time predictive intelligence, leaving authorities with insufficient lead time to respond."),
                ("Who is affected?",
                 "Disaster management officers, meteorologists, local authorities, and flood-affected communities."),
                ("What is the gap?",
                 "No accessible, ML-powered web application that accepts meteorological inputs and "
                 "instantly classifies flood risk in real time."),
                ("Desired Outcome",
                 "A Flask web application using XGBoost (96.55% accuracy) that accepts 6 meteorological "
                 "features and outputs a binary Flood / No Flood prediction with emergency response guidance."),
                ("How Might We?",
                 "How might we provide disaster management teams with a reliable, real-time ML flood "
                 "prediction system that enables timely evacuations and saves lives?"),
            ],
            [4.5*cm, 13*cm]
        ),
    ]

def p1_empathy(styles):
    return [
        header_banner("Empathy Map", "3 Marks"),
        sp(14),
        sec("Team Members"),
        team_table(), sp(12),
        sec("Primary User: Disaster Management Officer"),
        intro("The empathy map captures the thoughts, feelings, behaviours, and pain points of the "
              "primary user of the Rising Waters flood prediction system."),
        make_table(
            ["Quadrant","Key Insights"],
            [
                ("THINKS",
                 "\"Will rainfall data be enough to predict flooding accurately?\"  "
                 "\"Can I trust the model output for critical decisions?\"  "
                 "\"How do I explain results to community leaders?\""),
                ("FEELS",
                 "Anxious about missing a real flood event (false negatives).  "
                 "Relieved when system shows a clear No Flood result.  "
                 "Confident when model accuracy (96.55%) is displayed prominently."),
                ("SAYS",
                 "\"We need faster predictions before monsoon season.\"  "
                 "\"The system should clearly tell us what action to take.\"  "
                 "\"We need a history log to review past predictions.\""),
                ("DOES",
                 "Manually collects rainfall data from weather stations.  "
                 "Enters readings into the 6-field prediction form.  "
                 "Shares flood/no-flood result with field teams.  "
                 "Logs predictions for audit."),
                ("PAIN POINTS",
                 "No centralized ML platform for flood risk prediction.  "
                 "Slow manual analysis delays emergency response.  "
                 "No emergency action guidance alongside predictions."),
                ("GAINS",
                 "Real-time flood risk classification in <2 seconds.  "
                 "6 emergency action cards displayed on Flood Result page.  "
                 "Full prediction audit history with timestamps."),
            ],
            [3.5*cm, 14*cm]
        ),
    ]

# ══════════════════════════════════════════════════════════════════════════════
# PHASE 2
# ══════════════════════════════════════════════════════════════════════════════
def p2_journey(styles):
    return [
        header_banner("Customer Journey Map", "2 Marks"),
        sp(14),
        sec("Team Members"),
        team_table(), sp(12),
        sec("User Journey: Disaster Management Officer Using Rising Waters"),
        intro("The customer journey map documents the end-to-end experience of the primary user "
              "interacting with the Rising Waters flood prediction web application."),
        make_table(
            ["Stage","User Action","Touchpoint","Emotion","Opportunity"],
            [
                ("1. Awareness",  "Learns about the flood prediction web app",          "Training / NDMA circular", "Curious",   "Promote via NDMA and state disaster channels"),
                ("2. Access",     "Opens Rising Waters web app on browser",             "Home Dashboard (/)",       "Neutral",   "Show live model accuracy & prediction counts"),
                ("3. Input",      "Enters 6 meteorological readings into the form",     "Predict Page (/predict)",  "Focused",   "Add field tooltips with example values"),
                ("4. Submit",     "Clicks 'Predict Flood Risk' button",                 "POST /predict route",      "Anxious",   "Show animated loading indicator"),
                ("5. Flood Alert","Views red Flood Chance page with emergency cards",   "result_flood.html",        "Alarmed",   "Display 6 emergency protocol action cards"),
                ("6. Safe Alert", "Views green No Flood page with monitoring tips",     "result_noflood.html",      "Relieved",  "Show ongoing monitoring recommendations"),
                ("7. History",    "Reviews audit log of all past predictions",          "History Page (/history)",  "Confident", "Add CSV export and date-filter feature"),
                ("8. Report",     "Shares results with field teams and authorities",    "External channels",        "Empowered", "Add one-click share and print button"),
            ],
            [2.5*cm, 4*cm, 3.5*cm, 2*cm, 5.5*cm]
        ),
    ]

def p2_dfd(styles):
    return [
        header_banner("Data Flow Diagram", "2 Marks"),
        sp(14),
        sec("Team Members"),
        team_table(), sp(12),
        sec("Level 0 — Context Diagram"),
        intro("The context diagram shows the Rising Waters system boundary, its external entities, "
              "and the primary data flows entering and leaving the system."),
        make_table(
            ["Element","Description"],
            [
                ("External Entity", "Disaster Management Officer / Meteorologist"),
                ("System",          "Rising Waters Flood Prediction System (Flask + XGBoost)"),
                ("Input Flow",      "annual_rainfall, seasonal_rainfall, cloud_visibility, humidity, temperature, river_level"),
                ("Output Flow",     "Binary prediction label (Flood / No Flood) + probability score + emergency protocol"),
            ],
            [4*cm, 13.5*cm]
        ), sp(12),
        sec("Level 1 — Internal Data Flow"),
        intro("Shows how data moves between internal processes within the Rising Waters system."),
        make_table(
            ["Process ID","Process Name","Input","Output","Data Store"],
            [
                ("P1", "Form Input Capture",   "User web form values",      "Raw feature dictionary",       "—"),
                ("P2", "Input Validation",      "Raw feature dict",          "Validated dict / Error msg",   "—"),
                ("P3", "Feature Scaling",       "Validated features",        "Scaled NumPy array",           "scaler.save"),
                ("P4", "ML Prediction",         "Scaled NumPy array",        "Label (0/1) + Probability",   "floods.save"),
                ("P5", "Result Routing",        "Prediction label",          "HTTP redirect to result page", "—"),
                ("P6", "Prediction Logging",    "All inputs + result + time","New row appended",             "predictions_log.csv"),
            ],
            [1.5*cm, 4*cm, 4*cm, 4*cm, 4*cm]
        ),
    ]

def p2_solution_req(styles):
    return [
        header_banner("Solution Requirements", "2 Marks"),
        sp(14),
        sec("Team Members"),
        team_table(), sp(12),
        sec("Functional Requirements"),
        intro("Functional requirements define the specific behaviours and features the Rising Waters system must implement."),
        make_table(
            ["Req. ID","Requirement","Priority"],
            [
                ("FR-01", "System shall accept 6 meteorological inputs via a web form",                        "High"),
                ("FR-02", "System shall validate all inputs and return meaningful error messages",              "High"),
                ("FR-03", "System shall scale inputs using the pre-fitted StandardScaler (scaler.save)",       "High"),
                ("FR-04", "System shall load XGBoost model (floods.save) and return binary classification",   "High"),
                ("FR-05", "System shall display a dedicated Flood Chance result page (red theme)",             "High"),
                ("FR-06", "System shall display a dedicated No Flood Chance result page (green theme)",        "High"),
                ("FR-07", "System shall log every prediction with timestamp to predictions_log.csv",           "Medium"),
                ("FR-08", "System shall display full prediction history on the History page",                  "Medium"),
                ("FR-09", "System shall show model accuracy comparison chart on the Home Dashboard",           "Medium"),
            ],
            [2*cm, 12*cm, 3.5*cm]
        ), sp(10),
        sec("Non-Functional Requirements"),
        make_table(
            ["Req. ID","Category","Requirement"],
            [
                ("NFR-01", "Performance",     "Prediction response time shall be under 2 seconds"),
                ("NFR-02", "Accuracy",        "XGBoost model test accuracy shall be >= 95%"),
                ("NFR-03", "Availability",    "System shall be available 24/7 via IBM Cloud hosting"),
                ("NFR-04", "Usability",       "Responsive design, accessible on mobile and desktop browsers"),
                ("NFR-05", "Security",        "Session-based result passing; no raw model file exposure"),
                ("NFR-06", "Scalability",     "Dockerized deployment, ready for horizontal scaling"),
                ("NFR-07", "Maintainability", "Modular code: separate utils/, model/, templates/ directories"),
            ],
            [2*cm, 3.5*cm, 12*cm]
        ),
    ]

def p2_tech_stack(styles):
    return [
        header_banner("Technology Stack", "2 Marks"),
        sp(14),
        sec("Team Members"),
        team_table(), sp(12),
        sec("Define Your Technology Stack"),
        intro("Identify the programming languages, frameworks, databases, front-end tools, back-end tools, and APIs "
              "used to build the Rising Waters flood prediction solution. A well-chosen technology stack ensures the "
              "application is scalable, maintainable, and aligned with project requirements."),
        make_table(
            ["S.No","Architecture Component / Layer","Technology Chosen","Justification / Purpose"],
            [
                ("1",  "Machine Learning",         "XGBoost 1.7 + Scikit-learn 1.3",
                 "Best accuracy (96.55%) among 4 tested algorithms; fast inference for real-time prediction"),
                ("2",  "Data Processing",          "Pandas 2.x + NumPy 1.x",
                 "Efficient tabular data manipulation and array operations for the 5,000-row flood dataset"),
                ("3",  "Model Serialization",      "Joblib 1.3",
                 "Save and load floods.save (XGBoost model) and scaler.save (StandardScaler)"),
                ("4",  "Backend / Server-Side",    "Python 3.11 + Flask 2.x",
                 "Lightweight WSGI framework; rapid API development; integrates directly with ML objects"),
                ("5",  "Frontend / Client-Side",   "HTML5 + CSS3 + Vanilla JS",
                 "Dark-theme glassmorphism UI; responsive design; no framework overhead"),
                ("6",  "Templating Engine",        "Jinja2 3.x",
                 "Server-side HTML rendering; template inheritance via base.html eliminates duplication"),
                ("7",  "Cloud / Hosting",          "IBM Cloud Foundry",
                 "Free-tier cloud hosting; seamless deployment via manifest.yml; IBM Skill Wallet alignment"),
                ("8",  "Containerization",         "Docker 24+",
                 "Reproducible deployment environment; easy scaling; Dockerfile provided in repository"),
                ("9",  "Version Control & CI/CD",  "Git + GitHub",
                 "Source code management; collaborative development; structured 8-phase documentation repository"),
            ],
            [1.2*cm, 4*cm, 4*cm, 8.3*cm]
        ),
    ]

# ══════════════════════════════════════════════════════════════════════════════
# PHASE 3
# ══════════════════════════════════════════════════════════════════════════════
def p3_fit(styles):
    return [
        header_banner("Problem-Solution Fit", "3 Marks"),
        sp(14),
        sec("Team Members"),
        team_table(), sp(12),
        sec("Problem-Solution Fit Analysis"),
        intro("This document maps each identified problem to the specific solution feature in Rising Waters "
              "that addresses it, demonstrating a strong problem-solution fit."),
        make_table(
            ["S.No","Problem Identified","Solution Feature","Fit Level"],
            [
                ("1","No real-time ML-powered flood prediction tool available",
                 "XGBoost classifier (floods.save) achieving 96.55% accuracy",
                 "Strong"),
                ("2","Complex meteorological data difficult to interpret manually",
                 "6-field standardized input form with field descriptions and tooltips",
                 "Strong"),
                ("3","No emergency response guidance for prediction outputs",
                 "Flood Result page with 6 colour-coded emergency protocol action cards",
                 "Strong"),
                ("4","No accessible web interface for non-technical disaster management users",
                 "Flask web app with intuitive dark-theme UI accessible on any browser",
                 "Strong"),
                ("5","No prediction history or audit trail",
                 "predictions_log.csv + History page with full timestamped audit log",
                 "Strong"),
                ("6","Lack of 24/7 cloud accessibility for disaster teams",
                 "IBM Cloud Foundry deployment with Docker containerization",
                 "Strong"),
                ("7","Manual comparison of multiple ML models is time-consuming",
                 "Home Dashboard with built-in accuracy comparison (DT/RF/KNN/XGB)",
                 "Medium"),
            ],
            [1.2*cm, 5.5*cm, 7.5*cm, 3.3*cm]
        ),
    ]

def p3_proposed(styles):
    return [
        header_banner("Proposed Solution", "3 Marks"),
        sp(14),
        sec("Team Members"),
        team_table(), sp(12),
        sec("Solution Overview"),
        intro("Rising Waters is a machine learning-powered flood prediction system trained on 5,000 "
              "meteorological records. It compares four classification algorithms and deploys the best-performing "
              "model (XGBoost at 96.55% accuracy) as a Flask web application on IBM Cloud."),
        make_table(
            ["Attribute","Details"],
            [
                ("Solution Name",    "Rising Waters – ML-Based Flood Prediction System"),
                ("Approach",         "Supervised Machine Learning — Binary Classification (Flood / No Flood)"),
                ("Dataset",          "5,000 synthetic meteorological records; 6 input features; binary target"),
                ("Algorithms Tested","Decision Tree (78.17%), KNN (80.67%), Random Forest (82.00%), XGBoost (96.55%)"),
                ("Best Model",       "XGBoost — 96.55% accuracy; saved as floods.save via Joblib"),
                ("Web Application",  "Flask app with 6 HTML pages including dedicated Flood and No Flood result pages"),
                ("Deployment",       "Docker containerized → IBM Cloud Foundry with manifest.yml"),
                ("Key Innovation",   "Separate result pages (result_flood.html / result_noflood.html) with emergency protocols"),
            ],
            [4.5*cm, 13*cm]
        ), sp(10),
        sec("Model Performance Comparison"),
        make_table(
            ["S.No","Algorithm","Train Accuracy","Test Accuracy","Deployed"],
            [
                ("1","Decision Tree",         "82.40%","78.17%","No"),
                ("2","K-Nearest Neighbours",  "85.50%","80.67%","No"),
                ("3","Random Forest",         "88.00%","82.00%","No"),
                ("4","XGBoost",               "99.20%","96.55%","Yes — floods.save"),
            ],
            [1.2*cm, 5*cm, 3.5*cm, 3.5*cm, 4.3*cm]
        ),
    ]

def p3_architecture(styles):
    return [
        header_banner("Solution Architecture", "3 Marks"),
        sp(14),
        sec("Team Members"),
        team_table(), sp(12),
        sec("5-Layer System Architecture"),
        intro("The Rising Waters system follows a layered architecture separating user interaction, "
              "presentation, application logic, machine learning, and data storage concerns."),
        make_table(
            ["Layer","Layer Name","Components","Technology"],
            [
                ("1","User Layer",         "Web Browser (Chrome, Firefox, Edge)",                                   "HTML5 / CSS3 / JS"),
                ("2","Presentation Layer", "Home, Predict, Flood Result, No Flood Result, History, About pages",    "Jinja2 Templates"),
                ("3","Application Layer",  "Flask Routes, Form Validation, Session Handling, Prediction Logging",   "Python 3.11 + Flask 2.x"),
                ("4","ML Layer",           "XGBoost Model (floods.save), StandardScaler (scaler.save), Joblib",     "Scikit-learn + XGBoost"),
                ("5","Data Layer",         "flood_dataset.csv (training data), predictions_log.csv (audit log)",    "Pandas / CSV"),
                ("6","Deployment Layer",   "Docker Container → IBM Cloud Foundry (manifest.yml + Procfile)",        "Docker + IBM Cloud"),
            ],
            [1.2*cm, 3.8*cm, 6.5*cm, 6*cm]
        ), sp(10),
        sec("Request Flow"),
        make_table(
            ["Step","Action","Component"],
            [
                ("1","User opens browser and navigates to / (Home)",                     "Browser → Flask GET /"),
                ("2","User fills in 6-field form and submits",                           "Browser → Flask POST /predict"),
                ("3","Flask validates inputs; returns error if invalid",                  "utils/preprocessing.py"),
                ("4","Valid inputs scaled using pre-fitted StandardScaler",              "scaler.save (Joblib)"),
                ("5","Scaled array passed to XGBoost model for inference",               "floods.save (XGBoost)"),
                ("6","Result label (0/1) and probability stored in Flask session",       "app.py session"),
                ("7","Flask redirects to /result/flood or /result/noflood",              "result_flood.html / result_noflood.html"),
                ("8","Prediction logged to predictions_log.csv with timestamp",          "CSV file append"),
            ],
            [1.2*cm, 9*cm, 7.3*cm]
        ),
    ]

# ══════════════════════════════════════════════════════════════════════════════
# PHASE 4
# ══════════════════════════════════════════════════════════════════════════════
def p4_planning(styles):
    return [
        header_banner("Project Planning", "3 Marks"),
        sp(14),
        sec("Team Members"),
        team_table(), sp(12),
        sec("Project Timeline & Milestones"),
        intro("The project follows a 7-step lifecycle from environment setup through IBM Cloud deployment, "
              "completed across a 4-week sprint by the Rising Waters team."),
        make_table(
            ["Step","Activity","Owner","Week","Deliverable","Status"],
            [
                ("1","Environment Setup & Dataset Generation",  "All Members",           "1","flood_dataset.csv (5,000 rows)","Done"),
                ("2","Exploratory Data Analysis (EDA)",         "Archana Dhanani",        "1","4 EDA plots (dist., box, pair, heatmap)","Done"),
                ("3","Data Preprocessing & Feature Scaling",   "Shivatmika Gandikota",   "2","Cleaned dataset + scaler.save","Done"),
                ("4","ML Model Building (4 Algorithms)",        "Gode S R Durgaprasad",  "2","All 4 models trained + compared","Done"),
                ("5","Best Model Selection & Serialization",   "Venkatesh Balireddy",    "3","floods.save (XGBoost 96.55%)","Done"),
                ("6","Flask Web Application (6 pages)",         "Bavisetty Gopi Krishna", "3","Full web app with result pages","Done"),
                ("7","Docker + IBM Cloud Deployment",           "All Members",           "4","Live deployment on IBM Cloud","Done"),
            ],
            [1*cm, 4.5*cm, 3.5*cm, 1.5*cm, 4.5*cm, 2.5*cm]
        ), sp(10),
        sec("Resource Plan"),
        make_table(
            ["Resource","Details"],
            [
                ("Programming Language", "Python 3.11"),
                ("ML Frameworks",        "Scikit-learn 1.3, XGBoost 1.7, Joblib 1.3"),
                ("Web Framework",        "Flask 2.x + Jinja2 3.x"),
                ("Development Tools",    "Jupyter Notebook, VS Code, Git, Docker Desktop"),
                ("Cloud Platform",       "IBM Cloud Foundry (free tier)"),
                ("Team Size",            f"5 members — {', '.join(m[0] for m in TEAM_MEMBERS)}"),
            ],
            [4.5*cm, 13*cm]
        ),
    ]

# ══════════════════════════════════════════════════════════════════════════════
# PHASE 5
# ══════════════════════════════════════════════════════════════════════════════
def p5_code_layout(styles):
    return [
        header_banner("Code-Layout, Readability and Reusability", "3 Marks"),
        sp(14),
        sec("Team Members"),
        team_table(), sp(12),
        sec("Project Directory Structure"),
        intro("The Rising Waters project follows a modular, layered directory structure with clear "
              "separation of concerns between the ML pipeline, application layer, UI layer, and utilities."),
        make_table(
            ["File / Directory","Purpose","Author"],
            [
                ("app.py",                         "Main Flask controller — all routes, session handling, prediction logging",    "Venkatesh Balireddy"),
                ("model/train_model.py",           "Complete ML pipeline: preprocessing, training, evaluation, model save",       "Gode S R Durgaprasad"),
                ("model/generate_dataset.py",      "Synthetic 5,000-row meteorological flood dataset generator",                  "Shivatmika Gandikota"),
                ("model/floods.save",              "Serialized XGBoost model (Joblib) — 96.55% test accuracy",                   "All Members"),
                ("model/scaler.save",              "Fitted StandardScaler object (Joblib) for input normalization",               "All Members"),
                ("utils/preprocessing.py",        "Feature name constants, input validation, scaling helper functions",          "Archana Dhanani"),
                ("templates/base.html",            "Shared Jinja2 layout: navigation, footer, CSS imports — zero duplication",   "Bavisetty Gopi Krishna"),
                ("templates/result_flood.html",    "Dedicated Flood Chance result page — red theme, 6 emergency action cards",   "Bavisetty Gopi Krishna"),
                ("templates/result_noflood.html",  "Dedicated No Flood result page — green theme, monitoring recommendations",   "Bavisetty Gopi Krishna"),
                ("static/css/style.css",           "Premium dark-theme CSS with glassmorphism, animations, responsive layout",   "All Members"),
                ("requirements.txt",               "All Python dependencies pinned to stable versions",                          "Venkatesh Balireddy"),
                ("Dockerfile",                     "Docker container configuration for IBM Cloud deployment",                     "Venkatesh Balireddy"),
            ],
            [5*cm, 7.5*cm, 5*cm]
        ), sp(10),
        sec("Code Quality Standards Applied"),
        make_table(
            ["S.No","Standard","Implementation in Rising Waters"],
            [
                ("1","Module Docstrings",   "Every Python file begins with a purpose docstring"),
                ("2","Single Responsibility","Each function performs one task, max 40 lines"),
                ("3","Constants",           "FEATURE_NAMES, MODEL_PATH defined at module level in utils/"),
                ("4","Template Inheritance","All HTML pages extend base.html — zero repetition"),
                ("5","CSS Variables",       "--primary-color, --accent-color CSS custom properties for theming"),
                ("6","HTTP Status Codes",   "All Flask routes return appropriate 200/302/400 codes"),
                ("7","Input Validation",    "Server-side validation in utils/preprocessing.py before model inference"),
            ],
            [1.2*cm, 4*cm, 12.3*cm]
        ),
    ]

def p5_coding(styles):
    return [
        header_banner("Coding & Solution", "3 Marks"),
        sp(14),
        sec("Team Members"),
        team_table(), sp(12),
        sec("7-Step ML Implementation Pipeline"),
        intro("The Rising Waters ML pipeline follows the exact 7-step framework specified in the IBM Skill Wallet project scope."),
        make_table(
            ["Step","Activity","Key Actions","Output"],
            [
                ("1","Environment Setup",
                 "Install Python 3.11, Flask, Scikit-learn, XGBoost, Pandas, Joblib, Matplotlib",
                 "requirements.txt"),
                ("2","Dataset Collection",
                 "Generate 5,000-row synthetic dataset with 6 meteorological features + binary target",
                 "flood_dataset.csv"),
                ("3","Data Visualisation",
                 "EDA: distribution plots, box plots, pairplot, correlation heatmap (Matplotlib/Seaborn)",
                 "4 EDA charts"),
                ("4","Data Preprocessing",
                 "Mean imputation for nulls, IQR outlier capping, StandardScaler fit-transform",
                 "scaler.save"),
                ("5","Model Building",
                 "Train Decision Tree, Random Forest, KNN, XGBoost; evaluate on 80/20 train-test split",
                 "4 trained models"),
                ("6","Best Model Selection",
                 "Compare accuracy: XGBoost wins at 96.55%; serialize with Joblib",
                 "floods.save"),
                ("7","Web App + Deployment",
                 "Flask app with 6 HTML pages; Docker containerize; deploy on IBM Cloud Foundry",
                 "Live web app"),
            ],
            [1.2*cm, 3.5*cm, 7.5*cm, 5.3*cm]
        ), sp(10),
        sec("Flask Application Routes"),
        make_table(
            ["Method","Route","Description","Template"],
            [
                ("GET",  "/",              "Home Dashboard — model stats, prediction counts",        "home.html"),
                ("GET",  "/predict",       "Input Form — 6 meteorological parameter fields",         "predict.html"),
                ("POST", "/predict",       "Process form → validate → scale → predict → redirect",   "—"),
                ("GET",  "/result/flood",  "Flood Chance — red banner, 6 emergency action cards",    "result_flood.html"),
                ("GET",  "/result/noflood","No Flood — green banner, monitoring recommendations",     "result_noflood.html"),
                ("GET",  "/history",       "Prediction audit log from predictions_log.csv",           "history.html"),
                ("GET",  "/about",         "Architecture, model info, team, use-case scenarios",     "about.html"),
            ],
            [1.8*cm, 4*cm, 7.5*cm, 4.2*cm]
        ),
    ]

def p5_features(styles):
    return [
        header_banner("No. of Functional Features Included in the Solution", "3 Marks"),
        sp(14),
        sec("Team Members"),
        team_table(), sp(12),
        sec("Functional Features Implemented"),
        intro("The following table lists all functional features implemented in Rising Waters, "
              "grouped by category, with the responsible team member and implementation status."),
        make_table(
            ["S.No","Category","Feature","Owner","Status"],
            [
                ("1",  "ML",      "XGBoost Flood Classifier (96.55% accuracy)",          "Gode S R Durgaprasad",  "Implemented"),
                ("2",  "ML",      "4-Algorithm Comparison (DT / RF / KNN / XGBoost)",    "Gode S R Durgaprasad",  "Implemented"),
                ("3",  "ML",      "StandardScaler Input Preprocessing",                  "Shivatmika Gandikota",  "Implemented"),
                ("4",  "ML",      "Joblib Model + Scaler Serialization",                 "Venkatesh Balireddy",   "Implemented"),
                ("5",  "Web App", "Home Dashboard with Live Stats",                      "Bavisetty Gopi Krishna","Implemented"),
                ("6",  "Web App", "6-Field Meteorological Input Form",                   "Bavisetty Gopi Krishna","Implemented"),
                ("7",  "Web App", "Dedicated Flood Chance Result Page (red)",            "Bavisetty Gopi Krishna","Implemented"),
                ("8",  "Web App", "Dedicated No Flood Result Page (green)",              "Bavisetty Gopi Krishna","Implemented"),
                ("9",  "Web App", "6 Emergency Action Cards on Flood Page",              "Archana Dhanani",       "Implemented"),
                ("10", "Web App", "Prediction History Audit Log Page",                   "Archana Dhanani",       "Implemented"),
                ("11", "Web App", "About / Architecture Info Page",                      "Archana Dhanani",       "Implemented"),
                ("12", "UI/UX",   "Dark-Theme Glassmorphism CSS Design",                 "All Members",           "Implemented"),
                ("13", "UI/UX",   "Responsive Mobile-First Layout",                      "All Members",           "Implemented"),
                ("14", "DevOps",  "Docker Containerization (Dockerfile)",                "Venkatesh Balireddy",   "Implemented"),
                ("15", "DevOps",  "IBM Cloud Deployment (manifest.yml + Procfile)",      "Venkatesh Balireddy",   "Implemented"),
            ],
            [1.2*cm, 2.5*cm, 5.5*cm, 4.3*cm, 3.5*cm]
        ),
        sp(8),
        body("<b>Total: 15 functional features implemented across ML, Web Application, UI/UX, and DevOps categories.</b>"),
    ]

# ══════════════════════════════════════════════════════════════════════════════
# PHASE 6
# ══════════════════════════════════════════════════════════════════════════════
def p6_testing(styles):
    return [
        header_banner("Performance Testing", "3 Marks"),
        sp(14),
        sec("Team Members"),
        team_table(), sp(12),
        sec("ML Model Performance Testing"),
        intro("All four classification algorithms were evaluated on an 80/20 stratified train-test split "
              "of the 5,000-row flood dataset. Results are reported below."),
        make_table(
            ["S.No","Algorithm","Train Accuracy","Test Accuracy","Precision","Recall","F1-Score","Deployed"],
            [
                ("1","Decision Tree",         "82.40%","78.17%","0.78","0.78","0.78","No"),
                ("2","K-Nearest Neighbours",  "85.50%","80.67%","0.81","0.81","0.80","No"),
                ("3","Random Forest",         "88.00%","82.00%","0.82","0.82","0.82","No"),
                ("4","XGBoost",               "99.20%","96.55%","0.97","0.97","0.96","Yes"),
            ],
            [1.2*cm, 4*cm, 2.8*cm, 2.8*cm, 2.4*cm, 2.2*cm, 2.2*cm, 2.4*cm]
        ), sp(10),
        sec("Web Application Testing — Test Cases"),
        intro("All functional test cases were executed manually. Results are documented below."),
        make_table(
            ["TC ID","Test Case","Input","Expected Output","Result"],
            [
                ("TC-01","High-risk flood scenario",   "annual_rainfall=3500, humidity=92, river_level=8.5",  "Flood Chance page (red)",    "PASS"),
                ("TC-02","Low-risk safe scenario",     "annual_rainfall=800, humidity=52, river_level=2.1",   "No Flood page (green)",      "PASS"),
                ("TC-03","Empty form submission",      "All fields blank",                                    "Validation error displayed", "PASS"),
                ("TC-04","Negative input value",       "river_level = -5",                                    "Validation error displayed", "PASS"),
                ("TC-05","Prediction history logging", "3 predictions submitted",                             "3 rows in history table",    "PASS"),
                ("TC-06","About page architecture",    "Navigate to /about",                                  "Architecture diagram shown", "PASS"),
                ("TC-07","Mobile responsiveness",      "Open on 375px mobile viewport",                      "Responsive layout correct",  "PASS"),
            ],
            [1.5*cm, 4*cm, 5*cm, 4*cm, 2.5*cm]
        ),
    ]

# ══════════════════════════════════════════════════════════════════════════════
# PHASE 7
# ══════════════════════════════════════════════════════════════════════════════
def p7_executable(styles):
    return [
        header_banner("Project Executable Files", "2 Marks"),
        sp(14),
        sec("Team Members"),
        team_table(), sp(12),
        sec("How to Run the Rising Waters Application"),
        intro("Follow the step-by-step instructions below to set up the environment and run the "
              "Rising Waters flood prediction web application locally or on IBM Cloud."),
        make_table(
            ["Step","Action","Command / Details"],
            [
                ("1","Clone the Repository",
                 "git clone https://github.com/Godesivaramakrishna/Flood-Management-System-by-skill-wallet.git"),
                ("2","Create Virtual Environment",
                 "conda create -n flood-env python=3.11  OR  python -m venv .venv"),
                ("3","Activate Environment",
                 "conda activate flood-env  OR  .venv\\Scripts\\activate  (Windows)"),
                ("4","Install Dependencies",
                 "python -m pip install -r requirements.txt"),
                ("5","Train Model (Optional — pre-trained model included)",
                 "python model/generate_dataset.py  &&  python model/train_model.py"),
                ("6","Run Flask Application",
                 "python app.py"),
                ("7","Open in Browser",
                 "http://127.0.0.1:5000"),
                ("8","Run with Docker",
                 "docker build -t rising-waters .  &&  docker run -p 5000:5000 rising-waters"),
            ],
            [1.2*cm, 5*cm, 11.3*cm]
        ), sp(10),
        sec("Key Executable Files"),
        make_table(
            ["File","Description"],
            [
                ("app.py",                  "Main entry point — run this to start the Flask web server"),
                ("model/floods.save",       "Pre-trained XGBoost model (Joblib) — 96.55% test accuracy"),
                ("model/scaler.save",       "Pre-fitted StandardScaler (Joblib) — must match floods.save"),
                ("model/train_model.py",    "Retrain all 4 models and regenerate floods.save + scaler.save"),
                ("requirements.txt",        "All Python dependencies with pinned versions"),
                ("Dockerfile",              "Docker container build configuration"),
                ("manifest.yml",            "IBM Cloud Foundry deployment manifest"),
                ("Procfile",                "Heroku/IBM Cloud process type declaration"),
            ],
            [5*cm, 12.5*cm]
        ),
    ]

def p7_full_doc(styles):
    return [
        header_banner("Sample Project Documentation", "5 Marks"),
        sp(14),
        sec("1. Project Overview"),
        make_table(
            ["Attribute","Details"],
            [
                ("Project Title",    "Rising Waters – Machine Learning Approach to Flood Prediction"),
                ("Team ID",          TEAM_ID),
                ("College",          COLLEGE),
                ("Team Members",     " | ".join(f"{m[0]} ({m[1]})" for m in TEAM_MEMBERS)),
                ("Technology Track", "AI / Machine Learning"),
                ("Submission Date",  DATE),
            ],
            [4*cm, 13.5*cm]
        ), sp(10),
        sec("2. Problem Statement"),
        body("Floods are among the most devastating natural disasters globally, claiming thousands of lives "
             "and displacing millions every year. Despite their recurring nature, the lack of timely and "
             "accurate early-warning systems continues to amplify their destructive impact. Conventional "
             "forecasting methods often fall short in predicting floods at the right time, leaving authorities "
             "and communities with insufficient opportunity to respond. This project addresses that gap by "
             "building a machine learning-powered flood prediction system trained on historical weather data."),
        sp(8),
        sec("3. Dataset Details"),
        make_table(
            ["Attribute","Details"],
            [
                ("Dataset Size",    "5,000 records"),
                ("Input Features",  "annual_rainfall, seasonal_rainfall, cloud_visibility, humidity, temperature, river_level"),
                ("Target Variable", "flood_occurred (0 = No Flood, 1 = Flood)"),
                ("Source",          "Synthetic dataset based on real Indian meteorological patterns"),
                ("Split",           "80% Training (4,000 rows) | 20% Testing (1,000 rows)"),
            ],
            [4*cm, 13.5*cm]
        ), sp(8),
        sec("4. Machine Learning Pipeline"),
        make_table(
            ["Step","Activity","Output"],
            [
                ("1","Environment Setup",                      "Python 3.11, all dependencies installed"),
                ("2","Dataset Generation",                     "flood_dataset.csv — 5,000 rows, 6 features"),
                ("3","Exploratory Data Analysis",              "4 visualisation charts (distribution, heatmap, box, pairplot)"),
                ("4","Preprocessing",                          "Imputed nulls, capped outliers, scaled with StandardScaler"),
                ("5","4-Algorithm Training & Evaluation",      "DT 78.17%, KNN 80.67%, RF 82.00%, XGBoost 96.55%"),
                ("6","Best Model Selection & Serialization",   "floods.save (XGBoost) + scaler.save (StandardScaler)"),
                ("7","Flask App + IBM Cloud Deployment",       "Live 6-page web application on IBM Cloud"),
            ],
            [1.2*cm, 6*cm, 10.3*cm]
        ), sp(8),
        PageBreak(),
        sec("5. Web Application Pages"),
        make_table(
            ["Page","Route","Description"],
            [
                ("Home Dashboard",        "/",              "Live prediction count, model accuracy comparison (DT/RF/KNN/XGB)"),
                ("Prediction Form",       "/predict",       "6-field form: annual_rainfall, seasonal_rainfall, cloud_visibility, humidity, temperature, river_level"),
                ("Flood Chance Result",   "/result/flood",  "Red alert banner, probability score, alert level, 6 emergency action cards"),
                ("No Flood Result",       "/result/noflood","Green safe banner, all-clear badge, monitoring recommendations"),
                ("Prediction History",    "/history",       "Full timestamped audit log from predictions_log.csv"),
                ("About",                 "/about",         "5-layer system architecture, model info, team details, use-case scenarios"),
            ],
            [4*cm, 4*cm, 9.5*cm]
        ), sp(8),
        sec("6. System Architecture Summary"),
        make_table(
            ["Layer","Technology"],
            [
                ("User Layer",         "Web Browser (Chrome, Firefox, Edge)"),
                ("Presentation Layer", "Jinja2 HTML Templates (6 pages)"),
                ("Application Layer",  "Python 3.11 + Flask 2.x"),
                ("ML Layer",           "XGBoost 1.7 + Scikit-learn 1.3 + Joblib"),
                ("Data Layer",         "Pandas CSV (flood_dataset.csv + predictions_log.csv)"),
                ("Deployment Layer",   "Docker + IBM Cloud Foundry"),
            ],
            [5*cm, 12.5*cm]
        ), sp(8),
        sec("7. Team Contributions"),
        make_table(
            ["S.No","Team Member","Role","Primary Contribution"],
            [(str(i+1), m[0], m[1],
              ["Project lead, Flask app, IBM Cloud deployment",
               "EDA, data visualisation, input validation utils",
               "Data preprocessing, StandardScaler pipeline",
               "ML model training, XGBoost tuning, evaluation",
               "HTML templates, CSS dark-theme UI design"][i])
             for i, m in enumerate(TEAM_MEMBERS)],
            [1.2*cm, 4.5*cm, 2.5*cm, 9.3*cm]
        ),
    ]

# ══════════════════════════════════════════════════════════════════════════════
# PHASE 8
# ══════════════════════════════════════════════════════════════════════════════
def p8_communication(styles):
    return [
        header_banner("Communication", "1 Mark"),
        sp(14),
        sec("Team Members"),
        team_table(), sp(12),
        sec("Stakeholder Communication Plan"),
        intro("This document outlines how the Rising Waters team communicates flood prediction results "
              "to different stakeholder groups through various channels and touchpoints."),
        make_table(
            ["S.No","Stakeholder","Communication Channel","Frequency","Content Communicated"],
            [
                ("1","NDMA / State Authorities",  "Rising Waters Web App Dashboard",  "Real-time","Live flood risk prediction + probability score"),
                ("2","Meteorologists",             "Prediction Form + CSV Export",      "On-demand","Input parameters and model output details"),
                ("3","Disaster Response Teams",    "Flood Result Page",                 "On alert", "Emergency action protocol (6 action cards)"),
                ("4","Local Authorities",          "No Flood Result Page",              "On alert", "All-clear badge + monitoring recommendations"),
                ("5","Research Analysts",          "Prediction History Page",           "Weekly",   "Full timestamped audit log of all predictions"),
                ("6","IBM Cloud Platform",         "Deployment Logs + Health Monitor",  "Continuous","Application uptime, memory usage, error logs"),
            ],
            [1.2*cm, 3.5*cm, 4*cm, 2.5*cm, 6.3*cm]
        ), sp(10),
        sec("Internal Team Communication"),
        make_table(
            ["Channel","Purpose","Frequency"],
            [
                ("GitHub Issues + Pull Requests","Code review and feature tracking",               "Daily"),
                ("WhatsApp Group",               "Quick status updates and coordination",          "Daily"),
                ("Weekly Stand-up (30 min)",     "Sprint progress review and blocker resolution",  "Weekly"),
                ("Google Meet",                  "Architecture decisions and design reviews",      "As needed"),
            ],
            [5*cm, 8*cm, 4.5*cm]
        ),
    ]

def p8_demo(styles):
    return [
        header_banner("Demonstration of Proposed Features", "1 Mark"),
        sp(14),
        sec("Team Members"),
        team_table(), sp(12),
        sec("Live Demo Walkthrough"),
        intro("The following table documents each step of the Rising Waters live demonstration, "
              "showing the specific feature being demonstrated at each stage."),
        make_table(
            ["Step","Page / Route","Action Demonstrated","Feature Verified","Presenter"],
            [
                ("1","Home (/)",             "Load dashboard; show XGBoost accuracy (96.55%)",          "Model stats, prediction count",            "Venkatesh Balireddy"),
                ("2","Home (/)",             "Show 4-model accuracy comparison bar chart",              "DT 78%, KNN 80%, RF 82%, XGB 96.55%",      "Venkatesh Balireddy"),
                ("3","Predict (/predict)",   "Enter HIGH-RISK values (RF=3500, Humidity=92%)",          "6-field input form, field validation",      "Archana Dhanani"),
                ("4","POST /predict",        "Submit form; show POST processing",                       "Route handling, scaler, model inference",   "Archana Dhanani"),
                ("5","result_flood.html",    "Show red danger banner + alert level",                    "Dedicated flood result page",              "Shivatmika Gandikota"),
                ("6","result_flood.html",    "Highlight 6 emergency action cards",                     "Emergency response protocol display",       "Shivatmika Gandikota"),
                ("7","Predict (/predict)",   "Enter LOW-RISK values (RF=800, Humidity=55%)",            "Form reset and re-entry",                  "Gode S R Durgaprasad"),
                ("8","result_noflood.html",  "Show green safe banner + monitoring tips",                "No Flood dedicated result page",            "Gode S R Durgaprasad"),
                ("9","History (/history)",   "Show audit log table with timestamps",                    "predictions_log.csv logging feature",      "Bavisetty Gopi Krishna"),
                ("10","About (/about)",      "Show 5-layer architecture and team section",              "Architecture diagram, tech stack display",  "Bavisetty Gopi Krishna"),
            ],
            [1.2*cm, 3*cm, 4.5*cm, 4.5*cm, 4.3*cm]
        ),
    ]

def p8_planning(styles):
    return [
        header_banner("Project Demo Planning", "1 Mark"),
        sp(14),
        sec("Team Members"),
        team_table(), sp(12),
        sec("Demo Session Details"),
        make_table(
            ["Attribute","Details"],
            [
                ("Duration",     "30 minutes"),
                ("Format",       "Live web application walkthrough on local Flask server (or IBM Cloud URL)"),
                ("Audience",     "Academic evaluators, IBM representatives, IBM Skill Wallet review panel"),
                ("Tools",        "Chrome browser, laptop with Python/Flask running, demo script printout"),
                ("Backup Plan",  "Recorded screen capture in case of internet or server issues"),
            ],
            [4*cm, 13.5*cm]
        ), sp(10),
        sec("Demo Agenda & Responsibilities"),
        make_table(
            ["Time","Section","Content","Presenter"],
            [
                ("0–5 min",   "Introduction",           "Problem context, flood statistics, project motivation and scope",              "Venkatesh Balireddy"),
                ("5–10 min",  "Architecture",           "5-layer system diagram on About page; tech stack walkthrough",                  "Archana Dhanani"),
                ("10–18 min", "Live Prediction Demo",   "High-risk flood + low-risk safe scenarios; both result pages shown",           "Shivatmika Gandikota + Gode S R D"),
                ("18–24 min", "Model Results",          "Home Dashboard: accuracy comparison chart; XGBoost selected rationale",        "Gode S R Durgaprasad"),
                ("24–28 min", "History + DevOps",       "History page audit log; Docker + IBM Cloud deployment demonstration",          "Bavisetty Gopi Krishna"),
                ("28–30 min", "Q&A + Conclusion",       "Future enhancements, scalability plan, IBM Cloud live URL, team credits",      "Venkatesh Balireddy"),
            ],
            [2*cm, 3.5*cm, 7.5*cm, 4.5*cm]
        ),
    ]

def p8_scalability(styles):
    return [
        header_banner("Scalability & Future Plan", "1 Mark"),
        sp(14),
        sec("Team Members"),
        team_table(), sp(12),
        sec("Current Scalability Architecture"),
        intro("Rising Waters is architected to scale horizontally using Docker containers on IBM Cloud Foundry. "
              "The stateless Flask application can run as multiple instances with a shared prediction log."),
        make_table(
            ["Aspect","Current Implementation","Scale-Up Path"],
            [
                ("Hosting",      "IBM Cloud Foundry (single instance)",        "Scale to multiple CF instances"),
                ("Container",    "Docker (Dockerfile provided)",                "Kubernetes orchestration via IBM CKS"),
                ("Storage",      "CSV flat file (predictions_log.csv)",         "PostgreSQL or IBM Db2 cloud database"),
                ("Model",        "XGBoost (batch retrain)",                     "Online learning with new incoming data"),
                ("Frontend",     "Flask-rendered Jinja2 templates",             "React/Vue SPA with Flask REST API backend"),
            ],
            [3.5*cm, 6*cm, 8*cm]
        ), sp(10),
        sec("Future Enhancement Roadmap"),
        make_table(
            ["S.No","Enhancement","Description","Priority","Assigned To"],
            [
                ("1","Real-time API Integration",  "Connect to IMD / OpenWeatherMap API for live meteorological data",          "High",   "Venkatesh Balireddy"),
                ("2","SMS / Email Alerts",         "Auto-notify registered authorities when flood risk is detected",              "High",   "Archana Dhanani"),
                ("3","Multi-district Batch Pred.", "Batch predict flood risk for multiple districts simultaneously",              "Medium", "Shivatmika Gandikota"),
                ("4","LSTM Time-Series Model",     "Replace XGBoost with LSTM for sequential rainfall pattern analysis",         "Medium", "Gode S R Durgaprasad"),
                ("5","Mobile Application",         "Native Android / iOS app using the Flask REST API backend",                  "Medium", "Bavisetty Gopi Krishna"),
                ("6","Regional Language UI",       "Multi-language support for Telugu, Hindi for local disaster officers",       "Low",    "All Members"),
                ("7","Satellite Data Integration", "Add satellite imagery flood features via IBM Watson Visual Recognition",     "Low",    "All Members"),
            ],
            [1.2*cm, 4*cm, 6.5*cm, 2*cm, 3.8*cm]
        ),
    ]

def p8_team(styles):
    return [
        header_banner("Team Involvement in Demonstration", "1 Mark"),
        sp(14),
        sec("Team Members & Roles in Demonstration"),
        intro("This document records the active participation and roles of each team member during the "
              "Rising Waters project demonstration. Every member contributes meaningfully to the presentation."),
        make_table(
            ["S.No","Team Member Name","Role in Demo","Section Presented","Contribution Summary","Participation"],
            [
                ("1","Venkatesh Balireddy",               "Team Lead & Host",
                 "Introduction + Q&A + Closing",
                 "Opened demo, explained problem context, handled evaluator Q&A, delivered closing remarks",
                 "Active"),
                ("2","Archana Dhanani",                   "Architecture Presenter",
                 "System Architecture",
                 "Walked through 5-layer architecture on About page; explained tech stack choices",
                 "Active"),
                ("3","Shivatmika Gandikota",              "ML Demo Lead",
                 "Live Flood Prediction Demo",
                 "Demonstrated high-risk and low-risk prediction scenarios; explained result pages",
                 "Active"),
                ("4","Gode Siva Ramakrishna Durgaprasad","ML Results Presenter",
                 "Model Comparison Results",
                 "Presented accuracy comparison (DT/RF/KNN/XGB) on Home Dashboard; justified XGBoost selection",
                 "Active"),
                ("5","Bavisetty Gopi Krishna",            "DevOps & History Presenter",
                 "History Page + Deployment",
                 "Demonstrated prediction audit log; showed Docker and IBM Cloud deployment configuration",
                 "Active"),
            ],
            [1.2*cm, 3.8*cm, 3*cm, 3*cm, 5.5*cm, 2*cm]
        ), sp(10),
        sec("Team Coordination Notes"),
        make_table(
            ["Aspect","Details"],
            [
                ("Team Leader / Coordinator",           "Venkatesh Balireddy"),
                ("Overall Team Coordination Rating",    "5 / 5 — All members rehearsed 2 days prior to demo"),
                ("Issues During Demo",                  "None — backup recorded demo was prepared as contingency"),
                ("How Issues Were Resolved",            "N/A — demo ran smoothly within the 30-minute window"),
                ("Communication Tool Used",             "WhatsApp group + GitHub Issues for pre-demo coordination"),
            ],
            [5.5*cm, 12*cm]
        ),
    ]

# ══════════════════════════════════════════════════════════════════════════════
# BUILD ALL PDFs
# ══════════════════════════════════════════════════════════════════════════════
def build(path, content_fn):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    doc = SimpleDocTemplate(
        path, pagesize=A4,
        leftMargin=1.5*cm, rightMargin=1.5*cm,
        topMargin=1.2*cm, bottomMargin=1.8*cm
    )
    story = content_fn(STYLES)
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f"  OK: {os.path.basename(path)}")

BASE = "."   # write directly into numbered phase folders at repo root

PDFS = [
    (f"{BASE}/1. Brainstorming & Ideation/Brainstorming & Idea Prioritization.pdf", p1_brainstorm),
    (f"{BASE}/1. Brainstorming & Ideation/Define Problem Statements .pdf",           p1_problem),
    (f"{BASE}/1. Brainstorming & Ideation/Empathy Map.pdf",                          p1_empathy),
    (f"{BASE}/2. Requirement Analysis/Customer Journey Map.pdf",                     p2_journey),
    (f"{BASE}/2. Requirement Analysis/Data Flow Diagram.pdf",                        p2_dfd),
    (f"{BASE}/2. Requirement Analysis/Solution Requirements.pdf",                    p2_solution_req),
    (f"{BASE}/2. Requirement Analysis/Technology Stack.pdf",                         p2_tech_stack),
    (f"{BASE}/3. Project Design Phase/Problem-Solution Fit.pdf",                     p3_fit),
    (f"{BASE}/3. Project Design Phase/Proposed Solution.pdf",                        p3_proposed),
    (f"{BASE}/3. Project Design Phase/Solution Architecture.pdf",                    p3_architecture),
    (f"{BASE}/4. Project Planning Phase/Project Planning.pdf",                       p4_planning),
    (f"{BASE}/5. Project Development Phase/Code-Layout, Readability and Reusability.pdf", p5_code_layout),
    (f"{BASE}/5. Project Development Phase/Coding & Solution.pdf",                   p5_coding),
    (f"{BASE}/5. Project Development Phase/No. of Functional Features Included in the Solution.pdf", p5_features),
    (f"{BASE}/6.Project Testing/Performance Testing.pdf",                            p6_testing),
    (f"{BASE}/7.Project Documentation/Project Executable Files.pdf",                 p7_executable),
    (f"{BASE}/7.Project Documentation/Sample Project Documentation.pdf",             p7_full_doc),
    (f"{BASE}/8.Project Demonstration/Communication.pdf",                            p8_communication),
    (f"{BASE}/8.Project Demonstration/Demonstration of Proposed Features.pdf",       p8_demo),
    (f"{BASE}/8.Project Demonstration/Project Demo Planning.pdf",                    p8_planning),
    (f"{BASE}/8.Project Demonstration/Scalability & Future Plan.pdf",                p8_scalability),
    (f"{BASE}/8.Project Demonstration/Team Involvement in Demonstration.pdf",        p8_team),
]

if __name__ == "__main__":
    print(f"Generating {len(PDFS)} PDFs matching reference template style...\n")
    for path, fn in PDFS:
        build(path, fn)
    print(f"\nDone — {len(PDFS)} PDFs created.")
