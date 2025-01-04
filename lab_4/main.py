from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Toplevel, Menu
from tkinter.filedialog import askopenfile
from pathlib import Path
from collections import Counter
import spacy
import transformers

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/home/kl1rik/EAZIIS_7_sem/4/assets/frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


nlp_en = spacy.load("en_core_web_sm")
nlp_de = spacy.load("de_core_news_sm")
translator = transformers.pipeline("translation_en_to_de", model="Helsinki-NLP/opus-mt-en-de")


def translate_text(text):
    translation = translator(text)
    return translation[0]['translation_text']


def analyze_text(text, target_language="de"):
    doc = nlp_en(text)
    word_count = Counter([token.text.lower() for token in doc if token.is_alpha])
    translated_words = {word: translator(word)[0]['translation_text'] for word in word_count.keys()}

    pos_info = {word: (word_data, nlp_de(word_data)[0].pos_) for word, word_data in translated_words.items()}
    return word_count, translated_words, pos_info


def save_results(text, translation, word_info, translated_words, pos_info, syntax_tree, filename="results.txt"):
    with open(filename, "w", encoding="utf-8") as file:
        file.write("=== Перевод текста ===\n")
        file.write(translation + "\n\n")
        print(translation)
        file.write("=== Частотный список слов и переводов ===\n")
        for word, freq in word_info.items():
            translated_word = translated_words.get(word, "Нет перевода")
            grammar_info = pos_info.get(word, ("", "Нет информации"))[1]
            file.write(
                f"{word}: {freq}, Перевод: {translated_word}, Грамматическая информация: {grammar_info}\n"
            )
        file.write("\n=== Дерево синтаксического разбора ===\n")
        file.write(syntax_tree + "\n")



def select_document():
    global output_path
    output_path = askopenfile()
    with open(output_path.name, "r", encoding="utf-8") as file:
        text = file.read()

    translation = translate_text(text)
    word_count, translated_words, pos_info = analyze_text(text)

    doc = nlp_en(text)
    syntax_tree = "\n".join([f"{token.text} --> {token.dep_}" for token in doc])

    output = f"Документ: {output_path.name}\n\n"
    output += f"=== Перевод ===\n{translation}\n\n"
    output += "=== Частотный список ===\n"
    for word, freq in word_count.items():
        output += f"{word}: {freq}, Перевод: {translated_words[word]}, Грамматическая информация: {pos_info[word][1]}\n"
    output += "\n=== Дерево синтаксического разбора ===\n"
    output += syntax_tree

    # Передаём все необходимые аргументы в save_results
    save_results(
        text=text,
        translation=translation,
        word_info=word_count,
        translated_words=translated_words,
        pos_info=pos_info,
        syntax_tree=syntax_tree
    )
    text_area.insert("1.0", output)


def help_window():
    help_window = Toplevel(window)
    help_window.geometry("700x400")
    help_window.configure(bg="#ffcccc")

    canvas = Canvas(
        help_window,
        bg="#ffcccc",
        height=400,
        width=700,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    canvas.create_text(
        12.0,
        11.0,
        anchor="nw",
        text="Приложение переводит документ с английского на немецкий язык,\nанализирует текст и строит дерево синтаксического разбора.",
        fill="#000000",
        font=("Inter", 12)
    )

    canvas.create_text(
        12.0,
        100.0,
        anchor="nw",
        text="Кнопка “Выбрать документ” позволяет выбрать документ для анализа.",
        fill="#000000",
        font=("Inter", 12)
    )

    help_window.resizable(False, False)


window = Tk()
window.geometry("762x500")
window.configure(bg="#ffcccc")

canvas = Canvas(
    window,
    bg="#ffcccc",
    height=500,
    width=762,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)

button_image_help = PhotoImage(file=relative_to_assets("button_2.png"))
button_help = Button(
    image=button_image_help,
    borderwidth=0,
    highlightthickness=0,
    command=help_window,
    relief="flat"
)
button_help.place(x=181.0, y=17.0, width=77.0, height=48.0)

button_image_pick_document = PhotoImage(file=relative_to_assets("button_4.png"))
button_pick_document = Button(
    image=button_image_pick_document,
    borderwidth=0,
    highlightthickness=0,
    command=select_document,
    relief="flat"
)
button_pick_document.place(x=278.0, y=17.0, width=176.0, height=48.0)

text_area = Text(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
text_area.place(x=14.0, y=82.0, width=734.0, height=402.0)

window.resizable(False, False)
window.mainloop()
