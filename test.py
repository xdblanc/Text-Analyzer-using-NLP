import nltk
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
stop_words = set(stopwords.words('english'))
nltk.download('stopwords')
from nltk.corpus import wordnet

def get_synonyms(word):
    synonyms = set()
    for synset in wordnet.synsets(word):
        for lemma in synset.lemmas():
            synonyms.add(lemma.name())
    return synonyms

def calculate_similarity(synonym1, synonym2):
    synset1 = wordnet.synsets(synonym1)
    synset2 = wordnet.synsets(synonym2)

    if synset1 and synset2:  # Check if both synonyms have synsets
        similarity = synset1[0].wup_similarity(synset2[0])
        if similarity is not None:
            return similarity

    return 0  


def paraphrase_sentence(sentence):
    tokenized_sentence = word_tokenize(sentence)
    res=' '

    for word in tokenized_sentence:
      xx=word.lower()
      synonym2 = get_synonyms(word)
      if xx in stop_words or len(synonym2) < 3:
        res+=word+' '
        continue
      else:
        
        # print(synonym2)
        if len(synonym2) > 0:
          maximum =0
          for j in synonym2:
            if j !=word:
              similarity_score = calculate_similarity(word, j)
              if similarity_score > maximum:
                sim_word=j
                maximum=similarity_score
        else:
              sim_word=''
        res+=sim_word+' '
    return(res)






