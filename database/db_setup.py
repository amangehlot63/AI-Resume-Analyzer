import sqlite3

# Connect database
conn = sqlite3.connect('database/app.db')

# Create cursor
cursor = conn.cursor()


# =====================================================
# CREATE RESUME ANALYSIS TABLE
# =====================================================

cursor.execute('''

CREATE TABLE IF NOT EXISTS resume_analysis (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    filename TEXT,

    email TEXT,

    phone TEXT,

    ats_score INTEGER,

    job_match_score REAL,

    skills TEXT

)

''')


# =====================================================
# CREATE USERS TABLE
# =====================================================

cursor.execute('''

CREATE TABLE IF NOT EXISTS users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT UNIQUE,

    password TEXT

)

''')


# Save changes
conn.commit()

# Close connection
conn.close()

print("Database & table created successfully!")