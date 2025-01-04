import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import sent_tokenize

nltk.download("punkt")


def get_classic_ref(text):

    
    sentences = sent_tokenize(text)

    # Вычисление TF-IDF для предложений
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(sentences)

    
    cosine_sim_matrix = cosine_similarity(X, X)

    
    sentence_scores = cosine_sim_matrix.mean(axis=1)

    # Выбор N наиболее информативных предложений для реферата
    n = 8  
    top_indices = sentence_scores.argsort()[-n:][::-1]
    top_sentences = [sentences[i] for i in top_indices]

    summary = '\n'.join(top_sentences)
    return summary
