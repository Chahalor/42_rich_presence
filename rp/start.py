import os, sys, socket, time
from xmlrpc import server
from pypresence import Presence
import rp
from rp.connect import RPCNotConnectedError

def _mute_streams():
	sys.stdout.flush()
	sys.stderr.flush()
	with open("/dev/null", "rb", 0) as f:
		os.dup2(f.fileno(), sys.stdin.fileno())
	with open("/dev/null", "ab", 0) as f:
		os.dup2(f.fileno(), sys.stdout.fileno())
		os.dup2(f.fileno(), sys.stderr.fileno())

def _update_presence():
	try:
		rp.update()
	except RPCNotConnectedError:
		try:
			rp.connect()
			rp.update()
		except Exception as e:
			with open("/tmp/rp.log", "a") as f:
				f.write(f"Error connecting RPC: {e}\n")

def _handle_order(order: str) -> str:
	if order == "stop":
		sys.exit(0)
		return "Stopping daemon"
	elif order == "status":
		return rp.config.__str__()
	elif order == "update":
		_update_presence()
		return "Presence updated"
	else:
		return "Unknown command"

def daemonize():
	try:
		with open(rp.PID_FILE, "r") as f:
			_pid: int = int(f.read().strip())
			try:
				os.kill(_pid, 0)
				print(f"Daemon already running with PID {_pid}.")
				sys.exit(1)
			except ProcessLookupError:
				pass
	except FileNotFoundError:
		pass
	pid: int = os.fork()
	if pid > 0:
		sys.exit(0)
	os.setsid()
	print(f"Daemon started with PID {os.getpid()}")

	# _mute_streams()

	with open(rp.PID_FILE, "w+") as f:
		f.write(str(os.getpid()))
	
	_update_presence()
	if os.path.exists(rp.SOCKET_PATH):
		os.remove(rp.SOCKET_PATH)
	server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	server.bind(rp.SOCKET_PATH)
	server.listen(1)

	while True:
		conn, _ = server.accept()
		with conn:
			print("Client connected")
			data = conn.recv(1024)
			if not data:
				continue
			
			conn.sendall(_handle_order(data.decode().strip()).encode())


def start():
	daemonize()

def main():
	while True:
		time.sleep(5)
		with open("/tmp/rp.log", "a") as f:
			f.write("Daemon alive\n")

if __name__ == "__main__":
	daemonize()
	main()