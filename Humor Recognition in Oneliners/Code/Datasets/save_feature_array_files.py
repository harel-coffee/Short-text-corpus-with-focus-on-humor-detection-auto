import cPickle as pickle
import Feature_recognition_functions as frf

# load datasets
filepath = "File_directory/.../Code/Datasets" # Fill in the correct path to your files
    
# Positive samples
oneliners = pickle.load(open("%s/oneliners.pickle"%filepath))
long_jokes = pickle.load(open("%s/long_jokes.pickle"%filepath))

# Negative samples
reuters = pickle.load(open("%s/reuters.pickle"%filepath))
wikipedia = pickle.load(open("%s/wikipedia.pickle"%filepath))
proverbs = pickle.load(open("%s/proverbs.pickle"%filepath))

# Transform all samples to feature presence arrays
oneliners_arrays = []
long_jokes_arrays = []
reuters_arrays = []
wikipedia_arrays = []
proverbs_arrays = []

############## Oneliners ####################
counter = 0
for i in oneliners:
    oneliners_arrays.append(frf.find_all_features(i))
    counter += 1
    if counter % 100 == 0:
        print "%d Items processed!"%counter
print "Finished processing Oneliners into feature arrays."
with open('%s/oneliners_features.pickle'%filepath, 'wb') as ol_features:
    pickle.dump(oneliners_arrays, ol_features)

############## Longer jokes ####################
counter = 0
for i in long_jokes:
    try:
        long_jokes_arrays.append(frf.find_all_features(i))
    except:
        print "Memory error occurred, skipped sentence"
        continue
    counter += 1
    if counter % 250 == 0:
        print "%d Items processed! %d items found!"%(counter,len(long_jokes_arrays))
print "Finished processing long_jokes into feature arrays."
with open('%s/long_jokes_features.pickle'%filepath, 'wb') as j1_features:
    pickle.dump(long_jokes_arrays, j1_features)
    
############## Reuters ####################
counter = 0
for i in reuters:
    reuters_arrays.append(frf.find_all_features(i))
    counter += 1
    if counter % 500 == 0:
        print "%d Items processed!"%counter
print "Finished processing Reuters into feature arrays."
with open('%s/reuters_features.pickle'%filepath, 'wb') as r_features:
    pickle.dump(reuters_arrays, r_features)

############## Wikipedia ####################
counter = 0
for i in wikipedia:
    wikipedia_arrays.append(frf.find_all_features(i))
    counter += 1
    if counter % 10 == 0:
        print "%d Items processed!"%counter
print "Finished processing Wikipedia into feature arrays."
with open('%s/wikipedia_features.pickle'%filepath, 'wb') as w_features:
    pickle.dump(wikipedia_arrays, w_features)
  
############## Proverbs ####################
for i in proverbs:
    proverbs_arrays.append(frf.find_all_features(i))
print "Finished processing Proverbs into feature arrays."
with open('%s/proverbs_features.pickle'%filepath, 'wb') as p_features:
    pickle.dump(proverbs_arrays, p_features)

print "All files have been saved successfully!"

# Run this to replace the homographs with their counts and save the new arrays to a new file
oneliners_arrays = pickle.load(open('%s/oneliners_features.pickle'%filepath))
reuters_arrays = pickle.load(open('%s/reuters_features.pickle'%filepath))
wikipedia_arrays = pickle.load(open('%s/wikipedia_features.pickle'%filepath))
proverbs_arrays = pickle.load(open('%s/proverbs_features.pickle'%filepath))
long_jokes_arrays = pickle.load(open('%s/long_jokes_features.pickle'%filepath))

################# Oneliners #################
for i in range(len(oneliners_arrays)):
    oneliners_arrays[i][15] = len(oneliners_arrays[i][15])
    oneliners_arrays[i][16] = len(oneliners_arrays[i][16])
with open('%s/oneliners_features_2.pickle'%filepath, 'wb') as o_features:
    pickle.dump(oneliners_arrays, o_features)

################# Longer Jokes ##############
for i in range(len(long_jokes_arrays)):
    long_jokes_arrays[i][15] = len(long_jokes_arrays[i][15])
    long_jokes_arrays[i][16] = len(long_jokes_arrays[i][16])
    
print "Finished processing Homographs in long_jokes_features into counts."
with open('%s/long_jokes_features_2.pickle'%filepath, 'wb') as j2_features:
    pickle.dump(long_jokes_arrays, j2_features)
    
##############  Reuters  ####################
for i in range(len(reuters_arrays)):
    reuters_arrays[i][15] = len(reuters_arrays[i][15])
    reuters_arrays[i][16] = len(reuters_arrays[i][16])
with open('%s/reuters_features_2.pickle'%filepath, 'wb') as r_features:
    pickle.dump(reuters_arrays, r_features)
    
############## Wikipedia ####################
for i in range(len(wikipedia_arrays)):
    wikipedia_arrays[i][15] = len(wikipedia_arrays[i][15])
    wikipedia_arrays[i][16] = len(wikipedia_arrays[i][16])
with open('%s/wikipedia_features_2.pickle'%filepath, 'wb') as w_features:
    pickle.dump(wikipedia_arrays, w_features)

############### Proverbs ####################
for i in range(len(proverbs_arrays)):
    proverbs_arrays[i][15] = len(proverbs_arrays[i][15])
    proverbs_arrays[i][16] = len(proverbs_arrays[i][16])
with open('%s/proverbs_features_2.pickle'%filepath, 'wb') as p_features:
    pickle.dump(proverbs_arrays, p_features)

print "Finished gathering all features and turning homographs into homograph counts."