from app.utils.model import model
import numpy as np

def search_similar_questions(index, questions, answers, query, top_k=1):
    query_embedding = model.encode([query], normalize_embeddings=True)
    scores, indices = index.search(query_embedding, top_k)

    results = []
    for i, idx in enumerate(indices[0]):
        results.append({
            "question_similaire": questions[idx],
            "reponse_associee": answers[idx],
            "score": float(scores[0][i])
        })
    return results
