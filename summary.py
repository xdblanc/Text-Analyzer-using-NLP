import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from transformers import pipeline
from string import punctuation
from heapq import nlargest
from transformers import PegasusForConditionalGeneration, AutoTokenizer
import torch
import re

punctuation = punctuation + '\n'
def sum(text):
    nlp = spacy.load('en_core_web_sm')
    stopwords = list(STOP_WORDS)
    doc = nlp(text)
    tokens = [token.text for token in doc]
    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in stopwords:
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1               
    max_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word]/max_frequency
    sentence_tokens = [sent for sent in doc.sents]
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[word.text.lower()]
    select_length = int(len(sentence_tokens)*0.3)
    summary = nlargest(select_length, sentence_scores, key = sentence_scores.get)
    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)
    return(summary)
    
def pegtor(text):
    model_name = 'google/pegasus-cnn_dailymail'
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = PegasusForConditionalGeneration.from_pretrained(model_name).to(device)
    batch = tokenizer(text, truncation=True, padding='longest', return_tensors="pt").to(device)
    translated = model.generate(**batch)
    tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)
    return(tgt_text[0])


def piptrans(text):
    summarizer = pipeline("summarization")
    t3=summarizer(text, max_length=130, min_length=100, do_sample=False)
    return t3[0]['summary_text']

def summary(txt):
    l = re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', txt)

    c=len(l)
    p=q=r=""
    for i in l[0:c//3]:
        p=p+i
    for i in l[(c//3) :2*c//3]:
        q=q+i
    for i in l[2*c//3:c]:
        r=r+i
    
    return(sum(p)+piptrans(q)+pegtor(r))