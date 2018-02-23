#Imports
import cPickle as pickle
from sklearn.cross_validation import KFold
from sklearn.feature_selection import SelectKBest, chi2
import numpy as np
import feature_classification_functions as fcf
import tf_idf_classification_functions as c

filepath = "File_directory/.../Code/Datasets/" # Fill in the correct path to your files
oneliners_arrays = pickle.load(open('%s/oneliners.pickle'%filepath))
reuters_arrays = pickle.load(open('%s/reuters.pickle'%filepath))
wikipedia_arrays = pickle.load(open('%s/wikipedia.pickle'%filepath))
proverbs_arrays = pickle.load(open('%s/proverbs.pickle'%filepath))
long_jokes_arrays = pickle.load(open('%s/long_jokes.pickle'%filepath))

# Import files for feature recognition
# Load datasets containing the feature representations. Make sure to have ran save_feature_array_files at least once,
# .. and that you use the second feature representation file, containing homograph counts.
# Positive samples
oneliners_features = pickle.load(open('%s/oneliners_features_2.pickle'%filepath))
for i in range(len(oneliners_features)):
    oneliners_features[i].pop(-2) # Removes the values of the first homograph recognition method
    #oneliners_features[i].pop(-1) # Uncomment these two if you want to train and test the classifier without homophones and homographs
    #oneliners_features[i].pop(-1) # Any changes made on the lines in this for-loop, also need to be made for the other datasets
    oneliners_features[i] = np.asarray(oneliners_features[i])

# Negative samples
reuters_features = pickle.load(open('%s/reuters_features_2.pickle'%filepath))
for i in range(len(reuters_features)):
    reuters_features[i].pop(-2)
    reuters_features[i] = np.asarray(reuters_features[i])

wikipedia_features = pickle.load(open('%s/feature_array_files/wikipedia_features_2.pickle'%filepath))
for i in range(len(wikipedia_features)):
    wikipedia_features[i].pop(-2)
    wikipedia_features[i] = np.asarray(wikipedia_features[i])

proverbs_features = pickle.load(open('%s/feature_array_files/proverbs_features_2.pickle'%filepath))
for i in range(len(proverbs_features)):
    proverbs_features[i].pop(-2)
    proverbs_features[i] = np.asarray(proverbs_features[i])

long_jokes_features = pickle.load(open('%s/feature_array_files/long_jokes_features_2.pickle'%filepath))
for i in range(len(long_jokes_features)):
    long_jokes_features[i].pop(-2)
    long_jokes_features[i] = np.asarray(long_jokes_features[i])
    
#Use just as much Reuters headlines as there are oneliners (to prevent over-representation of Reuters headlines
reuters_arrays = reuters_arrays[0:len(oneliners_arrays)]
reuters_features = reuters_features[0:len(oneliners_features)]

datasets_neg_arrays = [proverbs_arrays, reuters_arrays, wikipedia_arrays]
datasets_neg_features = [proverbs_features, reuters_features, wikipedia_features]
dataset_names = ['Proverbs', 'Reuters','Wikipedia']
repeats = 30
for s in range(len(datasets_neg_arrays)):
    print "\n%s: "%dataset_names[s],
    avg_accuracies = []
    for r in range(0,repeats):
        kf = KFold(len(datasets_neg_arrays[s]), n_folds=10, shuffle = True) # Note that by design, this prevents the classifier from using more positive samples than there are negative ones, effectively using only 1019 oneliners against proverbs
        accuracies = []
        if r%10 == 0:
            print '%d / %d Finished'%(r,repeats) 
        for train_index,test_index in kf:
            train_set = [] # Contains tf idf representations of sentences
            test_set = []
            train_set_f = [] # Contains style-and ambiguity representations of sentences.
            test_set_f = []
            for i in train_index:
                train_set.append(['POS', oneliners_arrays[i]])
                train_set.append(['NEG', datasets_neg_arrays[s][i]])
                train_set_f.append(['POS', oneliners_features[i]])
                train_set_f.append(['NEG', datasets_neg_features[s][i]])
            longjoke_counter = 0 
            for i in test_index:
                longjoke_counter += 1
                test_set.append(['POS', oneliners_arrays[i]])
                test_set.append(['NEG', datasets_neg_arrays[s][i]])
                test_set_f.append(['POS', oneliners_features[i]])
                test_set_f.append(['NEG', datasets_neg_features[s][i]])
            train_f_x, train_f_y = fcf.create_feature_presence_vectors(train_set_f)
            test_f_x, test_f_y = fcf.create_feature_presence_vectors(test_set_f)
            train_x, train_y = c.create_tf_idf_train_vector(train_set)
            test_x, test_y = c.create_tf_idf_test_vector(test_set)
            ch2 = SelectKBest(chi2, k=500) #'all' for all features
            train_x = ch2.fit_transform(train_x, train_y)
            test_x = ch2.transform(test_x)
            'Run a bagged System III classifier:'
            accuracies.append(fcf.combined_experiment(train_x,train_y,test_x,test_y,train_f_x,train_f_y,test_f_x,test_f_y,'content'))
            'Run a single classification algorithm'
            #accuracies.append(fcf.nb_experiment(train_f_x,train_f_y,test_f_x,test_f_y))
        
        total_accuracy = 0.0
        for i in accuracies:
            total_accuracy += float(i)
        
        avg_accuracy = (total_accuracy / float(len(accuracies)))*100
        avg_accuracies.append(avg_accuracy)
    
    overall_accumulated_accuracy = 0.0
    for i in avg_accuracies:
        overall_accumulated_accuracy += float(i)
    overall_accuracy = (overall_accumulated_accuracy / float(len(avg_accuracies)))
    
    # PRINT statements
    print "Finished running System III %d times!"%len(avg_accuracies)
    print "\nAverage Accuracy : %.2f"%overall_accuracy