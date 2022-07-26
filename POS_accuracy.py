### import the taggers to evaluate
from turtle import pos
from nltk import pos_tag
import string
from sklearn import metrics
from flair.models import SequenceTagger
from flair.data import Sentence
tagger_FLAIR = SequenceTagger.load("C:/Users/gusta/Documents/GitHub/Reddit_MDA/RedditTaggerFinal150.pt")


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

def tag_sentence(sentence):
    '''Takes a sentence, cleans it with clean_sentence, and tags it using the FLAIR POS tagger. 
    Adds a look ahead/behind buffer of three items of type ("X", "X") to prevent negative indices and IndexErrors
    Returns a list of tuples of (word, pos_tag).'''
    cleaned_sentence = clean_sentence(sentence)
    flair_sentence = Sentence(cleaned_sentence)
    tagger_FLAIR.predict(flair_sentence)
    token_list = []
    for label in flair_sentence.get_labels('pos'):
        if not label.value in ["''", "``"]:    
            token_list.append(tuple([label.data_point.text] + [label.value])) 
    empty_look = [("X", "X"), ("X", "X"), ("X", "X")]
    tagged_sentence = empty_look + token_list + empty_look 
    return tagged_sentence


def sentence_tags(w_pos_list):
    gold = [x[1] for x in w_pos_list]
    words = [x[0] for x in w_pos_list]
    nltk_tags = [x[1] for x in pos_tag(words)]
    sent = " ".join(words)
    flair_tags = [x[1] for x in tag_sentence(sent)][3:-3]
    if len(gold) == len(nltk_tags) == len(flair_tags):
        return(gold, nltk_tags, flair_tags)
    else:
        print("Unequal token numbers")
        print(gold)
        print(flair_tags)
        return([],[],[])
        

gold = []
nltk_tags = []
flair_tags = []


with open("C:/Users/gusta/Documents/GitHub/Reddit_MDA/Tagged_JSONS/RC_2005-12_tagged_manual_Batch1_done.txt") as f:
    for line in f:
        if line.split("\t")[2] == "[]\n":
            pass
        else:
            print(line.split("\t")[0])
            sent_raw = line.split("\t")[2].strip("\n")
            sent_split = sent_raw.strip("[]").replace("'", "").split("], [")
            sentence = [x.split(", ") for x in sent_split]
            gold += sentence_tags(sentence)[0]
            nltk_tags += sentence_tags(sentence)[1]
            flair_tags += sentence_tags(sentence)[2]

with open("C:/Users/gusta/Documents/GitHub/Reddit_MDA/Tagged_JSONS/RC_2005-12_tagged_manual_Batch2_done.txt") as g:
    for line in g:
        if line.split("\t")[2] == "[]\n":
            pass
        else:
            print(line.split("\t")[0])
            sent_raw = line.split("\t")[2].strip("\n")
            sent_split = sent_raw.strip("[]").replace("'", "").split("], [")
            sentence = [x.split(", ") for x in sent_split]
            gold += sentence_tags(sentence)[0]
            nltk_tags += sentence_tags(sentence)[1]
            flair_tags += sentence_tags(sentence)[2]

with open("C:/Users/gusta/Documents/GitHub/Reddit_MDA/Tagged_JSONS/RC_2005-12_tagged_manual_Batch1_done.txt") as h:
    for line in h:
        if line.split("\t")[2] == "[]\n":
            pass
        else:
            print(line.split("\t")[0])
            sent_raw = line.split("\t")[2].strip("\n")
            sent_split = sent_raw.strip("[]").replace("'", "").split("], [")
            sentence = [x.split(", ") for x in sent_split]
            gold += sentence_tags(sentence)[0]
            nltk_tags += sentence_tags(sentence)[1]
            flair_tags += sentence_tags(sentence)[2]

with open("C:/Users/gusta/Documents/GitHub/Reddit_MDA/Tagged_JSONS/RC_2005-12_tagged_manual_Batch1_done.txt") as i:
    for line in i:
        if line.split("\t")[2] == "[]\n":
            pass
        else:
            print(line.split("\t")[0])
            sent_raw = line.split("\t")[2].strip("\n")
            sent_split = sent_raw.strip("[]").replace("'", "").split("], [")
            sentence = [x.split(", ") for x in sent_split]
            gold += sentence_tags(sentence)[0]
            nltk_tags += sentence_tags(sentence)[1]
            flair_tags += sentence_tags(sentence)[2]



nltk_classification = metrics.classification_report(gold, nltk_tags,)
flair_classification = metrics.classification_report(gold, flair_tags,)

with open("Tagging_accuracy_reports.txt", "w") as p:
    p.write(nltk_classification)
    p.write("\n\n\n")
    p.write(flair_classification)
