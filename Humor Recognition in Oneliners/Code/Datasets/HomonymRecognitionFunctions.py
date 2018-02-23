# Import libraries required for functions
from collections import OrderedDict
from nltk.corpus import wordnet as wn
import nltk.corpus
import string
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import Text_Processing as tp

stopwords = nltk.corpus.stopwords.words('english')
stopwords.extend(string.punctuation)
stopwords.append('')

#Functions

def filter_similar_definitions(definition_list):
    remove_items = []
    for i in range(len(definition_list)+1):
        for definition in range(i+1,len(definition_list)):
            # Remove definitions with high path similarity
            similarity = definition_list[i][0].path_similarity(definition_list[definition][0])
            if similarity >= 0.30:
                remove_items.append(definition_list[definition][0])
            # Remove items with word overlap > 10% in definitions after stopwordremoval
            if tp.measure_overlap_bows(definition_list[i][1], definition_list[definition][1], 0.1) == True:
                remove_items.append(definition_list[definition][0])
    remove_items = list(OrderedDict.fromkeys(remove_items))
    distinct_defs = []

    for item in definition_list:
        if item[0] not in remove_items:
            distinct_defs.append(item)
    return distinct_defs
       
def check_homography(word):
    definitions = []
    if word not in stopwords:
        definitions = [[n, n.definition()] for n in wn.synsets(word) if n.lemmas()[0].name() == word]
        definitions = filter_similar_definitions(definitions)
        if len(definitions) >= 2:
            return True

def identify_homographs(words, sentence):
    #nouns_and_verbs = find_nouns_and_verbs(sentence)
    homographs = [w for w in words if check_homography(w) == True]
    return homographs

def find_nouns_and_verbs(sentence):
    pos_tagged_sentence = tp.pos_tag_sentence(sentence)
    nouns = [lemmatizer.lemmatize(tp.strip_punctuation(word)) for word,pos in pos_tagged_sentence if pos == 'NN' or pos == 'NNS' or pos == 'NNP' or pos == 'NNPS']
    verbs = [lemmatizer.lemmatize(tp.strip_punctuation(word)) for word,pos in pos_tagged_sentence if pos == 'VB' or pos == 'VBD' or pos == 'VBG' or pos == 'VBN' or pos == 'VBP' or pos == 'VBZ'] 
    #adjectives = [lemmatizer.lemmatize(tp.strip_punctuation(word)) for word,pos in pos_tagged_sentence if pos == 'JJ' or pos == 'JJR' or pos == 'JJS'] 
    nouns_and_verbs = nouns + verbs #+ adjectives
    return nouns_and_verbs