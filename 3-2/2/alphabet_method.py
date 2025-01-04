def alphabet_detect_language(text):
    alphabets = {
        "english": set("abcdefghijklmnopqrstuvwxyz"),
        "spanish": set("abcdefghijklmnopqrstuvwxyzñáéíóúü")
    }

    text_set = set(text.lower())
    spanish, english = 0, 0
    for element in text_set:
        if element in alphabets['spanish']:
            spanish += 1
        if element in alphabets['english']:
            english += 1

    if spanish > english:
        return "spanish"
    elif english >= spanish:
        return "english"