# -*- coding: utf-8 -*-
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn import svm

from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(ngram_range=(1,3))

### Functions

def create_vector(instances, bag_of_words):
    labels = []
    vectors = []
    for instance in instances:
        label = instance[0]
        vector = np.zeros(len(bag_of_words))
        for i in range(len(bag_of_words)):
            if bag_of_words[i] in instance[1]:
                vector[i] += 1
        vectors.append(vector)
        labels.append(label)
    return vectors, labels

def create_tf_idf_train_vector(instances):
    labels = []
    data = []
    for instance in instances:
        label = instance[0]
        data.append(instance[1])
        labels.append(label)
    vectors = vectorizer.fit_transform(data)
    return vectors, labels
    
def create_tf_idf_test_vector(instances):
    labels = []
    data = []
    for instance in instances:
        label = instance[0]
        data.append(instance[1])
        labels.append(label)
    vectors = vectorizer.transform(data)
    return vectors, labels
