import os, sys, socket
import time
import rp

SOCKET_PATH = "/tmp/rich_presence.sock"
PID_FILE = "/tmp/rich_presence.pid"

def _mute_streams():
	sys.stdout.flush()
	sys.stderr.flush()
	with open("/dev/null", "rb", 0) as f:
		os.dup2(f.fileno(), sys.stdin.fileno())
	with open("/dev/null", "ab", 0) as f:
		os.dup2(f.fileno(), sys.stdout.fileno())
		os.dup2(f.fileno(), sys.stderr.fileno())

def _handle_order(order: str):
	if order == "stop":
		sys.exit(0)
	elif order == "status":
		client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
		client.connect(SOCKET_PATH)
		client.send("status from daemon".encode())
		client.close()
	else:
		client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
		client.connect(SOCKET_PATH)
		client.send(f"unknown order {order}".encode())
		client.close()

def daemonize():
	try:
		with open(PID_FILE, "r") as f:
			_pid: int = int(f.read().strip())
			if os.kill(_pid, 0) == 0:
				print(f"Daemon already running with PID {_pid}.")
				sys.exit(1)
	except FileNotFoundError:
		pass
	pid: int = os.fork()
	if pid > 0:
		sys.exit(0)
	os.setsid()
	print(f"Daemon started with PID {os.getpid()}")

	# _mute_streams()

	with open(PID_FILE, "w") as f:
		f.write(str(os.getpid()))
	
	if os.path.exists(SOCKET_PATH):
		os.remove(SOCKET_PATH)
	server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	server.bind(SOCKET_PATH)
	server.listen(1)

	print("Daemon started")

	while True:
		conn, _ = server.accept()
		with conn:
			print("Client connected")
			data = conn.recv(1024)
			if not data:
				break
			_handle_order(data.decode().strip())

def main():
	while True:
		time.sleep(5)
		with open("/tmp/rp.log", "a") as f:
			f.write("Daemon alive\n")

if __name__ == "__main__":
	daemonize()
	main()