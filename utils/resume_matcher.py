from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def match_resumes(resumes, job_description):
    # Combine job description and resumes
    documents = [job_description.lower()] + list(resumes.values())

    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)

    # Calculate cosine similarity
    cosine_similarities = cosine_similarity(
        tfidf_matrix[0:1], tfidf_matrix[1:]
    ).flatten()

    # Create a list of tuples (resume_index, similarity_score)
    matched_resumes = [
        (resume_name, score) for resume_name, score in zip(resumes, cosine_similarities)
    ]

    # Sort by similarity score in descending order
    matched_resumes.sort(key=lambda x: x[1], reverse=True)

    # Convert similarity scores to percentages
    matched_resumes = [
        (resume_name, round(score * 100, 2)) for resume_name, score in matched_resumes
    ]

    return matched_resumes
