import tkinter.filedialog

from pathlib import Path
import os
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Toplevel

from ref_methods.key_words_ref import get_key_words
from ref_methods.classic_ref import get_classic_ref
from ref_methods.ml_ref import get_ml_ref, summary_extraction
from langdetect import detect
import torch
import nltk
nltk.download('stopwords')
nltk.download('punkt')


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/home/kl1rik/EAZIIS_7_sem/3-2/3/assets/frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def save_output():
    output = text_area.get("1.0", "end")
    with open("save.txt", "w", encoding="utf-8") as file:
        file.write(output)
    print("Сохранено!")


def select_folder():
    global output_path
    output_path = tkinter.filedialog.askdirectory()

    for root, dirs, files in os.walk(output_path):
        for file in files:
            #print(os.path.join(root, file))
            path = os.path.join(root, file)
            with open(f'{os.path.join(root, file)}', 'r', encoding='utf-8') as file:
                text = file.read()
            output = f"\n\nСсылка на документ: {path} \n\n"
            output += "------- Ключевые слова -------\n"
            output += str(get_key_words(text)).replace('[', '').replace(']', '').replace("'", "")
            output += "\n\n------- Классический реферат -------\n"
            output += str(get_classic_ref(text))
            output += "\n\n ------- ML реферат ------- \n"
            if detect(text) == 'de':
                output += get_ml_ref(text, int(len(text.split()) / 4), int(len(text.split()) / 3))
            elif detect(text) == 'ru':
                output += summary_extraction(text)

            text_area.insert('1.0', output)

    return output_path


def select_document():
    global output_path
    output_path = tkinter.filedialog.askopenfile()

    with open(f'{output_path.name}', 'r', encoding='utf-8') as file:
        text = file.read()
    output = f"\n\nСсылка на документ: {output_path.name}\n\n"
    output += "------- Ключевые слова -------\n"
    output += str(get_key_words(text)).replace('[', '').replace(']', '').replace("'", "")
    output += "\n\n------- Классический реферат -------\n"
    output += str(get_classic_ref(text))
    output += "\n\n ------- ML реферат ------- \n"
    if detect(text) == 'de':
        output += get_ml_ref(text, int(len(text.split()) / 4), int(len(text.split()) / 3))
    elif detect(text) == 'ru':
        output += summary_extraction(text)


    text_area.insert('1.0', output)
    return output_path.name


def help_window():
    help_window = Toplevel(window)
    help_window.lift()
    help_window.geometry("500x500")
    help_window.configure(bg="#ffcccc") #379683

    canvas = Canvas(
        help_window,
        bg="#ffcccc", #379683
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
        text="Приложение поможет составить \nвам реферат документа с помощью\nSentence extraction и ML",
        fill="#000000",
        font=("Inter", 16 * -1)
    )

    canvas.create_text(
        12.0,
        219.0,
        anchor="nw",
        text="Кнопка “Выбрать документ” позволит вам\nвыбрать документ для создания реферата",
        fill="#000000",
        font=("Inter", 16 * -1)
    )

    canvas.create_text(
        13.0,
        291.0,
        anchor="nw",
        text="Кнопка “Выбрать папку” создаст реферат\nвсех документов из выбранной папки",
        fill="#000000",
        font=("Inter", 16 * -1)
    )

    canvas.create_text(
        12.0,
        90.0,
        anchor="nw",
        text="Кнопка ",
        fill="#000000",
        font=("Inter", 16 * -1)
    )

    canvas.create_text(
        135.0,
        90.0,
        anchor="nw",
        text="сохранит весь вывод",
        fill="#000000",
        font=("Inter", 16 * -1)
    )

    canvas.create_text(
        12.0,
        132.0,
        anchor="nw",
        text="программы в текстовый файл с\nназванием “save.txt”",
        fill="#000000",
        font=("Inter", 16 * -1)
    )

    image_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    image_1 = canvas.create_image(
        101.0,
        99.0,
        image=image_image_1
    )
    help_window.resizable(False, False)
    help_window.mainloop()


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
button_image_save = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_save = Button(
    image=button_image_save,
    borderwidth=0,
    highlightthickness=0,
    command=save_output,
    relief="flat"
)
button_save.place(
    x=113.0,
    y=17.0,
    width=47.600006103515625,
    height=47.600006103515625
)

button_image_help = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_help = Button(
    image=button_image_help,
    borderwidth=0,
    highlightthickness=0,
    command=help_window,
    relief="flat"
)
button_help.place(
    x=181.0,
    y=17.0,
    width=77.0,
    height=47.600006103515625
)

button_image_pick_folder = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_pick_folder = Button(
    image=button_image_pick_folder,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print(select_folder()),
    relief="flat"
)
button_pick_folder.place(
    x=474.0,
    y=17.0,
    width=176.0,
    height=47.600006103515625
)

button_image_pick_document = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_pick_document = Button(
    image=button_image_pick_document,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print(select_document()),
    relief="flat"
)
button_pick_document.place(
    x=278.0,
    y=17.0,
    width=176.0,
    height=47.600006103515625
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

menu = tkinter.Menu(tearoff=False)
menu.add_command(label="Copy", command=popup_copy)
menu.add_command(label="Cut", command=popup_cut)
menu.add_separator()
menu.add_command(label="Paste", command=popup_paste)
text_area.bind("<Button-3>", display_popup)

window.resizable(False, False)
window.mainloop()
