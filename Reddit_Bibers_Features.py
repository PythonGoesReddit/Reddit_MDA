
### functions 55 to 57, in which I check whether a verb is within a previously
### defined list, do not yet take inflectional endings into account!

import re
import string


## function for feature 2: verbs in the perfect aspect
def feature_02(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the number of 
    perfect aspect forms."""
    # Should the past perfect with "had" not also contribute towards counts here?
    # If I read this correctly, you need round parentheses below. Square ones are for one-character disjunctions.
    # Might also add "?:" to avoid grouping, i.e. (?:have|has|'ve|'s|had|'d)
    # Issues remain with "'s" and "'d" which are not unambiguously forms of HAVE.
    string1 = r"\b[have|has|'ve|'s]_\w+\s\w+_VBD\b"
    string2 = r"\b[have|has|'ve|'s]_\w+\s\w+_RB\s\w+_VBD\b"
    string3 = r"\b[have|has|'ve|'s]_\w+\s\w+_RB\s\w+_RB\s\w+_VBD\b"
    string4 = r"\b[have|has]_\w+\s\w+_[NN|NNS|NNP|NNPS|PRP|PRP$]\s\w+_VBD\b"
    return(counter)

## function for feature 3: present tense
def feature_03(tagged_string):
    """This function takes a list of words with PoS tags as input and returns the number of 
    verbs in the present tense (excluding infinitives)."""
    string1 = r"\b(?<!to)_\w+\s\w+_[VB|VBZ]\b"
    matches1 = re.findall(string1, tagged_string)
    counter = matches1
    return(counter)

## function for feature 10: demonstrative pronouns
def feature_10(tagged_string):
    """This function takes a list of words with PoS tags as input and returns the number of items
    that are demonstrative pronouns."""
    # Here also, you probably want round parentheses rather than square ones if I am not mistaken.
    string1 = r"\b[that|this|these|those]_\w+\s\w+_[VB|VBD|VBG|VBN|VBP|VBZ|MD|WP]"
    # Are we sure the above only catches demonstratives? What about complementizer/relativizer THAT ("Things that go bump in the night"...)
    # Again, here it would seem that the work of disambiguating demonstratives from other items should be done by the tagger?
    string2 = r"\b[that|this|these|those]_\w+\s[and|\.]"
    string3 = r"\bthat_\w+\s's_"
    return(counter)


## function for feature 12: DO as pro-verb
def feature_12(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the number of items
    that are DO used as a pro-verb."""
    string1 = r"\b[do|does|doing|did|done]_"
    string2 = r"\b[do|does|doing|did|done]_\w+\s\w+_VB"
    string3 = r"\b[do|does|doing|did|done]_\w+\s\w+_[RB|RBR|RBS]\s\w+_VB"
    string4 = r"_[\.|]\s[do|does|doing|did|done]_"
    string5 = r"\b[who|whom|whose|which]_\w+\s[do|does|doing|did|done]_" # Not sure about this one; could be either pro-verb or do-support in question, right?
    return(counter)

## function for feature 13: WH-questions
def feature_13(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the number of items
    that are WH-questions."""
    string1 = r"_\.\swho_\w+\s\w+_MD"
    string2 = r"_\.\swho_\w+\s[do|does|doing|did|have|has|had|having|be|been|am|are|is|was|were|being]_"
    # This is only "who" as a question word, right? What about the other WH-q-words?
    # Also, what about questions with a simple lexical verb, e.g. "Who left the stove on?" "What happened to Martha?" etc.
    matches1 = re.findall(string1, tagged_string)
    matches2 = re.findall(string2, tagged_string)
    counter = len(matches1) + len(matches2)
    return(counter)


## function for feature 15: gerunds
## (edited manually)
def feature_15(tagged_list):
    """This function takes a list of words with PoS tags as input and returns the number of items
    that are gerunds (participle forms serving nominal function)."""
    counter = 0
    string1 = r"\w+ing_VBG\b"
    for item in tagged_list:
        if item == string1:
            counter = counter + 1
        else:
            pass
    return(counter) 

## function for feature 17: agentless passives
def feature_17(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the 
    number of agentles passives within the string."""
    string1 = r"\b[be|am|are|is|was|were|been|being]_V[B|BD|BG|BN|BP|BZ]\s\w+_VBN\s(?!by_)"
    string2 = r"\b[be|am|are|is|was|were|been|being]_V[B|BD|BG|BN|BP|BZ]\s\w+_[RB|RBR|RBS]\s\w+_VBN\s(?!by_)"
    string3 = r"\b[be|am|are|is|was|were|been|being]_V[B|BD|BG|BN|BP|BZ]\s\w+_[RB|RBR|RBS]\s\w+_[RB|RBR|RBS]\s\w+_VBN\s(?!by_)"
    string4 = r"\b[be|am|are|is|was|were|been|being]_V[B|BD|BG|BN|BP|BZ]\s\w+_[NN|NNS|NNP|NNPS|PRP|PRP$]\s\w+_VBN\s(?!by_)"
    return(counter)    

## function for feature 18: BY passives
def feature_18(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the 
    number of BY-passives within the string."""
    string1 = r"\b[be|am|are|is|was|were|been|being]_V[B|BD|BG|BN|BP|BZ]\s\w+_VBN\sby_"
    string2 = r"\b[be|am|are|is|was|were|been|being]_V[B|BD|BG|BN|BP|BZ]\s\w+_[RB|RBR|RBS]\s\w+_VBN\sby_"
    string3 = r"\b[be|am|are|is|was|were|been|being]_V[B|BD|BG|BN|BP|BZ]\s\w+_[RB|RBR|RBS]\s\w+_[RB|RBR|RBS]\s\w+_VBN\sby_"
    string4 = r"\b[be|am|are|is|was|were|been|being]_V[B|BD|BG|BN|BP|BZ]\s\w+_[NN|NNS|NNP|NNPS|PRP|PRP$]\s\w+_VBN\sby_"
    matches1 = re.findall(string1, tagged_string)
    matches2 = re.findall(string2, tagged_string)
    matches3 = re.findall(string3, tagged_string)
    matches4 = re.findall(string4, tagged_string)
    counter = len(matches1) + len(matches2) + len(matches3) + len(matches4)
    return(counter)

## function for feature 19: BE as main verb
def feature_19(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the number of items
    that are BE used as a main verb."""
    string1 = r"\b[am|are|is|was|were|been|be|being]_\w+\s\w+_[DT|PRP$|IN|JJ|JJR|JJS]\b"
    matches1 = re.findall(string1, tagged_string)
    counter = len(matches1)
    return(counter) 

## function for feature 21: THAT verb complements
## this function still needs work!
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

## function for feature 23: WH clauses
## this function still needs work!
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
def feature_24(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the number of items
    that are infinitives."""
    string1 = r"\bto_\w+\s\w+_VB\b"
    string2 = r"\bto_\w+\s\w+_[RB|RBR|RBS]\s\w+_VB\b"
    matches1 = re.findall(string1, tagged_string)
    matches2 = re.findall(string2, tagged_string)
    counter = len(matches1) + len(matches2)
    return(counter)

## function for feature 25: present participial clauses
## (edited manually)     
def feature_25(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the number of items
    that are infinitives."""
    string1 = r"_\.\s\w+_VBG\s\w+_[IN|DT|RB|RBR|RBS|PRP|PRP$]\b"
    string2 = r"_\.\s\w+_VBG\s[who|whom|whose|which|what|where|when|how|whether|why|whoever|whomever|whichever|wherever|whenever|whatever|however]_\w+\b"
    matches1 = re.findall(string1, tagged_string)
    matches2 = re.findall(string2, tagged_string)
    counter = len(matches1) + len(matches2)
    return(counter)

## function for feature 26: past participial clauses
## (edited manually)
def feature_26(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the number of items
    that are past participial clauses."""
    string1 = r"_\.\s\w+_VBN\s\w+_[IN|RB|RBR|RBS]\b"
    matches1 = re.findall(string1, tagged_string)
    counter = len(matches1)
    return(counter)

## function for feature 27: past prt. WHIZ deletions
## (edited manually)
def feature_27(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the
    number of past participles WHIZ deletions."""
    string1 = r"_[NN|NNS|NNP|NNPS]\s\w+_VBN\s\w+_[IN|RB|RBR|RBS]\b"
    string2 = r"_[NN|NNS|NNP|NNPS]\s\w+_VBN\s[be|am|are|is|was|were|been|being]_"
    string3 = r"\b[everybody|somebody|anybody|everyone|someone|anyone|everything|something|anything]_\w+\s\w+_VBN\s\w+_[IN|RB|RBR|RBS]"
    string4 = r"\b[everybody|somebody|anybody|everyone|someone|anyone|everything|something|anything]_\w+\s\w+_VBN\s[be|am|are|is|was|were|been|being]_"
    return(counter)

## function for feature 28: present prt. WHIZ deletions
## (edited manually)
def feature_28(tagged_string):
    """This function takes a string of words with PoS tags as input and return the
    number of present participled WHIZ deletions."""
    string1 = r"_[NN|NNS|NNP|NNPS]\s\w+_VBG\b"
    matches1 = re.findall(string1, tagged_string)
    counter = len(matches1)
    return(counter)

## function for feature 31: WH relatives, subject position
def feature_31(tagged_string):
    string1 = r"\b\w+\s\w+_[NN|NNP|NNPS|NNS]\swh[o|om|ose|ich]_\w+\s\w+_[MD|VB|VBD|VBG|VBN|VBP|VBZ]\b"
    string2 = r"\b[ask|tell|told]\w+\s\w+\s\w+_[NN|NNP|NNPS|NNS]\swh[o|om|ose|ich]_\w+\s\w+_[MD|VB|VBD|VBG|VBN|VBP|VBZ]\b"
    string3 = r"\b\w+\s\w+_[NN|NNP|NNPS|NNS]\swh[o|om|ose|ich]_\w+\s\w+_[RB|RBR|RBS]\s\w+_[MD|VB|VBD|VBG|VBN|VBP|VBZ]\b"
    string4 = r"\b[ask|tell|told]\w+\s\w+\s\w+_[NN|NNP|NNPS|NNS]\swh[o|om|ose|ich]_\w+\s\w+[RB|RBR\RBS]\s\w+_[MD|VB|VBD|VBG|VBN|VBP|VBZ]\b"
    return(counter)  

## function for feature 38: adv. subordinator, other
def feature_38(tagged_string):
    string1 = r"\b[since|while|whilst|whereupon|whereas|whereby]_"
    string2 = r"\b[inasmuch|forasmuch|insofar|onsomuch]_\w+\sas_"
    string3 = r"\bas_\w+\s[long|soon]_\w+\sas_"
    string4 = r"\b[so|such]_\w+\sthat_\w+\s\w+_"
    string5 = r"\b[so|such]_\w+\sthat_\w+\s\w+_[NN|NNS|NNP|NNPS|JJ|JJR|JJS]\b"
    return(counter)

## function for feature 43: type/token ratio
def feature_43(untagged_list):
    """This function takes a list of words without PoS tags as input and returns
    the type-token ratio"""
    cleanwords=[word.lower().strip(string.punctuation) for word in untagged_list]
    ttr=len(set(cleanwords))/len(cleanwords)
    return ttr

## function for feature 44: word length
def feature_44(untagged_list):
    """This function takes a list of words without PoS tags as input and returns
    the mean length of all the words in the text."""
    nwords=len(untagged_list)
    wordlengths=[len(x.strip(string.punctuation)) for x in untagged_list]
    meanWL = sum(wordlengths)/nwords
    return(meanWL)

## function for feature 49: emphatics
def feature_49(tagged_string):
    """This function takes string of words with PoS tags as input and returns the
    number of emphatics within that string."""
    string1 = r"\b[just|really|most|more]_"
    string2 = r"\bfor_\w+\ssure_"
    string3 = r"\b[real|so]_\w+\s\w+_[JJ|JJR|JJS]\b"
    string4 = r"\ba_\w+\slot_"
    string5 = r"\bsuch_\w+\sa_"
    string6 = r"\b[do|does|doing|did]_\w+\s\w+_[VB|VBD|VBG|VBN|VBP|VBZ]\b"
    return(counter)

## function for feature 52: possibility modals
def feature_52(untagged_list):
    """This function takes a list of words without PoS tags as input and returns the number of items
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
def feature_53(untagged_list):
    """This function takes a list of words without PoS tags as input and returns the number of items
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
def feature_54(untagged_list):
    """This function takes a list of words without PoS tags as input and returns the number of items
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
def feature_55(untagged_list):
    """This function takes a list of words without PoS tags as input and returns the number of items
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
def feature_56(untagged_list):
    """This function takes a list of words without PoS tags as input and returns the number of items
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
def feature_57(untagged_list):
    """This function takes a list of words without PoS tags as input and returns the number of items
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


## function for feature 59: contractions
def feature_59(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the
    number of contractions within the string."""
    string1 = r"\b\w+_PRP\s'[m|re|s|d]_"
    string2 = r"\b\w+_MD\sn't_"
    string3 = r"\b\w+_[NN|NNS|NNP|NNPS]\s's_w+\s\w+_[MD|DT|PRP|IN]\b"
    string4 = r"\b\w+_[NN|NNS|NNP|NNPS]\s's_w+\s\w+_[RB|RBR|RBS]\s\w+_[MD|VB|VBG|VBN|VBD|VBP|VBZ]\b"
    string5 = r"\b\w+_[NN|NNS|NNP|NNPS]\s's_w+\s\w+_[JJ|JJR|JJS]\s\S_\."
    return(counter)    

## function for feature 60: THAT deletion
## this function still needs work!
def feature_60(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the
    number of that-deletions within the string."""
    return(counter)
## PUB/PRV/SUA + demonstrative pronoun/subjectpronoun
## PUB/PRV/SUA + PRO/N + AUX/V
## PUB/PRV/SUA + ADJ/ADV/DET/POSSPRO + (ADJ) + N + AUX/V

## function for feature 62: split infinitives
def feature_62(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the number of items
    that are split infinitives."""
    string1 = r"\bto_\w+\s\w+_[RB|RBR|RBS]\s\w+_VB\b"
    string2 = r"\bto_\w+\s\w+_[RB|RBR|RBS]\s\w+_[RB|RBR|RBS]\s\w+_VB\b"
    matches1 = re.findall(string1, tagged_string)
    matches2 = re.findall(string2, tagged_string)
    counter = len(matches1) + len(matches2)
    return(counter)
    
## function for feature 63: split auxiliaries
def feature_63(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the number of items
    that are split auxiliaries."""
    string1 = r"\b\w+_MD\s\w+_[RB|RBR|RBS]\s\w+_VB\b"
    string2 = r"\b\w+_MD\s\w+_[RB|RBR|RBS]\s\w+_[RB|RBR|RBS]\s\w+_VB\b"
    string3 = r"\b[am|are|be|is|was|were|been|being|have|had|has|having|do|does|doing|did]_\w+\s\w+_[RB|RBR|RBS]\s\w+_VB\b"
    string4 = r"\b[am|are|be|is|was|were|been|being|have|had|has|having|do|does|doing|did]_\w+\s\w+_[RB|RBR|RBS]\s\w+_[RB|RBR|RBS]\s\w+_VB\b"
    matches1 = re.findall(string1, tagged_string)
    matches2 = re.findall(string2, tagged_string)
    matches3 = re.findall(string3, tagged_string)
    matches4 = re.findall(string4, tagged_string)
    counter = len(matches1) + len(matches2) + len(matches3) + len(matches4)
    return(counter)







