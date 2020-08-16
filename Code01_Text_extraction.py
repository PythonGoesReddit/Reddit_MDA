
## this code should:
## - take monthly sets of Reddit comments in JSON format as input
## - go through each line and select the actual text only (disregard all the metadata)
## - save all the text (one comment per line) to a separate (monthly) txt-file which can then be used as input for the Biber-tagger

## maybe we should have two versions of this code? One that saves one comment per line and one that saves one sentence per line?

import json
import os

path = "FILEPATH"

errors = 0

for filename in os.listdir(path):
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
