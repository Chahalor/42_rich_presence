import json, time
import rp

class Config:
	def __init__(self):
		# discord presence elements
		self.pid: int = 0
		self.state: str = "Idle"
		self.start: int = int(time.time())
		self.end: int = int(time.time()) + 3600
		self.large_image: str = "https://wallpapercave.com/wp/wp2354163.jpg"
		self.large_text: str = "large presence"
		self.small_image: str = "https://wallpapercave.com/wp/wp2354163.jpg"
		self.small_text: str = "small presence"
		self.party_id: str = "42"
		self.party_size: list[int] = [0, 0]
		self.join: str = "21"
		self.spectate: str = "84"
		self.match: str = "69"
		self.buttons: list[dict[str, str]] = []
		self.instance: bool = False
		# app informations
		self.online: bool = False
		self.current: str = ""

	def __dict__(self):
		return {
			"pid": self.pid,
			"state": self.state,
			"start": self.start,
			"end": self.end,
			"large_image": self.large_image,
			"large_text": self.large_text,
			"small_image": self.small_image,
			"small_text": self.small_text,
			"party_id": self.party_id,
			"party_size": self.party_size,
			"join": self.join,
			"spectate": self.spectate,
			"match": self.match,
			# "buttons": self.buttons,
			"instance": self.instance
		}

	def __str__(self) -> str:
		return f"{json.dumps(self.__dict__(), indent=4)}"

	def _save(self, file_path):
		with open(file_path, 'w') as f:
			json.dump(self.settings, f)

	def _load(self, file_path):
		with open(file_path, 'r') as f:
			self.settings = json.load(f)
			self.pid = self.settings.get("pid", 0)
			self.state = self.settings.get("state", "Idle")
			self.start = self.settings.get("start", int(time.time()))
			self.end = self.settings.get("end", int(time.time()) + 3600)
			self.large_image = self.settings.get("large_image", "https://wallpapercave.com/wp/wp2354163.jpg")
			self.large_text = self.settings.get("large_text", "large presence")
			self.small_image = self.settings.get("small_image", "https://wallpapercave.com/wp/wp2354163.jpg")
			self.small_text = self.settings.get("small_text", "small presence")
			self.party_id = self.settings.get("party_id", "42")
			self.party_size = self.settings.get("party_size", [0, 0])
			self.join = self.settings.get("join", "21")
			self.spectate = self.settings.get("spectate", "84")
			self.match = self.settings.get("match", "69")
			self.buttons = self.settings.get("buttons", [])
			self.instance = self.settings.get("instance", False)
			self.login = self.settings.get("login", "")
			self.online = self.settings.get("online", False)

			self.current = self.settings.get("current", "")

config = Config()