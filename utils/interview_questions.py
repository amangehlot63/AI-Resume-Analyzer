# Generate interview questions
def generate_interview_questions(skills):

    question_bank = {

        'python': [
            'What are Python decorators?',
            'Explain list vs tuple in Python.',
            'What is OOP in Python?'
        ],

        'sql': [
            'What is JOIN in SQL?',
            'Difference between DELETE and TRUNCATE?',
            'What is normalization?'
        ],

        'flask': [
            'What is Flask?',
            'Explain Flask routing.',
            'What is Jinja2 template engine?'
        ],

        'machine learning': [
            'What is overfitting?',
            'Difference between supervised and unsupervised learning?',
            'Explain bias vs variance.'
        ],

        'html': [
            'What is semantic HTML?',
            'Difference between id and class?',
            'What are meta tags?'
        ],

        'css': [
            'What is Flexbox?',
            'Difference between relative and absolute positioning?',
            'What is CSS specificity?'
        ]
    }

    questions = []

    # Match skills with questions
    for skill in skills:

        if skill in question_bank:

            questions.extend(question_bank[skill])

    return questions