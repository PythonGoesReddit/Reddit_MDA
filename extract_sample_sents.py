import bz2
import json
import nltk
import os
import random

def extract_sent(line):
    data = json.loads(line)
    comment = data["body"]
    sents = nltk.tokenize.sent_tokenize(comment)
    return(random.choice(sents))

def select_lines(filepath):
    IDs = random.sample(range(0,100000),10)
    counter = 0
    sents = []
    with bz2.BZ2File(filepath) as f:
        while counter < 100001:
            counter += 1
            line = f.readline()
            if counter in IDs:
                try:
                    sents.append(extract_sent(line))
                except:
                    counter = 100001
    return(sents)

dirlist = []
for root, dirs, files in os.walk("/media/axel/Samsung_T5/reddit_data"):
    for name in files:
        if name.endswith(".bz2"):
            dirlist.append(os.path.join(root, name))


with open("/home/axel/Documents/github/Reddit_MDA/sample_sentences.txt", "w") as p:
    for fpath in dirlist:
        print(fpath)
        output = select_lines(fpath)
        for s in output:
           p.write(s.strip()+"\n")
