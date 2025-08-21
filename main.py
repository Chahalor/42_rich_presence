import requests
from pypresence import Presence
import time
import json
import sys
import json
import argparse
import subprocess
import os

class Request:
	def __init__(self, login: str, uid: str, secret: str):
		self.login = login
		self.uid = uid
		self.secret = secret
		self.token = None

	def _get_token(self, uid: str, secret: str) -> str:
		_data = {
			"grant_type": "client_credentials",
			"client_id": uid,
			"client_secret": secret
		}
		try:
			_response = requests.post(
				"https://api.intra.42.fr/oauth/token",
				data=_data
			)
			_response.raise_for_status()
			self.token = _response.json()["access_token"]
			return (self.token)
		except requests.RequestException as e:
			print(f"Error during request: {e}", file=sys.stderr)
			return ("")
		
	def request_data(self, path: str) -> dict:
		if not self.token:
			self._get_token(self.uid, self.secret)
		_headers = {"Authorization": f"Bearer {self.token}"}
		try:
			_response = requests.get(f"https://api.intra.42.fr/v2/{path}", headers=_headers)
			_response.raise_for_status()
			return (_response.json())
		except requests.RequestException as e:
			print(f"Error during request: {e}", file=sys.stderr)
			return ({})

class RP:
	def __init__(self, client_id: str):
		self.client_id = client_id
		self.rpc = Presence(client_id)

	def _connect(self,
			state: str,
			details: str="",
			start: int=int(time.time()),
			large_image: str="",
			large_text: str="",
		) -> None:
		self.rpc.connect()
		self.rpc.update(state=state, details=details, start=start)

	def run(
			self,
			state: str,
			details: str="",
			start: int=int(time.time()),
			large_image: str="",
			large_text: str=""
		) -> None:
		self._connect(state, details, start, large_image, large_text)
		print("RPC is running")

def _load_info(file_path: str) -> dict:
	with open(file_path, "r") as f:
		return (json.load(f))

def _parser() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="42 Rich Presence Client")
	parser.add_argument("file", type=str, help="Path to the config.json file")
	return (parser.parse_args())

def _daemonist(
		file: str
	) -> None:
	subprocess.Popen(
			[sys.executable, sys.argv[0], *sys.argv[1:]],
			stdout=subprocess.DEVNULL,
			stderr=subprocess.DEVNULL,
			stdin=subprocess.DEVNULL,
			preexec_fn=os.setpgrp
		)
	config = _load_info(file)
	print("Loaded config:", config, file=sys.stderr)

	requester = Request(
		login=config["login"],
		uid=config["UID"],
		secret=config["SECRET"]
	)
	rp = RP(client_id="1383806236763623496")
	rp.run(
		state="Online",
		details="Coding in 42",
		start=int(time.time()),
		large_image="large_image_key",
		large_text="Large Image Text"
	)
	while True:
		time.sleep(15)
	sys.exit(0)

def main() -> int:
	args = _parser()
	_daemonist(args.file)
	return (0)

if __name__ == "__main__":
	exit(main())