from app.utils.model import model
from app.utils.clean import clean_answer
import numpy as np

def search_similar_questions(index, questions, answers, query, top_k=1):
    cleaned_query = clean_answer(query)
    query_embedding = model.encode([cleaned_query], normalize_embeddings=True)
    scores, indices = index.search(query_embedding, top_k)

    results = []
    for i, idx in enumerate(indices[0]):
        results.append({
            "question_similaire": clean_answer(questions[idx]),
            "reponse_associee": clean_answer(answers[idx]),
            "score": float(scores[0][i])
        })
    return results
