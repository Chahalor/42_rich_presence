import requests
from pypresence import Presence
import time
import json
import sys
import json



def getUserLevel(cursus):
	for i in range(len(cursus)):
		if (cursus[i]["id"] == 283777): # main 42 cursus (not sus at all)
			return cursus[i]["level"]
	return 0 # level 0 is pretty sus ngl



if (len(sys.argv) != 2):
	print("usage: python3 <script.py> <config.json>")
	sys.exit()
	
with open(sys.argv[1]) as f:
    file = json.load(f)

UID = file["UID"]
SECRET = file["SECRET"]

login = file["login"]

data = {
	"grant_type" : "client_credentials",
	"client_id" : UID,
	"client_secret" : SECRET,
}

response = requests.post("https://api.intra.42.fr/oauth/token", data=data)
if (response.status_code != 200):
	raise Exception("request failed")

code = response.json()["access_token"]
print("access token aquired: " + code)
print(json.dumps(response.json(), indent=4))

header = {
	"Authorization": "Bearer " + code,
}


url = "https://api.intra.42.fr/v2/users/%s" % login
response = requests.get(url, headers=header)
if (response.status_code != 200):
	raise Exception("request failed")

user = response.json()
print(json.dumps(response.json(), indent=4))

start = int(time.time())
RPC = Presence("1383806236763623496")
RPC.connect()
print("RPC is online")


#
## Choose which infos to show
#
cursus = user["cursus_users"]


user_lvl = "sus level: " + str(getUserLevel(cursus)) + " 📮"
wallet = "wallet: " + str(user["wallet"]) + " coins (kinda sus)"
state = "sus location: " + (user["location"] or "hiding in vents 👀")
rank = "role: " + str(user["kind"]) + " (not the impostor)"
pp = user["image"]["link"] # your intra picture

RPC.update(
	details=state,
	state=user_lvl + " | Acting sus at 42 🔍",
	start=start,
	large_image = "42", # big 42 image
	small_image=pp,
)
print("RPC is setup - looking pretty sus 😎")

while True:
	time.sleep(15)
