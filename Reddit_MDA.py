# 06.05.21 - K Q: Do we need if __name__ == "__main__" for multiprocessing? 
# Open Q: Will commas be removed by the tagger?
# Should we transform all 'word_tuple's into 'tagged_sentence[index]'? Or does it improve readability?

#New comments
# 10.06.21: Flair tagger seems to be much slower (>30min for 3 files for me). Should we separate tagging and feature collection? 
# For example, we could tag the file, save it in the folder separately, and then use the tagged file for feature collection later
# Then if we have to change or re-run, we would have a copy of tagging / could do it separately to help with time / CPU power 
# Would take more hard drive space, but could also have it be optional, i.e. if tagged version exists, use that, if not, tag fresh and save
# I've added a multiprocessing system for which the feature dicts for each file get saved separately
# These can easily be combined into one file later and would allow us to divided up parts of Reddit across multiple computers

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
#from flair.models import SequenceTagger
#from flair.data import Sentence
import advertools as adv
from datetime import timedelta
start_time = time.time()

#dirname = os.path.dirname(__file__)
#data_folder = os.path.join(dirname, 'sample_data')
#all_files = [os.path.join("sample_data", file) for file in os.listdir(data_folder) if os.path.splitext(file)[1] == ".json"]

#tagger_FLAIR = SequenceTagger.load("final-model_64.pt")


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
                    if sentence.strip(string.punctuation): 
                        sentence_counter +=1 #keep track of which sentence it is (1st, 2nd, etc.)
                        sentence_dict = {"body": sentence, "author": author, "link_id": link_id, "sentence_no": sentence_counter, "subreddit": subreddit}
                        sentence_dict["features"] = s.copy()
                        prepped_json[str(base + "_" + str(link_id) + "_" + str(sentence_counter))] = sentence_dict #creates a dict within a dict, so that the key (filename, linkid, sentence number) calls the whole dict

            except json.decoder.JSONDecodeError:
                errors +=1 #keeps track of how many errors are encountered/lines skipped

        print("Total lines skipped = " + str(errors))
    return prepped_json

def lengthening(word):
    '''Takes a word as an argument. Returns True if any sequence of 3+
    identical characters is in the word, with the exception of multiple
    "w"s (to avoid false positives with websites). Else returns False.'''
    count = 1
    character = ""
    for c in word:
        if c == character and not c == "w":
            count += 1
            if count == 3:
                return(True)
        else:
            count = 1
            character = c
    return(False)

# Untagged feature extraction functions
def analyze_sentence(preprocessed_json):
    # AB: General comment: careful with the .count() function. It has no inherent concept of word boundaries, which will lead to false positives in some cases (see below)
    '''Takes the preprocessed json and adds to the features sub-dictionary the following keys and counts (values): "hashtag_201": no. of hashtags,
    "question_208": no. of question marks, "exclamation_209": no of exclamation marks, "lenchar_210": len of sentence in char, "lenword_211": len of sentence in words, 
    "conjuncts_045", "reddit_vocab".'''

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

        if sentence.endswith("?"):
            s["question_208"] += 1
            
        if sentence.endswith("!"):
            s["exclamation_209"] += 1
        
        s["emojis_218"] = adv.extract_emoji(sentence)["overview"]["num_emoji"]
        
        for emphatic in [" for sure"]: 
            s["amplifiers_048"] += sentence.count(emphatic)
        if sentence.startswith("for sure"): # AB: Catch cases of sentence-initial "for sure" that have been excluded through the insertion of spaces above
            s["amplifiers_048"] += 1

        for hedge in [" at about ", " something like ", " more or less", " kinda ", " sorta ", " almost ", " maybe "]:
            s["hedges_047"] += sentence.count(hedge)
        if sentence.startswith("at about ") or sentence.startswith("something like ") or sentence.startswith("more or less") or sentence.startswith("kinda ") or sentence.startswith("sorta "):
        # AB: Catch sentence-initial cases excluded by spaces above
            s["hedges_047"] += 1

        for conjunct in ["on the contrary", "on the other hand", "for example", "for instance", "by contrast", "by comparison", "in comparison",
                         "in contrast", "in particular", "in addition", "in conclusion", "in consequence", "in sum", "in summary", "in any event",
                         "in any case", "in other words", "as a result", "as a consequence"]:
            s["conjuncts_045"] += sentence.count(conjunct) # AB: I have not inserted any spaces above because the likelihood of false positives in all cases seems very low

        for conjunct in ["that is,", "else,", "altogether,", "rather,"]: #Will only catch sentences with proper punctuation but it's a start
            if sentence.startswith(conjunct):
                s["conjuncts_045"] += 1

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
        
        for emoticon in [":-)", ":)", ";-)", ":-P", ";-P", ":-p", ";-p", ":-(", ";-(", ":-O", "^^", "-.-", ":-$", ":-\\", ":-/", ":-|", ";-/", ";-\\",
                        ":-[", ":-]", ":-§", "owo", "*.*", ";)", ":P", ":p", ";P", ";p", ":(", ";(", ":O", ":o", ":|", ";/", ";\\", ":[", ":]", ":§"]:
            s["emoticons_207"] += sentence.count(emoticon)
            ## here: enter command to replace emojis. Otherwise they will be split and the letter will most likely be tagged as NOUN, which throws off some of the functions below.
            ### AB: This is not the place to do it, as whatever we do here will not persist into what is being piped to the tokenizer.
            ### AB: I added the operation to the clean_sentence() function

        words = sentence_dict["body"].split() #split into words for single word functions below
        
        sum_wordlen = 0
        for word in words:
            word = re.sub(r'[^\w\s]','', word)
            wordlen = len(word)
            sum_wordlen = sum_wordlen + wordlen
        s["wordlength_044"] = (sum_wordlen/len(words)) 
        # this works fine but the output might look weird since the words are here separated differently than they are by the tagger
        
        for i in range(len(words)):
            if lengthening(words[i].lower()):
                s["lengthening_206"] += 1
            if words[i].lower() in ["op", "subreddit", "sub", "subreddits", "upvoted", "posted", "repost", "thread", "upvotes", "upvote", "upvoting"
                    "reddit", "redditor", "redditors", "post", "posts", "mod", "mods", "flair", "karma", "downmod", "downmodding", "downvote", 
                    "downvoting", "modding"]:
                s["reddit_vocab_216"] += 1 
            
            if words[i].lower().startswith("u/"):
                s["link_202"] += 1 
                words[i] = "username" ## added these replacement statements to ease the later processing - and also for anonymisation (HM)
                
            if words[i].lower().startswith("r/"):
                s["link_202"] += 1 
                words[i] = "subredditname" ## added these replacement statements to ease the later processing (HM)

            if "http" in words[i].lower() or "www" in words[i].lower():
                s["interlink_203"] += 1 
                words[i] = "url" ## added these replacement statements to ease the later processing (HM)

            if not i == 0:
                if words[i].isupper() and not words[i]=="I":
                    s["caps_204"] += 1
            else:
                if words[i].isupper() and not (words[i] in ["A", "I"]): 
                    s["caps_204"] += 1  

def clean_sentence(sentence):
    '''Takes a sentence and returns it in all lowercase, with punctuation removed, and emojis removed.'''
    sentence = str(sentence).strip(string.punctuation).lower()
    for emoticon in [":-)", ":)", ";-)", ":-P", ";-P", ":-p", ";-p", ":-(", ";-(", ":-O", "^^", "-.-", ":-$", ":-\\", ":-/", ":-|", ";-/", ";-\\",
                        ":-[", ":-]", ":-§", "owo", "*.*", ";)", ":P", ":p", ";P", ";p", ":(", ";(", ":O", ":o", ":|", ";/", ";\\", ":[", ":]", ":§"]:
        sentence = sentence.replace(emoticon, "")
    ## emoticons already counted (but not removed) in the analyse_sentence function
    ## emojis already counted (but not removed) in the analyse_sentence function
    ## links and URLs counted AND removed in the analyse_sentence function
    return sentence    

 
# The function below is the previous NLTK tagger. I have hashed it out so we can revert to it in the event of any issues. (GK)
# To use the nltk tagger: import nltk and (first time only) nltk.download("tagsets")
# Can also look up nltk tags with (ex): nltk.help.upenn_tagset('NNS')

#def tag_sentence(sentence):
#    '''Takes a sentence, cleans it with clean_sentence, and tags it using the NLTK averaged_perceptron_tagger. 
#    Adds a look ahead/behind buffer of three items of type ("X", "X") to prevent negative indices and IndexErrors
#    Returns a list of tuples of (word, pos_tag).'''
#    cleaned_sentence = clean_sentence(sentence)
#    tokens = nltk.word_tokenize(cleaned_sentence)
#    tagged_sentence = nltk.pos_tag(tokens)
#    empty_look = [("X", "X"), ("X", "X"), ("X", "X")]
#    tagged_sentence = empty_look + tagged_sentence + empty_look 
#    return tagged_sentence

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
s = {"vpast_001": 0, "vpresperfect_002a": 0, "vpastperfect_002b": 0, "vpresent_003": 0, "advplace_004": 0, "advtime_position_005a": 0, "advtime_durfreq_005b": 0, 
     "profirpers_006": 0, "prosecpers_007": 0,"prothirdper_008": 0, "proit_009": 0, "prodemons_010": 0, "proindef_011": 0, 
     "pverbdo_012": 0, "whquest_013": 0, "nominalis_014": 0, "gerund_015": 0,"nouns_016": 0, "passagentl_017": 0, "passby_018": 0, 
     "mainvbe_019": 0, "exthere_020": 0, "thatvcom_021": 0, "thatacom_022": 0, "whclause_023": 0, "vinfinitive_024": 0, 
     "vpresentpart_025": 0, "vpastpart_026": 0, "vpastwhiz_027": 0, "vpresentwhiz_028":0, "thatresub_029": 0, "thatreobj_030": 0, 
     "whresub_031": 0, "whreobj_032": 0, "whrepied_033": 0, "sentencere_034": 0, "advsubcause_035": 0, "advsubconc_036": 0, 
     "advsubcond_037": 0, "advsubother_038": 0, "prepositions_039": 0, "adjattr_040": 0, "adjpred_041": 0, "adverbs_042": 0, 
     "ttratio_043": 0, "wordlength_044": 0, "conjuncts_045": 0, "downtoners_046": 0, "hedges_047": 0, "amplifiers_048": 0, 
     "discpart_050": 0, "demonstr_051": 0, "modalsposs_052": 0, "modalsness_053": 0, "modalspred_054": 0, 
     "vpublic_055": 0, "vprivate_056": 0, "vsuasive_057": 0, "vseemappear_058": 0, "contractions_059": 0, "thatdel_060": 0, 
     "strandprep_061": 0, "vsplitinf_062": 0, "vsplitaux_063": 0, "coordphras_064": 0, "coordnonp_065": 0, "negsyn_066": 0, 
     "negana_067": 0, "hashtag_201": 0, "link_202": 0, "interlink_203": 0, "caps_204": 0, "vimperative_205": 0, "lengthening_206":0,
     "emoticons_207":0, "question_208": 0, "exclamation_209": 0, "lenchar_210": 0, "lenword_211": 0, "comparatives_syn_212": 0, 
     "superlatives_syn_213": 0, "comparatives_ana_214": 0, "superlatives_ana_215":0, "reddit_vocab_216":0, "vprogressive_217": 0,
     "emojis_218":0}
placelist = ["aboard", "above", "abroad", "across", "ahead", "alongside", "anywhere", 
                 "ashore", "astern", "away", "behind", "below", "beneath", "between", "beyond",
                 "beside", "down", "downhill", "downstairs", "downstream", "downwind", "east",
                 "eastward", "eastwards", "elsewhere", "everywhere", "far", "here", "hereabouts",
                 "indoors", "inland", "inshore", "inside", "locally", "near", "nearby", "north",
                 "northward", "northwards", "nowhere", "offshore", "opposite", "outdoors", "outside", 
                 "overboard", "overhead", "overland", "overseas", "somewhere", "south", "southward", "southwards",
                 "there", "thereabouts", "through", "throughout", "under", "underfoot", "underground", "underneath",
                 "uphill", "upstairs", "upstream", "west", "westward", "westwards", "within"] 
timepoints = ["afterwards", "again", "already", "anymore", "before", "currently", "earlier", "early", "eventually",
              "formerly", "finally", 
                "immediately", "initially", "instantly", "late", "lately", "later", "momentarily", 
                "now", "nowadays",  "originally", "presently", "previously", "promptly", "recently", 
                "shortly", "simultaneously", "soon", "subsequently", "today", "tomorrow", "tonight",
                "yesterday"]
timedurfreq = ["always", "annually", "ceaselessly", "commonly", "constantly", "continually", "continuously", "customarily",
               "daily", "eternally", "evermore", "endlessly", "forever", "fortnightly", "frequently", "habitually", "hourly", "infrequently", "intermittently",
               "irregularly", "invariably", "monthly", "never", "occasionally", "often", "oftentimes", "once", "periodically",
               "perpetually", "persistently", "rarely", "repeatedly", "routinely", "seldom", "sometimes",
               "twice", "unceasingly", "usually","weekly", "yearly"]
firstpersonlist = ["i", "me", "we", "us", "my", "our", "myself", "ourselves"]
secondpersonlist = ["you", "yourself", "your", "yourselves"]
thirdpersonlist = ["she", "he", "they", "her", "him", "them", "his", "their", "himself","herself", "themselves"]
indefpronounlist = ["anybody", "anyone", "anything", "everybody", "everyone", "everything", "nobody", "none", "nothing", "nowhere", "somebody", "someone", "something"]
conjunctslist = ["alternatively", "altogether", "consequently", "conversely", "eg", "e.g.", "else", "furthermore",
                 "hence", "however", "ie", "i.e.", "instead", "likewise", "moreover", "namely", "nevertheless",
                 "nonetheless", "notwithstanding", "otherwise", "rather", "similarly", "therefore", "thus", "viz"]
conjunctsmultilist = ["on the contrary", "on the other hand", "for example", "for instance", "by contrast", "by comparison", 
                      "in comparison", "in contrast", "in particular", "in addition", "in conclusion", "in consequence", "in sum",
                      "in summary", "in any event", "in any case", "in other words", "as a result", "as a consequence"]
punct_final = [".", "!", "?", ":", ";"] # here, Biber also includes the long dash -- , but I am unsure how this would be rendered
belist = ["be", "am", "are", "is", "was", "were", "been", "being", "'m", "'re",] # I have added the contracted forms of am and are (AB)
havelist = ["have", "has", "had", "having"]
dolist = ["do", "does", "doing", "did", "done"]
subjpro = ["i", "we", "he", "she", "they"]
posspro = ["my", "our", "your", "his", "their", "its"]
DEM = ["that", "this", "these", "those"]
WHP = ["who", "whom", "whose", "which"]
WHO = ["what", "where", "when", "how", "whether", "why", "whoever", "whomever", "whichever", 
       "whenever", "whatever", "however"] 
discpart = ["well", "now", "anyway", "anyhow", "anyways", "though"]
QUAN = ["each", "all", "every", "many", "much", "few", "several", "some", "any"]
QUANPRO = ["everybody", "somebody", "anybody", "everyone", "someone", "anyone", "everything", "something", "anything", "anywhere"]
ALLP = [".", "!", "?", ":", ";", ","]  # here, Biber also includes the long dash -- , but I am unsure how this would be rendered 
downtonerlist = ["almost", "barely", "hardly", "merely", "mildly", "nearly", "only", "partially", "partly", "practically", "scarcely", "slightly", "somewhat"]
                # some others that could be included: a little, a bit, a tad (HM)
amplifierlist = ["absolutely", "altogether", "completely", "definitely", "enormously", "entirely", "extremely", "fully", "greatly", "highly", 
                 "intensely", "perfectly", "strongly", "thoroughly", "totally", "utterly", "very"]
asktelllist = ["ask", "asked", "asking", "asks", "tell", "telling", "tells", "told"]
titlelist = ["mr", "ms", "mrs", "prof", "professor", "dr", "sir"]
otheradvsublist = ["since", "while", "whilst", "whereupon", "whereas", "whereby", "such that", "so that", "such that", "inasmuch as", "forasmuch as", "insofar as", "insomuch as", "as long as", "as soon as"]
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


#POS-functions
def analyze_verb(index, tagged_sentence, features_dict):
    '''Takes the index position of the current word, a tagged sentence, and dictionary of all possible tags and updates relevant keys: "vpast_001", "vpresperfect_002a", "vpastperfect_002b", "vpresent_003", 
    "pverbdo_012", "passagentl_017", "passby_018", "mainvbe_019", "whclause_023", "vinfinitive_024", "vpresentpart_025", "vpastpart_026", "vpastwhiz_027", "vpresentwhiz_028",
    "vpublic_055", "vprivate_056", "vsuasive_057", "vseemappear_058", "contractions_059", 
    "thatdel_060", "vsplitinf_062", "vsplitaux_063", "vimperative_205".'''
      
    word_tuple = tagged_sentence[index]
    if word_tuple[1] == "VBD":
        features_dict["vpast_001"] += 1
    elif word_tuple[1] == "VB":
        if tagged_sentence[index-1][1] == "X" or tagged_sentence[index-1][0] == ",": 
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
        if (tagged_sentence[index-1][1] == "X" or tagged_sentence[index-1][0] in ALLP) and tagged_sentence[index+1][1] in ["IN", "DT", "RB", "WP","PRP", "WRB"]:
            features_dict["vpresentpart_025"] += 1
        elif tagged_sentence[index-1][1] == "NN":
            features_dict["vpresentwhiz_028"] += 1 
        elif tagged_sentence[index-1][0] in belist:
            features_dict["vprogressive_217"] += 1
        elif (tagged_sentence[index-2][0] in belist) and (tagged_sentence[index-1][1] == "RB"):
            features_dict["vprogressive_217"] += 1  
            features_dict["vsplitaux_063"] += 1
    elif word_tuple[1] == "VBN":
        if (tagged_sentence[index-1][1] == "X" or tagged_sentence[index-1][0] in ALLP):
            if tagged_sentence[index+1][1] in ["IN", "RB", "TO"]: # Biber (1988:233) notes for both that "these forms were edited by hand."
                features_dict["vpastpart_026"] += 1 ## this one seems accurate enough to me (HM)
        elif tagged_sentence[index-1][1] in ["NN", "NNP"] or tagged_sentence[index-1][0] in QUANPRO:
            if tagged_sentence[index+1][1] in ["IN", "RBR", "RB", "RBS"] or tagged_sentence[index+1][0] in belist:
                features_dict["vpastwhiz_027"] += 1 

    elif word_tuple[1] in ["VBP","VBZ"]:
        features_dict["vpresent_003"] += 1
    if word_tuple[0].startswith("seem") or word_tuple[0].startswith("appear"):
        features_dict["vseemappear_058"] += 1
        
    if word_tuple[0] in ["had", "'d"]: 
        move_on = True
        insert_adv = False
        x = index
        while move_on:
            x += 1
            if tagged_sentence[x][1] == "VBN":
                move_on = False
                features_dict["vpastperfect_002b"] += 1
                if insert_adv:
                    features_dict["vsplitaux_063"] += 1
            elif tagged_sentence[x][1].startswith("R") and tagged_sentence[x][0] not in ["n't", "not"]:
                insert_adv = True
            elif tagged_sentence[x][1].startswith("N") or tagged_sentence[x][1].startswith("P"):
                move_on = True 
                # HM: as intended by Biber (p. 223) we here also count questions with the word order HAD + NOUN/PRONOUN + VBN
                # HM: this does, however, not catch all questions using the past perfect (e.g. does not count "had many people been to the store?" due to inserted adjective)
            else: 
                move_on =  False 

    elif word_tuple[0] in ["have", "'ve", "has"]: 
        move_on = True
        insert_adv = False
        x = index
        while move_on: 
            # These while-statements are an attempt to get around the question of how much intervening material to allow by instead setting 
            # conditions for when to stop looking on (either because an instance of the feature has been found or an impermissible context has been encountered) (AB)
            x += 1
            if tagged_sentence[x][1] == "VBN":
                move_on = False
                features_dict["vpresperfect_002a"] += 1
                if insert_adv:
                    features_dict["vsplitaux_063"] += 1
            elif tagged_sentence[x][1].startswith("R") and tagged_sentence[x][0] not in ["n't", "not"]:
                insert_adv = True
            elif tagged_sentence[x][1].startswith("N") or tagged_sentence[x][1].startswith("P"): 
                # HM: as intended by Biber (p. 223) we here also count questions with the word order HAVE + NOUN/PRONOUN + VBN
                # HM: this does, however, not catch all questions using the present perfect (e.g. does not count "have many people been to the store?" due to inserted adjective)
                move_on = True
            else: 
                move_on = False
                
    elif word_tuple[0] in belist:
        if tagged_sentence[index+1][1] in ["DT", "PRP$", "JJ", "JJR", "JJS", "NN", "NNS", "NNP"]:
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
                    features_dict["amplifiers_048"] += 1
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

    if word_tuple[0] in publiclist:
        features_dict["vpublic_055"] += 1
        if tagged_sentence[index + 1][0] in ["this", "these", "that", "those", "I", "we", "he", "she", "they"]:
            features_dict["thatdel_060"] += 1
        elif tagged_sentence[index + 1][1].startswith("NN") or tagged_sentence[index + 1][1].startswith("PR"):
            if tagged_sentence[index + 2][1].startswith("V") or tagged_sentence[index + 2][1] == "MD":
                features_dict["thatdel_060"] += 1
        elif tagged_sentence[index + 1][1] in ["JJ", "JJR", "JJS", "RB", "RBR", "RBS", "PRP$", "DT"]:
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
    

def analyze_modal(index, tagged_sentence, features_dict):
    '''Takes the index position of the current word, a tagged sentence, and dictionary of all possible tags and updates relevant keys: 
    "modalsposs_052", "modalsness_053", "modalspred_054", "contractions_059", "vsplitaux_063".'''
    word_tuple = tagged_sentence[index]
    if word_tuple[0] in ["can","may","might","could"]:
        features_dict["modalsposs_052"] += 1
    elif word_tuple[0] in ["ought","should","must"]:
        features_dict["modalsness_053"] += 1
    elif word_tuple[0] in ["will","would","shall","'ll","'d"]: 
        features_dict["modalspred_054"] += 1
    if word_tuple[0].startswith("'"):
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
    
def analyze_adverb(index, tagged_sentence, features_dict):
    '''Takes the index position of the current word, a tagged sentence, and dictionary of all possible tags and updates relevant keys:
    "advplace_004", "advtime_005", "adverbs_042", "conjuncts_045",
    "downtoners_046", "hedges_047", "amplifiers_048", "discpart_050", "contractions_059", "negana_067".'''
    features_dict["adverbs_042"] += 1
    word_tuple = tagged_sentence[index]
    if word_tuple[0] == "not":
        features_dict["negana_067"] += 1
    if word_tuple[0] == "n't":
        features_dict["negana_067"] += 1
        features_dict["contractions_059"] += 1
    elif word_tuple[0] in placelist:
        features_dict["advplace_004"] += 1
    elif word_tuple[0] in timepoints:
        features_dict["advtime_position_005a"] += 1
    elif word_tuple[0] in timedurfreq:
        features_dict["advtime_durfreq_005b"] += 1
    elif word_tuple[0] in downtonerlist:
        features_dict["downtoners_046"] += 1
    elif word_tuple[0] in amplifierlist:
        features_dict["amplifiers_048"] += 1 
    elif word_tuple[0] in conjunctslist:
        features_dict["conjuncts_045"] += 1
    elif index == 0 and word_tuple[0] in discpart:
        features_dict["discpart_050"] += 1
 
def analyze_adjective(index, tagged_sentence, features_dict):
    '''Takes the index position of the current word, a tagged sentence, and dictionary of all possible tags and updates relevant keys:
    "adjattr_040", "adjpred_041", "comparatives_212", "superlatives_213".'''
    if tagged_sentence[index][1] == "JJR":
        features_dict["comparatives_syn_212"] += 1
    elif tagged_sentence[index][1] == "JJS":
        features_dict["superlatives_syn_213"] += 1
    if tagged_sentence[index-1][0] == "more":
        features_dict["comparatives_ana_214"] += 1
    elif tagged_sentence[index-1][0] == "most":
        features_dict["superlatives_ana_215"] += 1
        
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
      
def analyze_preposition(index, tagged_sentence, features_dict):
    '''Takes the index position of the current word, a tagged sentence, and dictionary of all possible tags and updates relevant keys: 
    "advsubcause_035", "advsubconc_036", "advsubcond_037", "advsubother_038", "prepositions_039", 
    "conjuncts_045", "hedges_047", "strandprep_061".'''
    word_tuple = tagged_sentence[index]
    if not word_tuple[0] in ["because", "unless", "whilst", "while", "though", "tho", "although", "that", "since", "whereupon", "whereas", "whereby"] + timepoints + timedurfreq + placelist: 
        features_dict["prepositions_039"] += 1 
    if word_tuple[0] in ["because", "becuase", "beacuse", "cause", "'cause", "cos", "'cos", "coz", "'coz", "caus", "'caus", "cuz", "'cuz", "bcoz", "bcuz", "bcos", "bcause", "bcaus"] and tagged_sentence[index+1][0] != "of":
        features_dict["advsubcause_035"] += 1 
        # AB: I decided against a separate feature for "because of" since it goes into "prepositions_039".
        # HM: I don't understand what this means. Biber (1988: 236-237) does not list "because of" as a preposition (even though it is an obvious contender),
        #     and it is purposefully excluded in the list above for "prepositions_039". Right now we are not counting "because of" at all, are we?
    elif word_tuple[0] == "although" or word_tuple[0] == "though" or word_tuple[0] == "tho":
        features_dict["advsubconc_036"] += 1 
        
    elif word_tuple[0] == "that" and tagged_sentence[index-1][0] in ["such", "so"]:
        features_dict["advsubother_038"] += 1 

    elif word_tuple[0] == "of" and tagged_sentence[index-1][0] in ["kind", "sort"] and not tagged_sentence[index-2][1] in ["JJ", "JJR", "JJS", "DT", "PRP$"]:
        if not tagged_sentence[index-2][0] in ["what", "whatever", "whichever"]:
            features_dict["hedges_047"] += 1

    if tagged_sentence[index+1][0] in ALLP or tagged_sentence[index+1][1] == "X":
        features_dict["strandprep_061"] += 1


def analyze_noun(index, tagged_sentence, features_dict):
    '''Takes the index position of the current word, a tagged sentence, and dictionary of all possible tags and updates relevant keys:
    "nominalis_014", "gerund_015", "nouns_016".'''
    word_tuple = tagged_sentence[index]

    if word_tuple[0].endswith("ing") or word_tuple[0].endswith("ings"):
        if word_tuple[1] not in notgerundlist:
            features_dict["gerund_015"] += 1
    elif word_tuple[0].endswith("tions") or word_tuple[0].endswith("tion") or word_tuple[0].endswith("ments") or word_tuple[0].endswith("ment") or word_tuple[0].endswith("ness") or word_tuple[0].endswith("ity") or word_tuple[0].endswith("nesses") or word_tuple[0].endswith("ities"):
        features_dict["nominalis_014"] += 1
    else: 
        features_dict["nouns_016"] += 1
        
def analyze_pronoun(index, tagged_sentence, features_dict):
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

    if word_tuple[0] in DEM:
        if tagged_sentence[index+1][0] == "and":
            features_dict["prodemons_010"] += 1
        elif tagged_sentence[index+1][1] in ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "MD", "WP"]:
            features_dict["prodemons_010"] += 1
        elif index == (len(tagged_sentence)-1):
            features_dict["prodemons_010"] += 1
    elif word_tuple[0] == "that" and tagged_sentence[index+1][0] == "'s":
        features_dict["prodemons_010"] += 1

def analyze_conjunction(index, tagged_sentence, features_dict):
    '''Takes the index position of the current word, a tagged sentence, and dictionary of all possible tags and updates relevant keys:
    "hedges_047", "coordphras_064", "coordnonp_065".'''
    word_tuple = tagged_sentence[index]

    if word_tuple[0] == "and": 
        if tagged_sentence[index-1][1].startswith("N") and tagged_sentence[index+1][1].startswith("N"):
            features_dict["coordphras_064"] += 1
        elif tagged_sentence[index-1][1].startswith("RB") and tagged_sentence[index+1][1].startswith("RB"):
            features_dict["coordphras_064"] += 1
        elif tagged_sentence[index-1][1].startswith("JJ") and tagged_sentence[index+1][1].startswith("JJ"):
            features_dict["coordphras_064"] += 1
        elif tagged_sentence[index-1][1].startswith("VB") and tagged_sentence[index+1][1].startswith("VB"):
            features_dict["coordphras_064"] += 1
        elif tagged_sentence[index-1][0] == ",":
            if tagged_sentence[index+1][0] in ["it", "so", "you", "then"]:
                features_dict["coordnonp_065"] += 1
            elif tagged_sentence[index+1][1] in subjpro or tagged_sentence[index+1][1] in DEM:
                    features_dict["coordnonp_065"] += 1                            
            elif tagged_sentence[index+1][0] == "there" and tagged_sentence[index+2][0] in belist:
                features_dict["coordnonp_065"] += 1
        elif tagged_sentence[index-1][0] in punct_final: 
            features_dict["coordnonp_065"] += 1
        elif tagged_sentence[index+1][0] in WHP or tagged_sentence[index+1][0] in WHO or tagged_sentence[index+1][0] in discpart:
            features_dict["coordnonp_065"] += 1
        elif tagged_sentence[index+1][0] in ["because", "although", "though", "if", "unless",] or tagged_sentence[index+1][0] in otheradvsublist: # added the otheradvsublist for this particular feature (GK)
            features_dict["coordnonp_065"] += 1
        elif tagged_sentence[index+1][0] in conjunctslist:
            features_dict["coordnonp_065"] += 1


    if word_tuple[0] == "and" and tagged_sentence[index+1][0] in WHP or tagged_sentence[index+1][0] in WHO:
        features_dict["coordnonp_065"] += 1 
    elif word_tuple[0] == "and" and tagged_sentence[index+1][0] in ["because", "although", "though", "if", "unless", "since", "while", "whilst", "whereas", "whereby"]:
        features_dict["coordnonp_065"] += 1 
    elif word_tuple[0] == "and" and tagged_sentence[index+1][0] in discpart:
        features_dict["coordnonp_065"] += 1
    elif word_tuple[0] == "and" and tagged_sentence[index+1][0] in conjunctslist:
        features_dict["coordnonp_065"] += 1


def analyze_determiner(index, tagged_sentence, features_dict):
    '''Takes the index position of the current word, a tagged sentence, and dictionary of all possible tags and updates relevant keys:
    "demonstr_051", "negsyn_066".'''
    word_tuple = tagged_sentence[index]

    if word_tuple[0] in DEM:
        features_dict["demonstr_051"] += 1
    elif word_tuple[0] == "neither" or word_tuple[0] == "nor":
        features_dict["negsyn_066"] += 1
    elif word_tuple[0] == "no":
        if tagged_sentence[index+1][1].startswith("NN") or tagged_sentence[index+1][1].startswith("JJ"):
            features_dict["negsyn_066"] += 1
        elif tagged_sentence[index+1][0] in QUAN:
            features_dict["negsyn_066"] += 1

def analyze_wh_word(index, tagged_sentence, features_dict):
    # Check: Ft 32 (Biber's way of finding this seems like it could be optimized)
    # Check: Ft 22 (catches unintended phrases)
    '''Takes the index position of the current word, a tagged sentence, and dictionary of all possible tags and updates relevant keys:
    "whquest_013", "thatvcom_021", "thatacom_022", "whrepied_033", "sentencere_034", "thatresub_029", "thatreobj_030", 
    "whresub_031", "whreobj_032".'''
    word_tuple = tagged_sentence[index]
    
    #21 that verb complements (e.g., / said that he went)  
    if tagged_sentence[index][0] == "that":
    # (a) and\nor\but\or\aho\ALL-P + that + DET/PRO/there/plural noun/proper noun/TITLE (these are i/za£-clauses in clause-initial positions)
        if tagged_sentence[index-1][0] in ALLP or tagged_sentence[index-1][0] in ["and", "nor", "but", "or", "who"]:
            if tagged_sentence[index+1][1].startswith("D") or tagged_sentence[index+1][1].startswith("PR") or tagged_sentence[index+1][0] == "there" or tagged_sentence[index+1][1].startswith("NNP") or tagged_sentence[index+1][1].startswith("NNS") or tagged_sentence[index+1][0] in titlelist:
                features_dict["thatvcom_021"] += 1
    # (b) PUB/PRV/SUA/SEEM/APPEAR + that + xxx (where xxx is NOT: V/AUX/CL-P/and)
        elif (tagged_sentence[index-1][0] in suasivelist) or (tagged_sentence[index-1][0] in privatelist) or (tagged_sentence[index-1][0] in publiclist):
            if not tagged_sentence[index+1][1].startswith("V"):
                if tagged_sentence[index+1][0] not in [ALLP, "and"]:
                    features_dict["thatvcom_021"] += 1
        elif (tagged_sentence[index-1][0].startswith("seem")) or (tagged_sentence[index-1][0].startswith("appear")):
            if not tagged_sentence[index+1][1].startswith("V"):
                if tagged_sentence[index+1][0] not in [ALLP, "and"]:
                    features_dict["thatvcom_021"] += 1            
    # (c) PUB/PRV/SUA + PREP + xxx + N + that (where xxx is any number of words, but NOT = N)
    #     (This algorithm allows an intervening prepositional phrase between a verb and its complement.)  
    ### HM: this is not implemented at the moment, since it seems very complicated and rather marginal. My guess is that we need to trash this whole feature anyway...
    
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
            
        if tagged_sentence[index-1][1].startswith("J"):
            features_dict["thatacom_022"] += 1 
                
    else:
        if word_tuple[0] in WHP: # WHP = ["who", "whom", "whose", "which"]
            if tagged_sentence[index-1][1] == "IN":
                features_dict["whrepied_033"] += 1 #pied-piping relative clauses (e.g., the manner in which he was told) PREP + WHP in relative clauses

            if word_tuple[0] == "which" and tagged_sentence[index-1][0] == ",": #34. sentence relatives (e.g., Bob likes fried mangoes, which is the most disgusting thing I've ever heard of) Biber: (These forms are edited by hand to exclude non-restrictive relative clauses.)
                features_dict["sentencere_034"] += 1

            #31. WH relative clauses on subject position (e.g., the man who likes popcorn) xxx + yyy + N + WHP + (ADV) + AUX/V (where xxx is NOT any form of the verbs ASK or TELL; to exclude indirect WH questions like Tom asked the man who went to the store)
            ##AB: Added the condition for ASK and TELL
            if tagged_sentence[index-1][1].startswith("N") and tagged_sentence[index-2][0] not in ["tell", "tells", "told", "telling", "ask", "asks", "asked", "asking"]:
                if tagged_sentence[index+1][1].startswith("R"):
                    if (tagged_sentence[index+2][1].startswith("V") or tagged_sentence[index+2][1].startswith("MD")):
                        features_dict["whresub_031"] += 1

                elif(tagged_sentence[index+1][1].startswith("V") or tagged_sentence[index+1][1].startswith("MD")):
                    features_dict["whresub_031"] += 1
        
            #32. WH relative clauses on object positions (e.g., the man who Sally likes) xxx + yyy + N + WHP + zzz (where xxx is NOT any form of the verbs ASK or TELL, to exclude indirect WH questions, and zzz is not ADV, AUX or V, to exclude relativization on subject position)
            #right now, only wh-words at least two words from the front and 2 from the end will be caught here (KM) -> won't catch ex "boys who Sally likes" (is that grammatically acceptable??) also won't catch passives, ex "the men who are liked by Sally" (kind of awkward tbh) (KM)
            #AB: The two words from the end is not a problem, since an object RC has, by definition a minimum of two items after the relativizer (subject and verb)
            #AB: I am hard-put to find a more felicitous example than "boys who Sally likes" that would pose a problem with the 2 words at the beginning either, so happy to disregard the issue.
            #AB: Edit: Does the problem at beginning or end not disappear entirely with out added "x"es?
            #AB: The example "the men who are liked by Sally" is an RC with the relatizive in subject gap and as such is appropriately captured under 031.
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
       


def analyze_there(index, tagged_sentence, features_dict):
    '''Takes the index position of the current word, a tagged sentence, and dictionary of all possible tags and updates relevant keys: 
    "exthere_020".'''
    if tagged_sentence[index][1] == "EX":
        features_dict["exthere_020"] += 1 
        
    
def analyze_particle(index, tagged_sentence, features_dict):
    '''Takes the index position of the current word, a tagged sentence, and dictionary of all possible tags and updates relevant keys: 
    "discpart_050".'''
    word_tuple = tagged_sentence[index]
    if index == 0 and word_tuple[0] in discpart:
        features_dict["discpart_050"] += 1
    else:
        pass
    
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
    
    r = open(os.path.join(dirname, 'results', preprocessed_file, "_r"), "w")
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


def process_sent(sent, feat):
    tagged_sentence = tag_sentence(sent)
    features_dict = s.copy()
    POS_tagger(tagged_sentence, features_dict)
    return features_dict[feat]

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

# for file in all_files:
#     MDA_analyzer(file)

print(timedelta(seconds=time.time() - start_time))

    
