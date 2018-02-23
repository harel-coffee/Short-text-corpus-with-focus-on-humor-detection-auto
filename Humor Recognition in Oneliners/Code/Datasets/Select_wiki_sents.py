# -*- coding: utf-8 -*-
import random
import string
import nltk
import cPickle as pickle
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(ngram_range=(1,3))
import write_functions as w
import Text_Processing as tp
import tf_idf_classification_functions as c

# Get default English stopwords and extend with punctuation
stopwords = nltk.corpus.stopwords.words('english')
stopwords.extend(string.punctuation)
stopwords.append('')

# Import the sentences that need processing from a pickle file
filename = "short_oneliners.pickle"
oneliners = pickle.load(open(filename))
print "File succesfully imported. The file contains %d sentences." %len(oneliners)
oneliners = [i.decode('utf8','replace') for i in oneliners]

filename2 = 'short_wiki_all_sentences.pickle' #you should have created this file at the end of the Deduplication step
wikipedia = pickle.load(open(filename2))
print "File succesfully imported. The file contains %d sentences." %len(wikipedia)
wikipedia = [i.decode('utf8','replace') for i in wikipedia]

def draw_from_list_randomly(dataset, samplesize): # Use if a random set needs to be drawn
    items = []
    rand_list = random.sample(dataset, samplesize)
    for i in rand_list:
        items.append(i.replace('\n',''))
    return items

def print_top_tfidf(vectorizer, clf, class_labels, top_n):
    """Prints features with the highest coefficient values, per class"""
    feature_names = vectorizer.get_feature_names()

    for class_label in enumerate(class_labels):
        top_list = np.argsort(clf.coef_[0])[-top_n:]
        #print("%s: %s" % (class_label,
        #      " - ".join(feature_names[j] for j in top_list)))
        top_feats = [feature_names[j] for j in top_list if feature_names[j] not in stopwords]
        print "Top %d features were found."%top_n
    return top_feats

train_set = []
for i in range(len(oneliners)):
    train_set.append(['POS', oneliners[i]])
    train_set.append(['NEG', wikipedia[i]])
train_x, train_y = c.create_tf_idf_train_vector(train_set)

data = []
labels = []
for instance in train_set:
    labels.append(instance[0])
    data.append(instance[1])
vectorizer.fit_transform(data)
clf = MultinomialNB()
clf.fit(train_x,train_y)

top_words = print_top_tfidf(vectorizer, clf, ['POS'], 6000)

''' Finished gathering top features from oneliners set compared to wiki set; continue selecting wiki sentences '''
def find_similar_sentences(source_list, top_word_list):
    keep_items = []
    for sentence in source_list:
        add_sentence = 0
        for tw in top_word_list:
            if tw in sentence:
                add_sentence = 1
                top_word_list.pop(top_word_list.index(tw))
        if add_sentence == 1:
            keep_items.append(sentence)
        if (source_list.index(sentence)+ 1) % 5000 == 0:
            print "Kept/processed: %d/%d"%(len(keep_items), source_list.index(sentence)+1)
    return keep_items

similar_sentences = find_similar_sentences(wikipedia, top_words)
print len(similar_sentences)

if len(similar_sentences) > len(oneliners):
    wiki_sentences = draw_from_list_randomly(similar_sentences, len(oneliners))
else:
    print 'Not enough sentences were found in the first shift. \nProcess will be reiterated with the top 1000 ngrams.'
    wiki_sentences = similar_sentences
    while len(wiki_sentences) < len(oneliners):
        print "No. of Wikipedia sentences similar to oneliners; %d" %len(wiki_sentences)
        wikipedia2 = [s for s in wikipedia if s not in wiki_sentences]
        top_2000 = print_top_tfidf(vectorizer, clf, ['POS'], 2000)
        second_shift_sents = find_similar_sentences(wikipedia2, top_2000)
        no_required_sents = len(oneliners) - len(wiki_sentences)
        if len(second_shift_sents) < no_required_sents:
            for i in second_shift_sents:
                wiki_sentences.append(i)
        else:
            for i in draw_from_list_randomly(second_shift_sents, no_required_sents):
                wiki_sentences.append(i)

print "Amount of kept items: %d"%len(wiki_sentences)

# Write away processed data
w.write_to_pickle("similar_wiki_sentences", wiki_sentences)
