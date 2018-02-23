import numpy as np
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier as RFC
import sys  
reload(sys)
sys.setdefaultencoding('utf8')

### Functions
def create_feature_presence_vectors(instances):
    labels = []
    vectors = []
    for instance in instances:
        label = instance[0]
        vector = instance[1]
        labels.append(label)
        vectors.append(vector)
    return vectors, labels
 
def svm_experiment(train_x,train_y,test_x,test_y):
    clf = svm.SVC(kernel='linear',cache_size = 512)
    clf.fit(train_x,train_y)
    p = clf.predict(test_x)
    accuracy = (np.sum(p == test_y)/np.float_(len(test_y)))
    #print 'Accuracy: %.4f'%(accuracy)
    return accuracy
    
def nb_experiment(train_x,train_y,test_x,test_y):
    clf = BernoulliNB()
    clf.fit(train_x,train_y)
    p = clf.predict(test_x)
    accuracy = (np.sum(p == test_y)/np.float_(len(test_y)))
    misclassifications = []
    for i in range(len(p)):
        if p[i] != test_y[i]:
            misclassifications.append(test_x[i])
    #print accuracy, misclassifications
    return accuracy

def combined_experiment(train_x,train_y,test_x,test_y,train_f_x,train_f_y,test_f_x,test_f_y, bias):
    labels = [] # Will contain all the final labels that result from the voting
    clf_c1 = MultinomialNB()
    clf_c1.fit(train_x,train_y)
    clf_c2 = BernoulliNB()
    clf_c2.fit(train_x,train_y)
    clf_f1 = svm.SVC(kernel='linear',cache_size = 512)
    clf_f1.fit(train_f_x,train_f_y)
    clf_f2 = svm.SVC(kernel='rbf',cache_size = 512)
    clf_f2.fit(train_f_x,train_f_y)
    
    p1 = clf_c1.predict(test_x)
    p2 = clf_c2.predict(test_x)
    p3 = clf_f1.predict(test_f_x)
    p4 = clf_f2.predict(test_f_x)
    if bias == 'content':
        for i in range(len(p1)):
            if p1[i] == p2[i] or p1[i] == p3[i]:
                labels.append(p1[i])
            else:
                labels.append(p2[i])
    elif bias == "syntax":
        for i in range(len(p1)):
            if p1[i] == p3[i] or p1[i] == p4[i]:
                labels.append(p1[i])
            else:
                labels.append(p3[i])
    else:
        print 'Please enter a valid bias ("syntax" or "content")!'
    p_combined = np.array(labels)
    accuracy = (np.sum(p_combined == test_y)/np.float_(len(test_y)))
    return accuracy

def rf_experiment(train_x,train_y,test_x,test_y):
    clf = RFC(n_estimators=25)
    clf.fit(train_x,train_y)
    p = clf.predict(test_x)
    accuracy = (np.sum(p == test_y)/np.float_(len(test_y)))
    return accuracy