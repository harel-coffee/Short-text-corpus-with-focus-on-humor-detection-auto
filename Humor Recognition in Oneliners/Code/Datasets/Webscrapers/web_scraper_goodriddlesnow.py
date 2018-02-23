# -*- coding: utf-8 -*-
from lxml import html
import requests
import write_functions as w

output1 = []
page_max = 385 #The link can access all jokes on the website

for i in range(1,page_max+1):
    request_page = requests.get('http://goodriddlesnow.com/jokes/find?sort=popularity&direction=desc&page=%d'%i)
    tree = html.fromstring(request_page.content)
    elements = tree.find_class('joke-question') + tree.find_class('joke-answer hide')

    output = []
    for el in elements:
        strip1 = el.text_content().strip('\n').strip('Joke: ')
        strip2 = strip1.strip(' ').strip('Punch line: ')
        output.append(strip2.replace('\n',' ').decode('utf-8', "replace"))
    #filter out all noise
    for k in range(0,len(output)/2):
        if 'Show Your Support :)' not in output[k+(len(output)/2)]:
            output[k] = '%s %s'%(output[k],output[int(k+(len(elements)/2))])
    output = output[0:5]
    for out in output:
        output1.append(out)

# Write away the found oneliners
w.write_to_pickle('goodriddlesnow',output1)