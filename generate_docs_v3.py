"""
generate_docs_v3.py
--------------------
Generates PDFs that EXACTLY match the user's first image reference:
  - Header: Two logos (left and right) extracted from the reference PDF
  - Title: Centered, Bold, Black text
  - Meta Table: Date, Team ID, Project Name, Max Marks (plain B&W table)
  - Content Tables: Plain B&W tables (no background colors, black grid)
Flood Management System content + correct team members.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT

W, H = A4

# ── Colors ────────────────────────────────────────────────────
BLACK  = colors.black
WHITE  = colors.white

# ── Team Info ─────────────────────────────────────────────────────────────────
TEAM_ID      = "Batch 2023-27 | ACOE"
PROJECT_NAME = "Rising Waters – ML-Based Flood Prediction System"
DATE         = "15 March 2026"

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
    s["title"] = ParagraphStyle("title", fontSize=16, fontName="Times-Bold",
        textColor=BLACK, alignment=TA_CENTER, leading=20, spaceAfter=20, spaceBefore=20)
    s["meta_key"] = ParagraphStyle("mk", fontSize=11, fontName="Times-Bold",
        textColor=BLACK, alignment=TA_LEFT)
    s["meta_val"] = ParagraphStyle("mv", fontSize=11, fontName="Times-Roman",
        textColor=BLACK, alignment=TA_LEFT)
    s["section"] = ParagraphStyle("section", fontSize=12, fontName="Times-Bold",
        textColor=BLACK, spaceBefore=14, spaceAfter=8)
    s["body"] = ParagraphStyle("body", fontSize=11, fontName="Times-Roman",
        textColor=BLACK, leading=15, spaceAfter=6, alignment=TA_JUSTIFY)
    s["th"] = ParagraphStyle("th", fontSize=11, fontName="Times-Bold",
        textColor=BLACK, alignment=TA_LEFT)
    s["td"] = ParagraphStyle("td", fontSize=11, fontName="Times-Roman",
        textColor=BLACK, alignment=TA_LEFT, leading=13)
    return s

STYLES = S()

# ── Logos Header ───────────────────────────────────────────────────────────
def header_logos():
    try:
        # SmartBridge on the left, SkillWallet on the right
        img_left = Image("logos/smartbridge.png", width=6*cm, height=2.8*cm)
        img_left.hAlign = 'LEFT'
        
        img_right = Image("logos/skillwallet.png", width=4.5*cm, height=2.1*cm)
        img_right.hAlign = 'RIGHT'
        
        tbl = Table([[img_left, img_right]], colWidths=[8*cm, 8*cm])
        tbl.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        return tbl
    except Exception as e:
        return Spacer(1, 1*cm) # Fallback if logos missing

# ── Metadata Banner ───────────────────────────────────────────────────────────
def header_banner(doc_title, max_marks):
    """Exact reference style: Logos -> Title -> B&W Table."""
    
    title_p  = Paragraph(f"{doc_title} Template" if not doc_title.endswith("Template") else doc_title, STYLES["title"])
    
    # Metadata table (Date | Team ID | Project Name | Maximum Marks)
    meta = Table(
        [
            [Paragraph("Date", STYLES["meta_key"]), Paragraph(DATE, STYLES["meta_val"])],
            [Paragraph("Team ID", STYLES["meta_key"]), Paragraph(TEAM_ID, STYLES["meta_val"])],
            [Paragraph("Project Name", STYLES["meta_key"]), Paragraph(PROJECT_NAME, STYLES["meta_val"])],
            [Paragraph("Maximum Marks", STYLES["meta_key"]), Paragraph(max_marks, STYLES["meta_val"])],
        ],
        colWidths=[4*cm, 12.5*cm]
    )
    meta.setStyle(TableStyle([
        ("GRID",          (0,0),(-1,-1), 1, BLACK),
        ("TOPPADDING",    (0,0),(-1,-1), 8),
        ("BOTTOMPADDING", (0,0),(-1,-1), 8),
        ("LEFTPADDING",   (0,0),(-1,-1), 8),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
    ]))

    return [header_logos(), title_p, meta]

# ── Table builder ─────────────────────────────────────────────────────────────
def make_table(headers, rows, col_widths):
    header_row = [Paragraph(h, STYLES["th"]) for h in headers]
    data = [header_row]
    for row in rows:
        data.append([
            Paragraph(str(c), STYLES["td"]) for c in row
        ])
    tbl = Table(data, colWidths=col_widths, repeatRows=1)
    tbl.setStyle(TableStyle([
        ("GRID",          (0,0),(-1,-1), 1, BLACK),
        ("TOPPADDING",    (0,0),(-1,-1), 8),
        ("BOTTOMPADDING", (0,0),(-1,-1), 8),
        ("LEFTPADDING",   (0,0),(-1,-1), 8),
        ("RIGHTPADDING",  (0,0),(-1,-1), 8),
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
    ]))
    return tbl

def sec(text):
    return Paragraph(text, STYLES["section"])

def body(text):
    return Paragraph(text, STYLES["body"])

def sp(n=8):
    return Spacer(1, n)

# ── Team members table (reusable) ──────────────────────────────────────────────
def team_table():
    rows = [(str(i+1), m[0], "", m[1]) for i, m in enumerate(TEAM_MEMBERS)]
    # In the screenshot for Phase 1, the columns are S.No, Team Member, Idea, Category, Group No.
    # Let's make a generic team members table for sections that need it.
    return make_table(["S.No", "Team Member Name", "Role"], 
                      [(str(i+1), m[0], m[1]) for i, m in enumerate(TEAM_MEMBERS)],
                      [1.5*cm, 9*cm, 6*cm])

# ══════════════════════════════════════════════════════════════════════════════
# PHASE 1
# ══════════════════════════════════════════════════════════════════════════════
def p1_brainstorm(styles):
    return header_banner("Brainstorming & Idea Prioritization", "3 Marks") + [
        sp(14),
        sec("Step 1: Brainstorm and Idea Listing"),
        body("Each team member lists out as many ideas as possible without judging them at this stage."),
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
            [1.5*cm, 4*cm, 5.5*cm, 3*cm, 2.5*cm]
        ), sp(12),
        sec("Step 2: Idea Prioritization"),
        body("Rate each grouped idea on feasibility and importance, then select the final idea(s) to move forward with."),
        make_table(
            ["Group No.","Final Idea","Feasibility","Importance","Priority","Selected"],
            [
                ("1","XGBoost ML Flood Prediction + Flask Web App","High","High","1","Yes"),
                ("2","IoT Sensor Network",                          "Medium","High","2","No"),
                ("3","Satellite Imagery CV",                        "Low","High","3","No"),
            ],
            [2*cm, 5*cm, 2.5*cm, 2.5*cm, 2*cm, 2.5*cm]
        ),
    ]

def p1_problem(styles):
    return header_banner("Define Problem Statements", "3 Marks") + [
        sp(14),
        sec("Step 1: Team Members"),
        team_table(), sp(12),
        sec("Problem Statement Definition"),
        body("A clear problem statement focuses the team on the core challenge and guides the design of the solution."),
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
            [4.5*cm, 12*cm]
        ),
    ]

def p1_empathy(styles):
    return header_banner("Empathy Map", "3 Marks") + [
        sp(14),
        sec("Primary User: Disaster Management Officer"),
        body("The empathy map captures the thoughts, feelings, behaviours, and pain points of the "
              "primary user of the Rising Waters flood prediction system."),
        make_table(
            ["Quadrant","Key Insights"],
            [
                ("THINKS",
                 "\"Will rainfall data be enough to predict flooding accurately?\"  \n"
                 "\"Can I trust the model output for critical decisions?\"  \n"
                 "\"How do I explain results to community leaders?\""),
                ("FEELS",
                 "Anxious about missing a real flood event (false negatives).  \n"
                 "Relieved when system shows a clear No Flood result.  \n"
                 "Confident when model accuracy (96.55%) is displayed prominently."),
                ("SAYS",
                 "\"We need faster predictions before monsoon season.\"  \n"
                 "\"The system should clearly tell us what action to take.\"  \n"
                 "\"We need a history log to review past predictions.\""),
                ("DOES",
                 "Manually collects rainfall data from weather stations.  \n"
                 "Enters readings into the 6-field prediction form.  \n"
                 "Shares flood/no-flood result with field teams.  \n"
                 "Logs predictions for audit."),
                ("PAIN POINTS",
                 "No centralized ML platform for flood risk prediction.  \n"
                 "Slow manual analysis delays emergency response.  \n"
                 "No emergency action guidance alongside predictions."),
                ("GAINS",
                 "Real-time flood risk classification in <2 seconds.  \n"
                 "6 emergency action cards displayed on Flood Result page.  \n"
                 "Full prediction audit history with timestamps."),
            ],
            [3.5*cm, 13*cm]
        ),
    ]

# ══════════════════════════════════════════════════════════════════════════════
# PHASE 2
# ══════════════════════════════════════════════════════════════════════════════
def p2_journey(styles):
    return header_banner("Customer Journey Map", "2 Marks") + [
        sp(14),
        sec("User Journey: Disaster Management Officer Using Rising Waters"),
        make_table(
            ["Stage","User Action","Touchpoint","Emotion","Opportunity"],
            [
                ("1. Awareness",  "Learns about the flood prediction web app",          "Training",                 "Curious",   "Promote via NDMA channels"),
                ("2. Access",     "Opens Rising Waters web app on browser",             "Home Dashboard (/)",       "Neutral",   "Show live model accuracy"),
                ("3. Input",      "Enters 6 meteorological readings into the form",     "Predict Page (/predict)",  "Focused",   "Add field tooltips"),
                ("4. Submit",     "Clicks 'Predict Flood Risk' button",                 "POST /predict route",      "Anxious",   "Show loading indicator"),
                ("5. Flood Alert","Views red Flood Chance page with emergency cards",   "result_flood.html",        "Alarmed",   "Display 6 action cards"),
                ("6. Safe Alert", "Views green No Flood page with monitoring tips",     "result_noflood.html",      "Relieved",  "Show monitoring tips"),
                ("7. History",    "Reviews audit log of all past predictions",          "History Page (/history)",  "Confident", "Add CSV export"),
                ("8. Report",     "Shares results with field teams and authorities",    "External channels",        "Empowered", "Add print button"),
            ],
            [2.5*cm, 4*cm, 3.5*cm, 2*cm, 4.5*cm]
        ),
    ]

def p2_dfd(styles):
    return header_banner("Data Flow Diagram", "2 Marks") + [
        sp(14),
        sec("Level 0 — Context Diagram"),
        make_table(
            ["Element","Description"],
            [
                ("External Entity", "Disaster Management Officer / Meteorologist"),
                ("System",          "Rising Waters Flood Prediction System (Flask + XGBoost)"),
                ("Input Flow",      "annual_rainfall, seasonal_rainfall, cloud_visibility, humidity, temperature, river_level"),
                ("Output Flow",     "Binary prediction label (Flood / No Flood) + probability score + emergency protocol"),
            ],
            [4*cm, 12.5*cm]
        ), sp(12),
        sec("Level 1 — Internal Data Flow"),
        make_table(
            ["Process ID","Process Name","Input","Output","Data Store"],
            [
                ("P1", "Form Input Capture",   "User web form values",      "Raw feature dictionary",       "—"),
                ("P2", "Input Validation",      "Raw feature dict",          "Validated dict / Error msg",   "—"),
                ("P3", "Feature Scaling",       "Validated features",        "Scaled NumPy array",           "scaler.save"),
                ("P4", "ML Prediction",         "Scaled NumPy array",        "Label (0/1) + Probability",   "floods.save"),
                ("P5", "Result Routing",        "Prediction label",          "HTTP redirect to result page", "—"),
                ("P6", "Prediction Logging",    "All inputs + result",       "New row appended",             "predictions_log.csv"),
            ],
            [1.5*cm, 3.5*cm, 3.5*cm, 4*cm, 4*cm]
        ),
    ]

def p2_solution_req(styles):
    return header_banner("Solution Requirements", "2 Marks") + [
        sp(14),
        sec("Functional Requirements"),
        make_table(
            ["Req. ID","Requirement","Priority"],
            [
                ("FR-01", "System shall accept 6 meteorological inputs via a web form",                        "High"),
                ("FR-02", "System shall validate all inputs and return meaningful error messages",              "High"),
                ("FR-03", "System shall scale inputs using the pre-fitted StandardScaler (scaler.save)",       "High"),
                ("FR-04", "System shall load XGBoost model (floods.save) and return binary classification",   "High"),
                ("FR-05", "System shall display a dedicated Flood Chance result page",                         "High"),
                ("FR-06", "System shall display a dedicated No Flood Chance result page",                      "High"),
                ("FR-07", "System shall log every prediction with timestamp to predictions_log.csv",           "Medium"),
                ("FR-08", "System shall display full prediction history on the History page",                  "Medium"),
                ("FR-09", "System shall show model accuracy comparison chart on the Home Dashboard",           "Medium"),
            ],
            [2*cm, 11*cm, 3.5*cm]
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
            [2*cm, 3.5*cm, 11*cm]
        ),
    ]

def p2_tech_stack(styles):
    return header_banner("Technology Stack", "2 Marks") + [
        sp(14),
        sec("Technology Stack Details"),
        make_table(
            ["S.No","Architecture Component","Technology Chosen","Justification / Purpose"],
            [
                ("1",  "Machine Learning",         "XGBoost 1.7 + Scikit-learn",
                 "Best accuracy (96.55%) among 4 tested algorithms; fast inference"),
                ("2",  "Data Processing",          "Pandas + NumPy",
                 "Efficient tabular data manipulation and array operations"),
                ("3",  "Model Serialization",      "Joblib",
                 "Save and load XGBoost model and StandardScaler"),
                ("4",  "Backend / Server-Side",    "Python 3.11 + Flask",
                 "Lightweight WSGI framework; integrates directly with ML objects"),
                ("5",  "Frontend / Client-Side",   "HTML5 + CSS3 + JS",
                 "Responsive design; no framework overhead"),
                ("6",  "Templating Engine",        "Jinja2",
                 "Server-side HTML rendering; template inheritance"),
                ("7",  "Cloud / Hosting",          "IBM Cloud Foundry",
                 "Free-tier cloud hosting; seamless deployment"),
                ("8",  "Containerization",         "Docker",
                 "Reproducible deployment environment; easy scaling"),
                ("9",  "Version Control",          "Git + GitHub",
                 "Source code management; collaborative development"),
            ],
            [1.2*cm, 4*cm, 4*cm, 7.3*cm]
        ),
    ]

# ══════════════════════════════════════════════════════════════════════════════
# PHASE 3
# ══════════════════════════════════════════════════════════════════════════════
def p3_fit(styles):
    return header_banner("Problem-Solution Fit", "3 Marks") + [
        sp(14),
        sec("Problem-Solution Fit Analysis"),
        make_table(
            ["S.No","Problem Identified","Solution Feature","Fit Level"],
            [
                ("1","No real-time ML-powered flood prediction tool available",
                 "XGBoost classifier (floods.save) achieving 96.55% accuracy",
                 "Strong"),
                ("2","Complex meteorological data difficult to interpret manually",
                 "6-field standardized input form with field descriptions",
                 "Strong"),
                ("3","No emergency response guidance for prediction outputs",
                 "Flood Result page with 6 emergency protocol action cards",
                 "Strong"),
                ("4","No accessible web interface for non-technical users",
                 "Flask web app with intuitive UI accessible on any browser",
                 "Strong"),
                ("5","No prediction history or audit trail",
                 "predictions_log.csv + History page with full timestamped log",
                 "Strong"),
                ("6","Lack of 24/7 cloud accessibility for disaster teams",
                 "IBM Cloud Foundry deployment with Docker containerization",
                 "Strong"),
                ("7","Manual comparison of multiple ML models is time-consuming",
                 "Home Dashboard with built-in accuracy comparison",
                 "Medium"),
            ],
            [1.2*cm, 5.5*cm, 6.5*cm, 3.3*cm]
        ),
    ]

def p3_proposed(styles):
    return header_banner("Proposed Solution", "3 Marks") + [
        sp(14),
        sec("Solution Overview"),
        make_table(
            ["Attribute","Details"],
            [
                ("Solution Name",    "Rising Waters – ML-Based Flood Prediction System"),
                ("Approach",         "Supervised Machine Learning — Binary Classification (Flood / No Flood)"),
                ("Dataset",          "5,000 synthetic meteorological records; 6 input features; binary target"),
                ("Algorithms Tested","Decision Tree (78.17%), KNN (80.67%), Random Forest (82.00%), XGBoost (96.55%)"),
                ("Best Model",       "XGBoost — 96.55% accuracy; saved as floods.save via Joblib"),
                ("Web Application",  "Flask app with 6 HTML pages including dedicated result pages"),
                ("Deployment",       "Docker containerized → IBM Cloud Foundry"),
                ("Key Innovation",   "Actionable emergency protocols based on prediction outcome"),
            ],
            [4.5*cm, 12*cm]
        ), sp(10),
        sec("Model Performance Comparison"),
        make_table(
            ["S.No","Algorithm","Train Accuracy","Test Accuracy","Deployed"],
            [
                ("1","Decision Tree",         "82.40%","78.17%","No"),
                ("2","K-Nearest Neighbours",  "85.50%","80.67%","No"),
                ("3","Random Forest",         "88.00%","82.00%","No"),
                ("4","XGBoost",               "99.20%","96.55%","Yes"),
            ],
            [1.2*cm, 5*cm, 3.5*cm, 3.5*cm, 3.3*cm]
        ),
    ]

def p3_architecture(styles):
    return header_banner("Solution Architecture", "3 Marks") + [
        sp(14),
        sec("5-Layer System Architecture"),
        make_table(
            ["Layer","Layer Name","Components","Technology"],
            [
                ("1","User Layer",         "Web Browser",                                                           "HTML5 / CSS3 / JS"),
                ("2","Presentation Layer", "Home, Predict, Flood Result, No Flood Result, History, About pages",    "Jinja2 Templates"),
                ("3","Application Layer",  "Flask Routes, Form Validation, Prediction Logging",                     "Python 3.11 + Flask"),
                ("4","ML Layer",           "XGBoost Model, StandardScaler, Joblib",                                 "Scikit-learn + XGBoost"),
                ("5","Data Layer",         "flood_dataset.csv, predictions_log.csv",                                "Pandas / CSV"),
                ("6","Deployment Layer",   "Docker Container, IBM Cloud Foundry",                                   "Docker + IBM Cloud"),
            ],
            [1.2*cm, 3.5*cm, 6.5*cm, 5.3*cm]
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
            [1.2*cm, 9*cm, 6.3*cm]
        ),
    ]

# ══════════════════════════════════════════════════════════════════════════════
# PHASE 4
# ══════════════════════════════════════════════════════════════════════════════
def p4_planning(styles):
    return header_banner("Project Planning", "3 Marks") + [
        sp(14),
        sec("Project Timeline & Milestones"),
        make_table(
            ["Step","Activity","Owner","Week","Status"],
            [
                ("1","Environment Setup & Dataset Generation",  "All Members",           "1","Done"),
                ("2","Exploratory Data Analysis (EDA)",         "Archana Dhanani",        "1","Done"),
                ("3","Data Preprocessing & Feature Scaling",   "Shivatmika Gandikota",   "2","Done"),
                ("4","ML Model Building (4 Algorithms)",        "Gode S R Durgaprasad",  "2","Done"),
                ("5","Best Model Selection & Serialization",   "Venkatesh Balireddy",    "3","Done"),
                ("6","Flask Web Application (6 pages)",         "Bavisetty Gopi Krishna", "3","Done"),
                ("7","Docker + IBM Cloud Deployment",           "All Members",           "4","Done"),
            ],
            [1*cm, 6*cm, 4.5*cm, 2.5*cm, 2.5*cm]
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
                ("Team Size",            f"5 members"),
            ],
            [4.5*cm, 12*cm]
        ),
    ]

# ══════════════════════════════════════════════════════════════════════════════
# PHASE 5
# ══════════════════════════════════════════════════════════════════════════════
def p5_code_layout(styles):
    return header_banner("Code-Layout, Readability and Reusability", "3 Marks") + [
        sp(14),
        sec("Project Directory Structure"),
        make_table(
            ["File / Directory","Purpose","Author"],
            [
                ("app.py",                         "Main Flask controller — all routes, session handling",    "Venkatesh B."),
                ("model/train_model.py",           "Complete ML pipeline: preprocessing, training, save",     "Gode S R D."),
                ("model/generate_dataset.py",      "Synthetic 5,000-row meteorological dataset generator",     "Shivatmika G."),
                ("model/floods.save",              "Serialized XGBoost model (Joblib) — 96.55% accuracy",     "All Members"),
                ("model/scaler.save",              "Fitted StandardScaler object (Joblib) for normalization", "All Members"),
                ("utils/preprocessing.py",        "Validation and scaling helper functions",                 "Archana D."),
                ("templates/base.html",            "Shared Jinja2 layout: navigation, footer, CSS imports",  "Bavisetty G. K."),
                ("templates/result_flood.html",    "Dedicated Flood Chance result page",                     "Bavisetty G. K."),
                ("templates/result_noflood.html",  "Dedicated No Flood result page",                         "Bavisetty G. K."),
                ("static/css/style.css",           "Premium UI design",                                       "All Members"),
                ("requirements.txt",               "Python dependencies",                                     "Venkatesh B."),
                ("Dockerfile",                     "Docker container configuration",                          "Venkatesh B."),
            ],
            [4.5*cm, 8.5*cm, 3.5*cm]
        ), sp(10),
        sec("Code Quality Standards Applied"),
        make_table(
            ["S.No","Standard","Implementation"],
            [
                ("1","Module Docstrings",   "Every Python file begins with a purpose docstring"),
                ("2","Single Responsibility","Each function performs one task, max 40 lines"),
                ("3","Constants",           "FEATURE_NAMES, MODEL_PATH defined at module level"),
                ("4","Template Inheritance","All HTML pages extend base.html — zero repetition"),
                ("5","CSS Variables",       "--primary-color, --accent-color used for theming"),
                ("6","HTTP Status Codes",   "All Flask routes return appropriate status codes"),
                ("7","Input Validation",    "Server-side validation before model inference"),
            ],
            [1.2*cm, 4*cm, 11.3*cm]
        ),
    ]

def p5_coding(styles):
    return header_banner("Coding & Solution", "3 Marks") + [
        sp(14),
        sec("7-Step ML Implementation Pipeline"),
        make_table(
            ["Step","Activity","Key Actions","Output"],
            [
                ("1","Environment Setup",
                 "Install Python, Flask, Scikit-learn, XGBoost, Pandas",
                 "requirements.txt"),
                ("2","Dataset Collection",
                 "Generate 5,000-row synthetic dataset with 6 features",
                 "flood_dataset.csv"),
                ("3","Data Visualisation",
                 "EDA: distribution plots, box plots, pairplot, heatmap",
                 "4 EDA charts"),
                ("4","Data Preprocessing",
                 "Mean imputation, IQR outlier capping, StandardScaler",
                 "scaler.save"),
                ("5","Model Building",
                 "Train Decision Tree, Random Forest, KNN, XGBoost",
                 "4 trained models"),
                ("6","Best Model Selection",
                 "Compare accuracy: XGBoost wins at 96.55%; serialize",
                 "floods.save"),
                ("7","Web App + Deployment",
                 "Flask app with 6 pages; Docker containerize; deploy",
                 "Live web app"),
            ],
            [1.2*cm, 3.5*cm, 7.5*cm, 4.3*cm]
        ), sp(10),
        sec("Flask Application Routes"),
        make_table(
            ["Method","Route","Description","Template"],
            [
                ("GET",  "/",              "Home Dashboard",                                         "home.html"),
                ("GET",  "/predict",       "Input Form",                                             "predict.html"),
                ("POST", "/predict",       "Process form → validate → scale → predict → redirect",   "—"),
                ("GET",  "/result/flood",  "Flood Chance — emergency action cards",                  "result_flood.html"),
                ("GET",  "/result/noflood","No Flood — monitoring recommendations",                  "result_noflood.html"),
                ("GET",  "/history",       "Prediction audit log from predictions_log.csv",          "history.html"),
                ("GET",  "/about",         "Architecture, model info, team details",                 "about.html"),
            ],
            [1.8*cm, 3.5*cm, 7.5*cm, 3.7*cm]
        ),
    ]

def p5_features(styles):
    return header_banner("No. of Functional Features Included in the Solution", "3 Marks") + [
        sp(14),
        sec("Functional Features Implemented"),
        make_table(
            ["S.No","Category","Feature","Owner","Status"],
            [
                ("1",  "ML",      "XGBoost Flood Classifier (96.55% accuracy)",          "Gode S R Durgaprasad",  "Implemented"),
                ("2",  "ML",      "4-Algorithm Comparison (DT / RF / KNN / XGBoost)",    "Gode S R Durgaprasad",  "Implemented"),
                ("3",  "ML",      "StandardScaler Input Preprocessing",                  "Shivatmika Gandikota",  "Implemented"),
                ("4",  "ML",      "Joblib Model + Scaler Serialization",                 "Venkatesh Balireddy",   "Implemented"),
                ("5",  "Web App", "Home Dashboard with Live Stats",                      "Bavisetty Gopi Krishna","Implemented"),
                ("6",  "Web App", "6-Field Meteorological Input Form",                   "Bavisetty Gopi Krishna","Implemented"),
                ("7",  "Web App", "Dedicated Flood Chance Result Page",                  "Bavisetty Gopi Krishna","Implemented"),
                ("8",  "Web App", "Dedicated No Flood Result Page",                      "Bavisetty Gopi Krishna","Implemented"),
                ("9",  "Web App", "6 Emergency Action Cards on Flood Page",              "Archana Dhanani",       "Implemented"),
                ("10", "Web App", "Prediction History Audit Log Page",                   "Archana Dhanani",       "Implemented"),
                ("11", "Web App", "About / Architecture Info Page",                      "Archana Dhanani",       "Implemented"),
                ("12", "UI/UX",   "Dark-Theme UI Design",                                "All Members",           "Implemented"),
                ("13", "UI/UX",   "Responsive Mobile-First Layout",                      "All Members",           "Implemented"),
                ("14", "DevOps",  "Docker Containerization (Dockerfile)",                "Venkatesh Balireddy",   "Implemented"),
                ("15", "DevOps",  "IBM Cloud Deployment",                                "Venkatesh Balireddy",   "Implemented"),
            ],
            [1.2*cm, 2.5*cm, 5.5*cm, 4.3*cm, 3*cm]
        ),
    ]

# ══════════════════════════════════════════════════════════════════════════════
# PHASE 6
# ══════════════════════════════════════════════════════════════════════════════
def p6_testing(styles):
    return header_banner("Performance Testing", "3 Marks") + [
        sp(14),
        sec("ML Model Performance Testing"),
        make_table(
            ["S.No","Algorithm","Train Acc","Test Acc","Precision","Recall","F1-Score","Deployed"],
            [
                ("1","Decision Tree",         "82.40%","78.17%","0.78","0.78","0.78","No"),
                ("2","K-Nearest Neighbours",  "85.50%","80.67%","0.81","0.81","0.80","No"),
                ("3","Random Forest",         "88.00%","82.00%","0.82","0.82","0.82","No"),
                ("4","XGBoost",               "99.20%","96.55%","0.97","0.97","0.96","Yes"),
            ],
            [1.2*cm, 4*cm, 2.2*cm, 2.2*cm, 1.8*cm, 1.8*cm, 1.8*cm, 1.5*cm]
        ), sp(10),
        sec("Web Application Testing — Test Cases"),
        make_table(
            ["TC ID","Test Case","Input","Expected Output","Result"],
            [
                ("TC-01","High-risk flood scenario",   "annual_rainfall=3500, humidity=92",   "Flood Chance page",          "PASS"),
                ("TC-02","Low-risk safe scenario",     "annual_rainfall=800, humidity=52",    "No Flood page",              "PASS"),
                ("TC-03","Empty form submission",      "All fields blank",                    "Validation error displayed", "PASS"),
                ("TC-04","Negative input value",       "river_level = -5",                    "Validation error displayed", "PASS"),
                ("TC-05","Prediction history logging", "3 predictions submitted",             "3 rows in history table",    "PASS"),
                ("TC-06","About page architecture",    "Navigate to /about",                  "Architecture diagram shown", "PASS"),
                ("TC-07","Mobile responsiveness",      "Open on 375px mobile viewport",       "Responsive layout correct",  "PASS"),
            ],
            [1.5*cm, 4*cm, 4.5*cm, 4*cm, 2.5*cm]
        ),
    ]

# ══════════════════════════════════════════════════════════════════════════════
# PHASE 7
# ══════════════════════════════════════════════════════════════════════════════
def p7_executable(styles):
    return header_banner("Project Executable Files", "2 Marks") + [
        sp(14),
        sec("How to Run the Rising Waters Application"),
        make_table(
            ["Step","Action","Command / Details"],
            [
                ("1","Clone the Repository",     "git clone https://github.com/Godesivaramakrishna/Flood-Management-System-by-skill-wallet.git"),
                ("2","Create Virtual Env",       "python -m venv .venv"),
                ("3","Activate Environment",     ".venv\\Scripts\\activate  (Windows)"),
                ("4","Install Dependencies",     "pip install -r requirements.txt"),
                ("5","Train Model (Optional)",   "python model/train_model.py"),
                ("6","Run Flask Application",    "python app.py"),
                ("7","Open in Browser",          "http://127.0.0.1:5000"),
                ("8","Run with Docker",          "docker build -t rising-waters .  &&  docker run -p 5000:5000 rising-waters"),
            ],
            [1.2*cm, 4*cm, 11.3*cm]
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
            [4.5*cm, 12*cm]
        ),
    ]

def p7_full_doc(styles):
    return header_banner("Sample Project Documentation", "5 Marks") + [
        sp(14),
        sec("1. Project Overview"),
        make_table(
            ["Attribute","Details"],
            [
                ("Project Title",    PROJECT_NAME),
                ("Team ID",          TEAM_ID),
                ("Team Members",     " | ".join(f"{m[0]}" for m in TEAM_MEMBERS)),
                ("Technology Track", "AI / Machine Learning"),
            ],
            [4*cm, 12.5*cm]
        ), sp(8),
        sec("2. Problem Statement"),
        body("Floods are among the most devastating natural disasters globally, claiming thousands of lives "
             "and displacing millions every year. Conventional forecasting methods lack the predictive "
             "intelligence required for timely early warnings. This project builds a machine learning-powered "
             "flood prediction web application to provide accurate, real-time risk assessment."),
        sp(8),
        sec("3. Dataset Details"),
        make_table(
            ["Attribute","Details"],
            [
                ("Dataset Size",    "5,000 records"),
                ("Input Features",  "annual_rainfall, seasonal_rainfall, cloud_visibility, humidity, temperature, river_level"),
                ("Target Variable", "flood_occurred (0 = No Flood, 1 = Flood)"),
                ("Source",          "Synthetic dataset based on real meteorological patterns"),
                ("Split",           "80% Training (4,000 rows) | 20% Testing (1,000 rows)"),
            ],
            [4*cm, 12.5*cm]
        ), sp(8),
        sec("4. Machine Learning Pipeline"),
        make_table(
            ["Step","Activity","Output"],
            [
                ("1","Environment Setup",                      "Python 3.11, all dependencies installed"),
                ("2","Dataset Generation",                     "flood_dataset.csv"),
                ("3","Exploratory Data Analysis",              "4 visualisation charts"),
                ("4","Preprocessing",                          "Imputed nulls, scaled with StandardScaler"),
                ("5","4-Algorithm Training",                   "DT 78.17%, KNN 80.67%, RF 82.00%, XGBoost 96.55%"),
                ("6","Best Model Selection",                   "floods.save (XGBoost) + scaler.save"),
                ("7","Deployment",                             "Live web application on IBM Cloud"),
            ],
            [1.2*cm, 5.5*cm, 9.8*cm]
        ), sp(8),
        PageBreak(),
        sec("5. Web Application Pages"),
        make_table(
            ["Page","Route","Description"],
            [
                ("Home Dashboard",        "/",              "Live prediction count, model accuracy comparison"),
                ("Prediction Form",       "/predict",       "6-field form for meteorological inputs"),
                ("Flood Chance Result",   "/result/flood",  "Red alert banner, 6 emergency action cards"),
                ("No Flood Result",       "/result/noflood","Green safe banner, monitoring recommendations"),
                ("Prediction History",    "/history",       "Full timestamped audit log"),
                ("About",                 "/about",         "5-layer system architecture, model info, team details"),
            ],
            [4*cm, 3*cm, 9.5*cm]
        ), sp(8),
        sec("6. System Architecture Summary"),
        make_table(
            ["Layer","Technology"],
            [
                ("User Layer",         "Web Browser"),
                ("Presentation Layer", "Jinja2 HTML Templates"),
                ("Application Layer",  "Python 3.11 + Flask"),
                ("ML Layer",           "XGBoost + Scikit-learn + Joblib"),
                ("Data Layer",         "Pandas CSV"),
                ("Deployment Layer",   "Docker + IBM Cloud Foundry"),
            ],
            [4.5*cm, 12*cm]
        ), sp(8),
        sec("7. Team Contributions"),
        make_table(
            ["S.No","Team Member","Role","Primary Contribution"],
            [(str(i+1), m[0], m[1],
              ["Project lead, Flask app, IBM Cloud deployment",
               "EDA, data visualisation, input validation utils",
               "Data preprocessing, StandardScaler pipeline",
               "ML model training, XGBoost tuning, evaluation",
               "HTML templates, CSS UI design"][i])
             for i, m in enumerate(TEAM_MEMBERS)],
            [1.2*cm, 4.5*cm, 2.5*cm, 8.3*cm]
        ),
    ]

# ══════════════════════════════════════════════════════════════════════════════
# PHASE 8
# ══════════════════════════════════════════════════════════════════════════════
def p8_communication(styles):
    return header_banner("Communication", "1 Mark") + [
        sp(14),
        sec("Stakeholder Communication Plan"),
        make_table(
            ["S.No","Stakeholder","Communication Channel","Frequency","Content Communicated"],
            [
                ("1","NDMA / Authorities",        "Web App Dashboard",  "Real-time","Live flood risk prediction"),
                ("2","Meteorologists",             "Prediction Form",    "On-demand","Input parameters and model output"),
                ("3","Disaster Response Teams",    "Flood Result Page",  "On alert", "Emergency action protocol"),
                ("4","Local Authorities",          "No Flood Result",    "On alert", "All-clear badge + monitoring"),
                ("5","Research Analysts",          "History Page",       "Weekly",   "Full audit log of all predictions"),
                ("6","IBM Cloud Platform",         "Deployment Logs",    "Continuous","Application uptime, error logs"),
            ],
            [1.2*cm, 3.5*cm, 4*cm, 2.5*cm, 5.3*cm]
        ), sp(10),
        sec("Internal Team Communication"),
        make_table(
            ["Channel","Purpose","Frequency"],
            [
                ("GitHub Issues + PRs",          "Code review and feature tracking",               "Daily"),
                ("WhatsApp Group",               "Quick status updates and coordination",          "Daily"),
                ("Weekly Stand-up",              "Sprint progress review and blocker resolution",  "Weekly"),
                ("Google Meet",                  "Architecture decisions and design reviews",      "As needed"),
            ],
            [4.5*cm, 7.5*cm, 4.5*cm]
        ),
    ]

def p8_demo(styles):
    return header_banner("Demonstration of Proposed Features", "1 Mark") + [
        sp(14),
        sec("Live Demo Walkthrough"),
        make_table(
            ["Step","Page / Route","Action Demonstrated","Feature Verified","Presenter"],
            [
                ("1","Home (/)",             "Load dashboard; show XGBoost accuracy",                   "Model stats",            "Venkatesh Balireddy"),
                ("2","Home (/)",             "Show 4-model accuracy comparison bar chart",              "DT/KNN/RF/XGB",          "Venkatesh Balireddy"),
                ("3","Predict (/predict)",   "Enter HIGH-RISK values (RF=3500, Humidity=92%)",          "Form validation",        "Archana Dhanani"),
                ("4","POST /predict",        "Submit form; show POST processing",                       "Model inference",        "Archana Dhanani"),
                ("5","result_flood.html",    "Show red danger banner + 6 emergency action cards",       "Flood result page",      "Shivatmika Gandikota"),
                ("6","Predict (/predict)",   "Enter LOW-RISK values (RF=800, Humidity=55%)",            "Form re-entry",          "Gode S R Durgaprasad"),
                ("7","result_noflood.html",  "Show green safe banner + monitoring tips",                "No Flood result page",   "Gode S R Durgaprasad"),
                ("8","History (/history)",   "Show audit log table with timestamps",                    "predictions_log.csv",    "Bavisetty Gopi Krishna"),
                ("9","About (/about)",       "Show 5-layer architecture and team section",              "Architecture diagram",   "Bavisetty Gopi Krishna"),
            ],
            [1.2*cm, 3*cm, 5*cm, 3.5*cm, 3.8*cm]
        ),
    ]

def p8_planning(styles):
    return header_banner("Project Demo Planning", "1 Mark") + [
        sp(14),
        sec("Demo Session Details"),
        make_table(
            ["Attribute","Details"],
            [
                ("Duration",     "30 minutes"),
                ("Format",       "Live web application walkthrough"),
                ("Audience",     "Academic evaluators, IBM representatives, Skill Wallet panel"),
                ("Tools",        "Chrome browser, laptop with Python/Flask running"),
                ("Backup Plan",  "Recorded screen capture in case of internet or server issues"),
            ],
            [3.5*cm, 13*cm]
        ), sp(10),
        sec("Demo Agenda & Responsibilities"),
        make_table(
            ["Time","Section","Content","Presenter"],
            [
                ("0–5 min",   "Introduction",           "Problem context, flood statistics, project motivation",              "Venkatesh Balireddy"),
                ("5–10 min",  "Architecture",           "5-layer system diagram on About page",                               "Archana Dhanani"),
                ("10–18 min", "Live Prediction Demo",   "High-risk flood + low-risk safe scenarios",                          "Shivatmika G + Gode S R D"),
                ("18–24 min", "Model Results",          "Home Dashboard: accuracy comparison chart",                          "Gode S R Durgaprasad"),
                ("24–28 min", "History + DevOps",       "History page audit log; IBM Cloud deployment",                       "Bavisetty Gopi Krishna"),
                ("28–30 min", "Q&A + Conclusion",       "Future enhancements, scalability plan, IBM Cloud live URL",          "Venkatesh Balireddy"),
            ],
            [2*cm, 3.5*cm, 7*cm, 4*cm]
        ),
    ]

def p8_scalability(styles):
    return header_banner("Scalability & Future Plan", "1 Mark") + [
        sp(14),
        sec("Current Scalability Architecture"),
        make_table(
            ["Aspect","Current Implementation","Scale-Up Path"],
            [
                ("Hosting",      "IBM Cloud Foundry (single instance)",        "Scale to multiple CF instances"),
                ("Container",    "Docker (Dockerfile provided)",                "Kubernetes orchestration via IBM CKS"),
                ("Storage",      "CSV flat file (predictions_log.csv)",         "PostgreSQL or IBM Db2 cloud database"),
                ("Model",        "XGBoost (batch retrain)",                     "Online learning with new incoming data"),
                ("Frontend",     "Flask-rendered Jinja2 templates",             "React/Vue SPA with Flask REST API backend"),
            ],
            [3.5*cm, 6*cm, 7*cm]
        ), sp(10),
        sec("Future Enhancement Roadmap"),
        make_table(
            ["S.No","Enhancement","Description","Priority","Assigned To"],
            [
                ("1","Real-time API",              "Connect to IMD / OpenWeatherMap API for live data",         "High",   "Venkatesh Balireddy"),
                ("2","SMS Alerts",                 "Auto-notify registered authorities when flood is detected", "High",   "Archana Dhanani"),
                ("3","Multi-district Pred.",       "Batch predict flood risk for multiple districts",           "Medium", "Shivatmika Gandikota"),
                ("4","LSTM Model",                 "Replace XGBoost with LSTM for sequential rainfall analysis","Medium", "Gode S R Durgaprasad"),
                ("5","Mobile Application",         "Native Android / iOS app using the Flask REST API backend", "Medium", "Bavisetty Gopi Krishna"),
                ("6","Regional Language UI",       "Multi-language support for Telugu, Hindi",                  "Low",    "All Members"),
            ],
            [1.2*cm, 3.5*cm, 6.5*cm, 2*cm, 3.3*cm]
        ),
    ]

def p8_team(styles):
    return header_banner("Team Involvement in Demonstration", "1 Mark") + [
        sp(14),
        sec("Team Members & Roles in Demonstration"),
        make_table(
            ["S.No","Team Member Name","Role in Demo","Section Presented","Participation"],
            [
                ("1","Venkatesh Balireddy",               "Team Lead & Host",       "Introduction + Closing",    "Active"),
                ("2","Archana Dhanani",                   "Architecture Presenter", "System Architecture",       "Active"),
                ("3","Shivatmika Gandikota",              "ML Demo Lead",           "Live Prediction Demo",      "Active"),
                ("4","Gode Siva Ramakrishna Durgaprasad","ML Results Presenter",   "Model Comparison Results",  "Active"),
                ("5","Bavisetty Gopi Krishna",            "DevOps Presenter",       "History Page + Deployment", "Active"),
            ],
            [1*cm, 4.5*cm, 3.5*cm, 4.5*cm, 3*cm]
        ), sp(10),
        sec("Team Coordination Notes"),
        make_table(
            ["Aspect","Details"],
            [
                ("Team Leader / Coordinator",           "Venkatesh Balireddy"),
                ("Overall Team Coordination Rating",    "5 / 5"),
                ("Any issues during demo",              "None"),
                ("How issues were resolved",            "N/A"),
            ],
            [5.5*cm, 11*cm]
        ),
    ]

# ══════════════════════════════════════════════════════════════════════════════
# BUILD ALL PDFs
# ══════════════════════════════════════════════════════════════════════════════
def build(path, content_fn):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    doc = SimpleDocTemplate(
        path, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm
    )
    story = content_fn(STYLES)
    doc.build(story)
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
    print(f"Generating {len(PDFS)} PDFs matching exact reference style...\n")
    for path, fn in PDFS:
        build(path, fn)
    print(f"\nDone — {len(PDFS)} PDFs created.")
