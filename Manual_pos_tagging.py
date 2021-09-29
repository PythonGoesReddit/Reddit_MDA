# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 07:59:53 2021

@author: mahle
"""

import json
import nltk

file = "/Users/mahle/Documents/Uni/01_Master/Unterlagen/Python/Python_group/RC_2005-12_tagged_FLAIR.json"

p = open("/Users/mahle/Documents/Uni/01_Master/Unterlagen/Python/Python_group/RC_2005-12_tagged_manual.txt", "w")
counter = 1

with open(file) as f:
    
    for item in file:
        counter +=1
        
        if counter > 0 and counter < 101: ## specify range here
            
            sentence = json.loads(item.strip())["body"]
            link_id = json.loads(item.strip())["link_id"]
            sentence_no = json.loads(item.strip())["sentence_no"]
            
            tokens = nltk.word_tokenize(sentence)
            tags_long = ""
            
            for token in tokens:
                tags = '["' + str(token) + ', ""], '
                tags_long.append(tags)
                p.write('{link_id: "' + str(link_id) + '", "sentence_no": ' + str(sentence_no) + ', manual_tagging: [[' + str(tags_long) + ']]}\n')
        
p.close()












