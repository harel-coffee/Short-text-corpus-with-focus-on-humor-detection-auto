# -*- coding: utf-8 -*-
# Import libraries
import csv
import cPickle as pickle
import Text_Processing as tp
import Feature_recognition_functions as frf
import string
punctuation = string.punctuation
punctuation += '"'

'The Code below handles the import of the annotated sentences, only keeping the unique occurrences'
with open('annotated_homographs_english_v4.csv') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    reduced_rows = []
    unique_sentences = []
    unique_ids = []
    duplicate_ids = []
    replace_list = []
    for row in spamreader:
        #print(', '.join(row))
        new_row = [row[-2], row[7], row[13], row[0]]
        reduced_rows.append(new_row)
        if new_row[0] not in unique_sentences:
            unique_sentences.append(new_row[0])
            if new_row[-1] not in unique_ids:
                unique_ids.append(new_row[-1])
        else:
            if new_row[-1] not in unique_ids and new_row[-1] not in duplicate_ids:
                duplicate_ids.append(new_row[-1])
                replace_list.append([new_row[-1],unique_ids[unique_sentences.index(new_row[0])]])

    print "Found %d rows!"%len(reduced_rows)

# Import the sentences that need processing from a pickle file
file_oneliners = "oneliners.pickle"
oneliners = pickle.load(open(file_oneliners))
print "File succesfully imported. The file contains %d sentences." %len(oneliners)

file_reuters = "reuters.pickle"
reuters = pickle.load(open(file_reuters))
print "File succesfully imported. The file contains %d sentences." %len(reuters)

file_wiki = 'wikipedia.pickle'
wikipedia = pickle.load(open(file_wiki))
print "File succesfully imported. The file contains %d sentences." %len(wikipedia)

datasets = [oneliners, reuters, wikipedia]

def check_groundtruth_homographs(preprocessed_sentence):
    'Import the data...'
    homographs = pickle.load(open('crowd_homographs_50.pickle'))
    #print "%d homographs found!"%len(homographs)
    found_homographs = []
    for word in preprocessed_sentence:
        if word in homographs:
            found_homographs.append(word)
    return homographs

def calculate_sentence_performance(correct_words,found_words,all_words):
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    for word in found_words:
        if word in correct_words:
            tp += 1
        else:
            fp += 1
    for word in all_words:
        if word not in found_words:
            if word not in correct_words:
                tn += 1
            else:
                fn += 1
    return [tp,tn,fp,fn]
    
def calculate_algorithm_performance(true_positives, true_negatives, false_positives, false_negatives):
    precision = true_positives / (true_positives + false_positives)
    recall = true_positives / (true_positives + false_negatives)
    fmeasure = 2 * ((precision * recall) / (precision + recall))
    accuracy = (true_positives + true_negatives) / (true_positives + true_negatives + false_positives+ false_negatives)
   
    return precision, recall, fmeasure, accuracy

total_homographs1 = [0.00000001,0.00000001,0.00000001,0.00000001] # Prevents 0 multiplication error
total_homographs2 = [0.00000001,0.00000001,0.00000001,0.00000001]
for sentence in unique_sentences:
    prepped_sent = tp.preprocess(sentence)
    # Create list of all homographs for each method
    groundtruth_sentence = check_groundtruth_homographs(prepped_sent)
    homographs1_results = frf.find_homographs1(prepped_sent)
    homographs2_results = frf.find_homographs2(prepped_sent, sentence)
    # Calculate true positives, true negatives, false positives and false negatives
    sent_result_1 = calculate_sentence_performance(groundtruth_sentence, homographs1_results, prepped_sent)
    sent_result_2 = calculate_sentence_performance(groundtruth_sentence, homographs2_results, prepped_sent)
    for i in range(len(sent_result_1)):
        total_homographs1[i] += sent_result_1[i]
        total_homographs2[i] += sent_result_2[i]

print total_homographs1
print total_homographs2
perf_homographs_1 = calculate_algorithm_performance(total_homographs1[0], total_homographs1[1], total_homographs1[2], total_homographs1[3])
print "Precision alg_1: %.3f \t Recall: %.3f \t F-measure: %.3f \t Accuracy: %.3f"%(perf_homographs_1[0], perf_homographs_1[1], perf_homographs_1[2], perf_homographs_1[3])

perf_homographs_2 = calculate_algorithm_performance(total_homographs2[0], total_homographs2[1], total_homographs2[2], total_homographs2[3])
print "Precision alg_2: %.3f \t Recall: %.3f \t F-measure: %.3f \t Accuracy: %.3f"%(perf_homographs_2[0], perf_homographs_2[1], perf_homographs_2[2], perf_homographs_2[3])
