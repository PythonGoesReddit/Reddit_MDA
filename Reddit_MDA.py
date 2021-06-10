# 06.05.21 - K Q: Do we need if __name__ == "__main__" for multiprocessing? 
# Open Q: Will commas be removed by the tagger?
# Open Q (HM): What about quoted material from previous comments/posts? Should we exclude it, and if yes, how?
# Should we transform all 'word_tuple's into 'tagged_sentence[index]'? Or does it improve readability?
# Remove emojis in the clean sentence function?

    ## NEEDED: feature 7: emoticons 
    ## NEEDED: feature 10: strategic lengthening 
    ## NEEDED: feature 11: alternating uppercase-lowercase 
    ## NEEDED: function for feature 12: community-specific acronyms/lexical items (such as 'op')

import json
import os
import nltk
import string
#import flair
import re
import time
import concurrent.futures
from multiprocessing import Pool, Manager
import psutil
from flair.models import SequenceTagger
from flair.data import Sentence
from datetime import timedelta
start_time = time.time()

dirname = os.path.dirname(__file__)
data_folder = os.path.join(dirname, 'sample_data')
all_files = [os.path.join("sample_data", file) for file in os.listdir(data_folder) if os.path.splitext(file)[1] == ".json"]

tagger_FLAIR = SequenceTagger.load("final-model_64.pt")


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

def open_reddit_json(filename):
    '''Takes Reddit json file. Separates each sentence into one dictionary.  
    Simplifies metainfo (retains body, author, link_id, subreddit). 
    Removes deleted and non-English comments. 
    Returns dict of dicts in format {id: {body: str, author: str, link_id: str, sentence_no: int, subreddit: str, features: dict}'''
    errors = 0
    base = os.path.splitext(filename)[0] #strip the .json extension

    with open(filename, "r", errors="replace") as j:
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
                    sentence_dict["features"] = s.copy()
                    prepped_json[str(base + "_" + str(link_id) + "_" + str(sentence_counter))] = sentence_dict #creates a dict within a dict, so that the key (filename, linkid, sentence number) calls the whole dict

            except json.decoder.JSONDecodeError:
                errors +=1 #keeps track of how many errors are encountered/lines skipped

        print("Total lines skipped = " + str(errors))
    return prepped_json


# Untagged feature extraction functions
def analyze_sentence(preprocessed_json):
    # AB: General comment: careful with the .count() function. It has no inherent concept of word boundaries, which will lead to false positives in some cases (see below)
    '''Takes the preprocessed json and adds to the features sub-dictionary the following keys and counts (values): "hashtag_201": no. of hashtags,
    "question_208": no. of question marks, "exclamation_209": no of exclamation marks, "lenchar_210": len of sentence in char, "lenword_211": len of sentence in words, "conjuncts_045"'''

    for id in preprocessed_json: 
        sentence_dict = preprocessed_json.get(id)
        sentence = sentence_dict["body"].lower() # AB: lowercasing spelling here, as most code below presupposes all lowercase.
        # AB: For individual items in the .count() functions, there is a tradeoff between " ITEM " and "ITEM".
        # AB: Without spaces, there may be unexpected false positives (e.g. "such a" counting "such astronomical costs" etc.)
        # AB: With spaces, we lose items in sentence-initial position and with following puncutation, e.g. "for instance,"
        # AB: I have made decisions on an educated-guess case basis here, and they fall into three types:
        # AB: a) keep "ITEM" because false positives are extremely unlikely (e.g. "in other words").
        # AB: b) insert spaces, because " ITEM " is going to catch all relevant cases (e.g. " such a " 
        s = sentence_dict["features"]

        s["hashtag_201"] = len(re.findall(r"#\w+", sentence)) # AB: Used a regex here because otherwise sequences of "#" or individual "#" are going to inflate the count

        s["question_208"] = sentence.count("?") # AB: Currently, something like "WHY????" will be counted as four questions. Arguably, a regex with r"\?+" would be better?

        s["exclamation_209"] = sentence.count("!") # AB: Same as above.
 
        s["conjuncts_045"] = sentence.count("that is,") #Will only catch sentences with proper punctuation but it's a start

        for emphatic in [" for sure", " a lot", " such a ", " such an ", " just ", " really", " most ", " more "]: 
        # AB: This whole category strikes me as ill-conceived. Almost all items can, and often do, serve other functions than emphatics:
        # AB: "such a(n)" as anaphoric determinatives ("But such an approach is not easily implemented."),
        # AB: "more/most" in adverb/adjective gradation ("more relevant") and general comparison ("more cases of the new covid mutant reported"), where they really aren't "emphatic"
        # AB: "a lot" as prenominal quantifier ("a lot of talk"). There might be something to be said for this being treated as emphatic, but then so should "much," which it isn't
        # AB: "just" is so versatile in situated use that any simple interpretation seems implausible
        # AB: (and my default, acontextual interpretation would be more in the direction of downtoner, e.g. "just saying")
        # AB: "really" is similar to "just" although perhaps a bit more clearly emphatic. But it can definitely meet other functions as well.
        # AB: That, to me, only leaves "for sure" as a clear-cut count case.
        # AB: One option would be to expend a whole lot of effort trying to get at the specifically emphatic cases of all the items in the list
        # AB: The other might be dropping this feature.
            s["emphatics_049"] += sentence.count(emphatic)
        s["emphatics_049"] -= sentence.count(" a lot of ") # AB: removing all the "a lot of" cases post-hoc. Biber does not do this, but I think it makes sense, because they are simple quantifiers, not emphatics
        if sentence.startswith("for sure"): # AB: Catch cases of sentence-initial "for sure" that have been excluded through the insertion of spaces above
            s["emphatics_049"] += 1

        for hedge in [" at about ", " something like ", " more or less", " kinda ", " sorta ", " almost ", " maybe "]:
            s["hedges_047"] += sentence.count(hedge)
        if sentence.startswith("at about ") or sentence.startswith("something like ") or sentence.startswith("more or less") or sentence.startswith("kinda ") or sentence.startswith("sorta "):
        # AB: Catch sentence-initial cases excluded by spaces above
            s["hedges_047"] += 1

        for conjunct in ["on the contrary", "on the other hand", "for example", "for instance", "by contrast", "by comparison", "in comparison", "in contrast", "in particular", "in addition", "in conclusion", "in consequence", "in sum", "in summary", "in any event", "in any case", "in other words", "as a result", "as a consequence"]:
            s["conjuncts_045"] += sentence.count(conjunct) # AB: I have not inserted any spaces above because the likelihood of false positives in all cases seems very low

        for advsub in ["inasmuch as", "forasmuch as", "insofar as", "insomuch as", " as long as ", " as soon as "]:
            s["advsubother_038"] += sentence.count(advsub)
        if sentence.startswith("as long as ") or sentence.startswith("as soon as "):
            s["advsubother_038"] += 1
            
        for advsubcond in [" if ", " unless ", " if, ", " unless, "]:
            s["advsubcond_037"] += sentence.count(advsubcond)
        if sentence.startswith("if ") or sentence.startswith("if, ") or sentence.startswith("unless ") or sentence.startswith("unless, "):
            s["advsubcond_037"] += 1
        s["lenchar_210"] = len(sentence) 
        s["lenword_211"] = len(sentence.split(" ")) 


        words = sentence_dict["body"].split() #split into words for single word functions below
        for i in range(len(words)):
            if words[i].lower().startswith("u/") or words[i].lower().startswith("r/"):
                s["link_202"] += 1 

            if "http" in words[i].lower() or "www" in words[i].lower():
                s["interlink_203"] += 1 

            if not i == 0:
                if words[i].isupper() and not words[i]=="I":
                    s["caps_204"] += 1
            else:
                if words[i].isupper() and not (words[i] in ["A", "I"]): #AB: changed this to work with indices rather than strings, so we can differentiate between sentence-initial and other contexts.
                    s["caps_204"] += 1  

def clean_sentence(sentence):
    '''Takes a sentence and returns it in all lowercase, with deviant/creative spelling normalized, 
    with punctuation removed, and emojis removed.'''
    sentence = str(sentence).strip(string.punctuation).lower()
    return sentence    

 
# The function below is the previous NLTK tagger. I have hashed it out so we can revert to it in the event of any issues. (GK)
# To use the nltk tagger: import nltk and (first time only) nltk.download("tagsets")
# Can also look up nltk tags with (ex): nltk.help.upenn_tagset('NNS')

#def tag_sentence(sentence):
    #'''Takes a sentence, cleans it with clean_sentence, and tags it using the NLTK averaged_perceptron_tagger. 
    #Adds a look ahead/behind buffer of three items of type ("X", "X") to prevent negative indices and IndexErrors
    #Returns a list of tuples of (word, pos_tag).'''
    #cleaned_sentence = clean_sentence(sentence)
    #tokens = nltk.word_tokenize(cleaned_sentence)
    #tagged_sentence = nltk.pos_tag(tokens)
    #empty_look = [("X", "X"), ("X", "X"), ("X", "X")]
    #tagged_sentence = empty_look + tagged_sentence + empty_look 
    #return tagged_sentence

# The function below is the newer FLAIR POS tagger. It uses the tagger_FLAIR, loaded in line 43 of the code. (GK) 

def tag_sentence(sentence):
    '''Takes a sentence, cleans it with clean_sentence, and tags it using the FLAIR POS tagger. 
    Adds a look ahead/behind buffer of three items of type ("X", "X") to prevent negative indices and IndexErrors
    Returns a list of tuples of (word, pos_tag).'''
    cleaned_sentence = clean_sentence(sentence)
    flair_sentence = Sentence(cleaned_sentence)
    tagger_FLAIR.predict(flair_sentence)
    token_list = []
    for entity in flair_sentence.get_spans('pos'):
        token_list.append(tuple([entity.text] + [entity.tag]))
    empty_look = [("X", "X"), ("X", "X"), ("X", "X")]
    tagged_sentence = empty_look + token_list + empty_look 
    return tagged_sentence        

## Definition of global variables incl. stopword lists and checkword lists for following POS-functions & feature dict
s = {"vpast_001": 0, "vpresperfect_002a": 0, "vpastperfect_002b": 0, "vpresent_003": 0, "advplace_004": 0, "advtime_005": 0, "profirpers_006": 0, "prosecpers_007": 0,"prothirdper_008": 0, "proit_009": 0, "prodemons_010": 0, "proindef_011": 0, "pverbdo_012": 0, "whquest_013": 0, "nominalis_014": 0, "gerund_015": 0,"nouns_016": 0, "passagentl_017": 0, "passby_018": 0, "mainvbe_019": 0, "exthere_020": 0, "thatvcom_021": 0, "thatacom_022": 0, "whclause_023": 0, "vinfinitive_024": 0, "vpresentpart_025": 0, "vpastpart_026": 0, "vpastwhiz_027": 0, "vpresentwhiz_028":0, "thatresub_029": 0, "thatreobj_030": 0, "whresub_031": 0, "whreobj_032": 0, "whrepied_033": 0, "sentencere_034": 0, "advsubcause_035": 0, "advsubconc_036": 0, "advsubcond_037": 0, "advsubother_038": 0, "prepositions_039": 0, "adjattr_040": 0, "adjpred_041": 0, "adverbs_042": 0, "ttratio_043": 0, "wordlength_044": 0, "conjuncts_045": 0, "downtoners_046": 0, "hedges_047": 0, "amplifiers_048": 0, "emphatics_049": 0, "discpart_050": 0, "demonstr_051": 0, "modalsposs_052": 0, "modalsness_053": 0, "modalspred_054": 0, "vpublic_055": 0, "vprivate_056": 0, "vsuasive_057": 0, "vseemappear_058": 0, "contractions_059": 0, "thatdel_060": 0, "strandprep_061": 0, "vsplitinf_062": 0, "vsplitaux_063": 0, "coordphras_064": 0, "coordnonp_065": 0, "negsyn_066": 0,  "negana_067": 0, "hashtag_201": 0, "link_202": 0, "interlink_203": 0, "caps_204": 0, "vimperative_205": 0, "question_208": 0, "exclamation_209": 0, "lenchar_210": 0, "lenword_211": 0, "comparatives_syn_212": 0, "superlatives_syn_213": 0, "comparatives_ana_214": 0, "superlatives_ana_215":0}
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
conjunctslist = ["alternatively", "altogether", "consequently", "conversely", "eg", "e.g.", "else", "furthermore",
                 "hence", "however", "ie", "instead", "likewise", "moreover", "namely", "nevertheless",
                 "nonetheless", "notwithstanding", "otherwise", "rather", "similarly", "therefore", "thus", "viz"]
conjunctsmultilist = ["on the contrary", "on the other hand", "for example", "for instance", "by contrast", "by comparison", "in comparison", "in contrast", "in particular", "in addition", "in conclusion", "in consequence", "in sum", "in summary", "in any event", "in any case", "in other words", "as a result", "as a consequence"]
punct_final = [".", "!", "?", ":", ";"] # here, Biber also includes the long dash -- , but I am unsure how this would be rendered
belist = ["be", "am", "are", "is", "was", "were", "been", "being", "'m", "'re",] # I have added the contracted forms of am and are (AB)
havelist = ["have", "has", "had", "having"]
dolist = ["do", "does", "doing", "did", "done"]
subjpro = ["i", "we", "he", "she", "they"]
posspro = ["my", "our", "your", "his", "their", "its"]
DEM = ["that", "this", "these", "those"]
WHP = ["who", "whom", "whose", "which"]
WHO = ["what", "where", "when", "how", "whether", "why", "whoever", "whomever", "whichever", 
       "whenever", "whatever", "however"] # can this be accomplished with tag WDT? (KM) # Tag WDT comprises Biber's WHP and WHO plus relativizer "that" afaict. (AB)
discpart = ["well", "now", "anyway", "anyhow", "anyways", "though"]
QUAN = ["each", "all", "every", "many", "much", "few", "several", "some", "any"]
QUANPRO = ["everybody", "somebody", "anybody", "everyone", "someone", "anyone", "everything", "something", "anything"]
ALLP = [".", "!", "?", ":", ";", ","]  # here, Biber also includes the long dash -- , but I am unsure how this would be rendered 
downtonerlist = ["almost", "barely", "hardly", "merely", "mildly", "nearly", "only", "partially", "partly", "practically", "scarcely", "slightly", "somewhat"]
                # some others that could be included: a little, a bit, a tad (HM)
amplifierlist = ["absolutely", "altogether", "completely", "enormously", "entirely", "extremely", "fully", "greatly", "highly", 
                 "intensely", "perfectly", "strongly", "thoroughly", "totally", "utterly", "very"]
asktelllist = ["ask", "asked", "asking", "asks", "tell", "telling", "tells", "told"] #this could also be accomplished with .startswith("ask"), .startswith("tell") or == "told" (KM)
titlelist = ["mr", "ms", "mrs", "prof", "professor", "dr", "sir"] #??????? (KM)
otheradvsublist = ["since", "while", "whilst", "whereupon", "whereas", "whereby", "such that", "so that", "such that", "inasmuch as", "forasmuch as", "insofar as", "insomuch as", "as long as", "as soon as"]
titlelist = ["mr", "ms", "mrs", "prof", "professor", "dr", "sir"]
notgerundlist = ["nothing", "everything", "something", "anything", "thing", "things", "string", "strings"]
publiclist = ["acknowledege", "acknowledges", "acknowledged", "acknowledging", "admit", "admits", "admitted", "admitting",
              "agree", "agrees", "agreed", "agreeing", "assert", "asserts", "asserted", "asserting", "claim", "claimed", 
              "claims", "claiming", "complain", "complains", "complained", "complaining", "declare", "declared", "declares",
              "declaring", "deny", "denies", "denied", "denying", "explain", "explains", "explained", "explaining", "hint",
              "hints", "hinted", "hinting", "insist", "insisted", "insists", "insisting", "mention", "mentions", "mentioned",
              "mentioning", "proclaim", "proclaims", "proclaimed", "proclaiming", "promise", "promises", "promised", "promising",
              "protest", "protests","protested", "protesting", "remark", "remarks", "remarking", "remarked", "reply", 
              "replied", "replies", "replying", "report", "reports", "reported", "reporting", "say", "says", "said", "saying",
              "suggest", "suggests", "suggested", "suggesting", "swear", "swears", "swore", "swearing", "write", "wrote", "writing", "writes"]
privatelist = ["anticipate", "anticipates", "anticipated", "anticipating", "assume", "assumes", "assumed", "assuming",
               "believe", "believes", "believed", "believing", "conclude", "concludes", "concluded", "concluding", "decide",
               "decides", "decided", "deciding", "demonstrate", "demostrates", "demonstrated","demonstrating", "determine",
               "determines", "determined", "determining", "discover", "discovers", "discovered", "discovering", "doubt",
               "doubts", "doubted", "doubting", "estimate", "estimated", "estimates", "estimating", "fear", "fears", "feared",
               "fearing", "feel", "feels", "feeled", "feeling", "find", "finds", "found", "finding", "forget", "forgets", 
               "forgot", "forgetting", "guess", "guesses", "guessed", "guessing", "hear", "hears", "heard", "hearing", "hope",
               "hopes", "hoped", "hoping", "imagine", "imagines", "imagined", "imagining", "imply", "implies", "implied", 
               "implying", "indicate", "indicates", "indicating", "indicated", "infer", "infers", "infered", "inferring", "inferred",
               "know", "knows", "knew", "knowing", "learn", "learns", "learnt", "learned", "learning", "mean", "means", "meant",
               "meaning", "notice", "notices", "noticed", "noticing", "prove", "proves", "proved", "proving", "realise", "realize",
               "realised", "realized", "realises","realizes", "realising", "realizing", "recognise", "recognize", "recognises",
               "recognizes", "recognised", "recognized", "recognising", "recognizing", "remember", "remembers", "remembered",
               "remembering", "reveal", "reveals", "revealing", "revealed", "see", "sees", "saw", "seen", "seeing", "show", "shows",
               "showed", "showing", "suppose", "supposed", "supposes", "supposing", "think", "thinks", "thought", "thinking",
               "understand", "understands", "understood", "understanding"]
suasivelist = ["agree", "agrees", "agreed", "agreeing", "arrange", "arranges", "arranged", "arranging", "ask", "asks", "asked",
               "asking", "beg", "begs", "begged", "begging", "command", "commands", "commanded", "commanding", "decide", "decides",
               "decided", "deciding", "demand", "demands", "demanding", "demanded", "grant", "grants", "granted", "granting",
               "insist", "insists", "insisted", "insisting", "instruct", "instructs", "instructed", "instructing", "ordain", 
               "ordains", "ordained", "ordaining", "pledge", "pledges", "pledging", "pledged", "pronounce", "pronounces", 
               "pronounced", "pronouncing", "propose", "proposes", "proposed", "proposing", "recommend", "recommends", "recommended",
               "recommending", "request", "requests", "requested", "requesting", "stipulate", "stipulates", "stipulated", "stipulating",
               "suggest", "suggests", "suggested", "suggesting", "urge", "urged", "urges", "urging"]
copulalist = ["be", "am", "is", "was", "were", "been", "being", "appear", "appears", "appeared", "appearing", "seem", "seems", "seemed", "seeming", 
              "sound", "sounds", "sounding", "sounded", "smell", "smells", "smelled", "smelling", "become", "becomes", "became", "becoming", "turn", 
              "turns", "turning", "turned", "turn", "grow", "grows", "grew", "growing", "growed", "grown", "get", "gets", "getting", "gotten", 
              "got", "look", "looks", "looking", "looked", "taste", "tastes", "tasted", "tasting", "feel", "feels", "feeled", "felt", "feeling"] 
            # AB: are these missing on purpose: "turnt", "grown", "gets", "getting", "gotten"?
            # HM: nope, sorry! added the missing ones. There are also some more marginal verbs which I didn't include, but I don't think 
            # we need to worry about these


#POS-functions
def analyze_verb(index, tagged_sentence, features_dict):  ## 1. Axel 2. Hanna
    '''Takes the index position of the current word, a tagged sentence, and dictionary of all possible tags and updates relevant keys: "vpast_001", "vpresperfect_002a", "vpastperfect_002b", "vpresent_003", 
    "pverbdo_012", "passagentl_017", "passby_018", "mainvbe_019", "whclause_023", "vinfinitive_024", "vpresentpart_025", "vpastpart_026", "vpastwhiz_027", "vpresentwhiz_028",
    "emphatics_049", "vpublic_055", "vprivate_056", "vsuasive_057", "vseemappear_058", "contractions_059", 
    "thatdel_060", "vsplitinf_062", "vsplitaux_063", "vimperative_205".'''
    ## already checked: "vpast_001", "pverbdo_012", "passagentl_017", "passby_018", "whclause_023", "vinfinitive_024", "vimperative_205", "vpresentpart_025", "vpresentwhiz_028", "vpastpart_026", "vpastwhiz_027", "vpresent_003", 
    ##          "emphatics_049", "vpublic_055", "vprivate_056", "vsuasive_057", "vseemappear_058", "vpastperfect_002b", "vpresperfect_002a", "mainvbe_019", "contractions_059", "thatdel_060", "vsplitinf_062", "vsplitaux_063", 
    ## still needs checking: 
      
    word_tuple = tagged_sentence[index]
    if word_tuple[1] == "VBD":
        features_dict["vpast_001"] += 1
    elif word_tuple[1] == "VB":
        if tagged_sentence[index-1][1] == "X" or tagged_sentence[index-1][0] == ",": ## counts base forms as imperatives if they are sentence-initial (or behind a comma) and as infinitives everywhere else, which is not ideal but a start (HM)
            features_dict["vimperative_205"] += 1
        else: 
            features_dict["vinfinitive_024"] += 1
            if tagged_sentence[index-2][0] == "to":
                if tagged_sentence[index-1][1] == "RB" and not tagged_sentence[index-1][0] in ["n't", "not"]:
                    features_dict["vsplitinf_062"] += 1
                else:
                    pass
            elif tagged_sentence[index-3][0] == "to":
                if tagged_sentence[index-2][1] == "RB" and not tagged_sentence[index-2][0] in ["n't", "not"]:
                    if tagged_sentence[index-1][1] == "RB" and not tagged_sentence[index-1][0] in ["n't", "not"]:
                        features_dict["vsplitinf_062"] += 1
                else:
                    pass
            
    elif word_tuple[1] == "VBG":
        if (tagged_sentence[index-1][1] == "X" or tagged_sentence[index-1][0] in ALLP) and tagged_sentence[index+1][1] in ["IN", "DT", "RB", "WP","PRP", "WRB"]: #gerund or present participle.. is this ok? or do we have to separate these 
            # AB: In Biber, this is in fact only for present participial clauses, a fairly narrow range of ING-forms. I implement it accordingly and would suggest a separate class of features for progressives (which Biber really does not seem to have considered in the 80s)
            # HM: I agree that it would be good to have a separate count for progressives, but how can we implement this given that our tag-set only has one tag for all ING-forms? Preceded by BE?
            features_dict["vpresentpart_025"] += 1
        elif tagged_sentence[index-1][1] == "NN":
            features_dict["vpresentwhiz_028"] += 1 
            # Iffy, because catches things like "with prices going up", which is not a case of WHIZ deletion (AB)
            # I agree, we might have to drop this one. Also catches stuff like "or is the passage saying something different" (HM)
    elif word_tuple[1] == "VBN":
        if (tagged_sentence[index-1][1] == "X" or tagged_sentence[index-1][0] in ALLP):
            if tagged_sentence[index+1][1] in ["IN", "RB", "TO"]: # Again, in Biber this is present participial clauses only. Biber (1988:233) notes for both that "these forms were edited by hand." So we may consider scrapping them, if automated accuracy is not sufficient.
                features_dict["vpastpart_026"] += 1 ## this one seems accurate enough to me (HM)
        elif tagged_sentence[index-1][1] in ["NN", "NNP"] or tagged_sentence[index-1][0] in QUANPRO:
            if tagged_sentence[index+1][1] in ["IN", "RBR", "RB", "RBS"] or tagged_sentence[index+1][0] in belist:
                features_dict["vpastwhiz_027"] += 1 
                # This reproduces the search strategy from Biber, but strikes me as extremely iffy. Needs further quality control.
                # I can't check this right now due to tagger problems, revisit later! (HM)
    elif word_tuple[1] in ["VBP","VBZ"]:
        features_dict["vpresent_003"] += 1
    if word_tuple[0].startswith("seem") or word_tuple[0].startswith("appear"):
        features_dict["vseemappear_058"] += 1
        
    if word_tuple[0] in ["had", "'d"]: 
        # Centering the lookup for perfect forms on the HAVE means counting only once for, e.g. "has considered, debated, but ultimately rejected a different search strategy". Let's discuss whether this is desirable. (AB)
        # I would say that this is acceptable. Such concatenations are probably very marginal.
        move_on = True
        insert_adv = False
        x = index
        while move_on: # These while-statements are an attempt to get around the question of how much intervening material to allow by instead setting conditions for when to stop looking on (either because an instance of the feature has been found or an impermissible context has been encountered) (AB)
            x += 1
            if tagged_sentence[x][1] == "VBN":
                move_on = False
                features_dict["vpastperfect_002b"] += 1
                if insert_adv:
                    features_dict["vsplitaux_063"] += 1
            elif tagged_sentence[x][1].startswith("R") and tagged_sentence[x][0] not in ["n't", "not"]: # Unfortunately, negators and adverbs have the same tags, so we manually exclude negators.
                insert_adv = True
            elif tagged_sentence[x][1].startswith("N") or tagged_sentence[x][1].startswith("P") or tagged_sentence[x][1].startswith("X"): # Currently excludes questions, in which the subject is between HAVE and the past participle. (AB)
                move_on =  False 
                ## this actually exlcudes Biber's other condition for feature 2: to also count questions he includes HAVE + N/PRO + VBN (HM)
                ## We should discuss whether we want that or not.

    elif word_tuple[0] in ["have", "'ve", "has"]: 
        # "'s" excluded because I see no reliable way to separate between IS and HAS contractions - unless we lemmatize (AB)
        # I thought we said that lemmatisation probably makes sense to also look for the public/private/suasive verbs below? (HM)
        # So if we do it anyway we can also insert it here later on.
        move_on = True
        insert_adv = False
        x = index
        while move_on: # These while-statements are an attempt to get around the question of how much intervening material to allow by instead setting conditions for when to stop looking on (either because an instance of the feature has been found or an impermissible context has been encountered) (AB)
            x += 1
            if tagged_sentence[x][1] == "VBN":
                move_on = False
                features_dict["vpresperfect_002a"] += 1
                if insert_adv:
                    features_dict["vsplitaux_063"] += 1
            elif tagged_sentence[x][1].startswith("R") and tagged_sentence[x][0] not in ["n't", "not"]:
                insert_adv = True
            elif tagged_sentence[x][1].startswith("N") or tagged_sentence[x][1].startswith("P") or tagged_sentence[x][1].startswith("X"): 
                # Currently excludes questions, in which the subject is between HAVE and the past participle. (AB)
                # see comment above on vpastperfect_002b (HM)
                move_on =  False
                
    elif word_tuple[0] in belist: # Something that is very obviously missing from Biber's list and also our features right now is progressive. Here would be the place to include them.
        if tagged_sentence[index+1][1] in ["DT", "PRP$", "JJ", "JJR", "JJS", "NN", "NNS", "NNP"]: # Biber also includes prepositions, but this seems to me to allow for too many false positives (AB)
            ## Why doesn't Biber also include adverbs here? "I AM REALLY interested"/"He is truly a liar" are also cases of BE as main verb.
            features_dict["mainvbe_019"] += 1
        else:
            move_on = True
            insert_adv = False
            x = index
            while move_on == True:
                x += 1
                if tagged_sentence[x][1] == "VBN":
                    move_on = False
                    if tagged_sentence[x+1][0] == "by":
                        features_dict["passby_018"] += 1
                        if insert_adv:
                            features_dict["vsplitaux_063"] += 1
                            ## HM: I think there is a mistake in Biber's formula here: for 63 he states AUX + ADV + VB (with VB meaning the base form of the verb),
                            ## but the example sentence he gives is "they are objectively SHOWN to", which does not use the base form.
                            ## So far in our code we only count split auxiliaries if the verb is in the past participle (VBN). Is this what we want?
                            ## What about interverning adverbs in progressive verb phrases? "I am really trying"?
                    elif tagged_sentence[x+1][1] == "IN": # Here, provision is made for by-passive with intervening PPs: "was shot in the head by an unidentified suspect"
                        x += 1
                        move_on2 = True
                        while move_on2:
                            x += 1
                            if tagged_sentence[x+1][1].startswith("N") or tagged_sentence[x+1][1].startswith("DT"): # One might include adjectives here as well, but prob at the cost of precision.
                                pass
                            elif tagged_sentence[x+1][0] == "by":
                                features_dict["passby_018"] += 1
                                if insert_adv:
                                    features_dict["vsplitaux_063"] += 1
                                move_on2 = False
                            else:
                                features_dict["passagentl_017"] += 1
                                if insert_adv:
                                    features_dict["vsplitaux_063"] += 1
                                move_on2 = False
                    else:
                        features_dict["passagentl_017"] += 1
                        if insert_adv:
                            features_dict["vsplitaux_063"] += 1  
                elif tagged_sentence[x][1].startswith("RB"):
                    if tagged_sentence[x][0] not in ["n't", "not"]:
                        insert_adv = True
                    else:
                        pass
                else:
                    move_on = False
    elif word_tuple[0] in dolist:
        move_on = True
        negator = False
        insert_adv = False
        x = index
        while move_on:
            x += 1
            if tagged_sentence[x][1].startswith("V"):
                move_on = False
                if negator == False:
                    features_dict["emphatics_049"] += 1
                if insert_adv:
                    features_dict["vsplitaux_063"] += 1
            elif tagged_sentence[x][0] in ["not", "n't"]:
                negator = True
            elif tagged_sentence[x][1].startswith("R"):
                insert_adv = True
            else:
                move_on = False
                #if not (tagged_sentence[index-1][0] in WHP+WHO and tagged_sentence[index-2][0] == "X"):
                    #features_dict["pverbdo_012"] += 1 # This follows the criteria in Biber, but seems too broad. Do we want things like "do someone a favor" "do the boogie" etc. here? (AB)
                        ## HM: this does indeed catch a lot of garbage ("does this mean", "do rides", "what he does" ...)
                        ## alternatively we could look for some restricted contexts in which do is sure to be a pro-verb: 
                        ## - followed by ", too": I DO, too.
                        ## - sentence-final position: I DO.
                        ## - followed by a placeholder: DO this/that/it/so.
                        ## I implemented this belows. Awaits evaluation from someone else.
    if word_tuple[0] in dolist:
        if tagged_sentence[index+1][1] == "X":
            features_dict["pverbdo_012"] += 1
        elif tagged_sentence[index+1][0] in ["too", "this", "that", "it", "so"]:
            if tagged_sentence[index+2][1] == "X" or tagged_sentence[index+2][0] in ALLP:
                features_dict["pverbdo_012"] += 1
            else:
                pass
    
    if word_tuple[0].startswith("'"):
        features_dict["contractions_059"] += 1

    
    ## for now I implemented this with a preliminary list of verbs in each class - change this condition once lemmatisation is implemented (HM)
    if word_tuple[0] in publiclist:
        features_dict["vpublic_055"] += 1
        if tagged_sentence[index + 1][0] in ["this", "these", "that", "those", "I", "we", "he", "she", "they"]: ## 60-1 pub/priv/sua + demonstrative pronoun/subjpro (I we he she they)
            features_dict["thatdel_060"] += 1
        elif tagged_sentence[index + 1][1].startswith("NN") or tagged_sentence[index + 1][1].startswith("PR"): ## 60-2 pub/priv/sua + PRO/N + AUX/V
            if tagged_sentence[index + 2][1].startswith("V") or tagged_sentence[index + 2][1] == "MD":
                features_dict["thatdel_060"] += 1
        elif tagged_sentence[index + 1][1] in ["JJ", "JJR", "JJS", "RB", "RBR", "RBS", "PRP$", "DT"]: ## 60-3 pub/priv/sua + adj/adv/det/posspro + (Adj) + N + AUX/V
            if tagged_sentence[index + 2][1].startswith("NN"):
                if tagged_sentence[index + 3][1].startswith("V") or tagged_sentence[index + 3][1] == "MD":
                    features_dict["thatdel_060"] += 1
        if tagged_sentence[index + 1][0] in WHP or tagged_sentence[index + 1][0] in WHO:
            if tagged_sentence[index + 2][1] != "MD":
                features_dict["whclause_023"] += 1
            else:
                pass

    if word_tuple[0] in privatelist:
        features_dict["vprivate_056"] += 1
        if tagged_sentence[index + 1][0] in ["this", "these", "that", "those", "I", "we", "he", "she", "they"]: ## 60-1 pub/priv/sua + demonstrative pronoun/subjpro (I we he she they)
            features_dict["thatdel_060"] += 1
        elif tagged_sentence[index + 1][1].startswith("NN") or tagged_sentence[index + 1][1].startswith("PR"): ## 60-2 pub/priv/sua + PRO/N + AUX/V
            if tagged_sentence[index + 2][1].startswith("V") or tagged_sentence[index + 2][1] == "MD":
                features_dict["thatdel_060"] += 1
        elif tagged_sentence[index + 1][1] in ["JJ", "JJR", "JJS", "RB", "RBR", "RBS", "PRP$", "DT"]: ## 60-3 pub/priv/sua + adj/adv/det/posspro + (Adj) + N + AUX/V
            if tagged_sentence[index + 2][1].startswith("NN"):
                if tagged_sentence[index + 3][1].startswith("V") or tagged_sentence[index + 3][1] == "MD":
                    features_dict["thatdel_060"] += 1
        if tagged_sentence[index + 1][0] in WHP or tagged_sentence[index + 1][0] in WHO:
            if tagged_sentence[index + 2][1] != "MD":
                features_dict["whclause_023"] += 1
            else:
                pass

    if word_tuple[0] in suasivelist:
        features_dict["vsuasive_057"] += 1
        if tagged_sentence[index + 1][0] in ["this", "these", "that", "those", "I", "we", "he", "she", "they"]: ## 60-1 pub/priv/sua + demonstrative pronoun/subjpro (I we he she they)
            features_dict["thatdel_060"] += 1
        elif tagged_sentence[index + 1][1].startswith("NN") or tagged_sentence[index + 1][1].startswith("PR"): ## 60-2 pub/priv/sua + PRO/N + AUX/V
            if tagged_sentence[index + 2][1].startswith("V") or tagged_sentence[index + 2][1] == "MD":
                features_dict["thatdel_060"] += 1
        elif tagged_sentence[index + 1][1] in ["JJ", "JJR", "JJS", "RB", "RBR", "RBS", "PRP$", "DT"]: ## 60-3 pub/priv/sua + adj/adv/det/posspro + (Adj) + N + AUX/V
            if tagged_sentence[index + 2][1].startswith("NN"):
                if tagged_sentence[index + 3][1].startswith("V") or tagged_sentence[index + 3][1] == "MD":
                    features_dict["thatdel_060"] += 1
        if tagged_sentence[index + 1][0] in WHP or tagged_sentence[index + 1][0] in WHO:
            if tagged_sentence[index + 2][1] != "MD":
                features_dict["whclause_023"] += 1
            else:
                pass
            
    # -> also needed for features 23 and 60
    # KM -> we also need this for feature 21. part a is down in analye_wh_word but parts b and c need to identify public/private/suasive verbs -- can we add that in this part when theyre identified?:
    # (b) PUB/PRV/SUA/SEEM/APPEAR + that + xxx (where xxx is NOT: V/AUX/CL-P/TJf/anrf){that-c\a\ises as complements to verbs which are not included in the above verb classes are not counted - see Quirk et al. 1985:1179ff.) 
    # (c) PUB/PRV/SUA + PREP + xxx + N + that (where xxx is any number of words, but NOT = N)(This algorithm allows an intervening prepositional phrase between a verb and its complement.)
    #     Biber also checks for that-deletion, which is probably bad in terms of precision and recall. I currently have strong reservations against implementing his search, but have not come up with a better one yet. (AB)
        
    

def analyze_modal(index, tagged_sentence, features_dict): ## 1. Axel 2. Hanna
    '''Takes the index position of the current word, a tagged sentence, and dictionary of all possible tags and updates relevant keys: 
    "modalsposs_052", "modalsness_053", "modalspred_054", "contractions_059", "vsplitaux_063".'''
    ## Several of the features that were origianlly intended for analyze_modal have been moved to analyze_verb instead.
    word_tuple = tagged_sentence[index] #returns a tuple (word, POS)
    if word_tuple[0] in ["can","may","might","could"]:
        features_dict["modalsposs_052"] += 1
    elif word_tuple[0] in ["ought","should","must"]:
        features_dict["modalsness_053"] += 1
    elif word_tuple[0] in ["will","would","shall","'ll","'d"]: 
        features_dict["modalspred_054"] += 1
    if word_tuple[0].startswith("'"): ## the tagger will not remove apostrophes!
        features_dict["contractions_059"] += 1
        
    move_on = True
    insert_adv = False
    x = index
    while move_on:
        x += 1
        if tagged_sentence[x][1].startswith("V"):
            move_on = False
            if insert_adv:
                features_dict["vsplitaux_063"] += 1
        elif tagged_sentence[x][0] in ["not", "n't"]:
            pass
        elif tagged_sentence[x][1].startswith("R"):
            insert_adv = True
        else:
            move_on = False
    
def analyze_adverb(index, tagged_sentence, features_dict): ## 1. Hanna 2. Raffaela 3. Axel
    '''Takes the index position of the current word, a tagged sentence, and dictionary of all possible tags and updates relevant keys:
    "advplace_004", "advtime_005", "adverbs_042", "conjuncts_045",
    "downtoners_046", "hedges_047", "amplifiers_048", "discpart_050", "contractions_059", "negana_067".'''
    features_dict["adverbs_042"] += 1
    word_tuple = tagged_sentence[index] #returns a tuple (word, POS)

    if word_tuple[0] == "not":
        features_dict["negana_067"] += 1
    if word_tuple[0] == "n't":
        features_dict["negana_067"] += 1
        features_dict["contractions_059"] += 1
    elif word_tuple[0] in placelist: ## added some more ideas to the list above (HM)
        features_dict["advplace_004"] += 1
    elif word_tuple[0] in timelist: ## added some more ideas to the list above (HM)
        features_dict["advtime_005"] += 1
    elif word_tuple[0] in downtonerlist: ## added some more ideas to the list above (HM)
        features_dict["downtoners_046"] += 1
    elif word_tuple[0] in amplifierlist:
        features_dict["amplifiers_048"] += 1 
    elif word_tuple[0] in conjunctslist:
        features_dict["conjuncts_045"] += 1 # so far, this list only includes "eg" not "e.g.", since that would probably be split by the tagger? AB: Added "e.g." to the list
    elif index == 0 and word_tuple[0] in discpart:
        features_dict["discpart_050"] += 1
    ## we also look for discourse particles (feature 050) in the particle-section, this is to make sure that
    ## we actually catch all of them in case they are tagged differently (HM)
    
#    if word_tuple[0] == "rather" and index == 0: # if-statement rather than if-else, because "rather"
#        if tagged_sentence[index+1][0] == ",": #punctuation will be removed already, right? (KM) then how do we find this without the comma? (HM) # AB: no, tagger keeps punctuation
#            features_dict["conjuncts_045"] += 1  ## we could try it simply without the comma and see how messy the output is
#        elif tagged_sentence[index+1][1] in ["CC", "CD", "DT", "EX", "IN", "LS", "MD", "NN", "NNS", "NNP", "NNPS", "PDT", "PRP", "PRP$", "RP", "TO", "UH", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "WDT", "WP", "WP$", "WRB"]:
#            features_dict["conjuncts_045"] += 1 
#    elif word_tuple[0] == "else" and index == 0 and tagged_sentence[index+1][0] == ",": #again, commas (KM) #AB: Should not be a problem.
#            features_dict["conjuncts_045"] += 1
#    elif word_tuple[0] == "altogether" and index == 0 and tagged_sentence[index+1] == ",":
#            features_dict["conjuncts_045"] += 1

 
def analyze_adjective(index, tagged_sentence, features_dict): ## 1. Kyla 2. Raffaela 3. Axel
    '''Takes the index position of the current word, a tagged sentence, and dictionary of all possible tags and updates relevant keys:
    "adjattr_040", "adjpred_041", "emphatics_049", "comparatives_212", "superlatives_213".'''
    if tagged_sentence[index][1] == "JJR":
        features_dict["comparatives_syn_212"] += 1
    elif tagged_sentence[index][1] == "JJS":
        features_dict["superlatives_syn_213"] += 1
    if tagged_sentence[index-1][0] == "more":
        features_dict["comparatives_ana_214"] += 1
    elif tagged_sentence[index-1][0] == "most":
        features_dict["superlatives_ana_215"] += 1
    ## AB: I am rewriting the part that checks for attributive versus predicative adjectives, as I think this will improve clarity.
    ## AB: The important statent in Biber (1989: 238) is that "any ADJ not identified as predicative" is treated as attributive.
    ## AB: So this means we only need to specify a condition for all predicative adjectives. When True: adj_pred + =1, when False: adj_attr += 1
    ## AB: Also note there is a logical inconsistency in Biber's condition "BE + ADJ (+ADV) + xxx": The optional ADV should go before the ADJ
    ## AB: I am, in fact, going to simplify our lookup, subject to durther discussion:
    ## AB: Any adjective preceded by an optional sequence of adverbs of any length, which in turn is preceded by a form of BE
    ## AB: (plus potentially other copular verbs like "feel", "look", "become") is predicative; anything else is attributive
    adj_type = "attr"
    x = index-1
    while adj_type == "attr" and tagged_sentence[x][1].startswith("R"):
        x -= 1
        if tagged_sentence[x][0] in copulalist:
            adj_type = "pred"
    if adj_type == "attr":
        features_dict["adjattr_040"] += 1
    elif adj_type == "pred":
        features_dict["adjpred_041"] += 1
#    if tagged_sentence[index-1][0] in belist:
#        if tagged_sentence[index+1][1].startswith("JJ") or tagged_sentence[index+1][1].startswith("NN"):
#            features_dict["adjattr_040"] += 1
#
#        elif not tagged_sentence[index+1][1].startswith("RB"): ##!!! Check not-statement (KM)
#            features_dict["adjpred_041"] += 1
#
#        if tagged_sentence[index+1][1].startswith("JJ") and not tagged_sentence[index+2][1].startswith("JJ") and not tagged_sentence[index+2][1].startswith("NN"): #Would it not be okay to have JJ in position +1 and +2? 
#            features_dict["adjpred_041"] += 1        
    if tagged_sentence[index-1][0] in ["real", "so"]: #and tagged_sentence[index][1] == "JJ":
        #I think this should work but should double check because it was catching junk at some point (KM)
        # AB: Turned this into an if rather than elif. Also, I think the part to the right of the boolean "and" is not needed?
        features_dict["emphatics_049"] += 1
      
def analyze_preposition(index, tagged_sentence, features_dict): ## 1. Gustavo 2. ?
    '''Takes the index position of the current word, a tagged sentence, and dictionary of all possible tags and updates relevant keys: 
    "advsubcause_035", "advsubconc_036", "advsubcond_037", "advsubother_038", "prepositions_039", 
    "conjuncts_045", "hedges_047", "strandprep_061".'''
    word_tuple = tagged_sentence[index] #returns a tuple (word, POS)
    if not word_tuple[0] in ["because", "unless", "whilst", "while", "though", "tho", "although", "that", "since", "whereupon", "whereas", "whereby"] + timelist + placelist: 
        features_dict["prepositions_039"] += 1 # AB: I am excluding conjunctions and time/place adverbials here, as they count towards other features
    if word_tuple[0] in ["because", "becuase", "beacuse", "cause", "'cause", "cos", "'cos", "coz", "'coz", "caus", "'caus", "cuz", "'cuz", "bcoz", "bcuz", "bcos", "bcause", "bcaus"] and tagged_sentence[index+1][0] != "of":
        features_dict["advsubcause_035"] += 1 # AB: I decided against a separate feature for "because of" since it goes into "prepositions_039".
        # AB: The list of possible forms of "because" is already quite long, but probably not exhaustive...
    elif word_tuple[0] == "although" or word_tuple[0] == "though" or word_tuple[0] == "tho":
        features_dict["advsubconc_036"] += 1 #AB: I added "though" tagged as "RB" ("Are you sure though?") to the dicpart list, so it contributes to feature
        # AB: "discpart_050" through the analyze_adverb function
        
    elif word_tuple[0] == "that" and tagged_sentence[index-1][0] in ["such", "so"]: #and not tagged_sentence[index+1][1] in ["JJ", "JJR", "JJS", "NN", "NNS", "NNP", "NNPS"]:
        features_dict["advsubother_038"] += 1 # AB: Above, the condition that no Adj or N can follow (used by Biber) has been commented out because our tagger allows us to
        # AB: make the kind of differentiation intended (between "that" as a complementizer and as a determinative/demonstrative PN). This means we avoid many false negatives.

    elif word_tuple[0] == "of" and tagged_sentence[index-1][0] in ["kind", "sort"] and not tagged_sentence[index-2][1] in ["JJ", "JJR", "JJS", "DT", "PRP$"]:
        if not tagged_sentence[index-2][0] in ["what", "whatever", "whichever"]:
            features_dict["hedges_047"] += 1

    if tagged_sentence[index+1][0] in ALLP or tagged_sentence[index+1][1] == "X":
        features_dict["strandprep_061"] += 1


def analyze_noun(index, tagged_sentence, features_dict): ## 1. Rafaela 2. Hanna
    '''Takes the index position of the current word, a tagged sentence, and dictionary of all possible tags and updates relevant keys:
    "nominalis_014", "gerund_015", "nouns_016".'''
    word_tuple = tagged_sentence[index] #returns a tuple (word, POS)

    if word_tuple[0].endswith("ing") or word_tuple[0].endswith("ings"):
        if word_tuple[1] not in notgerundlist:
            features_dict["gerund_015"] += 1 # this is edited manually by Biber
    elif word_tuple[0].endswith("tions") or word_tuple[0].endswith("tion") or word_tuple[0].endswith("ments") or word_tuple[0].endswith("ment") or word_tuple[0].endswith("ness") or word_tuple[0].endswith("ity") or word_tuple[0].endswith("nesses") or word_tuple[0].endswith("ities"):
        features_dict["nominalis_014"] += 1
    else: 
        features_dict["nouns_016"] += 1
        
def analyze_pronoun(index, tagged_sentence, features_dict): ## 1. Hanna 2. Gustavo
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
        ## we might be able to simply drop the one above, I think the other criteria for feature 10 might already capture most instances (HM)
        features_dict["prodemons_010"] += 1

    if word_tuple[0] in DEM:
        if tagged_sentence[index+1][0] == "and":
            features_dict["prodemons_010"] += 1
        elif tagged_sentence[index+1][1] in ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "MD", "WP"]:
            features_dict["prodemons_010"] += 1
        elif index == (len(tagged_sentence)-1):
            features_dict["prodemons_010"] += 1
    elif word_tuple[0] == "that" and tagged_sentence[index+1][0] == "'s": ## should this be 's or s ? Does the apostrophe get removed? (HM)
        features_dict["prodemons_010"] += 1

def analyze_conjunction(index, tagged_sentence, features_dict): ## 1. Gustavo 2. Raffaela
    '''Takes the index position of the current word, a tagged sentence, and dictionary of all possible tags and updates relevant keys:
    "hedges_047", "coordphras_064", "coordnonp_065".'''
    word_tuple = tagged_sentence[index] #returns a tuple (word, POS)

    if word_tuple[0] == "and": 
        if tagged_sentence[index-1][1].startswith("NN") and tagged_sentence[index+1][1].startswith("NN"):
            features_dict["coordphras_064"] += 1
        elif tagged_sentence[index-1][1].startswith("RB") and tagged_sentence[index+1][1].startswith("RB"):
            features_dict["coordphras_064"] += 1
        elif tagged_sentence[index-1][1].startswith("JJ") and tagged_sentence[index+1][1].startswith("JJ"):
            features_dict["coordphras_064"] += 1
        elif tagged_sentence[index-1][1].startswith("VB") and tagged_sentence[index+1][1].startswith("VB"):
            features_dict["coordphras_064"] += 1
        elif tagged_sentence[index-1][0] == ",": #commas taken out? (KM)
            if tagged_sentence[index+1][0] in ["it", "so", "you", "then"]:
                features_dict["coordnonp_065"] += 1
            elif tagged_sentence[index+1][1] in subjpro or tagged_sentence[index+1][1] in DEM: # So far, this identification of demonstrative pronoun is likely to be too crude. Maybe re-use function for feature 10?
                #I've added the function from feature 10 here. (GK)
                if tagged_sentence[index+1][0] == "and":
                    features_dict["coordnonp_065"] += 1
                elif tagged_sentence[index+1][1] in ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "MD", "WP"]:
                    features_dict["coordnonp_065"] += 1
                elif index == (len(tagged_sentence)-1):
                    features_dict["coordnonp_065"] += 1                            
            elif tagged_sentence[index+1][0] == "there" and tagged_sentence[index+2][0] in belist:
                features_dict["coordnonp_065"] += 1
        elif tagged_sentence[index-1][0] in punct_final: 
            features_dict["coordnonp_065"] += 1
        elif tagged_sentence[index+1][0] in WHP or tagged_sentence[index+1][0] in WHO or tagged_sentence[index+1][0] in discpart:
            features_dict["coordnonp_065"] += 1
        elif tagged_sentence[index+1][0] in ["because", "although", "though", "if", "unless",] or tagged_sentence[index+1][0] in otheradvsublist: # added the otheradvsublist for this particular feature (GK)
            features_dict["coordnonp_065"] += 1
        elif tagged_sentence[index+1][0] in conjunctslist or tagged_sentence[index+1][0] in conjunctsmultilist: # added the conjunctsmultilist for the this particular feature (GK)
            features_dict["coordnonp_065"] += 1
    #elif word_tuple[0] == "or":
        #if tagged_sentence[index-1][0] == "more" and tagged_sentence[index+1][0] == "less":
            #features_dict["hedges_047"] += 1 ## Move to analyze_sentence (KM)


    if word_tuple[0] == "and" and tagged_sentence[index+1][0] in WHP or tagged_sentence[index+1][0] in WHO:
        features_dict["coordnonp_065"] += 1 
    elif word_tuple[0] == "and" and tagged_sentence[index+1][0] in ["because", "although", "though", "if", "unless", "since", "while", "whilst", "whereas", "whereby"]:
        features_dict["coordnonp_065"] += 1 
    elif word_tuple[0] == "and" and tagged_sentence[index+1][0] in discpart:
        features_dict["coordnonp_065"] += 1
    elif word_tuple[0] == "and" and tagged_sentence[index+1][0] in conjunctslist:
        features_dict["coordnonp_065"] += 1

     
    # still missing: "coordnonp_065" (only for 'and' followed by adverbial subordinator or conjunct, depend on other features)


def analyze_determiner(index, tagged_sentence, features_dict): ## 1. Rafaela 2. Gustavo
    '''Takes the index position of the current word, a tagged sentence, and dictionary of all possible tags and updates relevant keys:
    "demonstr_051", "negsyn_066".'''
    word_tuple = tagged_sentence[index] #returns a tuple (word, POS)

    if word_tuple[0] in DEM:
        features_dict["demonstr_051"] += 1
    elif word_tuple[0] == "neither" or word_tuple[0] == "nor":
        features_dict["negsyn_066"] += 1
    elif word_tuple[0] == "no":
        if tagged_sentence[index+1][1].startswith("NN") or tagged_sentence[index+1][1].startswith("JJ"):
            features_dict["negsyn_066"] += 1
        elif tagged_sentence[index+1][0] in QUAN:
            features_dict["negsyn_066"] += 1

def analyze_wh_word(index, tagged_sentence, features_dict): ## 1. Kyla 2. Hanna
    # Check: Ft 32 (Biber's way of finding this seems like it could be optimized)
    # Check: Ft 22 (catches unintended phrases)
    '''Takes the index position of the current word, a tagged sentence, and dictionary of all possible tags and updates relevant keys:
    "whquest_013", "thatvcom_021", "thatacom_022", "whrepied_033", "sentencere_034", "thatresub_029", "thatreobj_030", 
    "whresub_031", "whreobj_032".'''
    word_tuple = tagged_sentence[index] #returns a tuple (word, POS)
    ## I changed the structure of the function so that we first distinguish between 'that' and all other items
    ## and then between WHO and WHP-items. I hope this makes sense?
    
    #21 that verb complements (e.g., / said that he went) 
    # (a) and\nor\but\or\aho\ALL-P + that + DET/PRO/there/plural noun/proper noun/TITLE (these are i/za£-clauses in clause-initial positions) 
    if tagged_sentence[index][0] == "that":
        if tagged_sentence[index-1][0] in ALLP or tagged_sentence[index-1][0] in ["and", "nor", "but", "or", "who"]:
            if tagged_sentence[index+1][1].startswith("D") or tagged_sentence[index+1][1].startswith("PR") or tagged_sentence[index+1][0] == "there" or tagged_sentence[index+1][1].startswith("NNP") or tagged_sentence[index+1][1].startswith("NNS") or tagged_sentence[index+1][0] in titlelist:
                features_dict["thatvcom_021"] += 1
    # moved b and c of 21 to analyze_verb (because they need to identify certain types of verbs)

    #29. that relative clauses on subject position (e.g., the dog that bit me) N -p (T#) + that + (ADV) + AUX/V {that relatives across intonation boundaries are identified by hand.)
    #30. that relative clauses on object position (e.g., the dog that I saw) N + (T#) + that + DET / SUBJPRO / POSSPRO / it / ADJ / plural noun/ proper noun / possessive noun / TITLE
        if tagged_sentence[index-1][1].startswith("NN"):
            if tagged_sentence[index+1][1].startswith("RB"):
                if (tagged_sentence[index+2][1].startswith("V") or tagged_sentence[index+2][1].startswith("MD")):
                    features_dict["thatresub_029"] += 1 
            elif tagged_sentence[index+1][1].startswith("VB") or tagged_sentence[index+1][1].startswith("MD"):
                features_dict["thatresub_029"] += 1

            elif tagged_sentence[index+1][1].startswith("DT") or tagged_sentence[index+1][1].startswith("JJ") or tagged_sentence[index+1][1] == "NNS" or tagged_sentence[index+1][1].startswith("NNP"):
                features_dict["thatreobj_030"] += 1

            elif tagged_sentence[index+1][0] == "it" or tagged_sentence[index+1][0] in subjpro or tagged_sentence[index+1][0] in posspro:
                features_dict["thatreobj_030"] += 1    
            
        if tagged_sentence[index-1][1].startswith("J"): #This catches things like I'm sure that's a, there's nothing good that can come out of it, etc. Biber keeps mentioning tone boundaries but I dont understand how you could do that computationally (he refers to it as T#)
            features_dict["thatacom_022"] += 1 #that adjective complements (e.g., I'm glad that you like it) ADJ + (T#) + that (complements across intonation boundaries were edited by hand)
                ## we could try restricting the search further by limiting the element in front of the adjective to a copular (and adverb?), but that is then probably too narrow (HM)
                ## further problem: this only catches instances in which 'that' is not dropped - what about "I am glad you liked it"? (HM)
                ## maybe this is one of the features we should leave out? (HM)
                
    else:
        if word_tuple[0] in WHP: # WHP = ["who", "whom", "whose", "which"]
            if tagged_sentence[index-1][1] == "IN":
                features_dict["whrepied_033"] += 1 #pied-piping relative clauses (e.g., the manner in which he was told) PREP + WHP in relative clauses

            if word_tuple[0] == "which" and tagged_sentence[index-1][0] == ",": #34. sentence relatives (e.g., Bob likes fried mangoes, which is the most disgusting thing I've ever heard of) Biber: (These forms are edited by hand to exclude non-restrictive relative clauses.)
                features_dict["sentencere_034"] += 1  ### this only works if the tagger does not delete commas (HM)

            #31. WH relative clauses on subject position (e.g., the man who likes popcorn) xxx + yyy + N + WHP + (ADV) + AUX/V (where xxx is NOT any form of the verbs ASK or TELL; to exclude indirect WH questions like Tom asked the man who went to the store)
            if tagged_sentence[index-1][1].startswith("N"):
                if tagged_sentence[index+1][1].startswith("R"):
                    if (tagged_sentence[index+2][1].startswith("V") or tagged_sentence[index+2][1].startswith("MD")):
                        features_dict["whresub_031"] += 1

                elif(tagged_sentence[index+1][1].startswith("V") or tagged_sentence[index+1][1].startswith("MD")):
                    features_dict["whresub_031"] += 1
        
            #32. WH relative clauses on object positions (e.g., the man who Sally likes) xxx + yyy + N + WHP + zzz (where xxx is NOT any form of the verbs ASK or TELL, to exclude indirect WH questions, and zzz is not ADV, AUX or V, to exclude relativization on subject position)
            #right now, only wh-words at least two words from the front and 2 from the end will be caught here (KM) -> won't catch ex "boys who Sally likes" (is that grammatically acceptable??) also won't catch passives, ex "the men who are liked by Sally" (kind of awkward tbh) (KM)
            if not tagged_sentence[index-2][0].startswith("ask") and not tagged_sentence[index-2][0].startswith("tell") and not tagged_sentence[index-2][0] == "told": 
                if not tagged_sentence[index+1][1].startswith("R") and not tagged_sentence[index+1][1].startswith("V") and not tagged_sentence[index+1][1].startswith("MD"):
                    features_dict["whreobj_032"] += 1 
                
        if word_tuple in WHO: # WHO = ["what", "where", "when", "how", "whether", "why", "whoever", "whomever", "whichever", "whenever", "whatever", "however"]
            #13. direct WH-questions CL-P/Tif + WHO + AUX (where AUX is not part of a contracted form)
            if tagged_sentence[index-1][1] == "X":  
                if tagged_sentence[index+1][1] == "MD":
                    features_dict["whquest_013"] += 1 
            elif tagged_sentence[index+1][1].startswith("V"):
                if tagged_sentence[index+1][0] in belist or tagged_sentence[index+1][0] in havelist or tagged_sentence[index+1][0] in dolist:
                    features_dict["whquest_013"] += 1
                    ## I changed this code to look for the first index position instead of sentence-final punctuation, since the tagger will separate the sentences.
       


def analyze_there(index, tagged_sentence, features_dict): ## 1. noone 2. Gustavo
    '''Takes the index position of the current word, a tagged sentence, and dictionary of all possible tags and updates relevant keys: 
    "exthere_020".'''
    if tagged_sentence[index][1] == "EX":
        features_dict["exthere_020"] += 1
    # depending on the accuracy of the tagger for this feature, it may be necessary to add further restraints
    
def analyze_particle(index, tagged_sentence, features_dict): ## 1. Hanna 2. Gustavo
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
## NEEDED: function to write meta-info for each text 

def POS_tagger(tagged_sentence, features_dict):
    for index in range(3, len(tagged_sentence)-3): #based on POS, apply different function
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

def MDA_analyzer(filepath):
    preprocessed_file = open_reddit_json(filepath) #reads in file, separates into sentences, initializes feature dict
    analyze_sentence(preprocessed_file) #updates raw-sentence based counts (i.e. punctuation marks, length)
    all_ft_dicts = []

    for id in preprocessed_file: #loops through all individual sentences in the file one by one
        sentence_dict = preprocessed_file.get(id) #retrieves entire dictionary and all sub-dicts for the given sentence
        sentence = sentence_dict["body"] #retrieves sentence only (str)) 
        features_dict = sentence_dict["features"] #retrieves s for the given sentence
        tagged_sentence = tag_sentence(sentence) #tags sentence, returning list of tuples with (word, pos)
        POS_tagger(tagged_sentence, features_dict)
        all_ft_dicts.append(sentence_dict)
    
    r = open(os.path.join(dirname, 'results'), "w")
    r.write(all_ft_dicts + '\n')
    r.close()

def tester(practice_sentences, feature):
    for practice_sentence in practice_sentences:
        tagged_sentence = tag_sentence(practice_sentence)
        features_dict = s.copy()
        POS_tagger(tagged_sentence, features_dict)
        
        #put breakpoint on line below
        print(practice_sentence, "//count = ", features_dict[feature]) 

practice_sentences = ["He then consequently ate five donuts in a row.", 
"Go buy donuts now else there won't be any left.", "I want something else.", 
"Go eat a donut instead of complaining.", "I would much rather have a donut now than later."]

#tester(practice_sentences, "conjuncts_045")

# if __name__ == "__main__":
    
#     ram_present = psutil.virtual_memory()[0] >> 30
#     if ram_present < 7:
#         print("WARNING: This is RAM-intensive operation. It cannot continue if you don't have at least 8 GB of RAM.\nExiting...")
#         sys.exit(0)
    
#     p = Pool()
    
#     results = p.map(MDA_analyzer, all_files)
#     print(results)
    
#     p.close()
#     p.join()

# with concurrent.futures.ProcessPoolExecutor() as executor:
#     executor.map(MDA_analyzer, all_files)

for file in all_files:
    MDA_analyzer(file)

print(timedelta(seconds=time.time() - start_time))

    
