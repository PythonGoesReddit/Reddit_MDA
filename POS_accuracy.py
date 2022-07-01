### import the taggers to evaluate
from nltk import pos_tag
from Reddit_MDA import tag_sentence
from sklearn import metrics

def sentence_tags(w_pos_list):
    gold = [x[1] for x in w_pos_list]
    words = [x[0] for x in w_pos_list]
    nltk_tags = [x[1] for x in pos_tag(words)]
    sent = " ".join(words)
    flair_tags = [x[1] for x in tag_sentence(sent)][3:-3]
    if len(gold) == len(nltk_tags) == len(flair_tags):
        return(gold, nltk_tags, flair_tags)
    else:
        return([],[],[])
        print("Unequal token numbers")

gold = []
nltk_tags = []
flair_tags = []


with open("Tagged_JSONS/RC_2005-12_tagged_manual_Batch1_done.txt") as f:
    for line in f:
        if line.split("\t")[2] == "[]\n":
            pass
        else:
            sent_raw = line.split("\t")[2].strip("\n")
            sent_split = sent_raw.strip("[]").replace("'", "").split("], [")
            sentence = [x.split(", ") for x in sent_split]
            gold += sentence_tags(sentence)[0]
            nltk_tags += sentence_tags(sentence)[1]
            flair_tags += sentence_tags(sentence)[2]



nltk_classification = metrics.classification_report(gold, nltk_tags)
flair_classification = metrics.classification_report(gold, flair_tags)

with open("Tagging_accuracy_reports.txt", "w") as p:
    p.write(nltk_classification)
    p.write("\n\n\n")
    p.write(flair_classification)
