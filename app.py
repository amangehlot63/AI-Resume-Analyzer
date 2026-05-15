# =========================================================
# AI RESUME ANALYZER & INTERVIEW ASSISTANT
# Main Flask Application
# =========================================================


from flask import redirect, session

from utils.auth import (
    register_user,
    login_user
)

from utils.database import (
    save_to_database,
    get_all_analyses
)

# =========================
# FLASK IMPORTS
# =========================

from flask import (
    Flask,
    render_template,
    request,
    send_file
)


# =========================
# PYTHON IMPORTS
# =========================

import os

# =========================
# PDF REPORT IMPORTS
# =========================

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


# =========================
# CUSTOM MODULE IMPORTS
# =========================

# Resume parser functions
from utils.parser import (
    extract_text_from_pdf,
    extract_email,
    extract_phone,
    extract_skills
)

# ATS score functions
from utils.ats_score import (
    calculate_ats_score,
    generate_suggestions
)

# Job description matcher
from utils.jd_matcher import (
    calculate_job_match
)

# Interview question generator
from utils.interview_questions import (
    generate_interview_questions
)


# =========================================================
# CREATE FLASK APP
# =========================================================

app = Flask(__name__)
app.secret_key = 'resume_analyzer_secret_key'

# =========================================================
# GLOBAL VARIABLES
# Used for PDF report generation
# =========================================================

global_ats_score = 0
global_job_match_score = 0
global_skills = []
global_suggestions = []
global_questions = []


# =========================================================
# FILE UPLOAD CONFIGURATION
# =========================================================

UPLOAD_FOLDER = 'static/uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# =========================================================
# HOME ROUTE
# =========================================================

@app.route('/')
def home():

    # Check user login
    if 'user' not in session:

        return redirect('/login')

    return render_template('index.html')


# =========================================================
# RESUME UPLOAD & ANALYSIS ROUTE
# =========================================================

@app.route('/upload', methods=['POST'])
def upload_resume():

    # Access global variables
    global global_ats_score
    global global_job_match_score
    global global_skills
    global global_suggestions
    global global_questions


    # -----------------------------------------------------
    # CHECK FILE EXISTENCE
    # -----------------------------------------------------

    if 'resume' not in request.files:
        return "No file uploaded"


    # Get uploaded file
    file = request.files['resume']


    # Get job description
    job_description = request.form['job_description']


    # Check empty filename
    if file.filename == '':
        return "No selected file"


    # -----------------------------------------------------
    # SAVE FILE
    # -----------------------------------------------------

    filepath = os.path.join(
        app.config['UPLOAD_FOLDER'],
        file.filename
    )

    file.save(filepath)


    # -----------------------------------------------------
    # EXTRACT RESUME TEXT
    # -----------------------------------------------------

    resume_text = extract_text_from_pdf(filepath)

    print("\n===== RESUME TEXT =====\n")
    print(resume_text)


    # -----------------------------------------------------
    # EXTRACT BASIC INFORMATION
    # -----------------------------------------------------

    email = extract_email(resume_text)

    phone = extract_phone(resume_text)

    print("\n===== EMAIL =====\n")
    print(email)

    print("\n===== PHONE =====\n")
    print(phone)


    # -----------------------------------------------------
    # EXTRACT SKILLS
    # -----------------------------------------------------

    skills = extract_skills(resume_text)

    print("\n===== SKILLS =====\n")
    print(skills)


    # -----------------------------------------------------
    # CALCULATE ATS SCORE
    # -----------------------------------------------------

    ats_score = calculate_ats_score(skills)

    print("\n===== ATS SCORE =====\n")
    print(ats_score)


    # -----------------------------------------------------
    # GENERATE SUGGESTIONS
    # -----------------------------------------------------

    suggestions = generate_suggestions(skills)

    print("\n===== SUGGESTIONS =====\n")
    print(suggestions)


    # -----------------------------------------------------
    # CALCULATE JOB MATCH SCORE
    # -----------------------------------------------------

    job_match_score = calculate_job_match(
        resume_text,
        job_description
    )

    print("\n===== JOB MATCH SCORE =====\n")
    print(job_match_score)


    # -----------------------------------------------------
    # GENERATE INTERVIEW QUESTIONS
    # -----------------------------------------------------

    questions = generate_interview_questions(skills)

    print("\n===== INTERVIEW QUESTIONS =====\n")
    print(questions)

    # Save analysis into database
    save_to_database(

        file.filename,
        email,
        phone,
        ats_score,
        job_match_score,
        skills

    )

    # -----------------------------------------------------
    # STORE DATA GLOBALLY
    # Used in PDF report generation
    # -----------------------------------------------------

    global_ats_score = ats_score

    global_job_match_score = job_match_score

    global_skills = skills

    global_suggestions = suggestions

    global_questions = questions


    # -----------------------------------------------------
    # SEND DATA TO FRONTEND
    # -----------------------------------------------------

    return render_template(

        'result.html',

        filename=file.filename,

        email=email,

        phone=phone,

        skills=skills,

        ats_score=ats_score,

        suggestions=suggestions,

        job_match_score=job_match_score,

        questions=questions
    )



# =========================================================
# SIGNUP ROUTE
# =========================================================

@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':

        username = request.form['username']

        password = request.form['password']

        success = register_user(username, password)

        if success:

            return redirect('/login')

        else:

            return "Username already exists"

    return render_template('signup.html')


# =========================================================
# LOGIN ROUTE
# =========================================================

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']

        password = request.form['password']

        user = login_user(username, password)

        if user:

            session['user'] = username

            return redirect('/')

        else:

            return "Invalid credentials"

    return render_template('login.html')


# =========================================================
# LOGOUT ROUTE
# =========================================================

@app.route('/logout')
def logout():

    session.pop('user', None)

    return redirect('/login')


# =========================================================
# HISTORY ROUTE
# =========================================================

@app.route('/history')
def history():


    # Check user login
    if 'user' not in session:

        return redirect('/login')
    

    # Fetch all analyses
    analyses = get_all_analyses()

    return render_template(

        'history.html',

        analyses=analyses
    )

# =========================================================
# PDF REPORT DOWNLOAD ROUTE
# =========================================================

@app.route('/download-report')
def download_report():

    # PDF file name
    pdf_file = "resume_report.pdf"


    # Create PDF document
    doc = SimpleDocTemplate(pdf_file)


    # PDF styles
    styles = getSampleStyleSheet()


    # PDF content list
    elements = []


    # -----------------------------------------------------
    # PDF TITLE
    # -----------------------------------------------------

    elements.append(

        Paragraph(
            "AI Resume Analyzer Report",
            styles['Title']
        )
    )

    elements.append(Spacer(1, 20))


    # -----------------------------------------------------
    # ATS SCORE
    # -----------------------------------------------------

    elements.append(

        Paragraph(
            f"ATS Score: {global_ats_score}/100",
            styles['BodyText']
        )
    )

    elements.append(Spacer(1, 10))


    # -----------------------------------------------------
    # JOB MATCH SCORE
    # -----------------------------------------------------

    elements.append(

        Paragraph(
            f"Job Match Score: {global_job_match_score}%",
            styles['BodyText']
        )
    )

    elements.append(Spacer(1, 10))


    # -----------------------------------------------------
    # SKILLS
    # -----------------------------------------------------

    elements.append(

        Paragraph(
            f"Skills: {', '.join(global_skills)}",
            styles['BodyText']
        )
    )

    elements.append(Spacer(1, 10))


    # -----------------------------------------------------
    # SUGGESTIONS
    # -----------------------------------------------------

    elements.append(

        Paragraph(
            "Suggestions:",
            styles['Heading2']
        )
    )

    for suggestion in global_suggestions:

        elements.append(

            Paragraph(
                f"• {suggestion}",
                styles['BodyText']
            )
        )


    elements.append(Spacer(1, 10))


    # -----------------------------------------------------
    # INTERVIEW QUESTIONS
    # -----------------------------------------------------

    elements.append(

        Paragraph(
            "Interview Questions:",
            styles['Heading2']
        )
    )

    for question in global_questions:

        elements.append(

            Paragraph(
                f"• {question}",
                styles['BodyText']
            )
        )


    # -----------------------------------------------------
    # BUILD PDF
    # -----------------------------------------------------

    doc.build(elements)


    # -----------------------------------------------------
    # DOWNLOAD PDF
    # -----------------------------------------------------

    return send_file(
        pdf_file,
        as_attachment=True
    )


# =========================================================
# RUN FLASK SERVER
# =========================================================

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000)