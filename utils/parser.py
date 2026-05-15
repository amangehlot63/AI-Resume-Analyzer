import PyPDF2
import re

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):

    text = ""

    # Open PDF file
    with open(pdf_path, 'rb') as file:

        # Create PDF reader object
        reader = PyPDF2.PdfReader(file)

        # Loop through all pages
        for page in reader.pages:

            # Extract text from page
            text += page.extract_text()

    return text


# Extract email from text
def extract_email(text):

    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+'

    match = re.search(pattern, text)

    if match:
        return match.group(0)

    return "Email not found"


# Extract phone number
def extract_phone(text):

    pattern = r'\+?\d[\d\s\-]{8,15}\d'

    match = re.search(pattern, text)

    if match:
        return match.group(0)

    return "Phone number not found"


# Extract skills from resume text
def extract_skills(text):

    # Convert text to lowercase
    text = text.lower()

    # Skill database
    skills_db = [
        'python',
        'java',
        'c',
        'c++',
        'html',
        'css',
        'javascript',
        'flask',
        'django',
        'sql',
        'mysql',
        'mongodb',
        'machine learning',
        'data science',
        'pandas',
        'numpy',
        'tensorflow',
        'power bi',
        'excel',
        'git',
        'github'
    ]

    found_skills = []

    # Check skills in text
    for skill in skills_db:

        if skill.lower() in text:
            found_skills.append(skill)

    return found_skills