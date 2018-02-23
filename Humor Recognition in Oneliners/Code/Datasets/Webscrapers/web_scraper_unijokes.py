# -*- coding: utf-8 -*-
from lxml import html
import requests
import write_functions as w

def scrape_webpages(url,upper_bound_page_no, name_text_class):
    elements = []
    
    for p in range(1, int(upper_bound_page_no)+1):
        tree = html.fromstring(requests.get('%s%s/'%(url, p), verify=False).content)
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
        
text_class_name = 'joke'
rating_classname = 'panel'
output1 = []
lines = []
found_lines = []
category_scores = []
keep_lines = []
tree = html.fromstring(requests.get('https://unijokes.com/1/', verify=False).content)
#print html.tostring(tree)

page_max = 1100

for p in range(1,page_max+1):
    tree = html.fromstring(requests.get('https://unijokes.com/%d/'%(p), verify=False).content)       
    category_scores += scrape_single_user_rating(tree, rating_classname)
found_lines += scrape_webpages('https://unijokes.com/', page_max, text_class_name)

# Filter out not funny jokes.  
if len(category_scores) == len(found_lines):
    for i in range(len(found_lines)):
        if category_scores[i] > 40.0:
            keep_lines.append(found_lines[i].text_content().split('Vote:')[0])
else:
    print 'The number of scores and the number of lines are imbalanced'
    print '%d scores found'%len(category_scores)
    print '%d lines found'%len(found_lines)
    
print "Finished processing.\nIt contained %d Funny lines."%(len(keep_lines))
   
for l in keep_lines:
    r = l.strip('\r')
    n = r.strip('\n')
    rn = n.replace('\r\n', '')
    space = rn.strip(' ')
    q = space.replace('Q: ','')
    a = q.replace('A: ',' ')
    lines.append(a.decode('utf-8', "replace"))

# Write away the found oneliners
w.write_to_pickle("unijokes", lines)
