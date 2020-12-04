import re
import json
import praw
import pprint
from requests import Session

path = "/Users/gusta/Desktop/Python/Codes reddit/"

# Creates empty lists for the authors
fullauthors = []
authors = []

with open('RC_2005-12.json', 'r') as obj:
    data = obj.read()

# Appends the author names to a list

result = re.findall(r"""author"(:".+?")""", data)
fullauthors.append(result)

# List collapsing

for sublist in fullauthors:
	for item in sublist:
		authors.append(item)

# Removes additional characters
		
cleanedlist1 = [sub.replace(':', '') for sub in authors] 
cleanedlist2 = [sub.replace('"', '') for sub in cleanedlist1]

# Initiates praw session

session = Session()
session.verify = "/path/to/certfile.pem"
reddit = praw.Reddit(client_id="Qhw6nE9tDBhPCw",
                     client_secret="h_Drz8nU5f0yVupjz5bYHm0U0_8",
                     user_agent="testscript by /u/independ8",)

print(reddit.user.me())
print(reddit.read_only)

# Creates empty blacklist

blacklist = []

redditor = reddit.redditor(cleanedlist2[10])
for item in cleanedlist2:
    if hasattr(redditor, 'fullname'):
        print ("alive")
    elif hasattr(redditor, 'is_suspended'):
        blacklist.append
    else:
        blacklist.append

# Writes list items into a new txt.file        

with open ('Blacklist2005-12.txt', 'w') as filehandle:
    for item in blacklist:
        filehandle.write('%s\n' % item)

        



        
