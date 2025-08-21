import os, sys, time, socket, json, signal

SOCKET_PATH = "/tmp/rp.sock"
PID_FILE = "/tmp/rp.pid"
config = {"login": "default", "UID": "", "SECRET": ""}

def handle_command(cmd: str):
	global config
	print(f"Received command: {cmd}", file=sys.stderr)
	if cmd.startswith("config "):
		key, value = cmd.split("=", 1)
		key = key.split()[1]
		config[key] = value
		return f"Updated {key} = {value}"
	elif cmd == "stop":
		os.remove(PID_FILE)
		os.remove(SOCKET_PATH)
		sys.exit(0)
	elif cmd == "status":
		return f"Running with config: {config}"
	return "Unknown command"

def daemon():
	# Sauvegarde le PID
	with open(PID_FILE, "w") as f:
		f.write(str(os.getpid()))

	# Crée un socket UNIX pour recevoir des commandes
	if os.path.exists(SOCKET_PATH):
		os.remove(SOCKET_PATH)
	server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	server.bind(SOCKET_PATH)
	server.listen(1)

	print("Daemon started. Listening on", SOCKET_PATH)

	while True:
		conn, _ = server.accept()
		data = conn.recv(1024).decode()
		if not data:
			continue
		response = handle_command(data.strip())
		conn.send(response.encode())
		conn.close()

if __name__ == "__main__":
	daemon()
