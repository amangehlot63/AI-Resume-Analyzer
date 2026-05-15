import sqlite3


# Save resume analysis
def save_to_database(

    filename,
    email,
    phone,
    ats_score,
    job_match_score,
    skills

):

    # Connect database
    conn = sqlite3.connect('database/app.db')

    cursor = conn.cursor()

    # Insert data
    cursor.execute('''

    INSERT INTO resume_analysis (

        filename,
        email,
        phone,
        ats_score,
        job_match_score,
        skills

    )

    VALUES (?, ?, ?, ?, ?, ?)

    ''', (

        filename,
        email,
        phone,
        ats_score,
        job_match_score,
        ', '.join(skills)

    ))

    # Save changes
    conn.commit()

    # Close connection
    conn.close()


    # Fetch all resume analyses
def get_all_analyses():

    # Connect database
    conn = sqlite3.connect('database/app.db')

    cursor = conn.cursor()

    # Fetch data
    cursor.execute('''

    SELECT *

    FROM resume_analysis

    ORDER BY id DESC

    ''')

    analyses = cursor.fetchall()

    # Close connection
    conn.close()

    return analyses