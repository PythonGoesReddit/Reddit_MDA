### this code should:
### - take monthly files as input (in pure txt or dictionary format)
### - run the Standford Tagger (part of NLTK module) over the files
### - save the annotated files

# for this code to work, the nltk module needs to be installed
import nltk
import os

path = >>>specify file path here<<<

# open files
for filename in os.listdir(path):
# at the moment, the code is written with the assumption of the data being in txt-files with one commment per line
  untagged_file = open(os.path.join(path, filename), "r", errors="surrogateescape")
  tagged_file = open(os.path.join(path, filename + "_tagged.txt"), "w", errors = "replace")
  for line in untagged_file:
# Step 1: Tokenisation
    tokens = nltk.word_tokenize(line)
# Step 2: Tagging
    tagged = nltk.pos_tags(tokens)
    tagged_file.write(tagged + "/n")
# save output
  tagged_file.close()
  untagged_file.close()





