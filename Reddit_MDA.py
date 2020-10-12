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
    
# initialize empty feature dictionary
def open_reddit_json(folder_path):
    '''Takes Reddit json file as input. Separates each sentence into one dictionary.  Simplifies metainfo (retains body, author, link_id, subreddit). Removes deleted and non-English comments. 
    Returns dict of dicts in format {id: {body: str, author: str, link_id: str, sentence_no: int, subreddit: str, features: dict}'''
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
                            sentence_dict = {"body": sentence, "author": author, "link_id": link_id, "sentence_no": sentence_counter, "subreddit": subreddit}#
                            feature_dict = {"vpast_001": 0, "vperfect_002": 0, "vpresent_003": 0, "advplace_004": 0, "advtime_005": 0, "profirpers_006": 0, "prosecpers_007": 0, "prothirper_008": 0, "proit_009" "vinfinitive_024": 0, "vpresentpart_025": 0, "vpastpart_026": 0, "vpastwhiz_027": 0, "vpresentwhiz_028":0,
                            "vsplitinf_062": 0, "vimperative_204": 0, "vseemappear_058": 0, "vpublic_055": 0, "vprivate_056": 0, "vsuasive_057": 0, "whclause_023": 0, "thatdel_060": 0}
                            sentence_dict["features"] = feature_dict
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

## add dict in dict for tags
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
    sentence = sentence.strip(string.punctuation).lower()
    ## NEEDED: remove emojis - Gustavo
    return sentence

def tag_sentence(sentence):
    '''Takes a sentence, cleans it with clean_sentence, and tags it using the NLTK averaged_perceptron_tagger. 
    Returns a list of tuples of (word, pos_tag).'''
    cleaned_sentence = clean_sentence(sentence)
    tokens = nltk.word_tokenize(cleaned_sentence)
    tagged_sentence = nltk.pos_tag(tokens)
    return tagged_sentence

def verb_features(sentence, features_dict):
    



# Output functions
## NEEDED: function to write a matrix of text_id * variables - Kyla?
## NEEDED: function to write meta-info for each text - Kyla


# CALL FUNCTIONS DOWN HERE
## NEEDED: Multiprocessing set up -- Axel & Kyla ?

# Biber tagging can probably come in the same script no problem once we've optimized the functions, 
# having 1000 or 2000 lines is not really an issue), example of my thoughts below, KM
# EX:
# preprocessed_file = open_reddit_json(path)
# full_dict = sentence_tagger(preprocessed_file)
# full_dict = raw_word_tagger(full_dict)

# for sentence in full_dict: 
#     sentence_dict = full_dict.get(sentence)
#     sentence = sentence_dict["body"]
#     tagged_sentence = tag_sentence(sentence)

    #change to dictionary, pass dictionary to function, function method updates dict (no return function)
#     for word_tuple in tagged_sentence:
#         if word_tuple[1].startswith("N"): #i.e. all nouns
#             noun_counter_f3 = noun_counter_f3 + function_for_nouns(word_tuple[0]) 
#           #one function per POS/condition, takes features dict as input, updates this dict with +=

#         elif word_tuple[1].startswith("V"): #i.e. all verbs
#             verb_counter_f5 = verb_counter_f5 + function_for_verbs(word_tuple[0]) #same here with verbs

#             if word_tuple[0] in ["should", "could", "modalverb"]:
#                    do this other function and save to counter, etc. 

#    sentence_dict["examplefeature_n3"] = noun_counter_f3
#    sentence_dict["examplefeature_n5"] = verb_counter_f5






# General open questions
## Question: What level of precision for the feature-identifying functions do we want to set in advance? 
## How many comments from how many months should inspect to determine the level of precision?



