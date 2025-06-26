from app.utils.model import model
from app.utils.clean import clean_answer
import numpy as np
from deep_translator import GoogleTranslator # ou DeepLTranslator 


def search_similar_questions(index, questions, answers, query, top_k=1, target_lang="en"):
    # Étape 1 : Traduction de la question utilisateur vers l'anglais (langue du modèle)
    query_translated = GoogleTranslator(source='auto', target=target_lang).translate(query)
    #query_translated = query
    cleaned_query = clean_answer(query_translated)
    query_embedding = model.encode([cleaned_query], normalize_embeddings=True)
    scores, indices = index.search(query_embedding, top_k)

    results = []
    for i, idx in enumerate(indices[0]):
        question_similaire = clean_answer(questions[idx])
        reponse_associee = clean_answer(answers[idx])

        #Retraduction en français
        question_similaire_translated = GoogleTranslator(source=target_lang, target='fr').translate(question_similaire)
        reponse_associee_translated = GoogleTranslator(source=target_lang, target='fr').translate(reponse_associee)

        results.append({
            "question_similaire": clean_answer(question_similaire_translated),
            "reponse_associee": clean_answer(reponse_associee_translated),
            "score": float(scores[0][i])
        })
    return results
