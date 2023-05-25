import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
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
    return summary

# Tokenize the text with the SpaCy pipeline. This segments the text into words, punctuation, and so on, using grammatical rules specific to the English language. 
# Count the number of times a word is used (not including stop words or punctuation), then normalize the count. A word that’s used more frequently has a higher normalized count.
# Calculate the sum of the normalized count for each sentence.
# Extract a percentage of the highest ranked sentences. These serve as our summary.