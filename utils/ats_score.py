# Calculate ATS score
def calculate_ats_score(skills):

    # Important skills list
    important_skills = [
        'python',
        'sql',
        'flask',
        'machine learning',
        'data science',
        'javascript',
        'html',
        'css',
        'mysql',
        'git',
        'github'
    ]

    score = 0

    # Score calculation
    for skill in skills:

        if skill.lower() in important_skills:
            score += 10

    # Maximum score limit
    if score > 100:
        score = 100

    return score



# Generate resume suggestions
def generate_suggestions(skills):

    important_skills = [
        'python',
        'sql',
        'flask',
        'machine learning',
        'data science',
        'git',
        'github'
    ]

    suggestions = []

    # Check missing skills
    for skill in important_skills:

        if skill not in skills:

            suggestions.append(
                f"Consider adding {skill} skills to improve ATS score."
            )

    return suggestions