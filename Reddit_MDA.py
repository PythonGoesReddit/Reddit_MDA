#All packages:
import json
import os
import nltk
import string
import re
import string
import time
from datetime import timedelta
start_time = time.time()

path = "/Users/kylamcconnell/Documents/Github/Reddit_MDA/sample_data/json"

# Preprocessing functions

eng_vocab_lower = set(word.lower() for word in nltk.corpus.words.words('en')) # List of English words for check_English()

def check_English(text):
    '''Calculates what % of all words in a piece of text are English.
    Parameter text is a string, parameter cutoff a float between 0 and 1.
    Returns either True or False depending on % of English words in the text,
    so it can be used as part of an if-statement.'''
    words = [x.lower().strip(string.punctuation) for x in text.split() if x.strip(string.punctuation)]
    eng_words = [x for x in words if x in eng_vocab_lower]
    if len(words) > 0:
        perc_eng = len(eng_words)/len(words) #BUG: I get a divide by 0 error here (KM)
        if perc_eng >= 0.4:
            return True
        else:
            return False
    
# initialize empty feature dictionary
def open_reddit_json(folder_path):
    '''Takes Reddit json file. Separates each sentence into one dictionary.  
    Simplifies metainfo (retains body, author, link_id, subreddit). 
    Removes deleted and non-English comments. 
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
                            sentence_dict = {"body": sentence, "author": author, "link_id": link_id, "sentence_no": sentence_counter, "subreddit": subreddit}
                            s = {"vpast_001": 0, "vperfect_002": 0, "vpresent_003": 0, "advplace_004": 0, "advtime_005": 0, "profirpers_006": 0, "prosecpers_007": 0, 
                            "prothirdper_008": 0, "proit_009": 0, "prodemons_010": 0, "proindef_011": 0, "pverbdo_012": 0, "whquest_013": 0, "nominalis_014": 0, "gerund_015": 0,
                            "nouns_016": 0, "passagentl_017": 0, "passby_018": 0, "mainvbe_019": 0, "exthere_020": 0, "thatvcom_021": 0, "thatacom_022": 0, "whclause_023": 0,
                            "vinfinitive_024": 0, "vpresentpart_025": 0, "vpastpart_026": 0, "vpastwhiz_027": 0, "vpresentwhiz_028":0, "thatresub_029": 0, "thatreobj_030": 0,
                            "whresub_031": 0, "whreobj_032": 0, "whrepied_033": 0, "sentencere_034": 0, "advsubcause_035": 0, "advsubconc_036": 0, "advsubcond_037": 0,
                            "advsubother_038": 0, "prepositions_039": 0, "adjattr_040": 0, "adjpred_041": 0, "adverbs_042": 0, "ttratio_043": 0, "wordlength_044": 0, "conjuncts_045": 0,
                            "downtoners_046": 0, "hedges_047": 0, "amplifiers_048": 0, "emphatics_049": 0, "discpart_050": 0, "demonstr_051": 0, "modalsposs_052": 0,
                            "modalsness_053": 0, "modalspred_054": 0, "vpublic_055": 0, "vprivate_056": 0, "vsuasive_057": 0, "vseemappear_058": 0, "contractions_059": 0, 
                            "thatdel_060": 0, "strandprep_061": 0, "vsplitinf_062": 0, "vsplitaux_063": 0, "coordphras_064": 0, "coordnonp_065": 0, "negsyn_066": 0, 
                            "negana_067": 0, "hashtag_201": 0, "link_202": 0, "interlink_203": 0, "caps_204": 0, "vimperative_205": 0,
                            "question_208": 0, "exclamation_209": 0, "lenchar_210": 0, "lenword_211": 0, "comparatives_212": 0, "superlatives_213": 0}
                            sentence_dict["features"] = s
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

## NEEDED: work on and flush out the following code:
## Think about more informative function names

def analyze_sentence(preprocessed_json):
    '''Takes the preprocessed json and adds to the features sub-dictionary the following keys and counts (values): "hashtag_201": no. of hashtags,
    "question_208": no. of question marks, "exclamation_209": no of exclamation marks, "lenchar_210": len of sentence in char, "lenword_211": len of sentence in words'''

    for id in preprocessed_json: 
        sentence_dict = preprocessed_json.get(id)
        sentence = sentence_dict["body"] 
        s = sentence_dict["features"]

        hashtag_counter = sentence.count("#")
        s["hashtag_201"] = hashtag_counter

        question_counter = sentence.count("?")
        s["question_208"] = question_counter

        exclamation_counter = sentence.count("!")
        s["exclamation_209"] = exclamation_counter 

        s["lenchar_210"] = len(sentence) 
        s["lenword_211"] = len(sentence.split(" ")) 

def analyze_raw_words(preprocessed_json):
    '''Takes the preprocessed json and updates the counts of the following keys in the features sub-dictionary: "link_202": no. of external links, 
    "interlink_203": no. of internal links, "caps_204": no of words in all caps.'''
    ## NEEDED: feature 7: emoticons - Gustavo
    ## NEEDED: feature 10: strategic lengthening 
    ## NEEDED: feature 11: alternating uppercase-lowercase 
    for id in preprocessed_json: 
        sentence_dict = preprocessed_json.get(id)
        sentence = sentence_dict["body"]
        s = sentence_dict["features"]

        for word in sentence.split():
            if word.startswith("u/") or word.startswith("r/"):
                s["link_202"] += 1 

            if "http" in word or "www" in word:
                s["interlink_203"] += 1 

            if word.isupper() and (word not in ["A", "I"]): #Capital A at the beginning of sentences is commmon but this will throw out A in the middle of a string, i.e. EVERYBODY GETS A JOOOB
                s["caps_204"] += 1  

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

    
## Definition of stopword lists and checkword lists for following POS-functions
placelist = ["aboard", "above", "abroad", "across", "ahead", "alongside", "around", 
                 "ashore", "astern", "away", "behind", "below", "beneath", "beside", "downhill",
                 "downstairs", "downstream", "east", "far", "hereabouts", "indoors", "inland", "inshore",
                 "inside", "locally", "near", "nearby", "north", "nowhere", "outdoors", "outside", 
                 "overboard", "overland", "overseas", "south", "underfoot", "underground", "underneath",
                 "uphill", "upstairs", "upstream", "west"]
timelist = ["afterwards", "again", "earlier", "early", "eventually", "formerly",
                "immediately", "initially", "instantly", "late", "lately", "later", "momentarily", 
                "now", "nowadays", "once", "originally", "presently", "previously", "recently", 
                "shortly", "simultaneously", "soon", "subsequently", "today", "tomorrow", "tonight",
                "yesterday"]
firstpersonlist = ["i", "me", "we", "us", "my", "our", "myself", "ourselves"]
secondpersonlist = ["you", "yourself", "your", "yourselves"]
thirdpersonlist = ["she", "he", "they", "her", "him", "them", "his", "their", "himself","herself", "themselves"]
indefpronounlist = ["anybody", "anyone", "anything", "everybody", "everyone", "everything", "nobody", "none", "nothing", "nowhere", "somebody", "someone", "something"]


## POS-functions

def analyze_verb(index, tagged_sentence, features_dict): 
    '''Takes a tagged word (tuple) and dictionary of all possible tags and updates relevant keys: "vpast_001", "vperfect_002", "vpresent_003", 
    "whclause_023", "vinfinitive_024", "vpresentpart_025", "vpastpart_026", "vpastwhiz_027", "vpresentwhiz_028",
    "vpublic_055", "vprivate_056", "vsuasive_057", "vseemappear_058", "contractions_059", 
    "thatdel_060", "vsplitinf_062", "vsplitaux_063", "vimperative_205".'''    
    word_tuple = tagged_sentence[index] #returns a tuple (word, POS)
    if word_tuple[1] == "VBD":
        features_dict["vpast_001"] += 1
    elif word_tuple[1] == "VBP" or word_tuple[1] == "VBZ": # this needs a lookahead function to check that it is not preceeded by 'to'
        features_dict["vpresent_003"] += 1
    elif word_tuple[1] == "VB": #is this the right form for infinitives?
        features_dict["vinfinitive_024"] += 1
    elif word_tuple[1] == "VBG": #gerund or present participle.. is this ok? or do we have to separate these
        features_dict["vpresentpart_025"] += 1
    elif word_tuple[1] == "VBN":
        features_dict["vpastpart_026"] += 1
    if word_tuple[0].startswith("seem") or word_tuple[0].startswith("appear"):
        features_dict["vseemappear_058"] += 1
    #if word_tuple[0].startswith():
    # 55, 56, 57 -> 23, 60
    
    # still missing: "vperfect_002", "whclause_023", "vpastwhiz_027", "vpresentwhiz_028",
    # "vpublic_055", "vprivate_056", "vsuasive_057", "contractions_059", "thatdel_060", "vsplitinf_062", "vsplitaux_063", "vimperative_205".

def analyze_modal(index, tagged_sentence, features_dict):
    '''Takes a tagged word (tuple) and dictionary of all possible tags and updates relevant keys: 
    "pverbdo_012", "passagentl_017", "passby_018","mainvbe_019",
    "emphatics_049", "modalsposs_052", "modalsness_053", "modalspred_054", "contractions_059", 
    "vimperative_205".'''
    # still missing: "pverbdo_012", "passagentl_017", "passby_018","mainvbe_019", "emphatics_049", "modalsposs_052", "modalsness_053",
    # "modalspred_054", "contractions_059", vimperative_205".

def analyze_adverb(index, tagged_sentence, features_dict):
    '''Takes a tagged word (tuple) and dictionary of all possible tags and updates relevant keys:
    "advplace_004", "advtime_005", "advsubcause_035", "advsubconc_036", "advsubcond_037", "advsubother_038", "adverbs_042", "conjuncts_045",
    "downtoners_046", "hedges_047", "amplifiers_048", "discpart_050", "negana_067".'''
    features_dict["adverbs_042"] += 1
    word_tuple = tagged_sentence[index] #returns a tuple (word, POS)
    if word_tuple[0] == "because":
        features_dict["advsubcause_035"] += 1
    elif word_tuple[0] == "although" or word_tuple[0] == "though" or word_tuple[0] == "tho":
        features_dict["advsubconc_036"] += 1
    elif word_tuple[0] == "if" or word_tuple[0] == "unless":
        features_dict["advsubcond_037"] += 1
    elif word_tuple[0] == "not":
        features_dict["negana_067"] += 1
    elif word_tuple[0] in placelist:
        features_dict["advplace_004"] += 1
    elif word_tuple[0] in timelist:
        features_dict["advtime_005"] += 1
    #elif 
    # still missing: "advsubother_038", "conjuncts_045", "downtoners_046", "hedges_047", "amplifiers_048", "discpart_050"
 
def analyze_adjective(index, tagged_sentence, features_dict):
    '''Takes a tagged word (tuple) and dictionary of all possible tags and updates relevant keys:
    "adjattr_040", "adjpred_041", "emphatics_049", "comparatives_212", "superlatives_213".'''
    word_tuple = tagged_sentence[index] #returns a tuple (word, POS)
    if word_tuple[1] == "JJR":
        features_dict["comparatives_212"] += 1
    elif word_tuple[1] == "JJS":
        features_dict["superlatives_213"] += 1
    # still missing: "adjattr_040", "adjpred_041", "emphatics_049"
      
def analyze_preposition(index, tagged_sentence, features_dict):
    '''Takes a tagged word (tuple) and dictionary of all possible tags and updates relevant keys: 
    "advsubcause_035", "advsubconc_036", "advsubcond_037", "advsubother_038", "prepositions_039", 
    "conjuncts_045", "hedges_047", "strandprep_061".'''
    features_dict["prepositions_039"] += 1 
    word_tuple = tagged_sentence[index] #returns a tuple (word, POS)
    if word_tuple[0] == "because":
        features_dict["advsubcause_035"] += 1
    elif word_tuple[0] == "although" or word_tuple[0] == "though" or word_tuple[0] == "tho":
        features_dict["advsubconc_036"] += 1
    elif word_tuple[0] == "if" or word_tuple[0] == "unless":
        features_dict["advsubcond_037"] += 1
    # still missing: "advsubother_038", "conjuncts_045", "hedges_047", "strandprep_061"
    
def analyze_noun(index, tagged_sentence, features_dict):
    '''Takes a tagged word (tuple) and dictionary of all possible tags and updates relevant keys:
    "nominalis_014", "gerund_015", "nouns_016".'''
    features_dict["nouns_016"] += 1
    word_tuple = tagged_sentence[index] #returns a tuple (word, POS)
    if word_tuple[0].endswith("ing") or word_tuple[0].endswith("ings"):
        features_dict["gerund_015"] += 1 # this is edited manually by Biber
    if word_tuple[0].endswith("tions") or word_tuple[0].endswith("tion") or word_tuple[0].endswith("ments") or word_tuple[0].endswith("ment") or word_tuple[0].endswith("ness") or word_tuple[0].endswith("ity") or word_tuple[0].endswith("nesses") or word_tuple[0].endswith("ities"):
        features_dict["nominalis_014"] += 1
        
def analyze_pronoun(index, tagged_sentence, features_dict):
    '''Takes a tagged word (tuple) and dictionary of all possible tags and updates relevant keys:
    "profirpers_006", "prosecpers_007", "prothirper_008", "proit_009", "prodemons_010", "proindef_011", "contractions_059".'''
    word_tuple = tagged_sentence[index] #returns a tuple (word, POS)
    if word_tuple[0] == "it":
        features_dict["proit_009"] += 1
    elif word_tuple[0] in firstpersonlist:
        features_dict["profirpers_006"] += 1
    elif word_tuple[0] in secondpersonlist:
        features_dict["prosecpers_007"] += 1
    elif word_tuple[0] in thirdpersonlist:
        features_dict["prothirdper_008"] += 1
    elif word_tuple[0] in indefpronounlist:
        features_dict["proindef_011"] += 1    
    # still missing: "prodemons_010", "contractions_059"

def analyze_conjunction(index, tagged_sentence, features_dict):
    '''Takes a tagged word (tuple) and dictionary of all possible tags and updates relevant keys:
    "coordphras_064", "coordnonp_065".'''
    # still missing: "coordphras_064", "coordnonp_065"
 
def analyze_determiner(index, tagged_sentence, features_dict):
    '''Takes a tagged word (tuple) and dictionary of all possible tags and updates relevant keys:
    "demonstr_051", "negsyn_066".'''
    # still missing: "demonstr_051", "negsyn_066"
    
def analyze_wh_word(index, tagged_sentence, features_dict):
    '''Takes a tagged word (tuple) and dictionary of all possible tags and updates relevant keys:
    "whquest_013", "thatvcom_021", "thatacom_022", "thatresub_029", "thatreobj_030", "whresub_031", "whreobj_032", 
    "whrepied_033", "sentencere_034", "conjuncts_045".'''
    word_tuple = tagged_sentence[index] #returns a tuple (word, POS)
    if word_tuple[0] == "which": # and previousword_tuple[0] == ",":
        features_dict["sentencere_034"] += 1
    #if word_tuple[0] == "that":
        # 21
        # 22
        # 29
        # 30
    #elif 
    # still missing: "whquest_013", "thatvcom_021", "thatacom_022", "thatresub_029", "thatreobj_030", "whresub_031", "whreobj_032", "whrepied_033", "conjuncts_045"

def analyze_there(index, tagged_sentence, features_dict):
    '''Takes a tagged word (tuple) and dictionary of all possible tags and updates relevant keys: 
    "exthere_020".'''
    features_dict["exthere_020"] += 1
    
def analyze_particle(index, tagged_sentence, features_dict):
    '''Takes a tagged word (tuple) and dictionary of all possible tags and updates relevant keys: 
    "hedges_047", "discpart_050".'''
    # still missing: "hedges_047", "discpart_050"
    
## still missing: the two features that run on the whole sentence: 43 type/token ratio and 44 word length
    
# Output functions
## NEEDED: function to write a matrix of text_id * variables
## NEEDED: function to write meta-info for each text 


# CALL FUNCTIONS DOWN HERE
## NEEDED: Multiprocessing set up 

preprocessed_file = open_reddit_json(path) #reads in file, separates into sentences, initializes feature dict

analyze_sentence(preprocessed_file) #updates raw-sentence based counts (i.e. punctuation marks, length)
analyze_raw_words(preprocessed_file) #updates raw-word based counts (i.e. links, emojis)

for id in preprocessed_file: #loops through all individual sentences in the file one by one
     sentence_dict = preprocessed_file.get(id) #retrieves entire dictionary and all sub-dicts for the given sentence
     sentence = sentence_dict["body"] #retrieves sentence only (str)) 
     features_dict = sentence_dict["features"] #retrieves s for the given sentence
     tagged_sentence = tag_sentence(sentence) #tags sentence, returning list of tuples with (word, pos)
     
     for index in range(1, len(tagged_sentence)): #based on POS, apply different function, each of which updates s
         current_tag = tagged_sentence[index][1]
         if current_tag.startswith("V"):
             analyze_verb(index, tagged_sentence, features_dict)
         elif current_tag == "MD":
             analyze_modal(index, tagged_sentence, features_dict)
         elif current_tag.startswith("N"):
             analyze_noun(index, tagged_sentence, features_dict)
         elif current_tag.startswith("RB"):
             analyze_adverb(index, tagged_sentence,features_dict)
         elif current_tag.startswith("J"):
             analyze_adjective(index, tagged_sentence, features_dict)
         elif current_tag.startswith("I"):
             analyze_preposition(index, tagged_sentence, features_dict)
         elif current_tag.startswith("W"):
             analyze_wh_word(index, tagged_sentence, features_dict)
         elif current_tag.startswith("CC"):
             analyze_conjunction(index, tagged_sentence, features_dict)
         elif current_tag.startswith("RP"):
             analyze_particle(index, tagged_sentence, features_dict)
         elif current_tag.startswith("DT"):
             analyze_determiner(index, tagged_sentence, features_dict)
         elif current_tag.startswith("PR"):
             analyze_pronoun(index, tagged_sentence, features_dict)
         elif current_tag.startswith("EX"):
             analyze_there(index, tagged_sentence, features_dict)
    # at some point the order of these elif-statements could be updated using freq counts from our data

    #for testing purposes
     print(sentence, features_dict)


## Add output functions here at end



# General open questions
## Question: What level of precision for the feature-identifying functions do we want to set in advance? 
## How many comments from how many months should inspect to determine the level of precision?
print(timedelta(seconds=time.time() - start_time))


