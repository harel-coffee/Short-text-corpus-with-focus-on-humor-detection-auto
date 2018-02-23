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
        #print i
        for j in i:
            split5 = [j.split(' ')]
            url_c_names.append('-'.join(s for i in split5 for s in i))
    return url_c_names

def scrape_webpages(url,upper_bound_page_no, name_text_class):
    elements = []
    
    for p in range(1, int(upper_bound_page_no)+1):
        tree = html.fromstring(requests.get('%s%s/'%(url,p)).content)
        elements += tree.find_class(name_text_class)
        
    print "Found %d lines"%len(elements)
    return elements

def scrape_single_user_rating(tree, rating_classname):
    rating_tree = tree.find_class(rating_classname)
    single_rating = []
    
    percentage = []
    
    for r in rating_tree:
        r_split = r.text_content().split('%')[0]
        single_rating = [str(i) for i in r_split if i in '0123456789.']
        rating = ''.join(s for s in single_rating)
        percentage.append(float(rating))
    
    scores = []
    for i in range(len(percentage)):
        scores.append(percentage[i])
    return scores
        
text_class_name = 'oneliner'
rating_classname = 'panel'
output1 = []
lines = []
found_lines = []
category_scores = []
keep_lines = []
tree = html.fromstring(requests.get('http://onelinefun.com/1/').content)
page_max = 359

for p in range(1,page_max+1):
    tree = html.fromstring(requests.get('http://onelinefun.com/%d/'%(p)).content)       
    category_scores += scrape_single_user_rating(tree, rating_classname)
found_lines += scrape_webpages('http://onelinefun.com/',page_max,text_class_name)

# Filter out not funny jokes.  
if len(category_scores) == len(found_lines):
    for i in range(len(found_lines)):
        if category_scores[i] > 40.0:
            keep_lines.append(found_lines[i].text_content().split('One-liner')[0])
else:
    print 'The number of scores and the number of lines are imbalanced'
    print '%d scores found'%len(category_scores)
    print '%d lines found'%len(found_lines)
    
print "Finished processing.\nIt contained %d Funny lines."%(len(keep_lines))
   
lines.append(keep_lines)

for cat_lines in lines:
    for l in cat_lines:
        strip1 = l.strip('\n')
        strip2 = strip1.strip(' ')
        output1.append(strip2.strip('\n'))

# Write away the found oneliners
w.write_to_pickle("onelinefun",output1)