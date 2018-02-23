# -*- coding: utf-8 -*-
import nltk.corpus
import string
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
from nltk.util import ngrams
from nltk.tokenize import word_tokenize
from senticnet.senticnet import Senticnet
sn = Senticnet()
#import unidecode

# Get default English stopwords and extend with punctuation
stopwords = nltk.corpus.stopwords.words('english')
stopwords.extend(string.punctuation)
stopwords.append('')

# The next lines are required for importing stanford pos-tagger, which is based on java
import os
from nltk.tag import StanfordPOSTagger
java_path = "C:/Program Files/Java/jdk1.8.0_144/bin/java.exe" # Replace this
os.environ['JAVAHOME'] = java_path
st = StanfordPOSTagger('File_directory/.../stanford-postagger-2017-06-09/models/english-bidirectional-distsim.tagger','File_directory/.../stanford-postagger-2017-06-09/stanford-postagger.jar')

'''------------------------------------Functions---------------------------------------'''
def measure_overlap_bows(a, b, threshold): 
    """Check if a and b are matches."""
    tokens_a = [strip_punctuation(token) for token in nltk.word_tokenize(a) if strip_punctuation(token) not in stopwords]
    tokens_b = [strip_punctuation(token) for token in nltk.word_tokenize(b) if strip_punctuation(token) not in stopwords]
    # Calculate Jaccard similarity
    ratio = len(set(tokens_a).intersection(tokens_b)) / float(len(set(tokens_a).union(tokens_b)))
    return (ratio >= threshold)

def strip_punctuation(token):
    new_token = token.lower()
    for i in string.punctuation:
        if i in new_token:
            new_token = token.strip(' ')
            new_token = new_token.split(i)
            new_token = ' '.join(new_token)
    return new_token

def preprocess_with_stopwords(text):
    result = [strip_punctuation(token) for token in nltk.word_tokenize(text)]
    return result

def preprocess(text):
    result = [strip_punctuation(token) for token in nltk.word_tokenize(text)\
                if strip_punctuation(token) not in stopwords]
    return result

def split_contractions(sentence):
    sentence = sentence.split(' ')
    processed_words = []
    for word in sentence:
#        if "'s" in word.lower():
#            word = word.split("'")
#            processed_words.append(word[0])
#            processed_words.append('is')
        if "'re" in word.lower():
            word = word.split("'")
            processed_words.append(word[0])
            processed_words.append('are')
        elif "'ll" in word.lower():
            word = word.split("'")
            processed_words.append(word[0])
            processed_words.append('will')
        elif "'m" in word.lower():
            word = word.split("'")
            processed_words.append(word[0])
            processed_words.append('am')
        elif "'t" in word.lower():
            if word.lower() == "can't":
                processed_words.append('can')
                processed_words.append('not')
            elif word.lower() == "won't":
                processed_words.append('will')
                processed_words.append('not')
            else:    
                processed_words.append(''.join(word.split("'")[0][:-1]))
                processed_words.append('not')
        else:
            processed_words.append(word)
    separator = ' '
    processed_sentence = separator.join(processed_words)
    return processed_sentence

def pos_tag_sentence(sentence):
    tokenized = nltk.word_tokenize(sentence)
    sent = [strip_punctuation(word) for word in tokenized]
    tagged_sentence = st.tag(' '.join(sent).split()) 
    return tagged_sentence

def create_POS_representation(sentence):
    pos_tagged_sentence = pos_tag_sentence(sentence)
    sent_tags = [pos for word,pos in pos_tagged_sentence]
    pos_representation = ' '.join(sent_tags)
    return pos_representation

def create_bow(instances):
    print "1. Create Bag-of-Words"
    bow = []
    for instance in instances:
        bow.append(preprocess(instance))
    print 'Done!'
    return list(set(bow))
 
def find_tagged_words(sentence, pos_tags):
    pos_tagged_sentence = pos_tag_sentence(sentence)
    words = [word for word,pos in pos_tagged_sentence if pos in pos_tags and word not in stopwords]          
    return words

def get_ngrams(text, n ):
    n_grams = ngrams(word_tokenize(text), n)
    return [ ' '.join(grams) for grams in n_grams]

def get_sentiment_score(preprocessed_sentence):
    score = 0.0
    absolute_score = 0.0
    for word in preprocessed_sentence:
        try:
            word_value = float(sn.polarity_intense(word))
            score += word_value
            if word_value < 0.0:
                absolute_score += (word_value * -1.0)
            else: 
                absolute_score += word_value
        except KeyError:
            continue
    return score, absolute_score
