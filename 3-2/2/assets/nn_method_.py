import nltk
from nltk.classify import textcat


def lang_nn(text):
    classifier = textcat.TextCat()
    language = classifier.guess_language(text)
    if language == 'rus':
        return "Русском"
    elif language == 'deu':
        return "Немецком"
    return language


lang_nn("Beispieltext auf Russisch")

#
# import fasttext
#
# # Загрузка предобученной модели fastText для определения языка
# model = fasttext.load_model('lid.176.bin')
#
# # Определение языка текста
# text = "Ваш текст для классификации"
# predicted_language = model.predict(text)[0][0]
#
# print(predicted_language)
