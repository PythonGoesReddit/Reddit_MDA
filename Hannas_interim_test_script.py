# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 13:15:40 2020

@author: mahle
"""
import nltk
import re

## function for feature 1: past tense
## DONE!
def feature_01(tagged_list):
  """This function takes a list of words with PoS tags as input and returns the number of items
  that are a verb in the past tense."""
  counter = 0
  for item in tagged_list:
    if item == "\w_+_VBD" or item == "\w{5,20}ed_\w+":
      counter = counter + 1
    else:
      pass
  return(counter)

## function for feature 2: verbs in the perfect aspect
def feature_02(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the number of 
    perfect aspect forms."""
    string1 = r"\b[have|has|'ve|'s]_\w+\s\w+_VBD"
    string2 = r"\b[have|has|'ve|'s]_\w+\s\w+_RB\s\w+_VBD"
    string3 = r"\b[have|has|'ve|'s]_\w+\s\w+_RB\s\w+_RB\s\w+_VBD"
    string4 = r"\b[have|has]_\w+\s\w+_[NN|NNS|NNP|NNPS|PRP|PRP$]\s\w+_VBD"
    matches1 = re.findall(string1, tagged_string)
    matches2 = re.findall(string2, tagged_string)
    matches3 = re.findall(string3, tagged_string)
    matches4 = re.findall(string4, tagged_string)
    counter = len(matches1) + len(matches2) + len(matches3) + len(matches4)
    return(counter)

## function for feature 3: present tense
def feature_03(tagged_list):
  """This function takes a list of words with PoS tags as input and returns the number of 
  verbs in the present tense."""
  counter = 0
## excluding infinitives, so "to" in front of the string
  for item in tagged_list:
    if item == "\w+_VB" or item == "\w+_VBZ":
      counter = counter + 1
    else:
      pass
  return(counter)
    

## function for feature 4: place adverbials
## DONE!
def feature_04(untagged_list):
  """This function takes a list of words with PoS tags as input and returns the number of items
  that are place adverbials."""
  counter = 0
  placelist = ["aboard", "above", "abroad", "across", "ahead", "alongside", "around", 
  "ashore", "astern", "away", "behind", "below", "beneath", "beside", "downhill",
  "downstairs", "downstream", "east", "far", "hereabouts", "indoors", "inland", "inshore",
  "inside", "locally", "near", "nearby", "north", "nowhere", "outdoors", "outside", 
  "overboard", "overland", "overseas", "south", "underfoot", "underground", "underneath",
  "uphill", "upstairs", "upstream", "west"]
  for item in untagged_list:
    if item in placelist:
      counter = counter + 1
    else:
      pass
  return(counter)

### 1. Create a dictionary with an several entries that each have an
###    element called "body" containing some text

dict1 = {"text1": {"body": "Is this really all that you remember from your Python class, which really was not that long ago?"}, 
         "text2": {"body": "Well, my dear, I think you should better get off your desk now and take a well-deserved break outside!"}, 
         "text3": {"body": "There are a number of things to pay attention to when composing this intricate piece of code - your snoring dog is not one of them."}, 
         "text4": {"body": "Apart from eating ice cream, every team member musn't forget to always push their changes to the GitHub page."}, 
         "text5": {"body": "The dog that I saw isn't going to take slightly longer than I'd hoped for."}}

### 2. Open each dictionary entry in the three formats that I need
for text in dict1:
    full_info = dict1.get(text)
    rawtext = full_info["body"]   
    rawtext = rawtext.lower()
### 2.1 Untagged list
    untagged_list =  nltk.word_tokenize(rawtext)
### 2.2 Tagged list
    tagged_list1 = nltk.pos_tag(untagged_list)
## This doed not return the format I expected. I thought it would be word_TAG,
## but it is actually a tuple ("word", "TAG")...
## The following code puts it in the format I want:
    tagged_list = []
    for tup in tagged_list1:
        fixedstring = str(tup[0] + "_" + tup[1])
        tagged_list.append(fixedstring)
    
### 2.3 Tagged string
    tagged_string = " "
    tagged_string = tagged_string.join(tagged_list)

### 3. Apply the functions from the "Reddit_Bibers_Features.py" script
    full_info["f01_counter"] = feature_01(tagged_list)
    full_info["f02_counter"] = feature_02(tagged_string)
    full_info["f03_counter"] = feature_03(tagged_list)
    full_info["f04_counter"] = feature_04(untagged_list)
     
### 4. Save the output
    dict1[text] = full_info

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    