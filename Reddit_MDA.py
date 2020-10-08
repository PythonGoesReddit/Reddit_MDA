#All packages:
import json
import os
import nltk
import string
import re
import string

#All path variables
path = "FILEPATH"

# Preprocessing functions

eng_vocab_lower = set(word.lower() for word in nltk.corpus.words.words('en')) # List of English words for check_English()

def check_English(text):
    '''Calculates how many % of all words in a piece of text are English.
    Parameter text is a string, parameter cutoff a float between 0 and 1.
    Returns either True or False depending on % of English words in the text,
    so it can be used as part of an if-statement.'''
    words = [x.lower().strip(string.punctuation) for x in text.split() if x.strip(string.punctuation)]
    eng_words = [x for x in words if x in eng_vocab_lower]
    perc_eng = len(eng_words)/len(words) #BUG: I get a divide by 0 error here (KM)
    if perc_eng >= 0.4:
        return True
    else:
        return False
    
def open_reddit_json(folder_path):
    '''Takes Reddit json file as input. Separates each sentence into one dictionary.  Simplifies metainfo (retains body, author, link_id, subreddit). Removes deleted and non-English comments. 
    Returns dict of dicts in format {id: {body: str, author: str, link_id: str, sentence_no: int, subreddit: str}'''
    errors = 0
    for filename in os.listdir(folder_path):
        if os.path.splitext(filename)[1] == ".json": #open file only if extension is .json, else will try to open folders and other random files
            base = os.path.splitext(filename)[0] #strip the .json extension
            with open(os.path.join(path, filename), "r", errors="replace") as j:
                print("Opening file: " + str(filename))
                prepped_json = {}
                counter = 0 #counts number of comments, for ID below
                for line in j:
                    counter += 1

                    try: 
                        if json.loads(line.strip())["body"] != "[deleted]" and check_English(json.loads(line.strip())["body"]): #does not consider deleted comments or comments that fail check_English
                            body = json.loads(line.strip())["body"]
                            author = json.loads(line.strip())["author"]
                            link_id = json.loads(line.strip())["link_id"]
                            subreddit = json.loads(line.strip())["subreddit"]

                        sentence_counter = 0
                        for sentence in nltk.tokenize.sent_tokenize(body): #separates into sentences
                            sentence_counter +=1 #keep track of which sentence it is (1st, 2nd, etc.)
                            sentence_dict = {"body": sentence, "author": author, "link_id": link_id, "sentence_no": sentence_counter, "subreddit": subreddit}
                            prepped_json[str(base + "_" + str(link_id) + "_" + str(sentence_counter))] = sentence_dict #creates a dict within a dict, so that the key (filename, linkid, sentence number) calls the whole dict

                    except json.decoder.JSONDecodeError:
                        errors +=1 #keeps track of how many errors are encountered/lines skipped

                print("Total lines skipped = " + str(errors))
            return prepped_json

## NEEDED: function to remove comments posted by bots (how can we reliably identify them?) - Gustavo
    ## BotDefense/BotBust scrape -> divided by year, checked against usernames
    ## usernames that literally include the word bot
    ## Gustavo --> this can come in the file read above I think (KM)

## Question: What about quoted material from previous comments/posts? Should we exclude it, and if yes, how?


# Untagged feature extraction functions

## NEEDED: function to calculate length of comment / sentence (?)
## NEEDED: work on and flush out the following code:
## Think about more informative function names

def sentence_tagger(preprocessed_json):
    '''Takes the preprocessed json and adds the key "hashtag_1" with the value of the number of hashtags in the sentence
    Additionally adds the key "link_2" with the value of the number of links in the sentence, the key "capital_3" with the value of the
    number of capitalized words in the sentence, the  key "question_8" with the value of the number of question marks and the key "exclamation_9"
    with value of the number of exclamation marks.'''

    for id in preprocessed_json: 
        sentence_dict = preprocessed_json.get(id)
        sentence = sentence_dict["body"] 

        hashtag_counter = sentence.count("#")
        sentence_dict["hashtag_1"] = hashtag_counter

        question_counter = sentence.count("?")
        sentence_dict["question_8"] = question_counter

        exclamation_counter = sentence.count("!")
        sentence_dict["exclamation_9"] = exclamation_counter 

        sentence_dict["sentence_len"] = len(sentence) 

        preprocessed_json[id] = sentence_dict
    return preprocessed_json

def raw_word_tagger(preprocessed_json):
    '''Takes the preprocessed json and adds the key "link_2" with the number of external links, "internal_link_2" with the number of internal links 
    and "capital_3" with the number of words in all caps.'''
    ## NEEDED: feature 7: emoticons - Gustavo
    ## NEEDED: feature 10: strategic lengthening 
    ## NEEDED: feature 11: alternating uppercase-lowercase 
    for id in preprocessed_json: 
        sentence_dict = preprocessed_json.get(id)
        sentence = sentence_dict["body"]

        link_counter = 0
        internal_link_counter = 0
        capital_counter = 0  
        for word in sentence.split():
            print(word)
            if word.startswith("u/") or word.startswith("r/"):
                internal_link_counter += 1

            if "http" in word or "www" in word:
                link_counter += 1

            if word.isupper() and (word not in ["A", "I"]): #Capital A at the beginning of sentences is commmon but this will throw out A in the middle of a string, i.e. EVERYBODY GETS A JOOOB
                capital_counter +=1

        sentence_dict["link_2"] = link_counter
        sentence_dict["internal_link_2"] = internal_link_counter
        sentence_dict["capital_3"] = capital_counter  
    
        preprocessed_json[id] = sentence_dict
    return preprocessed_json

## NEEDED: function for feature 12: community-specific acronyms/lexical items (such as 'op') - Gustavo ??

def clean_sentence(sentence):
    '''Takes a sentence and returns it in all lowercase, with deviant/creative spelling normalized, 
    with punctuation removed, and emojis removed.'''
    ## NEEDED: normalize deviant and creative spelling - Axel
    sentence = lower(sentence.strip(string.punctuation))
    ## NEEDED: remove emojis - Gustavo

def tag_sentence(sentence):
    '''Takes a sentence and tags it using the XX tagger.'''


# Output functions
## NEEDED: function to write a matrix of text_id * variables - Kyla?
## NEEDED: function to write meta-info for each text - Kyla


# CALL FUNCTIONS DOWN HERE
## NEEDED: Multiprocessing set up -- Axel & Kyla ?
current_file = open_reddit_json(path)







# General open questions
## Question: What level of precision for the feature-identifying functions do we want to set in advance? 
## How many comments from how many months should inspect to determine the level of precision?





############### Code below needs to be updated I believe? KM ###############




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
        tagged_list1 = nltk.pos_tag(untagged_list) # This also isn't currently using the Stanford Tagger, which we said we wanted for consistency with Nini.
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



