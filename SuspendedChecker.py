import re
import json
import praw
import pprint
from requests import Session

path = "~/Reddit_MDA/"
#path = "/Users/gusta/Desktop/Python/Codes reddit/"

# Creates empty lists for the authors
fullauthors = []
authors = []

# Potential code for looping over all files
# for filename in os.listdir(folder_path):
#         if os.path.splitext(filename)[1] == ".json":
#             with open(os.path.join(path, filename), "r", errors="replace") as data:
                #author = json.loads(line.strip())["author"]
                #fullauthors.append(author)

with open('sample_data/json/RC_2015-02.json', 'r') as obj:
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

#redditor = reddit.redditor(cleanedlist2[10])
user_list = [reddit.redditor(x) for x in cleanedlist2 if x != "[deleted]"]
for redditor in user_list:
    try: 
        if hasattr(redditor, 'fullname'):
            print(redditor, "alive")
        elif hasattr(redditor, 'is_suspended'):
            blacklist.append(redditor)
            print(redditor, "blacklist")
        else:
            print("ERROR", redditor)
    except:
        print(redditor)

# Writes list items into a new txt.file        

with open ('Blacklist2005-12.txt', 'w') as filehandle:
    for item in blacklist:
        filehandle.write('%s\n' % item)

        



        
