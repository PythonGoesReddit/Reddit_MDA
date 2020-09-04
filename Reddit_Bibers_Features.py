### these functions:
### - take one of the following items as input (presuming cleaned, lowercase data):
###   - a list with each word as a new item, without PoS-tags (untagged_list)
###   - a list with each word as a new item together with its PoS-tag (tagged_list)
###   - a string containing the whole sentence, each word with its PoS-tag (tagged_string)
### - identify one of Biber's original 67 features
### - return the count of the occurances the feature 


### this doesn't work because with a sting I can run a for-loop over the 
### individual items. - work with strings and re.findall (or similar) instead?

#### -> use .count("") function???

## function for feature 1: past tense
## DONE!
def feature_01(tagged_list):
  """This function takes a list of words with PoS tags as input and returns the number of items
  that are a verb in the past tense."""
  counter = 0
  for item in tagged_list:
    if item == "\w_+_VBD" or item == "\w{5,20}ed_\w+":
      counter = counter + 1
    else:
      pass
  return(counter)

## function for feature 2: verbs in the perfect aspect
def feature_02(tagged_string):
  """This function takes a string of words with PoS tags as input and returns the number of 
  perfect aspect forms."""
  counter = 0
  for item in tagged_string:
    string1 = "[have|has|'ve|'s]_\w+\s\w+_VBD"
    string1a = "[have|has|'ve|'s]_\w+\s\w+_RB\s\w+_VBD"
    string1b = "[have|has|'ve|'s]_\w+\s\w+_RB\s\w+_RB\s\w+_VBD"
    string2 = "[have|has]_\w+\s\w+_[NN|NNS|NNP|NNPS|PRP|PRP$]\s\w+_VBD"
    if item == string1 or item == string2 or item == string1a or item == string1b:
## problem with for-loop over string
      counter = counter + 1
    else:
      pass
  return(counter)

## function for feature 3: present tense
def feature_03(tagged_list):
  """This function takes a list of words with PoS tags as input and returns the number of 
  verbs in the present tense."""
  counter = 0
## excluding infinitives, so "to" in front of the string
  for item in tagged_list:
    if item == "\w+_VB" or item == "\w+_VBZ":
      counter = counter + 1
    else:
      pass
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
  for item in tagged_list:
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
  for item in tagged_list:
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
  for item in tagged_list:
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
  for item in tagged_list:
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
  for item in tagged_list:
    if item == "it":
      counter = counter + 1
    else:
      pass
  return(counter)

## function for feature 10: demonstrative pronouns
def feature_10(tagged_string):
  """This function takes a list of words with PoS tags as input and returns the number of items
  that are demonstrative pronouns."""
  counter = 0
  string1 = "[that|this|these|those]_\w+\s\w+_[VB|VBD|VBG|VBN|VBP|VBZ|MD|WP]"
  string1a = "[that|this|these|those]_\w+\s[and|\.]"
  string2 = "that_\w+\s's"
  for item in tagged_string:
      if item == string1 or item == string1a or item == string2:
          counter = counter + 1
      else:
          pass
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
def feature_12(tagged_string):
  """This function takes a string of words with PoS tags as input and returns the number of items
  that are DO used as a pro-verb."""
  counter = 0
  string1 = "[do|does|doing|did|done]"
  for item in tagged_string:
    if item == string1:
      counter = counter + 1
    else:
      pass
  return(counter)
## every instance of DO if not in the following constructions:
## DO + (ADV) + V
## ALL-P/WHP + DO

## function for feature 13: WH-questions
def feature_13(tagged_string):
  """This function takes a string of words with PoS tags as input and returns the number of items
  that are WH-questions."""
  counter = 0
  string1 = "\._\S+\swho_\w+\s\w+_MD"
  for item in tagged_string:
    if item == string1:
      counter = counter + 1
    else:
      pass
  return(counter)

## function for feature 14: Nominalisations
## DONE!!
def feature_14(tagged_list):
  """This function takes a list of words with PoS tags as input and returns the number of items
  that are nominalisations."""
  counter = 0
  string1 = "\w+[tions?|ments?|ness|ity|nesses|ities]_\w+"
  for item in tagged_list:
    if item == string1:
      counter = counter + 1
    else:
      pass
  return(counter)

## function for feature 15: gerunds
def feature:
## all participle forms serving nominal functions, edited manually

## function for feature 16: nouns
## DONE!
def feature_16(tagged_list):
  """This function takes a list of words with PoS tags as input and returns the number of items
  that are nouns (excluding nominalisations)."""
  counter = 0
  string1 = "\w+_NNS?"
  string2 = "\w+[tions?|ments?|ness|ity|nesses|ities]_\w+"
  for item in tagged_list:
    if item == string1 and not item == string2:
      counter = counter + 1
    else:
      pass
  return(counter)    

## function for feature 17: agentless passives
def feature:
## BE + (ADV) + (ADV) + VBN not followed by BY
## BE + N/PRO + VBN not followed by BY

## function for feature 18: BY passives
def feature:
## BE + (ADV) + (ADV) + VBN + BY
## BE + N/PRO + VBN + BY

## function for feature 19: BE as main verb
def feature_19(tagged_string):
 """This function takes a string of words with PoS tags as input and returns the number of items
  that are BE used as a main verb."""
  counter = 0
  string1 = "[am|are|is|was|were|been]_\w+\s\w+_[DT|PRP$|IN|JJ|JJR|JJS]\s"
  for item in tagged_string:
    if item == string1:
      counter = counter + 1
    else:
      pass
  return(counter)  

## function for feature 20: existential THERE
def feature_20(tagged_string):
  """This function takes a string of words with PoS tags as input and returns the number of items
  that are existential 'there'."""
  counter = 0
  string1 = "\sthere_\w+\s[am|are|is|was|were|been]_"
  string2 = "\sthere_\w+\s\w+_\w+\s[am|are|is|was|were|been]_"
  string3 = "\sthere_\w+\s's"
  for item in tagged_string:
    if item == string1 or item == string2 or item == string3:
      counter = counter + 1
    else:
      pass
  return(counter)

## function for feature 21: THAT verb complements
def feature_21(tagged_string):
  """This function takes a string of words with PoS tags as input and returns the number of items
  that are verbal complements with 'that'."""
  counter = 0
  string1 = "[and|nor|but|or|also|\.]_\w+\sthat_\w+\s\w+_[DT|NNS|NNP|NNPS|PRP|PRP$]"
  string1a = "[and|nor|but|or|also|\.]_\w+\sthat_\w+\sthere_\w+"
  string2 = ""
  string3 = ""
  for item in tagged_string:
    if item == string1:
      counter = counter + 1
    else:
      pass
  return(counter)
## PUB/PRV/SUA/SEEM/APPEAR + that + xxx (where xxx is not V/AUX/CL-p/and)
## PUB/PRV/SUA + PREP + xxx + N + that (where xxx is and number of words but 
## not xxx = N)
    

## function for feature 22: THAT adjective complements
def feature_22(tagged_string):
  """This function takes a string of words with PoS tags as input and returns the number of items
  that are "that" followed by adjectival complements."""
  counter = 0
  for item in tagged_string:
    if item == "\w+_JJ\sthat":
      counter = counter + 1
    else:
      pass
  return(counter)

## function for feature 23: WH clauses
def feature_23(tagged_string):
  """This function takes a string of words with PoS tags as input and returns the number of items
  that are wh-clauses."""
  counter = 0
  string1 = "\s[]_\w+\s[]_\w+\s\w+_"
  string2 = "\s[]_\w+\s[]_\w+\s\w+_MD\s"
  for item in tagged_string:
    if item == string1 and not item == string2:
      counter = counter + 1
    else:
      pass
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
  counter = 0
  string1 = "\sto_\w+\s\w+_VB\s"
  string2 = "\sto_\w+\s\w+_RB\s\w+_VB\s"
  for item in tagged_string:
    if item == string1 or item == string2:
      counter = counter + 1
    else:
      pass
  return(counter)

## function for feature 25: present participial clauses
def feature_25(tagged_string):
  """This function takes a string of words with PoS tags as input and returns the number of items
  that are infinitives."""
  counter = 0
  string1 = ".\s\w+_VBG\s\w+_[IN|DT|RB|RBR|RBS|PRP|PRP$]\s"
  string2 = ".\s\w+_VBG\s[]_\w+\s"
  for item in tagged_string:
    if item == string1 or item == string2:
      counter = counter + 1
    else:
      pass
  return(counter)
## ALL-P + VBG + WHP/WHO
## (edited manually)

## function for feature 26: past participial clauses
def feature_26(tagged_string):
  """This function takes a string of words with PoS tags as input and returns the number of items
  that are past participial clauses."""
  counter = 0
  string1 = ".\s\w+_VBD\s\w+_[IN|RB|RBR|RBS]\s"
  string2 = ".\s\w+_VBG\s[]_\w+\s"
  for item in tagged_string:
    if item == string1 or item == string2:
      counter = counter + 1
    else:
      pass
  return(counter)
## (edited manually)

## function for feature 27: past prt. WHIZ deletions
def feature:
## N/QUANPRO + VBN + PREP/BE/ADV (edited manually)

## function for feature 28: present prt. WHIZ deletions
def feature:
## N + VBG (edited manually)

## function for feature 29: THAT relatives, subject position
def feature_29(tagged_string):
  """This function takes a string of words with PoS tags as input and returns the number of items
  that are relative clauses with 'that' in subject position."""
  counter = 0
  string1 = "\w+_[NN|NNS]\sthat_\w+\s\w+_[MD|VB|VBD|VBG|VBN|VBP|VBZ]"
  string2 = "\w+_[NN|NNS]\sthat_\w+\s\w+_RB\s\w+_[MD|VB|VBD|VBG|VBN|VBP|VBZ]"
  for item in tagged_string:
    if item == string1 or item == string2:
      counter = counter + 1
    else:
      pass
  return(counter)

## function for feature 30: THAT relatives, object position
def feature:
## N + that + DET/SUBJPRO/POSSPRO/it/ADJ/pluralnoun/propernoun/possessive
## noun/TITLE

## function for feature 31: WH relatives, subject position
def feature:
## xxx + yyy + N + WHP + (ADV) + AUX/V
## where xxx is NOT any form of the verbs ASK or TELL

## function for feature 32: WH relatives, object position
def feature:
## xxx + yyy + N + WHP + zzz

## function for feature 33: WH relatives, pied piping
def feature:
## PREP + WHP

## function for feature 34: sentence relatives
def feature:
## ??

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
def feature_38(untagged_list):
  """This function takes a list of words with PoS tags as input and returns the number of items
  that are adverbial subordinators with multiple function."""
  counter = 0
  advsubordlist = ["since", "while", "whilst", "whereupon", "whereas", "whereby",
                   "such that", "inasmuch as", "forasmuch as", "insofar as", 
                   "insomuch as", "as long as", "as soon as"]
  ## add to advsubordlist: "so that XXX" and "such that XXX", with XXX being
  ## everything but noun or adjective
  for item in untagged_list:
    if item in advsubordlist:
      counter = counter + 1
    else:
      pass
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
def feature_40(tagged_string):
  """This function takes a string of words with PoS tags as input and returns the number of items
  that are attributive adjectives."""
  counter = 0
  string1 = "\s\w+_[JJ|JJR|JJS]\s\w+_[JJ|JJR|JJS|NN|NNS]"
  for item in tagged_string:
    if item == string1:
      counter = counter + 1
    else:
      pass
  return(counter)

## function for feature 41: predicative adjective
def feature:
## BE + ADJ + xxx where xxx is NOT an ADJ/ADV/N
## BE + ADJ + ADV + xxxx where xxx is NOT ADJ/N

## function for feature 42: adverbs
def feature_42(tagged_list):
  """This function takes a list of words with PoS tags as input and returns the number of items
  that are adverbs."""
  counter = 0
  for item in untagged_list:
    if item == "\w+_[RB|RBR|RBS]":
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
  meanwl=sum(wordlengths)/nwords
  return(meanWL)

## function for feature 45: conjuncts
def feature_45(untagged_list):
  """This function takes a list of words without PoS tags as input and returns the number of items
  that are conjuncts."""
  counter = 0
  conjunctslist = ["alternatively", "altogether", "consequently", "conversely",
                   "eg", "e.g.", "else", "furthermore", "hence", "however", 
                   "i.e.", "instead", "likewise", "moreover", "namely", "nevertheless",
                   "nonetheless", "notwithstanding", "otherwise", "rather",
                   "similarly", "therefore", "thus", "viz."]
  for item in untagged_list:
    if item in conjunctslist:
      counter = counter + 1
    else:
      pass
  return(counter)
    
## in + [comparison|contrast|particular|addition|conclusion|consequence|sum|
## summary|any event|any case|other words]
    
## for + [example|instance]
## by + [contrast|comparison]
## as a + [result|consequence]
## on the + [contrary|other hand]
## ALL-P + [that is|else|altogether] + ,
## ALL-P + rather + ,/xxx (where xxx is not ADJ/ADV)

## function for feature 46: downtoners
## DONE!
def feature_06(untagged_list):
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
def feature:
## [at about|somthing like|more or less|almost|maybe|xxx sort of|xxx kind of]
## where xxx is not DET/ADJ/POSSPRO/WHO

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
def feature:
## [for sure|a lot|such a|real + ADJ|so + ADJ|DO + V|just|really|most|more]

## function for feature 50: discourse particles
def feature_50(tagged_strings):
"""This function takes a list of words with PoS tags as input and returns the number of items
  that are discourse particles."""
  counter = 0
  for item in tagged_string:
    if item == "[\.|!|\?|:|;|-]_\w+\s[well|now|anyway|anyhow|anyways]":
      counter = counter + 1
    else:
      pass
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
  "grant", "insist", "instruct", "ordain", "pledge", pronounce", "propose", "recommend", 
  "request", "stipulate", "suggest", "urge"]
  for item in untagged_list:
    if item in suasiveverbslist:
      counter = counter + 1
    else:
      pass
  return(counter)

## function for feature 58: SEEM/APPEAR
## DONE!
def feature_06(untagged_list):
  """This function takes a list of words with PoS tags as input and returns the number of items
  that are the verbs SEEM or APPEAR."""
  counter = 0
  for item in untagged_list:
    if item == "appear" or item == "seem":
      counter = counter + 1
    else:
      pass
  return(counter)

## function for feature 59: contractions
def feature:
## all contractions on pronouns
## all contractions on auxiliary forms (negation)
## separately: 's suffixed on nouns:
##  N's + AUX/ADV+V/ADV+AUX/DET/POSSPRO/PREP/ADJ+CL-P

## function for feature 60: THAT deletion
def feature:
## PUB/PRV/SUA + demonstrative pronoun/subjectpronoun
## PUB/PRV/SUA + PRO/N + AUX/V
## PUB/PRV/SUA + ADJ/ADV/DET/POSSPRO + (ADJ) + N + AUX/V

## function for feature 61: stranded prepositions
def feature_61(tagged_string):
  """This function takes a string of words with PoS tags as input and returns the number of items
  that are stranded prepositions."""
  counter = 0
  string1 = "\w+_IN\s\S_."
  for item in tagged_string:
    if item == string1:
      counter = counter + 1
    else:
      pass
  return(counter)

## function for feature 62: split infinitives
def feature_62(tagged_string):
  """This function takes a string of words with PoS tags as input and returns the number of items
  that are the verbs SEEM or APPEAR."""
  counter = 0
  string1 = "\sto_\w+\s\w+_[RB|RBR|RBS]\s\w+_VB\s"
  string2 = "\sto_\w+\s\w+_[RB|RBR|RBS]\s\w+_[RB|RBR|RBS]\s\w+_VB\s"
  for item in tagged_string:
    if item == string1 or item == string2:
      counter = counter + 1
    else:
      pass
  return(counter)

## function for feature 63: split auxiliaries
def feature_63(tagged_string):
  """This function takes a string of words with PoS tags as input and returns the number of items
  that are split auxiliaries."""
  counter = 0
  string1 = "\s\w+_MD\s\w+_[RB|RBR|RBS]\s\w+_VB\s"
  string2 = "\s\w+_MD\s\w+_[RB|RBR|RBS]\s\w+_[RB|RBR|RBS]\s\w+_VB\s"
  for item in tagged_string:
    if item == string1 or item == string2:
      counter = counter + 1
    else:
      pass
  return(counter)

## function for feature 64: phrasal coordination
def feature_64(tagged_string):
  """This function takes a string of words with PoS tags as input and returns
  the number of phrasal coordinations."""
  counter = 0
  string1 = "\w+_[NN|NNS|NNP|NNPS]\sand_\w+\s\w+_[NN|NNS|NNP|NNPS]\s"
  string2 = "\w+_[RB|RBR|RBS]\sand_\w+\s\w+_[RB|RBR|RBS]\s"
  string3 = "\w+_[JJ|JJR|JJS]\sand_\w+\s\w+_[JJ|JJR|JJS]\s"
  string4 = "\w+_[VB|VBD|VBG|VBN|VBP|VBZ]\sand_\w+\s\w+_[VB|VBD|VBG|VBN|VBP|VBZ]\s"
  for item in tagged_string:
    if item == string1 or item == string2 or item == string3 or item == string4:
      counter = counter + 1
    else:
      pass
  return(counter)

## function for feature 65: non-phrasal coordination
def feature:
## , + and + it/so/then/you/there+BE/demonstrativepronoun/SUBJPRO
## CL-P + and
## and + WHP/WHO/adverbial subordinator/discourseparticle/conjunct

## function for feature 66: synthetic negation
def feature_66(tagged_string):
  """This function takes a string of words with PoS tags as input and returns the number of items
  that are NOT (= analytic negation)."""
  counter = 0
  string1 = 
  string2 = 
  for item in untagged_list:
    if item == string1 or item == string2:
      counter = counter + 1
    else:
      pass
  return(counter)
## no + QUANT/ADJ/N
## neither, nor

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
  
  
  
  
## additional featuer 2: superlatives





















