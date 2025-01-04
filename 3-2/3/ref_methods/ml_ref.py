from transformers import BartForConditionalGeneration, BartTokenizer
from pathlib import Path

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer


def get_ml_ref(text, min, max):
    
    # Загрузка предварительно обученной модели BART и токенизатора
    model_name = "facebook/bart-large-cnn"
    model = BartForConditionalGeneration.from_pretrained(model_name)
    tokenizer = BartTokenizer.from_pretrained(model_name)
   
    inputs = tokenizer(text, return_tensors="pt", max_length=1024, truncation=True, padding=True)

    
    summary_ids = model.generate(inputs["input_ids"], max_length=max, min_length=min, length_penalty=1.0, num_beams=8,
                                 early_stopping=True)

    
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    print("Резюме:")
    print(summary)
    return summary



def summary_extraction(text):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    stemmer = Stemmer("english")

    summarizer = Summarizer(stemmer)

    summary = summarizer(parser.document, 3)
    return ' '.join([str(sentence) for sentence in summary])
