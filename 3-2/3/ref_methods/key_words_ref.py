import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import string


def get_key_words(text):
    
    tokens = word_tokenize(text)

    
    stop_words = set(stopwords.words('russian') + list(string.punctuation))
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]

    # Расчет частотности слов
    fdist = FreqDist(filtered_tokens)

    # Извлечение N наиболее часто встречающихся слов
    n = 10  # количество ключевых слов, которые нужно извлечь
    keywords = [word for word, _ in fdist.most_common(n)]
    return keywords
