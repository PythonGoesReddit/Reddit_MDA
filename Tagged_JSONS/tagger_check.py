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

#read in line, split at backslash t, pull out elements indexed 1, 2, 3
#take element 3 of the human-coded items, which will be a string, and turn this into a list of tags only; make the machine-coded the same format
#make function
#x = x.strip("[]")
#list1 = x.split("], [")
#list2 = [x.strip("'") for x in list1]
#list3 = [y.split("', '") for y in list2]
#check how many times list 1 at index x is not the same as list 2 at index x
#write to notes file if not