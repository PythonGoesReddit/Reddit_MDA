# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 07:59:53 2021

@author: mahle
"""

import json

filepath = "Tagged_JSONS/RC_2005-12_tagged_FLAIR.json"

with open(filepath) as f:
    contents = f.read().strip("[]") # The stripping gets rid of irregular square brackets in the input file
    sentences = contents.replace("}, {","}\n{").split("\n") # The replace and split makes sure separate entries are handled separately (input file has no line breaks)
    batch = 1
    for x in range(len(sentences)):
        if x//100 == batch: # with each new multiple of 100 reached, increase the batch variable by 1
            batch +=1
        data = json.loads(sentences[x])
        tagged = data["sentence_tagged"][0] # the index 0 just gets rid of one superfluous level of parentheses
        untagged = [[x[0],"_"] for x in tagged][3:-3] # the [3:-3] slice gets rid of the three "X"s at the beginning and end of each sentence.
        link_id = data["link_id"]
        sentence_no = data["sentence_no"]
        with open("Tagged_JSONS/RC_2005-12_tagged_manual_Batch" + str(batch) + ".txt", "a") as p:
            p.write(link_id + "	" + str(sentence_no) + "	" + str(untagged) +"\n")
    p.close()   
            













