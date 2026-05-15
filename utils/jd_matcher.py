from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Calculate resume-job match score
def calculate_job_match(resume_text, job_description):

    # Create TF-IDF object
    vectorizer = TfidfVectorizer()

    # Convert texts into vectors
    vectors = vectorizer.fit_transform([
        resume_text,
        job_description
    ])

    # Calculate cosine similarity
    similarity = cosine_similarity(vectors)[0][1]

    # Convert to percentage
    match_score = round(similarity * 100, 2)

    return match_score