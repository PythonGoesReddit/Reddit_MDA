# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 07:59:53 2021

@author: mahle
"""

import json

filepath = "Tagged_JSONS/RC_2005-12_tagged_FLAIR.json"

counter = 1

with open(filepath) as f:
    contents = f.read().strip("[]") # The stripping gets rid of irregular square brackets in the input file
    sentences = contents.replace("}, {","}\n{").split("\n") # The replace and split makes sure separate entries are handled separately (input file has no line breaks)
    p = open("Tagged_JSONS/RC_2005-12_tagged_manual_Batch1.txt", "w")
    for x in range(0,100):
        data = json.loads(sentences[x])
        tagged = data["sentence_tagged"][0] # the index 0 just gets rid of one superfluous level of parentheses
        untagged = [[x[0],"_"] for x in tagged]
        link_id = data["link_id"]
        sentence_no = data["sentence_no"]
        p.write("\t".join(lin_id, sentence_no, untagged)+"\n")
    p.close()
    p = open("Tagged_JSONS/RC_2005-12_tagged_manual_Batch2.txt", "w")
    for x in range(100,200):
        data = json.loads(sentences[x])
        tagged = data["sentence_tagged"][0] # the index 0 just gets rid of one superfluous level of parentheses
        untagged = [[x[0],"_"] for x in tagged]
        link_id = data["link_id"]
        sentence_no = data["sentence_no"]
        p.write("\t".join(lin_id, sentence_no, untagged)+"\n")
    p.close()
    p = open("Tagged_JSONS/RC_2005-12_tagged_manual_Batch3.txt", "w")
    for x in range(200,300):
        data = json.loads(sentences[x])
        tagged = data["sentence_tagged"][0] # the index 0 just gets rid of one superfluous level of parentheses
        untagged = [[x[0],"_"] for x in tagged]
        link_id = data["link_id"]
        sentence_no = data["sentence_no"]
        p.write("\t".join(lin_id, sentence_no, untagged)+"\n")
    p.close()       
    p = open("Tagged_JSONS/RC_2005-12_tagged_manual_Batch4.txt", "w")
    for x in range(300,400):
        data = json.loads(sentences[x])
        tagged = data["sentence_tagged"][0] # the index 0 just gets rid of one superfluous level of parentheses
        untagged = [[x[0],"_"] for x in tagged]
        link_id = data["link_id"]
        sentence_no = data["sentence_no"]
        p.write("\t".join(lin_id, sentence_no, untagged)+"\n")
    p.close()
    p = open("Tagged_JSONS/RC_2005-12_tagged_manual_Batch5.txt", "w")
    for x in range(400,500):
        data = json.loads(sentences[x])
        tagged = data["sentence_tagged"][0] # the index 0 just gets rid of one superfluous level of parentheses
        untagged = [[x[0],"_"] for x in tagged]
        link_id = data["link_id"]
        sentence_no = data["sentence_no"]
        p.write("\t".join(lin_id, sentence_no, untagged)+"\n")
    p.close()       
                  
            













