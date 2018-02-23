# -*- coding: utf-8 -*-
'Import modules'
import Text_Processing as tp
import cPickle as pickle
from nltk import wordnet as wn
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import HomonymRecognitionFunctions as hrf

# import cmudictionary for alliterations
from nltk.corpus import cmudict
transcr = cmudict.dict()
cmuwords = []
for w in transcr:
    cmuwords.append(w)

def find_phoneme_chains(preprocessed_sentence):
    all_chains = []
    rhyme_chains = []
    max_all_chain = 0
    max_rhyme_chain = 0
    # Get n_grams
    sentence = ' '.join(preprocessed_sentence)
    ngrams = tp.get_ngrams(sentence, 2)
    for ngram in tp.get_ngrams(sentence, 3):
        ngrams.append(ngram) # Add trigrams
    for ngram in tp.get_ngrams(sentence, 4):
        ngrams.append(ngram) # Add quadgrams

    for ngram in ngrams:
        ngram = ngram.split(' ')
        # Process bigrams
        if len(ngram) == 2:
            if ngram[0] in cmuwords and ngram[1] in cmuwords:
                if transcr[ngram[0]][0][0] == transcr[ngram[1]][0][0]:
                    all_chains.append(ngram)
                    if len(ngram) > max_all_chain:
                        max_all_chain = len(ngram)
                if len(transcr[ngram[0]][0]) >= 2 and len(transcr[ngram[1]][0]) >= 2:
                    if transcr[ngram[0]][0][-1] == transcr[ngram[1]][0][-1] and transcr[ngram[0]][0][-2] == transcr[ngram[1]][0][-2]:
                        rhyme_chains.append(ngram)
                        if len(ngram) > max_rhyme_chain:
                            max_rhyme_chain = len(ngram)
        # Process trigrams
        if len(ngram) == 3:
            if ngram[0] in cmuwords and ngram[1] in cmuwords and ngram[2] in cmuwords:
                if transcr[ngram[0]][0][0] == transcr[ngram[1]][0][0] == transcr[ngram[2]][0][0]:
                    all_chains.append(ngram)
                    if len(ngram) > max_all_chain:
                        max_all_chain = len(ngram)
                if len(transcr[ngram[0]][0]) >= 2 and len(transcr[ngram[1]][0]) >= 2:
                    if transcr[ngram[0]][0][-1] == transcr[ngram[1]][0][-1] == transcr[ngram[2]][0][-1]\
                     and transcr[ngram[0]][0][-2] == transcr[ngram[1]][0][-2] == transcr[ngram[2]][0][-2]:
                        rhyme_chains.append(ngram)
                        if len(ngram) > max_rhyme_chain:
                            max_rhyme_chain = len(ngram)
        # Process trigrams
        if len(ngram) == 4:
            if ngram[0] in cmuwords and ngram[1] in cmuwords and ngram[2] in cmuwords and ngram[3] in cmuwords:
                if transcr[ngram[0]][0][0] == transcr[ngram[1]][0][0] == transcr[ngram[2]][0][0] == transcr[ngram[3]][0][0]:
                    all_chains.append(ngram)
                    if len(ngram) > max_all_chain:
                        max_all_chain = len(ngram)
                if len(transcr[ngram[0]][0]) >= 2 and len(transcr[ngram[1]][0]) >= 2:
                    if transcr[ngram[0]][0][-1] == transcr[ngram[1]][0][-1] == transcr[ngram[2]][0][-1] == transcr[ngram[3]][0][-1]\
                     and transcr[ngram[0]][0][-2] == transcr[ngram[1]][0][-2] == transcr[ngram[2]][0][-2]  == transcr[ngram[3]][0][-2]:
                        rhyme_chains.append(ngram)
                        if len(ngram) > max_rhyme_chain:
                            max_rhyme_chain = len(ngram)
    # normalize max length for sentence length after stopword removal
    max_all_chain = max_all_chain / float(len(preprocessed_sentence))
    max_rhyme_chain = max_rhyme_chain / float(len(preprocessed_sentence))
    
    return len(all_chains), max_all_chain, len(rhyme_chains), max_rhyme_chain

def find_negations(preprocessed_sentence):
    boolean = 0
    for word in preprocessed_sentence:
        if lemmatizer.lemmatize(word) == "not":
            boolean = 1
    return boolean

def check_for_antonym_presence(preprocessed_sentence):
    boolean = 0
    antonyms = []
    # Find the antonyms of all words
    word_lemmas = []
    for word in preprocessed_sentence:
        word_synsets = wn.wordnet.synsets(word)
        for i in word_synsets:
            word_lemmas.append(i.lemmas())
            for lemma in i.lemmas():
                if len(lemma.antonyms()) > 0:
                    antonyms.append(lemma.antonyms())
    
    # Add antonyms of adjectives similar to the adjectives used
    sentence = ' '.join(preprocessed_sentence)
    adjectives = tp.find_tagged_words(sentence, ['JJ','JJR','JJS'])
    adj_similars = []
    for adj in adjectives:
        for ss in wn.wordnet.synsets(adj,'a'):
            for similar in ss.similar_tos():
                adj_similars.append(similar)

    for ss in adj_similars:
        for lemma in ss.lemmas():
            if len(lemma.antonyms()) > 0:
                antonyms.append(lemma.antonyms())
    
    # Check whether antonyms are in the same sentence
    for lemma in word_lemmas:
        if lemma in antonyms:
            boolean = 1
    return boolean

def check_for_adultslang_presence(preprocessed_sentence):
    boolean = 0
    # Create list of slang words
    adult_slang = ['offensive term', 'offensive word', 'slang', 'vulgar term', 'vulgar word', 'obscene term', 'obscene word']
   
    # Check list for sexuality
    sentence = ' '.join(preprocessed_sentence)
    ngrams = tp.get_ngrams(sentence, 1)
    for ngram in tp.get_ngrams(sentence, 2):
        ngrams.append(ngram) # Add bigrams
    for ngram in tp.get_ngrams(sentence, 3):
        ngrams.append(ngram) # Add trigrams
    
    adult_slang2 = []
    hyponyms = []
    for i in wn.wordnet.synsets('sexual_activity'):
        hyponyms.append(i.hyponyms())
    for i in wn.wordnet.synsets('sexuality'):
        hyponyms.append(i.hyponyms())
    
    for h in hyponyms:
        for synset in h:
            hypo = [str(lemma.name()) for lemma in synset.lemmas()]
            for synset2 in synset.hyponyms():
                for lemma in synset2.lemmas():
                    hypo.append(str(lemma.name()))
                for synset3 in synset2.hyponyms():
                    for lemma in synset3.lemmas():
                        hypo.append(str(lemma.name()))
            for instance in hypo:
                token = tp.strip_punctuation(instance)
                adult_slang2.append(token)
    '''Finished retrieving sex words  '''
    
    # Check definitions for one of the ngrams in variable adult_slang
    definitions = []
    for word in preprocessed_sentence:
        word_synsets = wn.wordnet.synsets(word)
        for s in word_synsets:
            definitions.append(s.definition())
    for d in definitions:
        for slang in adult_slang:
            if slang in d:
                boolean = 1
    
    # check whether words in ngrams occur in adult_slang2 as well
    for n in ngrams:
        if n in adult_slang2:
            boolean = 1
    return boolean

def check_sentiment_polarity(preprocessed_sentence):
    sentiment = tp.get_sentiment_score(preprocessed_sentence)
    return sentiment

def find_pos_ratios(sentence):
    pos_sent = tp.create_POS_representation(sentence).split()
    pronouns = 0
    verbs = 0
    com_nouns = 0
    prop_nouns = 0
    modifiers = 0
    for i in pos_sent:
        if i in ['PRP','PRP$']:
            pronouns += 1
        elif i in ['VB','VBD','VBG', 'VBN','VBP','VBZ']:
            verbs += 1
        elif i in ['NN','NNS']:
            com_nouns += 1
        elif i in ['NNP','NNPS']:
            prop_nouns += 1
        elif i in ['JJ','JJR','JJS','RB','RBR','RBS']:
            modifiers += 1
    pronouns = pronouns / float(len(pos_sent))
    verbs = verbs / float(len(pos_sent))
    com_nouns = com_nouns / float(len(pos_sent))
    prop_nouns = prop_nouns / float(len(pos_sent))
    modifiers = modifiers / float(len(pos_sent))

    return pronouns, verbs, com_nouns, prop_nouns, modifiers

def find_homophones(preprocessed_sentence):
    boolean = 0
    for word in preprocessed_sentence:
        if word in cmuwords:
            for cmu in cmuwords:
                if transcr[word][0] == transcr[cmu][0] and word != cmu:
                    boolean = 1
    return boolean

def find_homographs1(preprocessed_sentence):
    'Import the data...'
    file_homographs = 'C:/Users/Sven/Google Drive/Sven vd Beukel (Msc)/feature_recognition/homographs.txt'
    homograph_list = open(file_homographs,'r').readlines()
    homograph_list = [i.strip('\n').decode('utf-8', 'replace') for i in homograph_list]
    homographs = []
    for word in preprocessed_sentence:
        if word in homograph_list:
            homographs.append(word)
    return homographs

def find_homographs2(preprocessed_sentence, full_sentence):
    homographs = [h for h in hrf.identify_homographs(preprocessed_sentence, full_sentence) if h.isdigit() != True]
    return homographs

def find_all_features(sentence):
    sentence = tp.split_contractions(sentence)
    prep_sentence = tp.preprocess(sentence)
    feature_array = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    phoneme_chains = find_phoneme_chains(prep_sentence)
    feature_array[0] = phoneme_chains[0] # No. of Alliteration chains
    feature_array[1] = phoneme_chains[1] # max. length of Alliteration chains
    feature_array[2] = phoneme_chains[2] # No. of Rhyme chains
    feature_array[3] = phoneme_chains[3] # max. length of Rhyme chains
    feature_array[4] = find_negations(prep_sentence) # Boolean: 1 if  a negation is present, 0 if not
    feature_array[5] = check_for_antonym_presence(prep_sentence) # Boolean: 1 if an antonym is present, 0 if not
    feature_array[6] = check_for_adultslang_presence(prep_sentence) # Boolean: 1 if adult slang is present, 0 if not
    sentiment = check_sentiment_polarity(prep_sentence) # Value between -1 (very negative) and 1 (very positive)
    feature_array[7] = sentiment[0] # Sentiment polarity value
    feature_array[8] = sentiment[1] # Absolute Sentiment polarity value
    pos_ratios = find_pos_ratios(sentence)
    feature_array[9] = pos_ratios[0]  # Ratio pronouns
    feature_array[10] = pos_ratios[1]  # Ratio verbs
    feature_array[11] = pos_ratios[2] # Ratio Common nouns
    feature_array[12] = pos_ratios[3] # Ratio Proper nouns
    feature_array[13] = pos_ratios[4] # Ratio Modifiers (Adverbs and adjectives)
    feature_array[14] = find_homophones(prep_sentence)  # Boolean: 1 if a homophone is present, 0 if not
    feature_array[15] = find_homographs1(prep_sentence) # Found homographs
    feature_array[16] = find_homographs2(prep_sentence, sentence) # Found homographs

    #print "Features processed and converted to feature arrays!"
    return feature_array