# -*- coding: utf-8 -*-
def write_to_pickle(filename, list_of_sentences):
    import cPickle as pickle
    f = open("%s.pickle"%filename, "wb")
    pickle.dump(list_of_sentences, f)
    f.close()
    print "The data was saved to %s.pickle. The file contains %d lines."%(filename, len(list_of_sentences))
    
def write_to_csv(filename, list_of_sentences):
    import csv
    with open("%s.csv"%filename, 'wb') as f:
        wr = csv.writer(f, delimiter=',')
        for row in list_of_sentences:
            wr.writerow([row[0], row[1], row[2], row[3]])
    print "The data was saved to %s.csv. The file contains %d lines."%(filename, len(list_of_sentences))