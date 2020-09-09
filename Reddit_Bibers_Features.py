### these functions:
### - take one of the following items as input (presuming cleaned, lowercase data):
###   - a list with each word as a new item, without PoS-tags (untagged_list)
###   - a list with each word as a new item together with its PoS-tag (tagged_list)
###   - a string containing the whole sentence, each word with its PoS-tag (tagged_string)
### - identify one of Biber's original 67 features
### - return the count of the occurances the feature 

### Many of these functions rely on punctuation to identify strings at the 
### beginning of a sentence. However, when we separate the comments into
### individual sentences, these pieces of punctuation will no longer be at the
### beginning of each sentence. Any solutions?

import re
import string

## function for feature 1: past tense
## DONE!
def feature_01(tagged_list):
    """This function takes a list of words with PoS tags as input and returns the number of items
    that are a verb in the past tense."""
    counter = 0
    for item in tagged_list:
        if item == r"\b\w_+_VBD\b" or item == r"\b\w{5,20}ed_\w+\b":
            counter = counter + 1
        else:
            pass
    return(counter)

## function for feature 2: verbs in the perfect aspect
## DONE!!
def feature_02(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the number of 
    perfect aspect forms."""
    string1 = r"\b[have|has|'ve|'s]_\w+\s\w+_VBD\b"
    string2 = r"\b[have|has|'ve|'s]_\w+\s\w+_RB\s\w+_VBD\b"
    string3 = r"\b[have|has|'ve|'s]_\w+\s\w+_RB\s\w+_RB\s\w+_VBD\b"
    string4 = r"\b[have|has]_\w+\s\w+_[NN|NNS|NNP|NNPS|PRP|PRP$]\s\w+_VBD\b"
    matches1 = re.findall(string1, tagged_string)
    matches2 = re.findall(string2, tagged_string)
    matches3 = re.findall(string3, tagged_string)
    matches4 = re.findall(string4, tagged_string)
    counter = len(matches1) + len(matches2) + len(matches3) + len(matches4)
    return(counter)

## function for feature 3: present tense
## DONE!!
def feature_03(tagged_string):
    """This function takes a list of words with PoS tags as input and returns the number of 
    verbs in the present tense (excluding infinitives)."""
    string1 = r"(?<!to)_\w+\s\w+_[VB|VBZ]\b"
    matches1 = re.findall(string1, tagged_string)
    counter = matches1
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

## function for feature 5: time adverbials
## DONE!
def feature_05(untagged_list):
    """This function takes a list of words with PoS tags as input and returns the number of items
    that are time adverbials."""
    counter = 0
    timelist = ["afterwards", "again", "earlier", "early", "eventually", "formerly",
                "immediately", "initially", "instantly", "late", "lately", "later", "momentarily", 
                "now", "nowadays", "once", "originally", "presently", "previously", "recently", 
                "shortly", "simultaneously", "soon", "subsequently", "today", "tomorrow", "tonight",
                "yesterday"]
    for item in untagged_list:
        if item in timelist:
            counter = counter + 1
        else:
            pass
    return(counter)

## function for feature 6: first person pronouns
## DONE!
def feature_06(untagged_list):
    """This function takes a list of words with PoS tags as input and returns the number of items
    that are first person pronouns."""
    counter = 0
    firstpersonlist = ["i", "me", "we", "us", "my", "our", "myself", "ourselves"]
    for item in untagged_list:
        if item in firstpersonlist:
            counter = counter + 1
        else:
            pass
    return(counter)

## function for feature 7: second person pronouns
## DONE!
def feature_07(untagged_list):
    """This function takes a list of words with PoS tags as input and returns the number of items
    that are second person pronouns."""
    counter = 0
    secondpersonlist = ["you", "yourself", "your", "yourselves"]
    for item in untagged_list:
        if item in secondpersonlist:
            counter = counter + 1
        else:
            pass
    return(counter)

## function for feature 8: third person pronouns
## DONE!
def feature_08(untagged_list):
    """This function takes a list of words with PoS tags as input and returns the number of items
    that are third person pronouns."""
    counter = 0
    thirdpersonlist = ["she", "he", "they", "her", "him", "them", "his", "their", "himself",
                       "herself", "themselves"]
    for item in untagged_list:
        if item in thirdpersonlist:
            counter = counter + 1
        else:
            pass
    return(counter)

## function for feature 9: pronoun IT
## DONE!
def feature_09(untagged_list):
    """This function takes a list of words with PoS tags as input and returns the number of items
    that are the pronoun IT."""
    counter = 0
    for item in untagged_list:
        if item == "it":
            counter = counter + 1
        else:
            pass
    return(counter)

## function for feature 10: demonstrative pronouns
## DONE!!
def feature_10(tagged_string):
    """This function takes a list of words with PoS tags as input and returns the number of items
    that are demonstrative pronouns."""
    string1 = r"\b[that|this|these|those]_\w+\s\w+_[VB|VBD|VBG|VBN|VBP|VBZ|MD|WP]"
    string2 = r"\b[that|this|these|those]_\w+\s[and|\.]"
    string3 = r"\bthat_\w+\s's"
    matches1 = re.findall(string1, tagged_string)
    matches2 = re.findall(string2, tagged_string)
    matches3 = re.findall(string3, tagged_string)
    counter = len(matches1) + len(matches2) + len(matches3)
    return(counter)

## function for feature 11: indefinite pronouns
## DONE!
def feature_11(untagged_list):
    """This function takes a list of words with PoS tags as input and returns the number of items
    that are indefinite pronouns."""
    counter = 0
    indefpronounlist = ["anybody", "anyone", "anything", "everybody", "everyone",
                        "everything", "nobody", "none", "nothing", "nowhere", "somebody", "someone", "something"]
    for item in untagged_list:
        if item in indefpronounlist:
            counter = counter + 1
        else:
            pass
    return(counter)

## function for feature 12: DO as pro-verb
## DONE!!
def feature_12(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the number of items
    that are DO used as a pro-verb."""
    string1 = r"\b[do|does|doing|did|done]_"
    string2 = r"\b[do|does|doing|did|done]_\w+\s\w+_VB"
    string3 = r"\b[do|does|doing|did|done]_\w+\s\w+_[RB|RBR|RBS]\s\w+_VB"
    string4 = r"_[.|]\s[do|does|doing|did|done]_"
    string5 = r"\b[who|whom|whose|which]_\w+\s[do|does|doing|did|done]_"
    matches1 = re.findall(string1, tagged_string)
    matches2 = re.findall(string2, tagged_string)
    matches3 = re.findall(string3, tagged_string)
    matches4 = re.findall(string4, tagged_string)
    matches5 = re.findall(string5, tagged_string)
    counter = len(matches1) - (len(matches2) + len(matches3) + len(matches4) + len(matches5))
    return(counter)

## function for feature 13: WH-questions
## DONE!!
def feature_13(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the number of items
    that are WH-questions."""
    string1 = r"\._\S+\swho_\w+\s\w+_MD"
    matches1 = re.findall(string1, tagged_string)
    counter = len(matches1)
    return(counter)

## function for feature 14: Nominalisations
## DONE!!
def feature_14(tagged_list):
    """This function takes a list of words with PoS tags as input and returns the number of items
    that are nominalisations."""
    counter = 0
    string1 = r"\w+[tions?|ments?|ness|ity|nesses|ities]_\w+"
    for item in tagged_list:
        if item == string1:
            counter = counter + 1
        else:
            pass
    return(counter)

## function for feature 15: gerunds
## DONE!!
def feature_15(tagged_list):
    """This function takes a list of words with PoS tags as input and returns the number of items
    that are gerunds (participle forms serving nominal function)."""
    counter = 0
    string1 = r"\w+ing_VBG"
    for item in tagged_list:
        if item == string1:
            counter = counter + 1
        else:
            pass
    return(counter) 
## edited manually

## function for feature 16: nouns
## DONE!
def feature_16(tagged_list):
    """This function takes a list of words with PoS tags as input and returns the number of items
    that are nouns (excluding nominalisations)."""
    counter = 0
    string1 = r"\b\w+_NNS?\b"
    string2 = r"\b\w+[tions?|ments?|ness|ity|nesses|ities]_\w+\b"
    for item in tagged_list:
        if item == string1 and not item == string2:
            counter = counter + 1
        else:
            pass
        return(counter)    

## function for feature 17: agentless passives
## DONE!!
def feature_17(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the 
    number of agentles passives within the string."""
    string1 = r"\b[be|am|are|is|was|were|been]_V[B|BD|BG|BN|BP|BZ]\s\w+_VBN\s(?!by_)"
    string2 = r"\b[be|am|are|is|was|were|been]_V[B|BD|BG|BN|BP|BZ]\s\w+_[RB|RBR|RBS]\s\w+_VBN\s(?!by_)"
    string3 = r"\b[be|am|are|is|was|were|been]_V[B|BD|BG|BN|BP|BZ]\s\w+_[RB|RBR|RBS]\s\w+_[RB|RBR|RBS]\s\w+_VBN\s(?!by_)"
    string4 = r"\b[be|am|are|is|was|were|been]_V[B|BD|BG|BN|BP|BZ]\s\w+_[NN|NNS|NNP|NNPS|PRP|PRP$]\s\w+_VBN\s(?!by_)"
    matches1 = re.findall(string1, tagged_string)
    matches2 = re.findall(string2, tagged_string)
    matches3 = re.findall(string3, tagged_string)
    matches4 = re.findall(string4, tagged_string)
    counter = len(matches1) + len(matches2) + len(matches3) + len(matches4)
    return(counter)    

## function for feature 18: BY passives
## DONE!!
def feature_18(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the 
    number of BY-passives within the string."""
    string1 = r"\b[be|am|are|is|was|were|been]_V[B|BD|BG|BN|BP|BZ]\s\w+_VBN\sby_"
    string2 = r"\b[be|am|are|is|was|were|been]_V[B|BD|BG|BN|BP|BZ]\s\w+_[RB|RBR|RBS]\s\w+_VBN\sby_"
    string3 = r"\b[be|am|are|is|was|were|been]_V[B|BD|BG|BN|BP|BZ]\s\w+_[RB|RBR|RBS]\s\w+_[RB|RBR|RBS]\s\w+_VBN\sby_"
    string4 = r"\b[be|am|are|is|was|were|been]_V[B|BD|BG|BN|BP|BZ]\s\w+_[NN|NNS|NNP|NNPS|PRP|PRP$]\s\w+_VBN\sby_"
    matches1 = re.findall(string1, tagged_string)
    matches2 = re.findall(string2, tagged_string)
    matches3 = re.findall(string3, tagged_string)
    matches4 = re.findall(string4, tagged_string)
    counter = len(matches1) + len(matches2) + len(matches3) + len(matches4)
    return(counter)

## function for feature 19: BE as main verb
## DONE!!
def feature_19(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the number of items
    that are BE used as a main verb."""
    string1 = r"\b[am|are|is|was|were|been]_\w+\s\w+_[DT|PRP$|IN|JJ|JJR|JJS]\b"
    matches1 = re.findall(string1, tagged_string)
    counter = len(matches1)
    return(counter) 

## function for feature 20: existential THERE
## DONE!!
def feature_20(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the number of items
    that are existential 'there'."""
    string1 = r"\bthere_\w+\s[am|are|is|was|were|been]_"
    string2 = r"\bthere_\w+\s\w+_\w+\s[am|are|is|was|were|been]_"
    string3 = r"\bthere_\w+\s's"
    matches1 = re.findall(string1, tagged_string)
    matches2 = re.findall(string2, tagged_string)
    matches3 = re.findall(string3, tagged_string)
    counter = len(matches1) + len(matches2) + len(matches3)
    return(counter)

## function for feature 21: THAT verb complements
def feature_21(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the number of items
    that are verbal complements with 'that'."""
    string1 = r"\b[and|nor|but|or|also|\.]_\w+\sthat_\w+\s\w+_[DT|NNS|NNP|NNPS|PRP|PRP$]"
    string2 = r"\b[and|nor|but|or|also|\.]_\w+\sthat_\w+\sthere_\w+"
    string3 = r""
    string4 = r""
    matches1 = re.findall(string1, tagged_string)
    matches2 = re.findall(string2, tagged_string)
    matches3 = re.findall(string3, tagged_string)
    matches4 = re.findall(string4, tagged_string)
    counter = len(matches1) + len(matches2) + len(matches3) + len(matches4)
    return(counter)
## PUB/PRV/SUA/SEEM/APPEAR + that + xxx (where xxx is not V/AUX/CL-p/and)
## PUB/PRV/SUA + PREP + xxx + N + that (where xxx is and number of words but 
## not xxx = N)
    

## function for feature 22: THAT adjective complements
## DONE!!
def feature_22(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the number of items
    that are "that" followed by adjectival complements."""
    string1 = r"\b\w+_JJ\sthat"
    matches1 = re.findall(string1, tagged_string)
    counter = len(matches1)
    return(counter)

## function for feature 23: WH clauses
def feature_23(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the number of items
    that are wh-clauses."""
    string1 = r"\b[]_\w+\s[]_\w+\s\w+_"
    string2 = r"\b[]_\w+\s[]_\w+\s\w+_MD\b"
    matches1 = re.findall(string1, tagged_string)
    matches2 = re.findall(string2, tagged_string)
    counter = len(matches1) + len(matches2)
    return(counter)
## PUB/PRV/SUA + WHP/WHO + xxx (where xxx is not AUX)
  
## WHP/WHO == [who|whom|whose|which|what|where|when|how|whether|why|whoever
## |whomever|whichever|wherever|whenever|whatever|however]
  
## PUB == ["acknowledge", "admit", "agree", "assert", "claim", "complain", 
##   "declare", "deny", "explain", "hint", "insist", "mention", "proclaim", "promise",
##  "protest", "remark", "reply", "report", "say", "suggest", "swear", "write"]
## PRV == ["anticipate", "assume", "believe", "conclude", "decide", "demonstrate",
##  "determine", "discover", "doubt", "estimate", "fear", "feel", "find", "forget", "guess",
##  "hear", "hope", "imagine", "imply", "indicate", "infer", "know", "learn", "mean", "notice",
##  "prove", "realize", "recognize", "remember", "reveal", "see", "show", "suppose", "think",
##  "understand", "realise", "recognise"]
## SUA == ["agree", "arrange", "ask", "beg", "command", "decide", "demand",
##   "grant", "insist", "instruct", "ordain", "pledge", pronounce", "propose", "recommend", 
##   "request", "stipulate", "suggest", "urge"]

## function for feature 24: infinitives
## DONE!!
def feature_24(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the number of items
    that are infinitives."""
    string1 = r"\bto_\w+\s\w+_VB\b"
    string2 = r"\bto_\w+\s\w+_RB\s\w+_VB\b"
    matches1 = re.findall(string1, tagged_string)
    matches2 = re.findall(string2, tagged_string)
    counter = len(matches1) + len(matches2)
    return(counter)

## function for feature 25: present participial clauses
## DONE!!
def feature_25(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the number of items
    that are infinitives."""
    string1 = r"_.\s\w+_VBG\s\w+_[IN|DT|RB|RBR|RBS|PRP|PRP$]\b"
    string2 = r"_.\s\w+_VBG\s[who|whom|whose|which|what|where|when|how|whether|why|whoever|whomever|whichever|wherever|whenever|whatever|however]_\w+\b"
    matches1 = re.findall(string1, tagged_string)
    matches2 = re.findall(string2, tagged_string)
    counter = len(matches1) + len(matches2)
    return(counter)
## (edited manually)

## function for feature 26: past participial clauses
## DONE!!
def feature_26(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the number of items
    that are past participial clauses."""
    string1 = r".\s\w+_VBD\s\w+_[IN|RB|RBR|RBS]\b"
    string2 = r".\s\w+_VBG\s[]_\w+\b"
    matches1 = re.findall(string1, tagged_string)
    matches2 = re.findall(string2, tagged_string)
    counter = len(matches1) + len(matches2)
    return(counter)
## (edited manually)

## function for feature 27: past prt. WHIZ deletions
## DONE!!
def feature_27(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the
    number of past participles WHIZ deletions."""
    string1 = r"_[NN|NNS|NNP|NNPS]\s\w+_VBN\s\w+_[IN|RB|RBR|RBS]"
    string2 = r"_[NN|NNS|NNP|NNPS]\s\w+_VBN\s[be|am|are|is|was|were|been|being]_"
    string3 = r"\b[everybody|somebody|anybody|everyone|someone|anyone|everything|something|anything]_\w+\s\w+_VBN\s\w+_[IN|RB|RBR|RBS]"
    string4 = r"\b[everybody|somebody|anybody|everyone|someone|anyone|everything|something|anything]_\w+\s\w+_VBN\s[be|am|are|is|was|were|been|being]_"
    matches1 = re.findall(string1, tagged_string)
    matches2 = re.findall(string2, tagged_string)
    matches3 = re.findall(string3, tagged_string)
    matches4 = re.findall(string4, tagged_string)
    counter = len(matches1) + len(matches2) + len(matches3) + len(matches4)
    return(counter)
## edited manually

## function for feature 28: present prt. WHIZ deletions
## DONE!!
def feature_28(tagged_string):
    """This function takes a string of words with PoS tags as input and return the
    number of present participled WHIZ deletions."""
    string1 = r"_[NN|NNS|NNP|NNPS]\s\w+_VBG\b"
    matches1 = re.findall(string1, tagged_string)
    counter = len(matches1)
    return(counter)
## edited manually

## function for feature 29: THAT relatives, subject position
## DONE!!
def feature_29(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the number of items
    that are relative clauses with 'that' in subject position."""
    string1 = r"\b\w+_[NN|NNS]\sthat_\w+\s\w+_[MD|VB|VBD|VBG|VBN|VBP|VBZ]\b"
    string2 = r"\B\w+_[NN|NNS]\sthat_\w+\s\w+_RB\s\w+_[MD|VB|VBD|VBG|VBN|VBP|VBZ]\b"
    matches1 = re.findall(string1, tagged_string)
    matches2 = re.findall(string2, tagged_string)
    counter = len(matches1) + len(matches2)
    return(counter)

## function for feature 30: THAT relatives, object position
## DONE!!
def feature_30(tagged_string):
    """This function takes a string of words with PoS tags as input and returns
    the number of that-relatives in object position."""
    string1 = r"\b\w+_[NN|NNS|NNP|NNPS]\sthat_\w+\s\w+_[DT|JJ|JJR|JJS|NNS|NNP|NNPS]\b"
    string2 = r"\b\w+_[NN|NNS|NNP|NNPS]\sthat_\w+\s[it|i|we|he|she|they|my|our|your|his|their|its]_"
    matches1 = re.findall(string1, tagged_string)
    matches2 = re.findall(string2, tagged_string)
    counter = len(matches1) + len(matches2)
    return(counter)

## function for feature 31: WH relatives, subject position
## DONE!!
def feature_31(tagged_string):
    """This function takes a string of words with PoS tags as input and returns
    the number of wh-relatives in subject position."""
    string1 = r"\b\w+\s\w+_[NN|NNP|NNPS|NNS]\swh[o|om|ose|ich]_\w+\s\w+_[MD|VB|VBD|VBG|VBN|VBP|VBZ]\b"
    string2 = r"\b[ask|tell|told]\w+\s\w+\s\w+_[NN|NNP|NNPS|NNS]\swh[o|om|ose|ich]_\w+\s\w+_[MD|VB|VBD|VBG|VBN|VBP|VBZ]\b"
    string3 = r"\b\w+\s\w+_[NN|NNP|NNPS|NNS]\swh[o|om|ose|ich]_\w+\s\w+_[RB|RBR|RBS]\s\w+_[MD|VB|VBD|VBG|VBN|VBP|VBZ]\b"
    string4 = r"\b[ask|tell|told]\w+\s\w+\s\w+_[NN|NNP|NNPS|NNS]\swh[o|om|ose|ich]_\w+\s\w+[RB|RBR\RBS]\s\w+_[MD|VB|VBD|VBG|VBN|VBP|VBZ]\b"
    matches1 = re.findall(string1, tagged_string)
    matches2 = re.findall(string2, tagged_string)
    matches3 = re.findall(string3, tagged_string)
    matches4 = re.findall(string4, tagged_string)
    counter = (len(matches1) - len(matches2)) + (len(matches3) - len(matches4))
    return(counter)

## function for feature 32: WH relatives, object position
## DONE!!
def feature_32(tagged_string):
    """This function takes a string of words with PoS tags as input and returns
    the number of wh-relatives in object position."""
    string1 = r"\b\w+\s\w+\s\w+_[NN|NNP|NNS|NNPS]\s[who|whose|which|whom]_\w+\s\w+\b"
    matches1 = re.findall(string1, tagged_string)
    counter = len(matches1)
    return(counter)  

## function for feature 33: WH relatives, pied piping
## DONE!!
def feature_33(tagged_string):
    """This function takes a string of words with PoS tags as input and returns
    the number of wh-relatives with pied piping."""
    string1 = r"\b\w+_IN\s[who|whom|whose|which]_"
    matches1 = re.findall(string1, tagged_string)
    counter = len(matches1)
    return(counter)

## function for feature 34: sentence relatives
## DONE!!
def feature_34(tagged_string):
    """This function takes a string of words with PoS tags as input and returns
    the number of sentence relatives."""
    string1 = r"_,\swhich_"
    matches1 = re.findall(string1, tagged_string)
    counter = matches1
    return counter
## edited manually

## function for feature 35: adv. subordinator, cause
## DONE!
def feature_35(untagged_list):
    """This function takes a list of words with PoS tags as input and returns the number of items
    that are BECAUSE (= adverbial subordinator of cause)."""
    counter = 0
    for item in untagged_list:
        if item == "because":
            counter = counter + 1
        else:
            pass
    return(counter)

## function for feature 36: adv. subordinator, concession
## DONE!
def feature_36(untagged_list):
    """This function takes a list of words with PoS tags as input and returns the number of items
    that are THOUGH or ALTOUGH (= adverbial subordinators of concession)."""
    counter = 0
    for item in untagged_list:
        if item == "although" or item == "though":
            counter = counter + 1
        else:
            pass
    return(counter)

## function for feature 37: adv. subordinator, condition
## DONE!
def feature_37(untagged_list):
    """This function takes a list of words with PoS tags as input and returns the number of items
    that are IF or UNLESS (= adverbial subordinators of condition)."""
    counter = 0
    for item in untagged_list:
        if item == "if" or item == "unless":
            counter = counter + 1
        else:
            pass
    return(counter)

## function for feature 38: adv. subordinator, other
## DONE!!
def feature_38(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the number of items
    that are adverbial subordinators with multiple function."""
    string1 = r"\b[since|while|whilst|whereupon|whereas|whereby|]_"
    string2 = r"\b[inasmuch|forasmuch|insofar|onsomuch]_\w+\sas_"
    string3 = r"\bas_\w+\s[long|soon]_\w+\sas_"
    string4 = r"\b[so|such]_\w+\sthat_\w+\s\w+_"
    string5 = r"\b[so|such]_\w+\sthat_\w+\s\w+_[NN|NNS|NNP|NNPS|JJ|JJR|JJS]\b"
    matches1 = re.findall(string1, tagged_string)
    matches2 = re.findall(string2, tagged_string)
    matches3 = re.findall(string3, tagged_string)
    matches4 = re.findall(string4, tagged_string)
    matches5 = re.findall(string5, tagged_string)
    counter = len(matches1) + len(matches2) + len(matches3) + (len(matches4) - len(matches5))
    return(counter)

## function for feature 39: preposition
## DONE!
def feature_39(untagged_list):
    """This function takes a list of words with PoS tags as input and returns the number of items
    that are prepositions."""
    counter = 0
    prepositionlist = ["against", "amid", "amidst", "among", "amongst", "at", "besides",
                       "between", "by", "despite", "during", "except", "for", "from", "in", "into", "minus",
                       "notwithstanding", "of", "off", "on", "onto", "opposite", "out", "per", "plus", "pro",
                       "re", "than", "through", "throughout", "thru", "to", "toward", "towards", "upon", 
                       "versus", "via", "with", "within", "without"]
    for item in untagged_list:
        if item in prepositionlist:
            counter = counter + 1
        else:
                pass
    return(counter)

## function for feature 40: attributive adjective
## DONE!!
def feature_40(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the number of items
    that are attributive adjectives."""
    string1 = r"\b\w+_[JJ|JJR|JJS]\s\w+_[JJ|JJR|JJS|NN|NNS]\b"
    matches1 = re.findall(string1, tagged_string)
    counter = len(matches1)
    return(counter)

## function for feature 41: predicative adjective
## DONE!!
def feature_41(tagged_string):
    """This function takes a string of words with PoS tags as input and returns
    the number of predicative adjectives."""
    string1 = r"\b[be|am|are|is|was|were|been|being]_\w+\s\w+_[JJ|JJR|JJS]\s\w+_"
    string2 = r"\b[be|am|are|is|was|were|been|being]_\w+\s\w+_[JJ|JJR|JJS]\s\w+_[JJ|JJR|JJS|RB|RBR|RBS|NN|NNP|NNPS|NNS]"
    string3 = r"\b[be|am|are|is|was|were|been|being]_\w+\s\w+_[JJ|JJR|JJS]\s\w+_[RB|RBR|RBS]\s\w+_"
    string4 = r"\b[be|am|are|is|was|were|been|being]_\w+\s\w+_[JJ|JJR|JJS]\s\w+_[RB|RBR|RBS]\s\w+_[JJ|JJR|JJS|NN|NNP|NNS|NNPS]\b"
    matches1 = re.findall(string1, tagged_string)
    matches2 = re.findall(string2, tagged_string)
    matches3 = re.findall(string3, tagged_string)
    matches4 = re.findall(string4, tagged_string)
    counter = (len(matches1) - len(matches2)) + (len(matches3) - len(matches4))
    return(counter)

## function for feature 42: adverbs
## DONE!!
def feature_42(tagged_list):
    """This function takes a list of words with PoS tags as input and returns the number of items
    that are adverbs."""
    counter = 0
    for item in tagged_list:
        if item == r"\b\w+_[RB|RBR|RBS]\b":
            counter = counter + 1
        else:
            pass
    return(counter)

## function for feature 43: type/token ratio
## DONE!!
def feature_43(untagged_list):
    """This function takes a list of words without PoS tags as input and returns
    the type-token ratio"""
    cleanwords=[word.lower().strip(string.punctuation) for word in untagged_list]
    ttr=len(set(cleanwords))/len(cleanwords)
    return ttr

## function for feature 44: word length
## DONE!!
def feature_44(untagged_list):
    """This function takes a list of words with PoS tags as input and returns
    the mean length of all the words in the text."""
    nwords=len(untagged_list)
    wordlengths=[len(x.strip(string.punctuation)) for x in untagged_list]
    meanWL = sum(wordlengths)/nwords
    return(meanWL)

## function for feature 45: conjuncts
## DONE!!
def feature_45(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the number of items
    that are conjuncts."""
    string1 = r"\b[alternatively|altogether|consequently|conversely|eg|e.g.|else|furthermore|hence|however|i.e.|instead|likewise|moreover|namely|nevertheless|nonetheless|notwithstanding|otherwise|rather|similarly|therefore|thus|viz.]_"
    string2 = r"\bin_\w+\s[comparison|contrast|particular|addition|conclusion|consequence|sum|summary]_"
    string3 = r"_.\srather_\w+\s\w+_,"
    string4 = r"_.\srather_\w+\s\w+"
    string5 = r"_.\srather_\w+\s\w+_[JJ|JJR|JJS|RB|RBR|RBS]"
    string6 = r"\bby_\w+\s[contrast|comparison]_"
    string7 = r"\bfor_\w+\s[example|instance]_"
    string8 = r"\bas_\w+\sa_\w+\s[result|consequence]_"
    string9 = r"\bin_\w+\sany_\w+\s[event|case]_"
    string10 = r"\bin_\w+\sother_\w+\swords_"
    string11 = r"\w_.\s[else|altogether]_\w+\s,_"
    string12 = r"\w_.\sthat_\w+_is_\w+\s,_"
    string13 = r"\bon_\w+\sthe_\w+\scontrary_"
    string14 = r"\bon_\w+\sthe_\w+\sother_\w+\shand_"
    matches1 = re.findall(string1, tagged_string)
    matches2 = re.findall(string2, tagged_string)
    matches3 = re.findall(string3, tagged_string)
    matches4 = re.findall(string4, tagged_string)
    matches5 = re.findall(string5, tagged_string)
    matches6 = re.findall(string6, tagged_string)
    matches7 = re.findall(string7, tagged_string)
    matches8 = re.findall(string8, tagged_string)
    matches9 = re.findall(string9, tagged_string)
    matches10 = re.findall(string10, tagged_string)
    matches11 = re.findall(string11, tagged_string)
    matches12 = re.findall(string12, tagged_string)
    matches13 = re.findall(string13, tagged_string)
    matches14 = re.findall(string14, tagged_string)
    counter = len(matches1) + len(matches2) + len(matches3) + (len(matches4) - len(matches5)) + len(matches6) + len(matches7) + len(matches8) + len(matches9) + len(matches10) + len(matches11) + len(matches12) + len(matches13) + len(matches14)
    return(counter)

## function for feature 46: downtoners
## DONE!
def feature_46(untagged_list):
    """This function takes a list of words with PoS tags as input and returns the number of items
    that are downtoners."""
    counter = 0
    downtonerlist = ["almost", "barely", "hardly", "merely", "mildly", "nearly", "only",
                     "partially", "partly", "practically", "scarcely", "slightly", "somewhat"]
    for item in untagged_list:
        if item in downtonerlist:
            counter = counter + 1
        else:
            pass
    return(counter)

## function for feature 47: hedges
## DONE!!
def feature_47(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the
    number of hedges within that string."""
    string1 = r"\b[almost|maybe]_"
    string2 = r"\bat_\w+\sabout_"
    string3 = r"\bsomething_\w+\slike_"
    string4 = r"\bmore_\w+\sor_\w+\sless_"
    string5 = r"\b\w+\s[sort|kind]_\w+\sof_"
    string6 = r"\b\w+_[DT|JJ|JJR|JJS|PRP$]\s[sort|kind]_\w+\sof_"
    string7 = r"\b[what|where|when|how|whether|why|whoever|whomever|whichever|wherever|whenever|whatever|however]\w+_\s[sort|kind]_\w+\sof_"
    matches1 = re.findall(string1, tagged_string)
    matches2 = re.findall(string2, tagged_string)
    matches3 = re.findall(string3, tagged_string)
    matches4 = re.findall(string4, tagged_string)
    matches5 = re.findall(string5, tagged_string)
    matches6 = re.findall(string6, tagged_string)
    matches7 = re.findall(string7, tagged_string)    
    counter = len(matches1) + len(matches2) + len(matches3) + len(matches4) + (len(matches5) - len(matches6) - len(matches7))
    return(counter)

## function for feature 48: amplifiers
## DONE!
def feature_48(untagged_list):
    """This function takes a list of words with PoS tags as input and returns the number of items
    that are amplifiers."""
    counter = 0
    amplifierlist = ["absolutely", "altogether", "completely", "enormously", "entirely", 
                     "extremely", "fully", "greatly", "highly", "intensely", "perfectly", "strongly", 
                     "thoroughly", "totally", "utterly", "very"]
    for item in untagged_list:
        if item in amplifierlist:
            counter = counter + 1
        else:
            pass
    return(counter)

## function for feature 49: emphatics
## DONE!!
def feature_49(tagged_string):
    """This function takes string of words with PoS tags as input and returns the
    number of emphatics within that string."""
    string1 = r"\b[just|really|most|more]_"
    string2 = r"\bfor_\w+\ssure_"
    string3 = r"\b[real|so]_\w+\s\w+_[JJ|JJR|JJS]\b"
    string4 = r"\ba_\w+\slot_"
    string5 = r"\bsuch_\w+\sa_"
    string6 = r"\b[do|does|doing|did]_\w+\s\w+_[VB|VBD|VBG|VBN|VBP|VBZ]"
    matches1 = re.findall(string1, tagged_string)
    matches2 = re.findall(string2, tagged_string)
    matches3 = re.findall(string3, tagged_string)
    matches4 = re.findall(string4, tagged_string)
    matches5 = re.findall(string5, tagged_string)
    matches6 = re.findall(string6, tagged_string)
    counter = len(matches1) + len(matches2) + len(matches3) + len(matches4) + len(matches5) + len(matches6)
    return(counter)

## function for feature 50: discourse particles
## DONE!!
def feature_50(tagged_string):
    """This function takes a list of words with PoS tags as input and returns the number of items
    that are discourse particles."""
    string1 = r"[\.|!|\?|:|;|-]_\w+\s[well|now|anyway|anyhow|anyways]_"
    matches1 = re.findall(string1, tagged_string)
    counter = len(matches1)
    return(counter)

## function for feature 51: demonstratives
## DONE!
def feature_51(untagged_list):
    """This function takes a list of words with PoS tags as input and returns the number of items
    that are demonstratives."""
    counter = 0
    demonstrativelist = ["that", "this", "these", "those"]
    for item in untagged_list:
        if item in demonstrativelist:
            counter = counter + 1
        else:
            pass
    return(counter)

## function for feature 52: possibility modals
## DONE!
def feature_52(untagged_list):
    """This function takes a list of words with PoS tags as input and returns the number of items
    that are possibility modals."""
    counter = 0
    possmodalslist = ["can", "might", "may", "could"]
    for item in untagged_list:
        if item in possmodalslist:
            counter = counter + 1
        else:
            pass
    return(counter)

## function for feature 53: necessity modals
## DONE!
def feature_53(untagged_list):
    """This function takes a list of words with PoS tags as input and returns the number of items
    that are necessity modals."""
    counter = 0
    nessmodalslist = ["ought", "should", "must"]
    for item in untagged_list:
        if item in nessmodalslist:
            counter = counter + 1
        else:
            pass
    return(counter)

## function for feature 54: predictive modals
## DONE!
def feature_54(untagged_list):
    """This function takes a list of words with PoS tags as input and returns the number of items
    that are predictive modals."""
    counter = 0
    predmodalslist = ["will", "would", "shall"]
    for item in untagged_list:
        if item in predmodalslist:
            counter = counter + 1
        else:
            pass
    return(counter)

## function for feature 55: public verbs
## DONE!
def feature_55(untagged_list):
    """This function takes a list of words with PoS tags as input and returns the number of items
    that are public verbs."""
    counter = 0
    publicverbslist = ["acknowledge", "admit", "agree", "assert", "claim", "complain", 
                       "declare", "deny", "explain", "hint", "insist", "mention", "proclaim", "promise",
                       "protest", "remark", "reply", "report", "say", "suggest", "swear", "write"]
    for item in untagged_list:
        if item in publicverbslist:
            counter = counter + 1
        else:
            pass
    return(counter)

## function for feature 56: private verbs
## DONE!
def feature_56(untagged_list):
    """This function takes a list of words with PoS tags as input and returns the number of items
    that are private verbs."""
    counter = 0
    privateverbslist = ["anticipate", "assume", "believe", "conclude", "decide", "demonstrate",
                        "determine", "discover", "doubt", "estimate", "fear", "feel", "find", "forget", "guess",
                        "hear", "hope", "imagine", "imply", "indicate", "infer", "know", "learn", "mean", "notice",
                        "prove", "realize", "recognize", "remember", "reveal", "see", "show", "suppose", "think",
                        "understand", "realise", "recognise"]
    for item in untagged_list:
        if item in privateverbslist:
            counter = counter + 1
        else:
            pass
    return(counter)

## function for feature 57: suasive verbs
## DONE!
def feature_57(untagged_list):
    """This function takes a list of words with PoS tags as input and returns the number of items
    that are suasive verbs."""
    counter = 0
    suasiveverbslist = ["agree", "arrange", "ask", "beg", "command", "decide", "demand",
                        "grant", "insist", "instruct", "ordain", "pledge", "pronounce", "propose", "recommend", 
                        "request", "stipulate", "suggest", "urge"]
    for item in untagged_list:
        if item in suasiveverbslist:
            counter = counter + 1
        else:
            pass
    return(counter)

## function for feature 58: SEEM/APPEAR
## DONE!!
def feature_58(untagged_list):
    """This function takes a list of words with PoS tags as input and returns the number of items
    that are the verbs SEEM or APPEAR."""
    counter = 0
    string1 = r"appea[r|rs|red|ring]"
    string2 = r"see[m|ms|ming|med]"
    for item in untagged_list:
        if item == string1 or item == string2:
            counter = counter + 1
    else:
        pass
    return(counter)

## function for feature 59: contractions
## DONE!!
def feature_59(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the
    number of contractions within the string."""
    string1 = r"\b\w+_PRP\s'[m|re|s|d]_" ## all contractions on pronouns
    string2 = r"\b\w+_MD\sn't_" ## all contractions on auxiliary forms (negation)
    string3 = r"\b\w+_[NN|NNS|NNP|NNPS]\s's_w+\s\w+_[MD|DT|PRP|IN]\b"
    string4 = r"\b\w+_[NN|NNS|NNP|NNPS]\s's_w+\s\w+_[RB|RBR|RBS]\s\w+_[MD|VB|VBG|VBN|VBD|VBP|VBZ]\b"
    string5 = r"\b\w+_[NN|NNS|NNP|NNPS]\s's_w+\s\w+_[JJ|JJR|JJS]\s\S_."
    matches1 = re.findall(string1, tagged_string)
    matches2 = re.findall(string2, tagged_string)
    matches3 = re.findall(string3, tagged_string)
    matches4 = re.findall(string4, tagged_string)
    matches5 = re.findall(string5, tagged_string)
    counter = len(matches1) + len(matches2) + len(matches3) + len(matches4) + len(matches5)
    return(counter)    

## function for feature 60: THAT deletion
def feature_60(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the
    number of that-deletions within the string."""
    string1 = r""
    string2 = r""
    string3 = r""
    string4 = r""
    matches1 = re.findall(string1, tagged_string)
    matches2 = re.findall(string2, tagged_string)
    matches3 = re.findall(string3, tagged_string)
    matches4 = re.findall(string4, tagged_string)
    counter = len(matches1) + len(matches2) + len(matches3) + len(matches4)
    return(counter)
## PUB/PRV/SUA + demonstrative pronoun/subjectpronoun
## PUB/PRV/SUA + PRO/N + AUX/V
## PUB/PRV/SUA + ADJ/ADV/DET/POSSPRO + (ADJ) + N + AUX/V

## function for feature 61: stranded prepositions
## DONE!!
def feature_61(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the number of items
    that are stranded prepositions."""
    string1 = r"\w+_IN\s\S_."
    matches1 = re.findall(string1, tagged_string)
    counter = len(matches1)
    return(counter)

## function for feature 62: split infinitives
## DONE!!
def feature_62(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the number of items
    that are the verbs SEEM or APPEAR."""
    string1 = r"\bto_\w+\s\w+_[RB|RBR|RBS]\s\w+_VB\b"
    string2 = r"\bto_\w+\s\w+_[RB|RBR|RBS]\s\w+_[RB|RBR|RBS]\s\w+_VB\b"
    matches1 = re.findall(string1, tagged_string)
    matches2 = re.findall(string2, tagged_string)
    counter = len(matches1) + len(matches2)
    return(counter)
    
## function for feature 63: split auxiliaries
## DONE!!
def feature_63(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the number of items
    that are split auxiliaries."""
    string1 = r"\b\w+_MD\s\w+_[RB|RBR|RBS]\s\w+_VB\b"
    string2 = r"\b\w+_MD\s\w+_[RB|RBR|RBS]\s\w+_[RB|RBR|RBS]\s\w+_VB\b"
    matches1 = re.findall(string1, tagged_string)
    matches2 = re.findall(string2, tagged_string)
    counter = len(matches1) + len(matches2)
    return(counter)

## function for feature 64: phrasal coordination
## DONE!!
def feature_64(tagged_string):
    """This function takes a string of words with PoS tags as input and returns
    the number of phrasal coordinations."""
    string1 = r"\w+_[NN|NNS|NNP|NNPS]\sand_\w+\s\w+_[NN|NNS|NNP|NNPS]\s"
    string2 = r"\w+_[RB|RBR|RBS]\sand_\w+\s\w+_[RB|RBR|RBS]\s"
    string3 = r"\w+_[JJ|JJR|JJS]\sand_\w+\s\w+_[JJ|JJR|JJS]\s"
    string4 = r"\w+_[VB|VBD|VBG|VBN|VBP|VBZ]\sand_\w+\s\w+_[VB|VBD|VBG|VBN|VBP|VBZ]\s"
    matches1 = re.findall(string1, tagged_string)
    matches2 = re.findall(string2, tagged_string)
    matches3 = re.findall(string3, tagged_string)
    matches4 = re.findall(string4, tagged_string)
    counter = len(matches1) + len(matches2) + len(matches3) + len(matches4)
    return(counter)

## function for feature 65: non-phrasal coordination
def feature_65(tagged_string):
    """This function takes a string of words with PoS tags as input and return the 
    number of non-phrasal coordinations within the string."""
    string1 = r"_,\sand_\w+\s[it|so|then|you|I|we|he|she|they|that|this|these|thsoe]_"
    string2 = r"_,\sand_\w+\s\w+_[]"
    string3 = r"_,\sand_\w+\sthere_\w+\s[be|am|are|is|was|were|been|being]_"
    string4 = r"_.\sand_\w+\s"
    string5 = r"\band_\w+\s[who|whom|whose|which|what|where|when|how|whether|why||whoever|whomever|whichever|wherever|whenever|whatever|however]_"
    string6 = r"\band_\w+\s[well|now|anyway|anyhow|anyways|because|although|though|if|unless|since|while|whilst|whereupon|whereas|whereby]_"
    string7 = r"\band_\w+\s[inasmuch|forasmuch|insofar|onsomuch]_\w+\sas_"
    string8 = r"\band_\w+\sas_\w+\s[long|soon]_\w+\sas_"
    string9 = r"\band_\w+\s[so|such]_\w+\sthat_\w+\s\w+_"
    string10 = r"\band_\w+\s[so|such]_\w+\sthat_\w+\s\w+_[NN|NNS|NNP|NNPS|JJ|JJR|JJS]\b"
    matches1 = re.findall(string1, tagged_string)
    matches2 = re.findall(string2, tagged_string)
    matches3 = re.findall(string3, tagged_string)
    matches4 = re.findall(string4, tagged_string)
    matches5 = re.findall(string5, tagged_string)
    matches6 = re.findall(string6, tagged_string)
    matches7 = re.findall(string7, tagged_string)
    matches8 = re.findall(string8, tagged_string)
    matches9 = re.findall(string9, tagged_string)
    matches10 = re.findall(string10, tagged_string)   
    counter = len(matches1) + len(matches2) + len(matches3) + len(matches4) + len(matches5) + len(matches6) + len(matches7) + len(matches8) + (len(matches9) - len(matches10))
    return(counter)
## and + conjunct -> see feature 45

## function for feature 66: synthetic negation
## DONE!!
def feature_66(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the number of items
    that are synthetic negation."""
    string1 = r"\b[neither|nor]_\w+\b"
    string2 = r"\b[no]_\w+\s\w+_[JJ|JJR|JJS|NN|NNS|NNP|NNPS]\b"
    string3 = r"\b[no]_\w+\s[each|all|every|many|much|few|several|some|any]_"
    matches1 = re.findall(string1, tagged_string)
    matches2 = re.findall(string2, tagged_string)
    matches3 = re.findall(string3, tagged_string)
    counter = len(matches1) + len(matches2) + len(matches3)
    return(counter)

## function for feature 67: analytic negation
## DONE!
def feature_67(untagged_list):
    """This function takes a list of words without PoS tags as input and returns the number of items
    that are NOT (= analytic negation)."""
    counter = 0
    for item in untagged_list:
        if item == "not":
            counter = counter + 1
        else:
            pass
    return(counter)

## additional feature 1: comparatives 
## DONE!!
def feature_comp(tagged_list):
    """This function takes a list of words with PoS tags as input and returns the number of comparative
    adjectives within the list."""
    counter = 0
    for item in tagged_list:
        if item == r"\w+_JJR":
            counter = counter + 1
        else:
            pass
    return(counter)
  
## additional featuer 2: superlatives
## DONE!!
def feature_sup(tagged_list):
    """This function takes list of words with PoS tags as input and returns the number of superlative
    adjectives within the list."""
    counter = 0
    for item in tagged_list:
        if item == r"\w+_JJS":
            counter = counter + 1
        else:
            pass
    return(counter)



















