# -*- coding: utf-8 -*-
from lxml import html
import requests
import write_functions as w

def find_categories(tree,name_category_class):      
    categories = tree.find_class(name_category_class)
    url_c_names = []
    for c in categories:
        c_name = c.text_content().lower()
        split_c_name = c_name.split('\n')
        split_c_name = filter(None,split_c_name)
        
        split2 = []
        for i in split_c_name:
            split2 += i.split('\r')
        split2 = filter(None,split2)
        
        split3 = []
        for i in split2:
            split3.append(i.strip())
        split3 = filter(None,split3)
        split4 = [[i.strip(' ')] for i in split3]

    for i in split4:
        for j in i:
            split5 = [j.split(' ')]
            url_c_names.append('-'.join(s for i in split5 for s in i))
    return url_c_names

def scrape_webpages(url,upper_bound_page_no, name_text_class):
    elements = []
    
    for p in range(1, int(upper_bound_page_no)+1):
        #request_page = requests.get('%s%s'%(url,p))
        tree = html.fromstring(requests.get('%s%s'%(url,p)).content)
        elements += tree.find_class(name_text_class)
        
    print "Found %d lines"%len(elements)
    return elements

def scrape_user_ratings(tree, pos_classname,neg_classname):
    thumbs_up = tree.find_class(pos_classname)
    pos_ratings = []
    single_rating = []
    for t in thumbs_up:
        single_rating = [str(i) for i in t.text_content() if i in '0123456789']
        pos_no = ''
        for s in single_rating:
            pos_no = pos_no + s
        pos_ratings.append(int(pos_no))
    #Negative ratings
    thumbs_down = tree.find_class(neg_classname)
    neg_ratings = []
    single_rating = []
    for t in thumbs_down:
        single_rating = [str(i) for i in t.text_content() if i in '0123456789']
        neg_no = ''
        for s in single_rating:
            neg_no = neg_no + s
        neg_ratings.append(int(neg_no))
    #Calculate and return overall score
    scores = []
    if len(pos_ratings) == len(neg_ratings):
        for i in range(len(pos_ratings)):
            scores.append(pos_ratings[i]-neg_ratings[i])
    else:
        print 'Missing a positive or negative vote'
    return scores

text_class_name = 'joke-text'
category_class_name = 'jokes-nav'
pos_classname = 'like'
neg_classname = 'dislike'
output1 = []
tree = html.fromstring(requests.get('http://www.laughfactory.com/jokes/word-play-jokes/1').content)
categories = find_categories(tree, category_class_name)
print 'Categories Identified: %d'%len(categories)
lines = []

for c in categories[3:]: # Skip the categories Popular jokes, latest jokes and joke of the day, as these will all contain doubles anyways
    found_lines = []
    category_scores = []
    keep_lines = []
    tree = html.fromstring(requests.get('http://www.laughfactory.com/jokes/%s/1'%c).content)
    page_max = 40 # In this specific case, no category has more than 40 pages

    for p in range(1,page_max):
        tree = html.fromstring(requests.get('http://www.laughfactory.com/jokes/%s/%d'%(c,p)).content)       
        category_scores = category_scores + scrape_user_ratings(tree, pos_classname,neg_classname)
    found_lines += scrape_webpages('http://www.laughfactory.com/jokes/%s/'%(c),page_max,text_class_name)
    # Filter out not funny jokes.    
    if len(category_scores) == len(found_lines):
        for i in range(len(found_lines)):
            if category_scores[i] >= 0:
                keep_lines.append(found_lines[i].text_content())
    else:
        print 'The number of scores and the number of lines are imbalanced'
        print '%d scores found'%len(category_scores)
        print '%d lines found'%len(found_lines)
    
    print "Finished processing %s.\nIt contained %d funny lines."%(c,len(keep_lines))
    for l in keep_lines:
        r = l.strip('\r')
        n = r.strip('\n')
        rn = n.replace('\r\n', '')
        space = rn.strip(' ')
        q = space.replace('Q:','')
        a = q.replace('A:','')
        lines.append(a.decode('utf-8', "replace"))
        
print len(lines)
print lines[0:5]
# split_output1 = []
# split2_output1 = []
# output2 = []
# for i in lines:
#     split_output1 += i.split('\n')
# for i in split_output1:
#     split2_output1 += i.split('\r')
# split2_output1 = filter(None,split2_output1)
# split3_output1 = [[i.strip(' ')] for i in split2_output1]
# 
# for i in split3_output1:
#     output2 += filter(None,i)
# print output2[0:5]
# # Write away the found oneliners
w.write_to_pickle("laughfactory", lines)