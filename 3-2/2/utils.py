from bs4 import BeautifulSoup


def extract_text_from_html(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    soup = BeautifulSoup(content, "html.parser")
    text = soup.get_text()
    return text