from collections import Counter
from bs4 import BeautifulSoup
import os
import re
import json


def extract_ngrams(text, n=3):
    text = re.sub(r'\s+', ' ', text.lower())
    return [text[i:i + n] for i in range(len(text) - n + 1)]


def build_language_profile(folder_path, n=3):
    ngrams_counter = Counter()
    for filename in os.listdir(folder_path):
        if filename.endswith(".html"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                soup = BeautifulSoup(content, "html.parser")
                text = soup.get_text()
                ngrams_counter.update(extract_ngrams(text, n))
    return ngrams_counter


def save_profile_to_json(profile, filename):
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(profile, json_file, ensure_ascii=False)


def create_language_profiles(english_folder, spanish_folder, ngrams_folder):
    if not os.path.exists(ngrams_folder):
        os.makedirs(ngrams_folder)

    english_profile = build_language_profile(english_folder)
    spanish_profile = build_language_profile(spanish_folder)

    save_profile_to_json(english_profile, os.path.join(ngrams_folder, 'english_profile.json'))
    save_profile_to_json(spanish_profile, os.path.join(ngrams_folder, 'spanish_profile.json'))


# create_language_profiles(
#     "htmls/eng",
#     "htmls/spanish",
#     "ngrams"
# )

def load_profile_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as json_file:
        return Counter(json.load(json_file))


def calculate_similarity(profile1, profile2):
    total = sum(profile1.values()) + sum(profile2.values())
    intersection = sum((profile1 & profile2).values())
    return intersection / total if total > 0 else 0


def ngram_detect_language(text, english_profile, spanish_profile, n=3):
    text_ngrams = Counter(extract_ngrams(text, n))
    english_similarity = calculate_similarity(text_ngrams, english_profile)
    spanish_similarity = calculate_similarity(text_ngrams, spanish_profile)

    return 'english' if english_similarity > spanish_similarity else 'spanish'
