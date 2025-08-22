import os, json, socket, sys
import rp

def _get_status() -> dict:
	socket_client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	socket_client.connect(rp.SOCKET_PATH)
	socket_client.sendall(b"status")
	socket_client.settimeout(2)
	with socket_client:
		data = socket_client.recv(1024)
		if not data:
			return {}
		return json.loads(data.decode("utf-8"))


def status() -> int:
	try:
		os.kill(int(open(rp.PID_FILE).read().strip()), 0)
	except ProcessLookupError:
		print("Rich presence client is not running.")
		return 1
	_status = _get_status()
	if _status:
		print("Rich presence client is running.")
		print("config: " + json.dumps(_status, indent=4))
		return 0
	return 0