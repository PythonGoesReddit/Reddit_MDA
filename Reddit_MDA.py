#All packages:
import json
import os
import nltk

#All path variables
path = "FILEPATH"

# Preprocessing functions
def open_reddit_json(folder_path):
    errors = 0
    for filename in os.listdir(folder_path):
        if os.path.splitext(filename)[1] == ".json": #open file only if extension is .json, else will try to open folders and other random files
            with open(os.path.join(path, filename), "r", errors="replace") as j:
                base = os.path.splitext(filename)[0] #strip the .json extension so that we can save a file with the same name as .txt later
                #textfile = open(os.path.join(path, "cleaned", base + "_cleaned.txt"), "a", errors="replace") #open new file to write -- same name but .txt
                textfile = open(os.path.join(path, "cleaned", base + "_cleaned.json"), "w", errors="replace")
                counter = 0
                for line in j:
                    counter += 1
                    try:
                        comment = json.loads(line.strip())["body"]
                        counter_comment = {counter: comment}
                        textfile.write(json.dumps(counter_comment))
                        #textfile.write(comment + " \n ")
                    except json.decoder.JSONDecodeError:
                        errors +=1 #keeps track of how many errors are encountered/lines skipped
                textfile.close()
    print("Total lines skipped = " + str(errors))
    print("Saving and exiting...")

## NEEDED: function to remove unneeded meta info (author custom CSS, etc.) - Kyla
## NEEDED: function to change data from one dictionary entry per comment to one entry per sentence - Axel(??) 
## NEEDED: function to remove deleted commments, i.e. comments for which the body text is only "deleted" - Kyla or Axel
## NEEDED: function to remove comments posted by bots (how can we reliably identify them?) - Gustavo
## NEEDED: function to remove posts with too few English words - Axel 
## NEEDED: function to save preprocessed data and check if this step could be skipped for debugging - Kyla



# Untagged feature extraction functions
## NEEDED: function to calculate length of comment / sentence (?)
## NEEDED: work on and flush out the following code:
## Think about more informative function names
resultsfile = open("filepath","w")
for filename in os.listdir(path):
  textfile = open(filename, "r")
  linenumber = 0
  for line in textfile.readlines():
    linenumber += 1 
    commentWL = line.split() # split character string into a list
    feature1_counter = feature1_func(commentWL)# extract the count for each feature with the pre-defined feature-functions
    feature2_counter = feature2_func(commentWL) 
    ...
# print the counts for each comment into a new file
    print(str(linenumber), + ";" + str(feature1_counter) + ";" + str(feature2_counter) + ...)
    textfile.close()
resultsfile.close()

## function for feature 1: hashtags
def feature1_func(wordlist):
  """This function takes a list of words as input and returns the number of items
  that contain at least one hashtag (#)."""
  counter = 0
  for item in wordlist:
    if "#" in item:
      counter = counter + 1
    else:
      pass
  return(counter)

## function for feature 2: URLS (maybe subdivide in u/..., r/..., and www...)
def feature2_func(wordlist):
  """This function takes a list of words as input and returns the number of items
  that contain an identifiable link to another user, subreddit, or website."""
  counter = 0
  for item in wordlist:
    if item.startswith("u/") or item.startswith("r/") or item.startswith("http") or item.startswith("www"):
      counter = counter + 1
    else:
      pass
  return(counter)

## function for feature 3: capitalisation 
def feature3_func(wordlist):
  """This function takes a list of words as input and returns the number of items
  that are in upper case only."""
  counter = 0
  for item in wordlist:
   if item.isupper():
      counter = counter + 1
    else:
      pass
  return(counter)
### maybe it would make sense to exclude "I" here, since it is usually upper case?
### And maybe also sentence initial "A"?

## function for feature 4: imperatives
def feature4_func(wordlist):
  """This function takes a list of words as input and returns the number of items
  that are an imperative."""
  counter = 0
  for item in wordlist:
   if :
      counter = counter + 1
    else:
      pass
  return(counter)

## NEEDED: function for feature 7: emoticons - Gustavo
## NEEDED: function for question marks and exclamation marks (two features combined) - Kyla
## NEEDED: function for feature 10: strategic lengthening - Kyla ?? (I don't know what this means though...)
## NEEDED: function for feature 11: alternating uppercase-lowercase - Kyla ??
## NEEDED: function for feature 12: community-specific acronyms/lexical items (such as 'op') - Gustavo ??



# Data prep ("cleaning") functions:
## NEEDED: function to turn all words to lowercase - Axel
## NEEDED: function to normalize deviant and creative spelling - Axel (probably combined with lowercase?)
## NEEDED: function to remove punctuation (?) - Axel
## NEEDED: function to remove emojis - Gustavo



# Tagging and feature extraction functions 
## NEEDED: update of following code for Stanford tagger - Hanna (to function, file opening - line by line not whole file duplicated?)
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

## NEEDED: additional functions from Nini's MAT output - Hanna
### Might (doch) be better here to import from Hannas other file, i.e. 
from Reddit_Bibers_Features import feature_01, feature_02
### Might also be worth it to try to reduce the number of functions here, combining ones that can be combined.
### Also worth thinking about function names for informativity
## NEEDED: function for comparatives - Hanna
## NEEDED: function for superlatives - Hanna




# Output functions
## NEEDED: function to write a matrix of text_id * variables - Kyla?
## NEEDED: function to write meta-info for each text - Kyla


# CALL FUNCTIONS DOWN HERE
## NEEDED: Multiprocessing set up -- Axel & Kyla ?
