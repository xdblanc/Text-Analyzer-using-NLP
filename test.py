import nltk
from nltk.corpus import wordnet
from nltk import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
import nltk
from nltk.corpus import wordnet
import random
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('stopwords')
from styleformer import Styleformer

import spacy
import nltk
from nltk.stem import WordNetLemmatizer
import spacy
nlp = spacy.load('en_core_web_sm')
stop_words = set(stopwords.words('english'))



def puraj(input):
    flag=False

    def active_to_passive(text):
        sf=Styleformer(style=2)
        res=sf.transfer(text)
        return res

    def passive_to_active(text):
        sf=Styleformer(style=3)
        res=sf.transfer(text)
        return res
    def is_active_voice(sentence):
        doc = nlp(sentence)
        for token in doc:
            if token.dep_ == "nsubj" and token.head.pos_ == "VERB":
                return True
        return False

    def find_tense(sentence):
        doc = nlp(sentence)

        for token in doc:
            if token.tag_.startswith("VB"):
                if token.tag_ == "VBD":
                    return "Past"
                elif token.tag_ == "VBG":
                    return "Present continuous"
                elif token.tag_ == "VBN":
                    return "Past participle"
                elif token.tag_ == "VBP":
                    return "Present"
                elif token.tag_ == "VBZ":
                    return "Present"
                else:
                    return "Unknown"

        return "Unknown"
    def convert_to_past_tense(sentence):
        doc = nlp(sentence)
        converted_words = [token.lemma_ if token.tag_ == "VBZ" else token.text for token in doc]
        converted_sentence = " ".join(converted_words)
        return converted_sentence

    def convert_to_present_tense(sentence):
    
        words = nltk.word_tokenize(sentence)
        # Initialize WordNet lemmatizer
        lemmatizer = WordNetLemmatizer()
        # Lemmatize each word to its base form
        present_tense_words = [lemmatizer.lemmatize(word, pos='v') for word in words]
        # Join the converted words back into a sentence
        present_tense_sentence = " ".join(present_tense_words)
        return present_tense_sentence


    def find_similar_synonyms(word):
        synonyms = []
        
        # Retrieve synsets for the word
        synsets = wordnet.synsets(word)
        
        # Iterate over each synset
        for synset in synsets:
            # Retrieve synonyms for each synset
            for lemma in synset.lemmas():
                # Add the synonym to the list
                synonyms.append(lemma.name())
        
        # Remove duplicates and sort the list of synonyms
        synonyms = list(set(synonyms))
        
        # Sort synonyms based on their similarity to the word
        synonyms.sort(key=lambda x: nltk.edit_distance(word, x))
        
        # Return the three most similar synonyms
        return synonyms[:5]

    def paraphrase_sentence(sentence):
        tokenized_sentence = word_tokenize(sentence)
        res=' '

        for word in tokenized_sentence:
        
            xx=word.lower()
            synonym2 = find_similar_synonyms(word)
            if xx in stop_words or len(synonym2) < 3:
                res+=word+' '
                continue
            else:

                if len(synonym2) >= 3:
                    for j in synonym2:
                        x=0
                        if j !=word:
                            x=random.randint(0,len(synonym2)-1)
                        
                        sim_word=synonym2[x]
                else:
                    sim_word=''
                res+=sim_word+' '
        return(res)


    s=sent_tokenize(input)
    final=''
    for i in s:
        flag=is_active_voice(i)

        if flag==False:
            res=passive_to_active(i)
        elif flag==True:
            res=active_to_passive(i)
        
        tense = find_tense(res)
        if tense!='Present':    
            sen = convert_to_present_tense(res)
        elif tense=='Present':
            sen = convert_to_past_tense(res)

        output_text_1=(sen.capitalize())
        final+=output_text_1+" "

    return(paraphrase_sentence(final))
