import os

# List of all features:
feats = {"vpast_001": "SIMPLE PAST VERB FORMS", # done by HM
"vpresperfect_002a": "PRESENT PERFECT VERB FORMS", # done by HM
"vpastperfect_002b": "PAST PERFECT VERB FORMS", 
"vpresent_003": "PRESENT TENSE VERB FORMS",
"advplace_004": "PLACE ADVERBIALS", # RT
"advtime_position_005a": "TIME ADVERBIALS - POINTS IN TIME",
"advtime_durfreq_005b": "TIME ADVERBIALS - DURATION AND FREQUENCY",
"profirpers_006": "FIRST PERSON PRONOUNS", # done by HM
"prosecpers_007": "SECOND PERSON PRONOUNS", # done by HM
"prothirdper_008": "THIRD PERSON PRONOUNS", # done by HM
"proit_009": "PRONOUN IT", # done by HM
"prodemons_010": "DEMONSTRATIVE PRONOUNS",
"proindef_011": "INDEFINITE PRONOUNS",
"pverbdo_012": "PRO-VERB DO",
"whquest_013": "WH QUESTIONS",
"nominalis_014": "NOMINALIZATION (-TION(S), -MENT(S), -NESS(ES), -ITY(IES)", #RT
"gerund_015": "GERUNDS",
"nouns_016": "NOUNS",
"passagentl_017": "AGENTLESS PASSIVES",
"passby_018": "BY-PASSIVES",
"mainvbe_019": "MAIN VERB BE",
"exthere_020": "EXISTENTIAL THERE", # done by HM
"thatvcom_021": "THAT AS A VERBAL COMPLEMENT",
"thatacom_022": "THAT AS AN ADJECTIVAL COMPLEMENT",
"whclause_023": "WH CLAUSES",
"vinfinitive_024": "VERBAL INFIITIVES",
"vpresentpart_025": "VERBAL PRESENT PARTICIPLE (???)",
"vpastpart_026": "VERBAL PAST PARTICIPLE (???)", 
"vpastwhiz_027": "PAST PARTICIPIAL WHIZ DELETION (E.G.: THE SOLUTION PRODUCED BY THIS PROCESS)",
"vpresentwhiz_028":"PRESENT PARTICIPIAL WHIZ DELETION (E.G.: THE EVENT CAUSING THIS DECLINE)",
"thatresub_029": "THAT RC WITH SUBJECT POSITION (THE BOY THAT LIVED)",
"thatreobj_030": "THAT RC WITH OBJECT POSITION (THE SCRIPT THAT I WROTE)",
"whresub_031": "WH RC WITH SUBJECT POSITION (THE BOY WHO LIVED)",
"whreobj_032": "WH RC WITH OBJECT POSITION (THE MAN WHO SALLY LIKES)",
"whrepied_033": "WH RC WITH PIED PIPING (THE MANNER IN WHICH HE WAS TOLD)",
"sentencere_034": "SENTENCE RELATIVES (KIM DREAMS IN PYTHON, WHICH IS A BIT SCARY)",
"advsubcause_035": "ADVERBIAL SUBORDINATOR BECAUSE", 
"advsubconc_036": "CONCESSIVE ADVERBIAL SUBORDINATOR (AL)THOUGH",
"advsubcond_037": "CONDITIONAL ADVERBIAL SUBORDINATORS IF/UNLESS",
"advsubother_038": "OTHER ADVERBIAL SUBORDINATORS (LOOK UP THE LIST BEFORE CODING)",
"prepositions_039": "PREPOSITIONS",
"adjattr_040": "ATTRIBUTIVE ADJECTIVES",
"adjpred_041": "PREDICATIVE ADJECTIVES",
"adverbs_042": "ADVERBS",
"ttratio_043": "TYPE-TOKEN-RATIO (PROBABLY WORTHLESS FOR SHORT-TEXT MDA)",
"wordlength_044": "WORD LENGTH (USE MEAN INSTEAD OF COUNT FOR THIS)",
"conjuncts_045": "CONJUNCTS (LOOK UP LIST BEFORE CODING",
"downtoners_046": "DOWNTONERS (LOOK UP LIST BEFORE CODING",
"hedges_047": "HEDGES (LOOK UP LIST BEFORE CODING)",
"amplifiers_048": "AMPLIFIERS (LOOK UP LIST BEFORE CODING)",
"emphatics_049": "EMPHATICS (LOOK UP LIST BEFORE CODING)",
"discpart_050": "DISCOURSE PARTICLES (LOOK UP LIST BEFORE CODING)",
"demonstr_051": "DEMONSTRATIVE DETERMINATIVES (THAT, THIS, THESE, THOSE AS DETERMINERS)",
"modalsposs_052": "POSSIBILITY MODALS CAN, MAY, MIGHT, COULD (INCLUDING CONTRACTED FORMS)",
"modalsness_053": "NECESSITY MODALS OUGHT, SHOULD, MUST (INCLUDING CONTRACTED FORMS)",
"modalspred_054": "PREDICTIVE MODALS WILL, WOULD, SHALL (INCLUDING CONTRACTED FORMS)",
"vpublic_055": "PUBLIC VERBS (LOOK UP LIST BEFORE CODING)",
"vprivate_056": "PRIVATE VERBS (LOOK UP LIST BEFORE CODING)",
"vsuasive_057": "SUASIVE VERBS (LOOK UP LIST BEFORE CODING)",
"vseemappear_058": "SEEM/APPEAR",
"contractions_059": "CONTRACTIONS (ALL CONTRACTED FORMS BUT NOT POSSESSIVE 'S)",
"thatdel_060": "SUBORDINATOR THAT-DELETION",
"strandprep_061": "STRANDED PREPOSITIONS",
"vsplitinf_062": "SPLIT INFINITIVES",
"vsplitaux_063": "SPLIT AUXILIARIES (ARE OBJECTIVELY SHOWN TO...)",
"coordphras_064": "PHRASAL COORDINATION ('AND' CONNECTING TWO ADV/ADJ/N/V PHRASES)",
"coordnonp_065": "CLAUSAL COORDINATION ('AND' CONNECTING TWO CLAUSES)",
"negsyn_066": "SNYTHETIC NEGATION (NO + QUANT/ADJ/N, NEITHER, NOR)",
"negana_067": "ANALYTIC NEGATION (NOT, N'T)",
"hashtag_201": "HASHTAGS", # done by HM
"link_202": "EXTERNAL URLS", # done by HM
"interlink_203": "INTERNAL URLS",
"caps_204": "WORDS IN ALL CAPS",
"vimperative_205": "IMPERATIVE VERB FORMS",
"lengthening_206": "STRATEGIC LENGTHENING",
"emoticons_207": "EMOTICONS",
"question_208": "QUESTION MARKS", # done by HM
"exclamation_209": "EXCLAMATION MARKS", # done by HM
"lenchar_210": "LENGTH OF THE SENTENCE IN CHARACTERS",
"lenword_211": "LENGTH OF THE SENTENCE IN WORDS",
"comparatives_syn_212": "SYNTHETIC COMPARATIVES (ADJ-ER)",
"superlatives_syn_213": "SYNTHETIC SUPERLATIVES (ADJ-EST)",
"comparatives_ana_214": "ANALYTICAL COMPARATIVES (MORE + ADJ)",
"superlatives_ana_215":"ANALYTICAL SUPERLATIVES (MOST + ADJ)",
"reddit_vocab_216": "COMMUNITY-SPECIFIC ACRONYMS OR LEXICAL ITEMS", 
"vprogressive_217": "VERB PHRASES IN PROGRESSIVE ASPECT",
"emojis_218": "EMOJIS",
"coordAnd_219": "ALL INSTANCES OF AND",
"coordBut_220": "ALL INSTANCES OF BUT",
"coordOr_221": "ALL INSTANCES OF OR"}


### Asking user input about which feature to code.
show_feats = input("This is a script for manual coding of features. Hit 'f' and enter if you want to see a list of the features. Else, simply hit enter.\n")
if show_feats == "f":
    for key in feats:
        print(key + ": " + feats[key])

feature = input("Please type in the identifier of the feature you want to code: ")
while not feature in feats.keys():
    feature = input("I am sorry, this is not one of the feature codes. Please type in the identifier of the feature you want to code: ")

print("\n\nOkay, "+feats[feature]+" it is!\n"\
      "You will be shown one sentence at a time.\n"\
      "Please enter the number of "+ feats[feature] + " you see in the sentence.\n\n")


pos = 0
neg = 0
sents = 0

### Keeping track of sentences already coded for this feature.
### This allows the user to interrupt the script at any point
### and pick up where they left off later on.
already_coded = set()
if os.path.exists("manual_coding_"+feature+".txt"):
    print("I found a file with some coding done already. Picking up where you left off. ")
    with open("manual_coding_"+feature+".txt", "r") as p:
        for line in p:
            print(line)
            already_coded.add(line.split("\t")[0])
            if line.split("\t")[1].strip("\n") == "0":
                neg += 1
            else:
                pos += 1
            sents += 1


print(already_coded)



input("Hit ENTER to begin. ")

f = open("sample_sentences.txt", "r", encoding="utf-8", errors="ignore")

while pos<10 or neg<10 or sents<100:
    l = f.readline().split("\t")
    if len(l) == 2 and not l[0] in already_coded:
        ID = l[0]
        s = l[1].strip("\n")
        count = "x"
        while not count.isdigit():
            print("\n\n<<<< "+s+" >>>>>")
            count = input("Type in how many instances of "+ feats[feature] + " are in this sentence.\n\n")
            if not count.isdigit():
                print("Sorry, input needs to be an integer.")
        if count == "0":
            neg +=1
        else:
            pos += 1
        sents +=1
        with open("manual_coding_"+feature+".txt", "a") as p:
            p.write(ID + "\t" + count+"\n")
    elif len(l) == 2 and l[0] in already_coded:
        pass
    else:
        break

p.close()
        
