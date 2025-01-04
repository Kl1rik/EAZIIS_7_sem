from pathlib import Path
from tkinter import Tk, Canvas, Text, Button, PhotoImage, Toplevel
from utils import extract_text_from_html
from alphabet_method import alphabet_detect_language
from ngram_method import ngram_detect_language, load_profile_from_json
from bs4 import BeautifulSoup
from transformers import pipeline
import tkinter as tk
import tkinter.filedialog
import os
import tensorflow as tf




OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets/frame0")
language_classifier = pipeline("text-classification", model="papluca/xlm-roberta-base-language-detection")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def select_document():
    global output_path
    output_path = tk.filedialog.askdirectory()
    return output_path

def get_files(directory):
    file_list = os.listdir(directory)

    files_in_dir = list()
    for file_name in file_list:
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
            files_in_dir.append(file_path)
    return files_in_dir


def ngram_method():
    ngrams_folder = 'ngrams'
    document_dir = select_document()
    english_profile = load_profile_from_json(os.path.join(ngrams_folder, 'english_profile.json'))
    spanish_profile = load_profile_from_json(os.path.join(ngrams_folder, 'spanish_profile.json'))

    for filename in os.listdir(document_dir):
        if filename.endswith(".html"):
            file_path = os.path.join(document_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                soup = BeautifulSoup(content, "html.parser")
                text = soup.get_text()
                language = ngram_detect_language(text, english_profile, spanish_profile)
                text_area.insert('1.0',
                                 f"Файл '{file_path}' распознан как язык: {language}. Определено с помощью метода n-грамм.\n")


def alph_method():
    document_dir = select_document()
    files_in_dir = get_files(document_dir)

    for file in files_in_dir:
        text = extract_text_from_html(file)
        language_of_doc = alphabet_detect_language(text)
        text_area.insert('1.0',
                         f"Файл {file} написан на {language_of_doc} языке. Определено с помощью алфавитного метода\n")


def nn_method():
    document_dir = select_document()
    files_in_dir = get_files(document_dir)

    for file in files_in_dir:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            soup = BeautifulSoup(content, "html.parser")
            text = soup.get_text()
            text = text[:512]
            prediction = language_classifier(text)
            language = prediction[0]['label']
            text_area.insert('1.0',
                             f"Файл {file} написан на языке: {language}. Определено с помощью нейросетевого метода.\n")


def save_output():
    output = text_area.get("1.0", "end")
    with open("save.txt", "w") as file:
        file.write(output)
    print("Сохранено!")


def help_window_up():
    help_window = Toplevel(window)
    help_window.lift()
    help_window.geometry("500x500")
    help_window.configure(bg="#379683")

    canvas = Canvas(
        help_window,
        bg="#ff6c94",
        height=500,
        width=500,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    canvas.create_text(
        12.0,
        11.0,
        anchor="nw",
        text="Данное приложение поможет вам\nопределить на каком языке написаны\nдокументы с расширением .html",
        fill="#FFFFFF",
        font=("Inter", 16 * -1)
    )

    canvas.create_text(
        12.0,
        185.0,
        anchor="nw",
        text="Кнопка “Помощь” откроет данное окно",
        fill="#FFFFFF",
        font=("Inter", 16 * -1)
    )

    canvas.create_text(
        12.0,
        219.0,
        anchor="nw",
        text="Кнопка “Методом N-грамм” определит\nязык документов в выбранной папке\nметодом N-грамм",
        fill="#FFFFFF",
        font=("Inter", 16 * -1)
    )

    canvas.create_text(
        13.0,
        291.0,
        anchor="nw",
        text="Кнопка “Алфавитный метод” определит\nязык документов в выбранной папке\nалфавитным методом",
        fill="#FFFFFF",
        font=("Inter", 16 * -1)
    )

    canvas.create_text(
        11.0,
        363.0,
        anchor="nw",
        text="Кнопка “Нейросетевой метод” определит\nязык документов в выбранной папке\nнейросетевым методом",
        fill="#FFFFFF",
        font=("Inter", 16 * -1)
    )

    canvas.create_text(
        12.0,
        90.0,
        anchor="nw",
        text="Кнопка ",
        fill="#FFFFFF",
        font=("Inter", 16 * -1)
    )

    canvas.create_text(
        135.0,
        90.0,
        anchor="nw",
        text="сохранит весь вывод",
        fill="#FFFFFF",
        font=("Inter", 16 * -1)
    )

    canvas.create_text(
        12.0,
        132.0,
        anchor="nw",
        text="программы в текстовый файл с\nназванием “save.txt”",
        fill="#FFFFFF",
        font=("Inter", 16 * -1)
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    image_3 = canvas.create_image(
        100.0,
        100.0,
        image=button_image_1
    )

    help_window.resizable(False, False)
    help_window.mainloop()



window = Tk()

window.geometry("762x500")
window.configure(bg = "#372183")


canvas = Canvas(
    window,
    bg = "#015e00",
    height = 500,
    width = 762,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
button_ngram_method_image = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_ngram_method = Button(
    image=button_ngram_method_image,
    borderwidth=0,
    highlightthickness=0,
    command=ngram_method,
    relief="flat"
)
button_ngram_method.place(
    x=178.0,
    y=14.0,
    width=174.0,
    height=47.599998474121094
)

button_alphabet_method_image = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_alphabet_method = Button(
    image=button_alphabet_method_image,
    borderwidth=0,
    highlightthickness=0,
    command=alph_method,
    relief="flat"
)
button_alphabet_method.place(
    x=371.0,
    y=14.0,
    width=174.0,
    height=47.599998474121094
)

button_save_image = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_save = Button(
    image=button_save_image,
    borderwidth=0,
    highlightthickness=0,
    command=save_output,
    relief="flat"
)
button_save.place(
    x=15.0,
    y=14.0,
    width=47.599998474121094,
    height=47.599998474121094
)

button_help_image = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_help = Button(
    image=button_help_image,
    borderwidth=0,
    highlightthickness=0,
    command=help_window_up,
    relief="flat"
)
button_help.place(
    x=82.0,
    y=14.0,
    width=77.0,
    height=47.599998474121094
)

button_nn_method_image = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_nn_method = Button(
    image=button_nn_method_image,
    borderwidth=0,
    highlightthickness=0,
    command=nn_method,
    relief="flat"
)
button_nn_method.place(
    x=564.0,
    y=14.0,
    width=176.0,
    height=47.599998474121094
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    381.0,
    284.0,
    image=entry_image_1
)
text_area = Text(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
text_area.place(
    x=14.0,
    y=82.0,
    width=734.0,
    height=402.0
)


def display_popup(event):
    menu.post(event.x_root, event.y_root)

def popup_copy():
    text_area.event_generate("<<Copy>>")

def popup_cut():
    text_area.event_generate("<<Cut>>")

def popup_paste():
    text_area.event_generate("<<Paste>>")

menu = tk.Menu(tearoff=False)
menu.add_command(label="Copy", command=popup_copy)
menu.add_command(label="Cut", command=popup_cut)
menu.add_separator()
menu.add_command(label="Paste", command=popup_paste)
text_area.bind("<Button-3>", display_popup)


window.resizable(False, False)
window.mainloop()
