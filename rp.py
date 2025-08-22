import requests
from pypresence import Presence
import time
import json
import sys
import json



def getUserLevel(cursus):
	for i in range(len(cursus)):
		if (cursus[i]["id"] == 283777): # main 42 cursus
			return cursus[i]["level"]
	return 0



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
RPC = Presence("1408374003411849216")
RPC.connect()
print("RPC is online")


#
## Choose which infos to show
#
cursus = user["cursus_users"]


user_lvl = "user level: " + str(getUserLevel(cursus))
wallet = "wallet: " + str(user["wallet"])
state = "location: " + (user["location"] or "unavailable")
rank = "rank: " + str(user["kind"])
pp = user["image"]["link"] # your intra picture

RPC.update(
	details=state,
	state=user_lvl,
	start=start,
	large_image = "42", # big 42 image
	small_image=pp,
)
print("RPC is setup")

while True:
	time.sleep(15)
