
# Open Q: Will commas be removed by the tagger?

#BUG: I accidentally did some lookaheads using word_tuple instead of tagged_sentence... sorry! (KM)

# Code for easily checking output (adapt word positions for given feature)
    # sentence = [word[0] for word in tagged_sentence]
    # print(word_minus1[0], word_tuple[0], "//", " ".join(sentence))
    # print()

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

dirname = os.path.dirname(__file__)
path = os.path.join(dirname, 'sample_data')

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

## Question: What about quoted material from previous comments/posts? Should we exclude it, and if yes, how?


# Untagged feature extraction functions
def analyze_sentence(preprocessed_json):
    '''Takes the preprocessed json and adds to the features sub-dictionary the following keys and counts (values): "hashtag_201": no. of hashtags,
    "question_208": no. of question marks, "exclamation_209": no of exclamation marks, "lenchar_210": len of sentence in char, "lenword_211": len of sentence in words, "conjuncts_045"'''

    for id in preprocessed_json: 
        sentence_dict = preprocessed_json.get(id)
        sentence = sentence_dict["body"] 
        s = sentence_dict["features"]

        s["hashtag_201"] = sentence.count("#")

        s["question_208"] = sentence.count("?")

        s["exclamation_209"] = sentence.count("!")
 
        s["conjuncts_045"] = sentence.count("that is,") #Will only catch sentences with proper punctuation but it's a start

        for emphatic in ["for sure", "a lot", "such a", "such an", "just", "really", "most", "more"]: 
            s["emphatics_049"] += sentence.count(emphatic)

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
    ## look into what might or might not be necessary here
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
                 "uphill", "upstairs", "upstream", "west"] ## some others that could be included: apart, back, here, out, there (HM)
timelist = ["afterwards", "again", "earlier", "early", "eventually", "formerly",
                "immediately", "initially", "instantly", "late", "lately", "later", "momentarily", 
                "now", "nowadays", "once", "originally", "presently", "previously", "recently", 
                "shortly", "simultaneously", "soon", "subsequently", "today", "tomorrow", "tonight",
                "yesterday"] # some others that could be included: then, always (HM)
firstpersonlist = ["i", "me", "we", "us", "my", "our", "myself", "ourselves"]
secondpersonlist = ["you", "yourself", "your", "yourselves"]
thirdpersonlist = ["she", "he", "they", "her", "him", "them", "his", "their", "himself","herself", "themselves"]
indefpronounlist = ["anybody", "anyone", "anything", "everybody", "everyone", "everything", "nobody", "none", "nothing", "nowhere", "somebody", "someone", "something"]
conjunctslist = ["alternatively", "altogether", "consequently", "conversely", "eg", "else", "furthermore",
                 "hence", "however", "ie", "instead", "likewise", "moreover", "namely", "nevertheless",
                 "nonetheless", "notwithstanding", "otherwise", "rather", "similarly", "therefore", "thus", "viz"]
punct_final = [".", "!", "?", ":", ";"] # here, Biber also includes the long dash -- , but I am unsure how this would be rendered
belist = ["be", "am", "are", "is", "was", "were", "been", "being"] 
# we could probably lemmatize instead of using a manual list for forms of verbs (KM)
subjpro = ["i", "we", "he", "she", "they"]
posspro = ["my", "our", "your", "his", "their", "its"]
DEM = ["that", "this", "these", "those"]
WHP = ["who", "whom", "whose", "which"]
WHO = ["what", "where", "when", "how", "whether", "why", "whoever", "whomever", "whichever", 
       "whenever", "whatever", "however"] # can this be accomplished with tag WDT? (KM)
discpart = ["well", "now", "anyway", "anyhow", "anyways"]
QUAN = ["each", "all", "every", "many", "much", "few", "several", "some", "any"]
ALLP = [".", "!", "?", ":", ";", ","]  # here, Biber also includes the long dash -- , but I am unsure how this would be rendered
downtonerlist = ["almost", "barely", "hardly", "merely", "mildly", "nearly", "only", "partially", "partly", "practically", "scarcely", "slightly", "somewhat"]
                # some others that could be included: a little, a bit, a tad (HM)
amplifierlist = ["absolutely", "altogether", "completely", "enormously", "entirely", "extremely", "fully", "greatly", "highly", 
                 "intensely", "perfectly", "strongly", "thoroughly", "totally", "utterly", "very"]
asktelllist = ["ask", "asked", "asking", "asks", "tell", "telling", "tells", "told"] #this could also be accomplished with .startswith("ask"), .startswith("tell") or == "told" (KM)


#POS-functions
def analyze_verb(index, tagged_sentence, features_dict):  ## Axel
    '''Takes the index position of the current word, a tagged sentence, and dictionary of all possible tags and updates relevant keys: "vpast_001", "vperfect_002", "vpresent_003", 
    "whclause_023", "vinfinitive_024", "vpresentpart_025", "vpastpart_026", "vpastwhiz_027", "vpresentwhiz_028",
    "vpublic_055", "vprivate_056", "vsuasive_057", "vseemappear_058", "contractions_059", 
    "thatdel_060", "vsplitinf_062", "vsplitaux_063", "vimperative_205".'''    
    word_tuple = tagged_sentence[index] #returns a tuple (word, POS)

    if word_tuple[1] == "VBD":
        features_dict["vpast_001"] += 1
    elif word_tuple[1] == "VVI": 
        features_dict["vinfinitive_024"] += 1
    elif word_tuple[1] == "VBG": #gerund or present participle.. is this ok? or do we have to separate these
        features_dict["vpresentpart_025"] += 1
    elif word_tuple[1] == "VBN":
        features_dict["vpastpart_026"] += 1
    elif word_tuple[1] in ["VBP", "VBZ"]:
        features_dict["vpresent_003"] += 1
    
    if word_tuple[0].startswith("seem") or word_tuple[0].startswith("appear"):
        features_dict["vseemappear_058"] += 1
    
    try:
        word_plus1 = tagged_sentence[index + 1]
        word_plus2 = tagged_sentence[index + 2]
        if word_plus1[1] == "WDT" and word_plus2[1] == "PRP":
            features_dict["whclause_023"] += 1
    except IndexError:
        pass
        
    #"vperfect_002" -> how many places should it lookahead for a form of have?
    #if word_tuple[0].startswith():
    # 55, 56, 57 -> 23, 60
        
    # still missing: 
    # "vpastwhiz_027",
    # 27. past participial WHIZ deletion relatives (e.g., the solution produced by this process) N/QUANPRO + VBN + PREP/BE/ADV
    #
    #  "vpresentwhiz_028",
    #present participial WHIZ deletion relatives (e.g., the event causing this decline is . . .)N + VBG (these forms were edited by hand)
    #
    # "vpublic_055", "vprivate_056", "vsuasive_057", "contractions_059", "thatdel_060", "vsplitinf_062", "vsplitaux_063", "vimperative_205".

def analyze_modal(index, tagged_sentence, features_dict): ## Axel
    '''Takes the index position of the current word, a tagged sentence, and dictionary of all possible tags and updates relevant keys: 
    "pverbdo_012", "passagentl_017", "passby_018","mainvbe_019",
    "emphatics_049", "modalsposs_052", "modalsness_053", "modalspred_054", "contractions_059", 
    "vimperative_205".'''
    #word_tuple = tagged_sentence[index] #returns a tuple (word, POS)

    # still missing: "pverbdo_012", "passagentl_017", "passby_018","mainvbe_019", "emphatics_049", "modalsposs_052", "modalsness_053",
    # "modalspred_054", "contractions_059", vimperative_205".
    
    ## originally I thought it might make sense to look for contractions (feature 59) within the pronoun-section as well, but it is probably
    ## sufficient to look for them here, isn't it? (HM)

def analyze_adverb(index, tagged_sentence, features_dict): ## Hanna
    '''Takes the index position of the current word, a tagged sentence, and dictionary of all possible tags and updates relevant keys:
    "advplace_004", "advtime_005", "adverbs_042", "conjuncts_045",
    "downtoners_046", "hedges_047", "amplifiers_048", "discpart_050", "negana_067".'''
    features_dict["adverbs_042"] += 1
    word_tuple = tagged_sentence[index] #returns a tuple (word, POS)
    if word_tuple[0] == "not" or word_tuple[0] == "n't":
        features_dict["negana_067"] += 1
    elif word_tuple[0] in placelist: ## added some more ideas to the list above (HM)
        features_dict["advplace_004"] += 1
    elif word_tuple[0] in timelist: ## added some more ideas to the list above (HM)
        features_dict["advtime_005"] += 1
    elif word_tuple[0] in downtonerlist: ## added some more ideas to the list above (HM)
        features_dict["downtoners_046"] += 1
    elif word_tuple[0] in amplifierlist:
        features_dict["amplifiers_048"] += 1 
    elif word_tuple[0] == "almost" or word_tuple[0] == "maybe":
        features_dict["hedges_047"] += 1
    elif word_tuple[0] in conjunctslist:
        features_dict["conjuncts_045"] += 1 # so far, this list only includes "eg" not "e.g.", since that would probably be split by the tagger?
    elif index == 0 and word_tuple[0] in discpart:
        features_dict["discpart_050"] += 1
    ## we also look for particles in the particle-section, this is to make sure that
    ## we actually catch all of them in case they are tagged differently (HM)
    try: 
        word_plus1 = tagged_sentence[index + 1] 
        if word_tuple[0] == "rather" and index == 0:
            if word_plus1[0] == ",": #punctuation will be removed already, right? (KM) then how do we find this without the comma? (HM)
                features_dict["conjuncts_045"] += 1
            elif word_plus1[1] in ["CC", "CD", "DT", "EX", "IN", "LS", "MD", "NN", "NNS", "NNP", "NNPS", "PDT", "PRP", "PRP$", "RP", "TO", "UH", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "WDT", "WP", "WP$", "WRB"]:
                features_dict["conjuncts_045"] += 1 
        elif word_tuple[0] == "else" and index == 0 and word_plus1[0] == ",": #again, commas (KM)
                features_dict["conjuncts_045"] += 1
        elif word_tuple[0] == "altogether" and index == 0 and word_plus1 == ",":
                features_dict["conjuncts_045"] += 1
    except IndexError:
        pass
    
 
def analyze_adjective(index, tagged_sentence, features_dict): ## Kyla
    '''Takes the index position of the current word, a tagged sentence, and dictionary of all possible tags and updates relevant keys:
    "adjattr_040", "adjpred_041", "emphatics_049", "comparatives_212", "superlatives_213".'''
    word_tuple = tagged_sentence[index] #returns a tuple (word, POS)
   
    if word_tuple[1] == "JJR":
        features_dict["comparatives_212"] += 1
    elif word_tuple[1] == "JJS":
        features_dict["superlatives_213"] += 1
    
    if index > 0:
        word_minus1 = tagged_sentence[index - 1]
        if word_minus1[0] in belist:
            try:
                word_plus1 = tagged_sentence[index + 1]
                if word_plus1[1].startswith("JJ") or word_plus1[1].startswith("NN"):
                    features_dict["adjattr_040"] += 1

                elif not word_plus1[1].startswith("RB"): 
                    features_dict["adjpred_041"] += 1

                try:
                    word_plus2 = tagged_sentence[index + 2]
                    if word_plus1[1].startswith("JJ") and not word_plus2[1].startswith("JJ") and not word_plus2[1].startswith("NN"): #Would it not be okay to have JJ in position +1 and +2?
                        features_dict["adjpred_041"] += 1

                except IndexError:
                    pass  

            except IndexError:
                pass
            
            #49. emphatics: for sure/a lot/such a/real + ADJ/so + ADJ/DO + VIjust/reallyImost /more
        elif word_minus1[0] in ["real", "so"] and word_tuple[1] == "JJ":
            #BUG: This is catching so much junk, I don't understand why (so I comes up a lot ) KM
            features_dict["emphatics_049"] += 1
      
def analyze_preposition(index, tagged_sentence, features_dict): ## Gustavo
    '''Takes the index position of the current word, a tagged sentence, and dictionary of all possible tags and updates relevant keys: 
    "advsubcause_035", "advsubconc_036", "advsubcond_037", "advsubother_038", "prepositions_039", 
    "conjuncts_045", "hedges_047", "strandprep_061".'''
    ## There are several features in here that I think would be better in the analyze_sentence function becuase they are just looking for surface forms
    ## For example, instead of looking for the word proceeding 'as' or 'of', we could just count in the full, untagged sentence (before it is separated into words)
    ## for "kind of" and "inasmuch as" -- kind of like what we're doing with emphatics in analyze_sentence()
    ## I'd be happy to do this as my next task if we think its best (KM)
    ## Other candidates would also be things like "on the other hand", etc.
    features_dict["prepositions_039"] += 1 
    word_tuple = tagged_sentence[index] #returns a tuple (word, POS)

    if word_tuple[0] == "because":
        features_dict["advsubcause_035"] += 1
    elif word_tuple[0] == "although" or word_tuple[0] == "though" or word_tuple[0] == "tho":
        features_dict["advsubconc_036"] += 1
    elif word_tuple[0] == "if" or word_tuple[0] == "unless":
        features_dict["advsubcond_037"] += 1
    elif word_tuple[0] == "of": 
       pass #What was meant here? (KM)
    
    if index > 0:
        word_minus1 = tagged_sentence[index - 1]
        #Gustavo, I moved this up here (KM)
        if word_tuple[0] == "that" and word_minus1 in ["such", "so"] and not word_plus1[1] in ["JJ", "JJR", "JJS", "NN", "NNS", "NNP", "NNPS"]:
            features_dict["advsubother_038"] += 1 # Using not statement here again. There is also an overlap with the "such that" construction in Biber's original features. (GK)
        if word_tuple[0] == "like" and word_minus1[0] == "something":
            features_dict["hedges_047"] += 1
            #I don't really like how we're handling hedges here, it feels like there has to be a better way
            #Maybe they could be handled in the full sentence, pretagged function if they just need surface forms
            #Any other ideas? (KM)
            # I agree that this way of looking for the hedges is tedious, but I can't think of a better way to do it.
        if word_minus1[0] == "kind" or word_minus1[0] == "sort":
            pass #What was meant here? (KM)
            # Is it possible that the code maybe got slightly mixed up through the restructuring into the "try"-layout?
            # I thought that this if-statemtn was followed or preceded by a condition wordtuple[0]=="of" and word_minus2[1]!=DET/ADJ/POSSPRO/WHO
            # in order to look for "kind of" and "sort of" (p.240) (HM)
            # Ok sorry I broke that :D maybe we can move this to the whole sentence analyzer function? And just look for the phrases "kind of" and "sort of" (and kinda/sorta)
            #Same goes for below, in as much as, etc. (KM)
        if index > 1: 
            word_minus2 = tagged_sentence[index - 2]
            if word_minus2[1] not in ["DT", "JJ", "JJR", "JJS", "PRP", "WP"]:
                features_dict["hedges_047"] += 1

    try:
        word_plus1 = tagged_sentence[index + 1]
        if word_plus1[0] in ALLP:
            features_dict["strandprep_061"] += 1
        elif word_tuple[0] == "at" and word_plus1[0] == "about":
            features_dict["hedges_047"] += 1
        elif word_tuple[0] == "for" and word_plus1 in ["example", "instance"]:
            features_dict["conjuncts_045"] += 1
        elif word_tuple[0] == "by" and word_plus1 in ["contrast", "comparison"]:
            features_dict["conjuncts_045"] += 1
        elif word_tuple[0] == "in": 
            try: 
                word_plus2 = tagged_sentence[index + 2]
                if word_plus1[0] in ["comparison", "contrast", "particular", "addition", "conclusion", "consequence", "sum", "summary"]:
                    features_dict["conjuncts_045"] += 1
                elif word_plus1[0] == "any" and word_plus2[0] in ["event", "case"]:
                    features_dict["conjuncts_045"] += 1
                elif word_plus1[0] == "other" and word_plus2[0] == "words":
                    features_dict["conjuncts_045"] += 1
            except IndexError:
                pass
    except IndexError: 
        pass

    try:
        word_plus2 = tagged_sentence[index + 2]
        if word_tuple[0] == "as" and word_plus1[0] == "a" and word_plus2[0] in ["result", "consequence"]:
            features_dict["conjuncts_045"] += 1
        elif word_tuple[0] == "on" and word_plus1[0] == "the":
            if word_plus2[0] == "contrary":
                features_dict["conjuncts_045"] += 1
        #Gustavo, I moved your features up here so that it doesn't have to assign word_plus2 twice (KM)
        #But I think these features maybe can go in the whole sentence section (and kind of / sort of / kinda / sorta, see comments above)
        elif word_tuple[0] in ["inasmuch", "forasmuch", "insofar", "insomuch"] and word_plus1 == "as":
            features_dict["advsubother_038"] += 1
        elif word_tuple[0] == "as" and word_plus1[0] in ["long", "soon"] and word_plus2[0] == "as":
            features_dict["advsubother_038"] += 1
        elif word_plus2[0] == "other":
            try: 
                word_plus3 = tagged_sentence[index + 3]
                if word_plus3 == "hand":
                    features_dict["conjuncts_045"] += 1
            except IndexError:
                pass
    except IndexError:
        pass


    
    # still missing: "advsubother_038"
    
def analyze_noun(index, tagged_sentence, features_dict): ## Rafaela
    '''Takes the index position of the current word, a tagged sentence, and dictionary of all possible tags and updates relevant keys:
    "nominalis_014", "gerund_015", "nouns_016".'''
    word_tuple = tagged_sentence[index] #returns a tuple (word, POS)
    if word_tuple[0].endswith("ing") or word_tuple[0].endswith("ings"):
        features_dict["gerund_015"] += 1 # this is edited manually by Biber
    else:
        if word_tuple[0].endswith("tions") or word_tuple[0].endswith("tion") or word_tuple[0].endswith("ments") or word_tuple[0].endswith("ment") or word_tuple[0].endswith("ness") or word_tuple[0].endswith("ity") or word_tuple[0].endswith("nesses") or word_tuple[0].endswith("ities"):
            features_dict["nominalis_014"] += 1
        else: 
            features_dict["nouns_016"] += 1
        
def analyze_pronoun(index, tagged_sentence, features_dict): ## Hanna
    '''Takes the index position of the current word, a tagged sentence, and dictionary of all possible tags and updates relevant keys:
    "profirpers_006", "prosecpers_007", "prothirper_008", "proit_009", "prodemons_010", "proindef_011".'''
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
    elif word_tuple[0] == "that" and index == 0: ## this was edited by hand by Biber
        features_dict["prodemons_010"] += 1
    try:
        word_plus1 = tagged_sentence[index + 1]
        if word_tuple[0] in DEM:
            if word_plus1[0] == "and":
                features_dict["prodemons_010"] += 1
            elif word_plus1[1] in ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "MD", "WP"]:
                features_dict["prodemons_010"] += 1
            elif index == (len(tagged_sentence)-1):
                features_dict["prodemons_010"] += 1
        elif word_tuple[0] == "that" and word_plus1[0] == "'s": ## should this be 's or s ? Does the apostrophe get removed? 
            features_dict["prodemons_010"] += 1
    except IndexError: 
        pass

def analyze_conjunction(index, tagged_sentence, features_dict): ## Gustavo
    '''Takes the index position of the current word, a tagged sentence, and dictionary of all possible tags and updates relevant keys:
    "hedges_047", "coordphras_064", "coordnonp_065".'''
    word_tuple = tagged_sentence[index] #returns a tuple (word, POS)
    try:
        if index > 0:
            word_minus1 = word_tuple[index - 1]
            word_plus1 = word_tuple[index + 1]
            if word_tuple[0] == "and": 
                if word_minus1[1].startswith("NN") and word_plus1[1].startswith("NN"):
                    features_dict["coordphras_064"] += 1
                elif word_minus1[1].startswith("RB") and word_plus1[1].startswith("RB"):
                    features_dict["coordphras_064"] += 1
                elif word_minus1[1].startswith("JJ") and word_plus1[1].startswith("JJ"):
                    features_dict["coordphras_064"] += 1
                elif word_minus1[1].startswith("VB") and word_plus1[1].startswith("VB"):
                    features_dict["coordphras_064"] += 1
                elif word_minus1[0] == ",": #commas taken out? (KM)
                    if word_plus1[0] in ["it", "so", "you", "then"]:
                        features_dict["coordnonp_065"] += 1
                    elif word_plus1[1] in subjpro or word_plus1[1] in DEM: # So far, this identification of demonstrative pronoun is likely to be too crude. Maybe re-use function for feature 10?
                        features_dict["coordnonp_065"] += 1
                    elif word_plus1[0] == "there" and word_plus2[0] in belist:
                        features_dict["coordnonp_065"] += 1
                elif word_minus1[0] in punct_final: 
                    features_dict["coordnonp_065"] += 1
                elif word_plus1[0] in WHP or word_plus1[0] in WHO or word_plus1[0] in discpart:
                    features_dict["coordnonp_065"] += 1
                elif word_plus1[0] : #adverbial subordinator (nos. 35-8)
                    features_dict["coordnonp_065"] += 1
                elif word_plus1[0] : #conjunct (no. 45)
                    features_dict["coordnonp_065"] += 1
            elif word_tuple[0] == "or":
                if word_minus1[0] == "more" and word_plus1[0] == "less":
                    features_dict["hedges_047"] += 1
    except IndexError:
        pass
    
    try:
        word_plus1 = word_tuple[index + 1]
        if word_tuple == "and" and word_plus1 in WHP or word_plus1 in WHO:
            features_dict["coordnonp_065"] += 1 
        elif word_tuple == "and" and word_plus1 in ["because", "although", "though", "if", "unless", "since", "while", "whilst", "whereas", "whereby"]:
            features_dict["coordnonp_065"] += 1 
    except IndexError: 
        pass
    
    # still missing: "coordnonp_065" (only for 'and' followed by adverbial subordinator or conjunct, depend on other features)


def analyze_determiner(index, tagged_sentence, features_dict): ## Rafaela
    '''Takes the index position of the current word, a tagged sentence, and dictionary of all possible tags and updates relevant keys:
    "demonstr_051", "negsyn_066".'''
    word_tuple = tagged_sentence[index] #returns a tuple (word, POS)

    if word_tuple[0] in DEM:
        features_dict["demonstr_051"] += 1
    elif word_tuple[0] == "neither" or word_tuple[0] == "nor":
        features_dict["negsyn_066"] += 1
    elif word_tuple[0] == "no":
        try: 
            word_plus1  = word_tuple[index + 1]
            if word_plus1[1].startswith("NN") or word_plus1[1].startswith("JJ"):
                features_dict["negsyn_066"] += 1
            elif word_plus1[0] in QUAN:
                features_dict["negsyn_066"] += 1
        except IndexError:
            pass
     
def analyze_wh_word(index, tagged_sentence, features_dict): ## Kyla
    # Check: Ft 32 (Biber's way of finding this seems like it could be optimized)
    # Check: Ft 22 (catches unintended phrases)
    '''Takes the index position of the current word, a tagged sentence, and dictionary of all possible tags and updates relevant keys:
    "whquest_013", "thatvcom_021", "thatacom_022", "thatresub_029", "thatreobj_030", "whresub_031", "whreobj_032", 
    "whrepied_033", "sentencere_034".'''
    word_tuple = tagged_sentence[index] #returns a tuple (word, POS)
   
    if word_tuple[0] in WHP: #["who", "whom", "whose", "which"]
        if index > 0:
            try:
                word_minus1 = tagged_sentence[index - 1]
                if word_minus1[1] == "IN":
                    features_dict["whrepied_033"] += 1 #pied-piping relative clauses (e.g., the manner in which he was told) PREP + WHP in relative clauses

                if word_tuple[0] == "which" and word_minus1[0] == ",": #34. sentence relatives (e.g., Bob likesfried mangoes, which is the most disgusting thing I've ever heard of) Biber: (These forms are edited by hand to exclude non-restrictive relative clauses.)
                    features_dict["sentencere_034"] += 1 

            except IndexError:
                pass

            if index > 1:
                try: #right now, only wh-words at least two words from the front and 2 from the end will be caught here (KM) -> won't catch ex "boys who Sally likes" (is that grammatically acceptable??) also won't catch passives, ex "the men who are liked by Sally" (kind of awkward tbh) (KM)
                    word_minus2 = tagged_sentence[index - 2]
                    word_plus1 = tagged_sentence[index + 1]

                    if not word_minus2[0].startswith("ask") and not word_minus2[0].startswith("tell") and not word_minus2[0] == "told": 
                        if not word_plus1[1].startswith("R") and not word_plus1[1].startswith("V") and not word_plus1[1].startswith("MD"):
                            
                            features_dict["whreobj_032"] += 1 #32. WH relative clauses on object positions (e.g., the man who Sally likes) xxx + yyy + N + WHP + zzz (where xxx is NOT any form of the verbs ASK or TELL, to exclude indirect WH questions, and zzz is not ADV, AUX or V, to exclude relativization on subject position)

                except IndexError:
                    pass

    elif word_tuple[0] == "that":
        if index > 0:
            try:
                word_minus1 = tagged_sentence[index - 1]
                if word_minus1[1].startswith("J"): #This catches things like I'm sure that's a, there's nothing good that can come out of it, etc. Biber keeps mentioning tone boundaries but I dont understand how you could do that computationally (he refers to it as T#)
                    features_dict["thatacom_022"] += 1 #that adjective complements (e.g., I'm glad that yo like it) ADJ + (T#) + that (complements across intonation boundaries were edited by hand)

                try:
                    word_plus1 = word_tuple[index + 1]
                    word_plus2 = word_tuple[index + 2] 
                    
                    print("TEST")
                    #BUG: never reaches this point? print statements here ignored? or does my sample just not have any examples? (KM)

                    #29. that relative clauses on subject position (e.g., the dog that bit me) N -p (T#) + that + (ADV) + AUX/V {that relatives across intonation boundaries are identified by hand.)
                    #30. that relative clauses on object position (e.g., the dog that I saw) N + (T#) + that + DET / SUBJPRO / POSSPRO / it / ADJ / plural noun/ proper noun / possessive noun / TITLE
                    if word_minus1[1].startswith("NN"):
                        if word_plus1[1].startswith("RB") and (word_plus2[1].startswith("V") or word_plus2[1].startswith("MD")):
                            features_dict["thatresub_029"] += 1 
                            sentence = [word[0] for word in tagged_sentence]

                        elif word_plus1[1].startswith("VB") or word_plus1[1].startswith("MD"):
                            features_dict["thatresub_029"] += 1
                            sentence = [word[0] for word in tagged_sentence]

                        elif word_plus1[1].startswith("DT") or word_plus1[1].startswith("JJ") or word_plus1[1] == "NNS" or word_plus1[1].startswith("NNP"):
                            features_dict["thatreobj_030"] += 1

                        elif word_plus1[0] == "it" or word_plus1[0] in subjpro or word_plus1[0] in posspro:
                            features_dict["thatreobj_030"] += 1

                        # if word_minus1[0] in ["and", "nor", "but", "or", "also"] or word_minus1[0] in punct_final or word_minus1[0] == ",":
                        # start to 021, tbc

                    if index > 2:
                        try:
                            word_minus3 = word_tuple[index - 3]

                            #31. WH relative clauses on subject position (e.g., the man who likes popcorn) xxx + yyy + N + WHP + (ADV) + AUX/V (where xxx is NOT any form of the verbs ASK or TELL; to exclude indirect WH questions like Tom asked the man who went to the store)
                            if word_minus1[1].startswith("N") and word_plus1[1].startswith("R") and (word_plus2[1].startswith("V") or word_plus2[1].startswith("MD")):
                                features_dict["whresub_031"] += 1
                                print("TEST")
                                #BUG: Doesn't get here on my file
                            elif word_minus1[1].startswith("N") and (word_plus1[1].startswith("V") or word_plus1[1].startswith("MD")):
                                features_dict["whresub_031"] += 1
                                print("TEST")
                                #BUG: Doesn't get here on my file

                        except IndexError:
                            pass

                except IndexError:
                    pass
                
            except IndexError:
                pass

            #TO ADD:
            #13. direct WH-questions CL-P/Tif + WHO + AUX (where AUX is not part of a contracted form)
            #21 21. that verb complements (e.g., / said that he went) (a) and\nor\but\or\aho\ALL-P + that + DET/PRO/^^e/plural noun/proper noun/TITLE (these are i/za£-clauses in clause-initial positions) (b) PUB/PRV/SUA/SEEM/APPEAR + that + xxx (where xxx is NOT: V/AUX/CL-P/TJf/anrf){that-c\a\ises as complements to verbs which are not included in the above verb classes are not counted - see Quirk et al. 1985:1179ff.) (c) PUB/PRV/SUA + PREP + xxx + N + that (where xxx is any number of words, but NOT = N)(This algorithm allows an intervening prepositional phrase between a verb and its complement.)(d) Tt + that
            

def analyze_there(index, tagged_sentence, features_dict): ## noone...
    '''Takes the index position of the current word, a tagged sentence, and dictionary of all possible tags and updates relevant keys: 
    "exthere_020".'''
    features_dict["exthere_020"] += 1
    
def analyze_particle(index, tagged_sentence, features_dict): ## Hanna
    '''Takes the index position of the current word, a tagged sentence, and dictionary of all possible tags and updates relevant keys: 
    "discpart_050".'''
    word_tuple = tagged_sentence[index] #returns a tuple (word, POS)
    ## we also look for particles in the adverb-section, this is to make sure that
    ## we actually catch all of them in case they are tagged differently (HM)
    if index == 0 and word_tuple[0] in discpart:
        features_dict["discpart_050"] += 1
    else:
        pass
    
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
     
     for index in range(0, len(tagged_sentence)): #based on POS, apply different function, each of which updates s
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
     #print(sentence, features_dict)
     #print(tagged_sentence)
    
    #helpful for in console, first import nltk and (first time only) nltk.download("tagsets")
    # nltk.help.upenn_tagset('NNS')
    # nltk.help.upenn_tagset()



## Add output functions here at end



# General open questions
## Question: What level of precision for the feature-identifying functions do we want to set in advance? 
## How many comments from how many months should inspect to determine the level of precision?
print(timedelta(seconds=time.time() - start_time))


