# Imports
import cPickle as pickle
import write_functions as w
import Text_Processing as tp

# Import the sentences that need processing in pickle
filename = "Webscrapers/name_of_file.pickle"
unprocessed_sentences = pickle.load(open(filename))
print "File succesfully imported. %s contains %d sentences." %(filename, len(unprocessed_sentences))

''' uncomment (and copy with different variable names) lines below in case more pickle files need to be imported'''
# filename2 = 'filename2.pickle'
# unprocessed_sentences2 = pickle.load(open(filename2))
# print "File succesfully imported. %s contains %d sentences." %(filename2, len(unprocessed_sentences2))
# for i in unprocessed_sentences2:
#     unprocessed_sentences.append(i)

# Make sure all sentences are decoded correctly
unprocessed_sentences = [i.decode('utf8','replace') for i in unprocessed_sentences]
print "A total of %d lines were imported and are ready for deduplication!"%len(unprocessed_sentences)

''''Compare all sentences s for similarity with the sentences on index > s'''
keep_items = []
for i in range(len(unprocessed_sentences)):
    unique_item = True
    for item in keep_items:
        if tp.measure_overlap_bows(unprocessed_sentences[i], item, 0.9) == True:
            unique_item = False
    if unique_item == True:
        keep_items.append(unprocessed_sentences[i])
    if i%50 == 0: # Used to track progress of the deduplication process, might take a while
        print "Processed sentences:\t %d"%i

print "Amount of kept items: %d"%len(keep_items)
keep_short = []
keep_long = []
for item in keep_items:
    if len(item) < 140:
        keep_short.append(item)
    else:
        keep_long.append(item)

print "Amount of short items kept: %d"%len(keep_short)
# Write away processed data
w.write_to_pickle("deduplicated_file", keep_short)
# Uncomment next line to also store longer items
#w.write_to_pickle("deduplicated_long_jokes", keep_long)