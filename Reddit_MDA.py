#All packages:
import json
import os
import nltk

#All path variables
path = "FILEPATH"

# Preprocessing functions

## Open file, remove deleted comments, split into sentences, simplify metainfo, add unique ID
### Returns dict of dicts in format {id: {body: str, author: str, link_id: str, sentence_no: int, subreddit: str}
def open_reddit_json(folder_path):
    '''Takes Reddit json file as input. Separates each sentence into one dictionary.  Simplifies metainfo (retains body, author, link_id, subreddit). Removes deleted comments. 
    Returns dict of dicts where the key is the filename plus a unique (ascending) integer identifier, the value is the body and other metainfo as a dict.'''
    errors = 0
    for filename in os.listdir(folder_path):
        if os.path.splitext(filename)[1] == ".json": #open file only if extension is .json, else will try to open folders and other random files
            base = os.path.splitext(filename)[0] #strip the .json extension
            with open(os.path.join(path, filename), "r", errors="replace") as j:
                print("Opening file: " + str(filename))
                prepped_json = {}
                counter = 0 #counts number of comments
                for line in j:
                    counter += 1

                    try:   
                        if json.loads(line.strip())["body"] != "[deleted]": #does not consider deleted comments
                            comment = json.loads(line.strip())["body"]
                            author = json.loads(line.strip())["author"]
                            link_id = json.loads(line.strip())["link_id"]
                            subreddit = json.loads(line.strip())["subreddit"]

                            if len(tokenize.sent_tokenize(comment)) > 1: #for comments that are more than 1 sentence
                                sentence_counter = 0
                                for sentence in tokenize.sent_tokenize(comment): #separates into sentences
                                    if len(sentence) > 1:
                                        sentence_counter +=1 #keep track of which sentence it is (1st, 2nd, etc.)
                                        comment_dict = {"body": sentence, "author": author, "link_id": link_id, "sentence_no": sentence_counter, "subreddit": subreddit}

                            else:
                                sentence_counter = 1
                                comment_dict = {"body": comment, "author": author, "link_id": link_id, "sentence_no": sentence_counter, "subreddit": subreddit}

                            prepped_json[str(base + "_" + str(counter))] = comment_dict

                    except json.decoder.JSONDecodeError:
                        errors +=1 #keeps track of how many errors are encountered/lines skipped

                print("Total lines skipped = " + str(errors))
            return prepped_json

## NEEDED: function to remove comments posted by bots (how can we reliably identify them?) - Gustavo
## NEEDED: function to remove posts with too few English words - Axel 
## Question: What about quoted material from previous comments/posts? Should we exclude it, and if yes, how?


# Untagged feature extraction functions
## NEEDED: function to calculate length of comment / sentence (?)
## NEEDED: work on and flush out the following code:
## Think about more informative function names

# resultsfile = open("filepath","w")
# for filename in os.listdir(path):
#   textfile = open(filename, "r")
#   linenumber = 0
#   for line in textfile.readlines():
#     linenumber += 1 
#     commentWL = line.split() # split character string into a list
#     feature1_counter = feature1_func(commentWL)# extract the count for each feature with the pre-defined feature-functions
#     feature2_counter = feature2_func(commentWL) 
#     ...
# # print the counts for each comment into a new file
#     print(str(linenumber), + ";" + str(feature1_counter) + ";" + str(feature2_counter) + ...)
#     textfile.close()
#resultsfile.close()

## function for feature 1: hashtags, feature 2: links,  feature 3: capital letters, feature 8: question marks, feature 9: exclamation marks
### Note: seems to currently count how many words are capitalized (i.e. first letter), not whole words?
def feature_tagger(preprocessed_json):
    '''This function takes the preprocessed json and adds the key "hashtag_no" with the value of the number of hashtags in the sentence
    Additionally adds the key "link_no" with the value of the number of links in the sentence, the key "capital_counter" with the value of the
    number of capitalized words in the sentence, the  key "question_no" with the value of the number of question marks and the key "exclamation_no"
    with value of the number of exclamation marks.'''
    for id in preprocessed_json:
        full_info = preprocessed_json.get(id)
        comment = full_info["body"] 

        hashtag_counter = comment.count("#")
        full_info["hashtag_no"] = hashtag_counter

        question_counter = comment.count("?")
        full_info["question_no"] = question_counter

        exclamation_counter = comment.count("!")
        full_info["exclamation_no"] = exclamation_counter

        link_counter = 0
        capital_counter = 0
        for word in comment:

          if word.startswith("u/") or word.startswith("r/") or word.startswith("http") or word.startswith("www"):
            link_counter += 1

          if word.isupper() and (word not in ["A", "I"]):
            capital_counter +=1

        full_info["link_no"] = link_counter
        full_info["capital_no"] = capital_counter      

        preprocessed_json[id] = full_info
    return preprocessed_json

## function for feature 4: imperatives
# def feature4_func(wordlist):
#   """This function takes a list of words as input and returns the number of items
#   that are an imperative."""
#   counter = 0
#   for item in wordlist:
#    if :
#       counter = counter + 1
#     else:
#       pass
#   return(counter)

## NEEDED: function for feature 7: emoticons - Gustavo
## NEEDED: function for feature 10: strategic lengthening - Kyla ?? (I don't know what this means though...)
##          -> this refers to repetition of vowels or consonants, like in  "He is soooooo cuteeee!"
## NEEDED: function for feature 11: alternating uppercase-lowercase - Kyla ??
##          -> for some examples see https://www.reddit.com/r/puppersheckingdying/
## NEEDED: function for feature 12: community-specific acronyms/lexical items (such as 'op') - Gustavo ??

## Question: What level of precision for the feature-identifying functions do we want to set in advance? 


# Data prep ("cleaning") functions:
## NEEDED: function to turn all words to lowercase - Axel
## NEEDED: function to normalize deviant and creative spelling - Axel (probably combined with lowercase?)
## NEEDED: function to remove punctuation (?) - Axel
## NEEDED: function to remove emojis - Gustavo



# Tagging and feature extraction functions 
## NEEDED: update of following code for Stanford tagger - Hanna (to function, file opening - line by line not whole file duplicated?)
## -> did I do this correctly?
### Might (doch) be better here to import from Hannas other file, i.e. 
from Reddit_Bibers_Features import feature_01, feature_02, feature_03, feature_04
### Might also be worth it to try to reduce the number of functions here, combining ones that can be combined.
### -> this is probably a good idea, but only once all the functions are finished and working,
###    since they take different input formats. 
### Also worth thinking about function names for informativity

def Biber_tagger(cleaned_json):
    """This function takes the preprocessed and cleaned jsons as input and adds
    a key with a counter as value for each of Biber's original 67 features, as well as 
    two additional features (comparatives and superlatives). The functions for
    identifying each individual feature need to be imported beforehand."""
    for id in cleaned_json:
        full_info = cleaned_json.get(id)
        rawtext = full_info["body"]   
## create the three necessary input formats for the functions    
## Untagged list
        untagged_list =  nltk.word_tokenize(rawtext)
## Tagged list
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

## Apply the functions from the "Reddit_Bibers_Features.py" script
        full_info["f01_counter"] = feature_01(tagged_list)
        full_info["f02_counter"] = feature_02(tagged_string)
        full_info["f03_counter"] = feature_03(tagged_list)
        full_info["f04_counter"] = feature_04(untagged_list)
    
        cleaned_json[id] = full_info
    return cleaned_json

## for functions on superlatives + comparatives: see Reddit_Bibers_Features.py




# Output functions
## NEEDED: function to write a matrix of text_id * variables - Kyla?
## NEEDED: function to write meta-info for each text - Kyla


# CALL FUNCTIONS DOWN HERE
## NEEDED: Multiprocessing set up -- Axel & Kyla ?
