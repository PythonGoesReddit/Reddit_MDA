# Notes on Features
- Add to Biber's original features in numerical order only once the key has been added to feature_dict in open_reddit_json (or is initialized elsewhere)
- Use Biber's original numbers for his features
- Add our own features in the list starting at 200, also only once initialized
- Use the POS-separated list below to decide which functions the features should come in 
- Use the POS-separated list to denote if our implementation of the tagging has been checked and is ready to go 

# Bibers Original Features
- "vpast_001": verbs in past tense
- "vperfect_002": verbs in perfect aspect
- "vpresent_003": verbs in present tense
- "advplace_004": place adverbials
- "advtime_005": time adverbials
- "profirpers_006": first person pronouns
- "prosecpers_007": second person pronouns
- "prothirper_008": third person pronouns
- "proit_009": pronoun "it"

- "nouns_016": total number of nouns

- "whclause_023": WH-clause
- "vinfinitive_024": infinitives
- "vpresentpart_025": present participial clauses
- "vpastpart_026": past participal clauses
- "vpastwhiz_027": past prt. WHIZ deletions
- "vpresentwhiz_028": present prt. WHIZ deletions

- "vpublic_055": public verbs
- "vprivate_056": private verbs
- "vsuasive_057": suasive verbs

- "vseemappear_058": 'seem'/'appear'

- "thatdel_060": 'that' deletion

- "vsplitinf_062": split infinitives

## New features
- "link_202": external links
- "interlink_203": reddit-interal links
- "caps_204": words in all caps

- "vimperative_210": imperative verbs




# Division by POS
## VERBS
### ALL VERBS
- feature 01: verbs in past tense
- feature 02: verbs in perfect aspect
 - feature 03: verbs in present tense
 - feature 24: infinitives  
 - feature 25: present participial clauses
 - feature 26: past participial clauses
 - feature 27: past prt. WHIZ deletions
 - feature 28: present prt. WHIZ deletions
 - feature 62: split infinitives
 - imperatives (listed as feature 4 in the other script) KM

## FULL VERBS ONLY
 - feature 58: 'seem'/'appear'
 - feature 55: public verbs
 - feature 56: private verbs
 - feature 57: suasive verbs
 - feature 23: WH-clauses (depend on public/private/suasive verbs)
 - feature 60: THAT deletion (depends on public/private/suasive verbs)
   PRIMARY VERBS ONLY
 - feature 12: 'do' as a pro-verb
 - feature 19: 'be' as main verb
 - feature 17: agentless passives
 - feature 18: 'by' passives
 - feature 59: contractions
   MODAL AUXILIARIES ONLY
 - feature 52: possibility modals
 - feature 53: necessity modals
 - feature 54: predictive modals
 - feature 63: split auxiliaries
 - feature 59: contractions

 ## ADVERBS:
 - feature 04: place adverbials
 - feature 05: time adverbials
 - feature 35: adv. subordinator, cause ('because')
 - feature 36: adv. subordinator, concession
 - feature 37: adv. subordinator, condition
 - feature 38: adv. subordinator, other
 - feature 42: total adverbs
 - feature 48: amplifiers
 - feature 67: analytic negation
 - feature 46: downtoners

 ## ADJECTIVES
 - feature 40: attributive adjective
 - feature 41: predicative adjective
 - additional feature 1: comparatives
 - additional feature 2: superlatives

 ## PREPOSITIONS
 - feature 39: preposition
 - feature 61: stranded prepositions

 ## NOUNS
 - feature 14: nominalisations
 - feature 15: gerunds
 - feature 16: total nouns

 ## PRONOUNS
 - feature 06: first person pronouns
 - feature 07: second person pronouns
 - feature 08: third person pronouns
 - feature 09: pronoun 'it'
 - feature 10: demonstrative pronouns
 - feature 11: indefinite pronouns
 - feature 59: contractions
  
 ## CONJUNCTIONS
 - feature 64: phrasal coordination
 - feature 65: non-phrasal coordination

 ## DETERMINERS:
 - feature 66: synthetic negation  
 - feature 51: demonstratives
  
 ## WH-stuff (basically all tags starting with W)
 - feature 34: sentence relatives ('which')
 - feature 31: WH relatives, subject position
 - feature 32: WH relatives, object position
 - feature 33: WH relatives, pied piping
 - feature 13: WH-questions

 ## WHOLE SENTENCE
 - feature 43: type/token ratio
 - feature 44: word length

## UNCLEAR:
 - feature 20: existential 'there' -> what would 'there' be tagged as?
 - feature 21: 'that' verb complements -> what would 'that' be tagged as?
 - feature 22: 'that' adjective complements -> what would 'that' be tagged as?
 - feature 29: 'that' relatives, subject position
 - feature 30: 'that' relatives, object position
 - feature 45: conjuncts (belong to multiple word classes)
 - feature 47: hedges (belong to multiple word classes)
 - feature 49: emphatics (belong to multiple word classes)
 - feature 50: discourse particles -> what would they be tagged as?

