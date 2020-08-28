### this code should:
### - take PoS-tagged monthly files (in txt or dictionary format) as input
### - identify the original 67 features of Biber's analysis
### - count the occurances for each feature by comment
### - save the feature count for each feature for each comment to a new 
### txt-file (which can later be combined with the additional features)

### this code presupposes cleaned, all-lowercase, POS-tagged data!

### for some functions it makes more sense to use an untagged list, the script
### should therefore produce both an untagged and a tagged list which can
### then be accessed by the functions as needed

### for some functions it makes more sense to have the tagged comment as 
### one long string, not at split items in a list. 
### produce two versions of each tagged comment and then have each function
### specify which version they want?

### this doesn't work because with a sting I can run a for-loop over the 
### individual items. - work with strings and re.findall (or similar) instead?


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
  string1a = "[that|this|these|those]_\w+\s[and]"
## still missing: followed by punctuation!
  string2 = "that_\w+\s's"
  for item in tagged_string:
      if item == string1 or item == string2:
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
  string1 = "[\.|!|\?|:|;|-]_\w+\swho_\w+\s\w+_MD"
  for item in tagged_string:
    if item == string1:
      counter = counter + 1
    else:
      pass
  return(counter)

## function for feature 14: Nominalisations
def feature:
## all words ending in -tion, -ment, -ness, -ity plus plural forms
## regex: \b\w+tions?_\w+\b \b\w+ments?_\w+\b \b\w+ness_\w+\b
##        \b\w+ity_\w+\b \b\w+nesses_\w+\b \b\w+ities_\w+\b

## function for feature 15: gerunds
def feature:
## all participle forms serving nominal functions, edited manually

## function for feature 16: nouns
def feature:
## all nouns in the dictionary, excluding those forms counted as nominalisations
## or gerunds
## regex: \b\w+_NNS?\b if not in:
##        \b\w+tions?_\w+\b \b\w+ments?_\w+\b \b\w+ness_\w+\b
##        \b\w+ity_\w+\b \b\w+nesses_\w+\b \b\w+ities_\w+\b
    

## function for feature 17: agentless passives
def feature:
## BE + (ADV) + (ADV) + VBN not followed by BY
## BE + N/PRO + VBN not followed by BY

## function for feature 18: BY passives
def feature:
## BE + (ADV) + (ADV) + VBN + BY
## BE + N/PRO + VBN + BY

## function for feature 19: BE as main verb
def feature:
## BE + DET/POSSPRO/TITLE/PREP/ADJ

## function for feature 20: existential THERE
def feature:
## there + (xx) + BE
## there's
## regex: \bthere_\w+\sis

## function for feature 21: THAT verb complements
def feature:
## and/nor/but/or/also/ALL-P + that + DET/PRO/there/plural noun/proper noun/TITLE
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
def feature:
## PUB/PRV/SUA + WHP/WHO + xxx (where xxx is not AUX)

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
def feature:
## ALL-P + VBG + PREP/DET/WHP/WHO/PRO/ADV
## (edited manually)

## function for feature 26: past participial clauses
def feature:
## ALL-P + VBN +PREP/ADV (edited manually)

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
def feature:
## ADJ + ADJ/N

## function for feature 41: predicative adjective
def feature:
## BE + ADJ + xxx where xxx is NOT an ADJ/ADV/N
## BE + ADJ + ADV + xxxx where xxx is NOT ADJ/N

## function for feature 42: adverbs
def feature:
## total of all adverbs

## function for feature 43: type/token ratio
def feature:
## see function from class?

## function for feature 44: word length
def feature:
## mean length of all the words in the text

## function for feature 45: conjuncts
def feature:
## [alternatively|altogether|consequently|conversely|eg|e.g.|else|furthermore|
## hence|however|i.e.|instead|likewise|moreover|namely|nevertheless|nonetheless|
## notwithstanding|otherwise|rather|similarly|therefore|thus|viz.]
    
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
def feature:
## PREP + ALL-P

## function for feature 62: split infinitives
def feature:
## to + ADV + (ADV) + VB

## function for feature 63: split auxiliaries
def feature:
## AUX + ADV + (ADV) + VB

## function for feature 64: phrasal coordination
def feature:
## xxx1 + and + xxx2
## where xxx1 and xxx2 are both ADV/ADJ/V/N

## function for feature 65: non-phrasal coordination
def feature:
## , + and + it/so/then/you/there+BE/demonstrativepronoun/SUBJPRO
## CL-P + and
## and + WHP/WHO/adverbial subordinator/discourseparticle/conjunct

## function for feature 66: synthetic negation
def feature:
## no + QUANT/ADJ/N
## neither, nor

## function for feature 67: analytic negation
## DONE!
def feature_06(tagged_list):
  """This function takes a list of words with PoS tags as input and returns the number of items
  that are NOT (= analytic negation)."""
  counter = 0
  for item in tagged_list:
    if item == "not":
      counter = counter + 1
    else:
      pass
  return(counter)






















