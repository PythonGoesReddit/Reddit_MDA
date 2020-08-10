### this code should:
### - take PoS-tagged monthly files (in txt or dictionary format) as input
### - identify the original 67 features of Biber's analysis
### - count the occurances for each feature by comment
### - save the feature count for each feature for each comment to a new txt-file (which can later be combined with the additional features)

import os

path = >>>specify file path here<<<

## function for feature 1: past tense
def feature_01(tagged_list):
  """This function takes a list of words with PoS tags as input and returns the number of items
  that are a verb in the past tense."""
  counter = 0
  pastlist = []
# this "pastlist" should contain "any past tense form that occurs in the dictionary, or
# any word not otherwise identified that is longer than six letters and ends in ed."
  for item in tagged_list:
    if item in pastlist:
      counter = counter + 1
    else:
      pass
  return(counter)

## function for feature 2: verbs in the perfect aspect
def feature_02(tagged_list):
  """This function takes a list of words with PoS tags as input and returns the number of 
  perfect aspect forms."""
  counter = 0
  for item in tagged_list:
    if       :
# HAVE + (ADV) + (ADV) + VBN
# or HAVE + N/PRO + VBN
      counter = counter + 1
    else:
      pass
  return(counter)

## function for feature 3: present tense
def feature

## function for feature 4: place adverbials
def feature_04(tagged_list):
  """This function takes a list of words with PoS tags as input and returns the number of items
  that are place adverbials."""
  counter = 0
  placelist = ["aboard", "above", "abroad", "across", "ahead", "alongside", "around", 
  "ashore", "astern", "away", "behind", "below", "beneath", "beside", "downhill",
  "downstairs", "downstream", "east", "far", "hereabouts", "indoors", "inland", "inshore",
  "inside", "locally", "near", "nearby", "north", "nowhere", "outdoors", "outside", 
  "overboard", "overland", "overseas", "south", "underfoot", "underground", "underneath",
  "uphill", "upstairs", "upstream", "west"]
  for item in tagged_list:
    if item in placelist:
      counter = counter + 1
    else:
      pass
  return(counter)

## function for feature 5: time adverbials
def feature_05(tagged_list):
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
def feature_06(tagged_list):
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
def feature_07(tagged_list):
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
def feature_08(tagged_list):
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
def feature_09(tagged_list):
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
def feature

## function for feature 11: indefinite pronouns
def feature_11(tagged_list):
  """This function takes a list of words with PoS tags as input and returns the number of items
  that are indefinite pronouns."""
  counter = 0
  indefpronounlist = ["anybody", "anyone", "anything", "everybody", "everyone",
  "everything", "nobody", "none", "nothing", "nowhere", "somebody", "someone", "something"]
  for item in tagged_list:
    if item in indefpronounlist:
      counter = counter + 1
    else:
      pass
  return(counter)

## function for feature 12: DO as pro-verb
def feature

## function for feature 13: WH-questions
def feature

## function for feature 14: Nominalisations
def feature

## function for feature 15: gerunds
def feature

## function for feature 16: nouns
def feature

## function for feature 17: agentless passives
def feature

## function for feature 18: BY passives
def feature

## function for feature 19: BE as main verb
def feature

## function for feature 20: existential THERE
def feature

## function for feature 21: THAT verb complements
def feature

## function for feature 22: THAT adjective complements
def feature

## function for feature 23: WH clauses
def feature

## function for feature 24: infinitives
def feature

## function for feature 25: present participial clauses
def feature

## function for feature 26: past participial clauses
def feature

## function for feature 27: past prt. WHIZ deletions
def feature

## function for feature 28: present prt. WHIZ deletions
def feature

## function for feature 29: THAT relatives, subject position
def feature

## function for feature 30: THAT relatives, object position
def feature

## function for feature 31: WH relatives, subject position
def feature

## function for feature 32: WH relatives, object position
def feature

## function for feature 33: WH relatives, pied piping
def feature

## function for feature 34: sentence relatives
def feature

## function for feature 35: adv. subordinator, cause
def feature

## function for feature 36: adv. subordinator, concession
def feature

## function for feature 37: adv. subordinator, condition
def feature

## function for feature 38: adv. subordinator, other
def feature

## function for feature 39: preposition
def feature_39(tagged_list):
  """This function takes a list of words with PoS tags as input and returns the number of items
  that are prepositions."""
  counter = 0
  prepositionlist = ["against", "amid", "amidst", "among", "amongst", "at", "besides",
  "between", "by", "despite", "during", "except", "for", "from", "in", "into", "minus",
  "notwithstanding", "of", "off", "on", "onto", "opposite", "out", "per", "plus", "pro",
  "re", "than", "through", "throughout", "thru", "to", "toward", "towards", "upon", 
  "versus", "via", "with", "within", "without"]
  for item in tagged_list:
    if item in prepositionlist:
      counter = counter + 1
    else:
      pass
  return(counter)

## function for feature 40: attributive adjective
def feature

## function for feature 41: predicative adjective
def feature

## function for feature 42: adverbs
def feature

## function for feature 43: type/token ratio
def feature

## function for feature 44: word length
def feature

## function for feature 45: conjuncts
def feature

## function for feature 46: downtoners
def feature_06(tagged_list):
  """This function takes a list of words with PoS tags as input and returns the number of items
  that are downtoners."""
  counter = 0
  downtonerlist = ["almost", "barely", "hardly", "merely", "mildly", "nearly", "only",
  "partially", "partly", "practically", "scarcely", "slightly", "somewhat"]
  for item in tagged_list:
    if item in downtonerlist:
      counter = counter + 1
    else:
      pass
  return(counter)

## function for feature 47: hedges
def feature

## function for feature 48: amplifiers
def feature_48(tagged_list):
  """This function takes a list of words with PoS tags as input and returns the number of items
  that are amplifiers."""
  counter = 0
  amplifierlist = ["absolutely", "altogether", "completely", "enormously", "entirely", 
  "extremely", "fully", "greatly", "highly", "intensely", "perfectly", "strongly", 
  "thoroughly", "totally", "utterly", "very"]
  for item in tagged_list:
    if item in amplifierlist:
      counter = counter + 1
    else:
      pass
  return(counter)

## function for feature 49: emphatics
def feature

## function for feature 50: discourse particles
def feature

## function for feature 51: demonstratives
def feature_51(tagged_list):
  """This function takes a list of words with PoS tags as input and returns the number of items
  that are demonstratives."""
  counter = 0
  demonstrativelist = ["that", "this", "these", "those"]
  for item in tagged_list:
    if item in demonstrativelist:
      counter = counter + 1
    else:
      pass
  return(counter)

## function for feature 52: possibility modals
def feature_52(tagged_list):
  """This function takes a list of words with PoS tags as input and returns the number of items
  that are possibility modals."""
  counter = 0
  possmodalslist = ["can", "might", "may", "could"]
  for item in tagged_list:
    if item in possmodalslist:
      counter = counter + 1
    else:
      pass
  return(counter)

## function for feature 53: necessity modals
def feature_53(tagged_list):
  """This function takes a list of words with PoS tags as input and returns the number of items
  that are necessity modals."""
  counter = 0
  nessmodalslist = ["ought", "should", "must"]
  for item in tagged_list:
    if item in nessmodalslist:
      counter = counter + 1
    else:
      pass
  return(counter)

## function for feature 54: predictive modals
def feature_54(tagged_list):
  """This function takes a list of words with PoS tags as input and returns the number of items
  that are predictive modals."""
  counter = 0
  predmodalslist = ["will", "would", "shall"]
  for item in tagged_list:
    if item in predmodalslist:
      counter = counter + 1
    else:
      pass
  return(counter)

## function for feature 55: public verbs
def feature_55(tagged_list):
  """This function takes a list of words with PoS tags as input and returns the number of items
  that are public verbs."""
  counter = 0
  publicverbslist = ["acknowledge", "admit", "agree", "assert", "claim", "complain", 
  "declare", "deny", "explain", "hint", "insist", "mention", "proclaim", "promise",
  "protest", "remark", "reply", "report", "say", "suggest", "swear", "write"]
  for item in tagged_list:
    if item in publicverbslist:
      counter = counter + 1
    else:
      pass
  return(counter)

## function for feature 56: private verbs
def feature_56(tagged_list):
  """This function takes a list of words with PoS tags as input and returns the number of items
  that are private verbs."""
  counter = 0
  privateverbslist = ["anticipate", "assume", "believe", "conclude", "decide", "demonstrate",
  "determine", "discover", "doubt", "estimate", "fear", "feel", "find", "forget", "guess",
  "hear", "hope", "imagine", "imply", "indicate", "infer", "know", "learn", "mean", "notice",
  "prove", "realize", "recognize", "remember", "reveal", "see", "show", "suppose", "think",
  "understand", "realise", "recognise"]
  for item in tagged_list:
    if item in privateverbslist:
      counter = counter + 1
    else:
      pass
  return(counter)

## function for feature 57: suasive verbs
def feature_57(tagged_list):
  """This function takes a list of words with PoS tags as input and returns the number of items
  that are suasive verbs."""
  counter = 0
  suasiveverbslist = ["agree", "arrange", "ask", "beg", "command", "decide", "demand",
  "grant", "insist", "instruct", "ordain", "pledge", pronounce", "propose", "recommend", 
  "request", "stipulate", "suggest", "urge"]
  for item in tagged_list:
    if item in suasiveverbslist:
      counter = counter + 1
    else:
      pass
  return(counter)

## function for feature 58: SEEM/APPEAR
def feature_06(tagged_list):
  """This function takes a list of words with PoS tags as input and returns the number of items
  that are the verbs SEEM or APPEAR."""
  counter = 0
  for item in tagged_list:
    if item == "appear" or item == "seem":
      counter = counter + 1
    else:
      pass
  return(counter)

## function for feature 59: contractions
def feature

## function for feature 60: THAT deletion
def feature

## function for feature 61: stranded prepositions
def feature

## function for feature 62: split infinitives
def feature

## function for feature 63: split auxiliaries
def feature

## function for feature 64: phrasal coordination
def feature

## function for feature 65: non-phrasal coordination
def feature

## function for feature 66: synthetic negation
def feature

## function for feature 67: analytic negation
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




