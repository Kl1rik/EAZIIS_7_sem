import pyttsx3
import requests

from datetime import datetime
import speech_recognition as sr
from bs4 import BeautifulSoup


def text_to_speech(text, voice_str, rate_str, volume_str):
    engine = pyttsx3.init()

    voice_dict = {'Male': 0, 'Female': 1}
    voices = engine.getProperty('voices')

    voice = voices[voice_dict[voice_str]].id
    engine.setProperty('voice', voice)

    rate = 150
    volume = 0.5

    rate_volume_dic = {'Fast': 2, 'Default': 1, 'Slow': 0.5}

    rate = rate * rate_volume_dic[rate_str]
    engine.setProperty('rate', rate)

    volume = volume * rate_volume_dic[volume_str]
    engine.setProperty('volume', volume)
    engine.say(text)
    engine.runAndWait()
    engine.stop()


def recognize_speech(text):
    result = ""
    recognizer = sr.Recognizer()
    with sr.Microphone(device_index=1) as source:
        print('Listening :)')
        audio = recognizer.listen(source)

    try:
        out_text = recognizer.recognize_google(audio)

        out_text = out_text.lower()
        rez = "hmm, can't find anything, try again"
        if "security" in out_text:
            rez = "This article proposes an ML-based cyber security mechanism to optimize intrusion detection that attacks internet objects (IoT). Our approach consists of bringing together several learning methods namely supervised learning, unsupervised learning and reinforcement learning within the same Canvas."

        elif 'crime' in out_text:
            rez = "There have been increased levels of cybercrime in the database industry, which has hurt the confidentiality, integrity, and availability of these systems. Most organizations apply several security layers to detect and prevent database crimes."

        elif "cockroach" in out_text:
            rez = "Madagascar hissing cockroaches (Gromphadorhina portentosa) fitted with electrodes and sensors could help to search for humans after an earthquake."

        elif "chat" in out_text:
            rez = "Some scientists have long been aware of the potential of large language models. But for many, it was ChatGPTs release as a free-to-use dialogue agent in November 2022 that quickly revealed this technologys power and pitfalls."

        elif "air quality prediction" in out_text:
            rez = "Urban activities, particularly vehicle traffic, are contributing significantly to environmental pollution with detrimental effects on public health. The ability to anticipate air quality in advance is critical for public authorities and the general public to plan and manage these activities, which ultimately help in minimizing the adverse impact on the environment and public health effectively."

        if "tell about" in out_text:
            text_to_speech(rez, 'Female', 'Default', 'Default')#Male
            result = out_text + " : " + rez

        elif "print" in out_text:
            result = rez
        else:
            result = "No such command: " + out_text
    except Exception as e:
        result = "Error!"
    return result
