# Read in data from NLTK and from Flair, retrieve ID and tagged sentence
# Drop additional [X,X] items
# Read in manual POS tags 
# Match on ID
# Check accuracy 
# Output mismatched items (total tags, correct tags -- human is correct)

import os
import json

dirname = os.path.dirname(__file__)

with open(os.path.join(dirname, 'RC_2005-12_tagged_FLAIR.json'), "r", errors="replace") as f:
    for line in f:
        flair_tagged = json.loads(line.strip())["tagged_sentence"]
        link_id = json.loads(line.strip())["link_id"]
        sentence_no = json.loads(line.strip())["sentence_no"]


with open(os.path.join(dirname, 'RC_2005-12_tagged_FLAIR.json'), "r", errors="replace") as n:
    for line in n:
        nltk_tagged = json.loads(line.strip())["tagged_sentence"]
        link_id = json.loads(line.strip())["link_id"]
        sentence_no = json.loads(line.strip())["sentence_no"]

# open 
# type of match function, i.e. how to get the percent match 
# combining the individual ranking functions
# json files currently lists 
# matching based on the human coding identifiers (not currently written as a dict)
