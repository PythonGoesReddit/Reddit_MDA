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
## startswith? KM

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
    matches1 = re.findall(string1, tagged_string)
    matches2 = re.findall(string2, tagged_string)
    matches3 = re.findall(string3, tagged_string)
    matches4 = re.findall(string4, tagged_string)
    counter = len(matches1) + len(matches2) + len(matches3) + len(matches4)
    return(counter)

## function for feature 3: present tense
def feature_03(tagged_string):
    """This function takes a list of words with PoS tags as input and returns the number of 
    verbs in the present tense (excluding infinitives)."""
    string1 = r"\b(?<!to)_\w+\s\w+_[VB|VBZ]\b"
    matches1 = re.findall(string1, tagged_string)
    counter = matches1
    return(counter)
    

## function for feature 6: first person pronouns
def feature_06(untagged_list):
    """This function takes a list of words without PoS tags as input and returns the number of items
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
def feature_07(untagged_list):
    """This function takes a list of words without PoS tags as input and returns the number of items
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
def feature_08(untagged_list):
    """This function takes a list of words without PoS tags as input and returns the number of items
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
def feature_09(untagged_list):
    """This function takes a list of words without PoS tags as input and returns the number of items
    that are the pronoun IT."""
    counter = 0
    for item in untagged_list:
        if item == "it":
            counter = counter + 1
        else:
            pass
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
    matches1 = re.findall(string1, tagged_string)
    matches2 = re.findall(string2, tagged_string)
    matches3 = re.findall(string3, tagged_string)
    counter = len(matches1) + len(matches2) + len(matches3)
    return(counter)

## function for feature 11: indefinite pronouns
def feature_11(untagged_list):
    """This function takes a list of words without PoS tags as input and returns the number of items
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
def feature_12(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the number of items
    that are DO used as a pro-verb."""
    # Round brackets needed instead of square below
    string1 = r"\b[do|does|doing|did|done]_"
    string2 = r"\b[do|does|doing|did|done]_\w+\s\w+_VB"
    string3 = r"\b[do|does|doing|did|done]_\w+\s\w+_[RB|RBR|RBS]\s\w+_VB"
    string4 = r"_[\.|]\s[do|does|doing|did|done]_"
    string5 = r"\b[who|whom|whose|which]_\w+\s[do|does|doing|did|done]_" # Not sure about this one; could be either pro-verb or do-support in question, right?
    matches1 = re.findall(string1, tagged_string)
    matches2 = re.findall(string2, tagged_string)
    matches3 = re.findall(string3, tagged_string)
    matches4 = re.findall(string4, tagged_string)
    matches5 = re.findall(string5, tagged_string)
    counter = len(matches1) - (len(matches2) + len(matches3) + len(matches4) + len(matches5))
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

## function for feature 16: nouns
def feature_16(tagged_list):
    """This function takes a list of words with PoS tags as input and returns the number of items
    that are nouns (excluding nominalisations)."""
    counter = 0
    string1 = r"\b\w+_NNS?\b"
    string2 = r"\b\w+[tions|tion|ments|ment|ness|ity|nesses|ities]_\w+\b"
    for item in tagged_list:
        if item == string1 and not item == string2:
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
    matches1 = re.findall(string1, tagged_string)
    matches2 = re.findall(string2, tagged_string)
    matches3 = re.findall(string3, tagged_string)
    matches4 = re.findall(string4, tagged_string)
    counter = len(matches1) + len(matches2) + len(matches3) + len(matches4)
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

## function for feature 20: existential THERE
def feature_20(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the number of items
    that are existential 'there'."""
    string1 = r"\bthere_\w+\s[am|are|is|was|were|been|be|beign]_"
    string2 = r"\bthere_\w+\s\w+_\w+\s[am|are|is|was|were|been|be|being]_"
    string3 = r"\bthere_\w+\s's"
    matches1 = re.findall(string1, tagged_string)
    matches2 = re.findall(string2, tagged_string)
    matches3 = re.findall(string3, tagged_string)
    counter = len(matches1) + len(matches2) + len(matches3)
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
    

## function for feature 22: THAT adjective complements
def feature_22(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the number of items
    that are "that" followed by adjectival complements."""
    string1 = r"\b\w+_[JJ|JJR|JJS]\sthat"
    matches1 = re.findall(string1, tagged_string)
    counter = len(matches1)
    return(counter)

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
    matches1 = re.findall(string1, tagged_string)
    matches2 = re.findall(string2, tagged_string)
    matches3 = re.findall(string3, tagged_string)
    matches4 = re.findall(string4, tagged_string)
    counter = len(matches1) + len(matches2) + len(matches3) + len(matches4)
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

## function for feature 29: THAT relatives, subject position
def feature_29(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the number of items
    that are relative clauses with 'that' in subject position."""
    string1 = r"\b\w+_[NN|NNS]\sthat_\w+\s\w+_[MD|VB|VBD|VBG|VBN|VBP|VBZ]\b"
    string2 = r"\b\w+_[NN|NNS]\sthat_\w+\s\w+_[RB|RBR|RBS]\s\w+_[MD|VB|VBD|VBG|VBN|VBP|VBZ]\b"
    matches1 = re.findall(string1, tagged_string)
    matches2 = re.findall(string2, tagged_string)
    counter = len(matches1) + len(matches2)
    return(counter)

## function for feature 30: THAT relatives, object position
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
def feature_32(tagged_string):
    """This function takes a string of words with PoS tags as input and returns
    the number of wh-relatives in object position."""
    string1 = r"\b\w+\s\w+\s\w+_[NN|NNP|NNS|NNPS]\s[who|whose|which|whom]_\w+\s\w+\b"
    matches1 = re.findall(string1, tagged_string)
    counter = len(matches1)
    return(counter)  

## function for feature 33: WH relatives, pied piping
def feature_33(tagged_string):
    """This function takes a string of words with PoS tags as input and returns
    the number of wh-relatives with pied piping."""
    string1 = r"\b\w+_IN\s[who|whom|whose|which]_"
    matches1 = re.findall(string1, tagged_string)
    counter = len(matches1)
    return(counter)

## function for feature 34: sentence relatives
## (edited manually)
def feature_34(tagged_string):
    """This function takes a string of words with PoS tags as input and returns
    the number of sentence relatives."""
    string1 = r"_,\swhich_"
    matches1 = re.findall(string1, tagged_string)
    counter = matches1
    return counter


## function for feature 38: adv. subordinator, other
def feature_38(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the number of items
    that are adverbial subordinators with multiple function."""
    string1 = r"\b[since|while|whilst|whereupon|whereas|whereby]_"
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

## function for feature 40: attributive adjective
def feature_40(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the number of items
    that are attributive adjectives."""
    string1 = r"_[JJ|JJR|JJS]\s\w+_[JJ|JJR|JJS|NN|NNS]\b"
    matches1 = re.findall(string1, tagged_string)
    counter = len(matches1)
    return(counter)

## function for feature 41: predicative adjective
def feature_41(tagged_string):
    """This function takes a string of words with PoS tags as input and returns
    the number of predicative adjectives."""
    string1 = r"\b[be|am|are|is|was|were|been|being]_\w+\s\w+_[JJ|JJR|JJS]\s\w+_"
    string2 = r"\b[be|am|are|is|was|were|been|being]_\w+\s\w+_[JJ|JJR|JJS]\s\w+_[JJ|JJR|JJS|RB|RBR|RBS|NN|NNP|NNPS|NNS]\b"
    string3 = r"\b[be|am|are|is|was|were|been|being]_\w+\s\w+_[JJ|JJR|JJS]\s\w+_[RB|RBR|RBS]\s\w+_"
    string4 = r"\b[be|am|are|is|was|were|been|being]_\w+\s\w+_[JJ|JJR|JJS]\s\w+_[RB|RBR|RBS]\s\w+_[JJ|JJR|JJS|NN|NNP|NNS|NNPS]\b"
    matches1 = re.findall(string1, tagged_string)
    matches2 = re.findall(string2, tagged_string)
    matches3 = re.findall(string3, tagged_string)
    matches4 = re.findall(string4, tagged_string)
    counter = (len(matches1) - len(matches2)) + (len(matches3) - len(matches4))
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

## function for feature 45: conjuncts
def feature_45(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the number of items
    that are conjuncts."""
    string1 = r"\b[alternatively|altogether|consequently|conversely|eg|e.g.|else|furthermore|hence|however|i.e.|instead|likewise|moreover|namely|nevertheless|nonetheless|notwithstanding|otherwise|rather|similarly|therefore|thus|viz.]_"
    string2 = r"\bin_\w+\s[comparison|contrast|particular|addition|conclusion|consequence|sum|summary]_"
    string3 = r"_\.\srather_\w+\s\w+_,"
    string4 = r"_\.\srather_\w+\s\w+"
    string5 = r"_\.\srather_\w+\s\w+_[JJ|JJR|JJS|RB|RBR|RBS]"
    string6 = r"\bby_\w+\s[contrast|comparison]_"
    string7 = r"\bfor_\w+\s[example|instance]_"
    string8 = r"\bas_\w+\sa_\w+\s[result|consequence]_"
    string9 = r"\bin_\w+\sany_\w+\s[event|case]_"
    string10 = r"\bin_\w+\sother_\w+\swords_"
    string11 = r"\w_\.\s[else|altogether]_\w+\s,_"
    string12 = r"\w_\.\sthat_\w+_is_\w+\s,_"
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
def feature_46(untagged_list):
    """This function takes a list of words without PoS tags as input and returns the number of items
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
def feature_48(untagged_list):
    """This function takes a list of words without PoS tags as input and returns the number of items
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
def feature_49(tagged_string):
    """This function takes string of words with PoS tags as input and returns the
    number of emphatics within that string."""
    string1 = r"\b[just|really|most|more]_"
    string2 = r"\bfor_\w+\ssure_"
    string3 = r"\b[real|so]_\w+\s\w+_[JJ|JJR|JJS]\b"
    string4 = r"\ba_\w+\slot_"
    string5 = r"\bsuch_\w+\sa_"
    string6 = r"\b[do|does|doing|did]_\w+\s\w+_[VB|VBD|VBG|VBN|VBP|VBZ]\b"
    matches1 = re.findall(string1, tagged_string)
    matches2 = re.findall(string2, tagged_string)
    matches3 = re.findall(string3, tagged_string)
    matches4 = re.findall(string4, tagged_string)
    matches5 = re.findall(string5, tagged_string)
    matches6 = re.findall(string6, tagged_string)
    counter = len(matches1) + len(matches2) + len(matches3) + len(matches4) + len(matches5) + len(matches6)
    return(counter)

## function for feature 50: discourse particles
def feature_50(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the number of items
    that are discourse particles."""
    string1 = r"_\.\s[well|now|anyway|anyhow|anyways]_"
    matches1 = re.findall(string1, tagged_string)
    counter = len(matches1)
    return(counter)

## function for feature 51: demonstratives
def feature_51(untagged_list):
    """This function takes a list of words without PoS tags as input and returns the number of items
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
    matches1 = re.findall(string1, tagged_string)
    matches2 = re.findall(string2, tagged_string)
    matches3 = re.findall(string3, tagged_string)
    matches4 = re.findall(string4, tagged_string)
    matches5 = re.findall(string5, tagged_string)
    counter = len(matches1) + len(matches2) + len(matches3) + len(matches4) + len(matches5)
    return(counter)    

## function for feature 60: THAT deletion
## this function still needs work!
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
def feature_61(tagged_string):
    """This function takes a string of words with PoS tags as input and returns the number of items
    that are stranded prepositions."""
    string1 = r"_IN\s\S_."
    matches1 = re.findall(string1, tagged_string)
    counter = len(matches1)
    return(counter)

## function for feature 62: split infinitives
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

## function for feature 64: phrasal coordination
def feature_64(tagged_string):
    """This function takes a string of words with PoS tags as input and returns
    the number of phrasal coordinations."""
    string1 = r"_[NN|NNS|NNP|NNPS]\sand_\w+\s\w+_[NN|NNS|NNP|NNPS]\b"
    string2 = r"_[RB|RBR|RBS]\sand_\w+\s\w+_[RB|RBR|RBS]\b"
    string3 = r"_[JJ|JJR|JJS]\sand_\w+\s\w+_[JJ|JJR|JJS]\b"
    string4 = r"_[VB|VBD|VBG|VBN|VBP|VBZ]\sand_\w+\s\w+_[VB|VBD|VBG|VBN|VBP|VBZ]\b"
    matches1 = re.findall(string1, tagged_string)
    matches2 = re.findall(string2, tagged_string)
    matches3 = re.findall(string3, tagged_string)
    matches4 = re.findall(string4, tagged_string)
    counter = len(matches1) + len(matches2) + len(matches3) + len(matches4)
    return(counter)

## function for feature 65: non-phrasal coordination
## this function still needs work!
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




















