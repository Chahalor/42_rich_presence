#!/usr/bin/env python3
import os, sys, socket, subprocess

SOCKET_PATH = "/tmp/rich_presence.sock"
PID_FILE = "/tmp/rich_presence.pid"

def send_cmd(cmd):
	client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	client.connect(SOCKET_PATH)
	client.send(cmd.encode())
	response = client.recv(1024).decode()
	client.close()
	print(response)

if len(sys.argv) < 2:
	print("Usage: rp [start|stop|config|status]")
	sys.exit(1)

cmd = sys.argv[1]

if cmd == "start":
	if os.path.exists(PID_FILE):
		print("Daemon already running")
	else:
		subprocess.Popen([sys.executable, "daemon.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		print("Daemon started")
elif cmd in ("stop", "status") or cmd.startswith("config"):
	send_cmd(" ".join(sys.argv[1:]))
else:
	print("Unknown command")
