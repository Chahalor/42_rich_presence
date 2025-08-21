import argparse
import sys

class Command:
	def __init__(self, name: str, description: str, handler, args: list[str] = []):
		self._name = name
		self._description = description
		self._handler = handler
		self._args = args

	def __repr__(self):
		return f"<Command {self._name}>"

	def __str__(self):
		return f"_name: {self._name}, _description: {self._description}, _args: {self._args}"


# ===============================
# Handlers (fonctions par commande)
# ===============================

def cmd_start(args):
	
	print("🚀 Starting Rich Presence client...")

def cmd_stop(args):
	print("🛑 Stopping Rich Presence client...")

def cmd_status(args):
	print("📊 Client is running (fake status here).")

def cmd_config(args):
	print(f"⚙️ Setting config {args.key} = {args.value}")


# ===============================
# Liste des commandes
# ===============================

list_commands: dict[str, Command] = {
	"start":  Command("start",  "Start the Rich Presence client",  cmd_start),
	"stop":   Command("stop",   "Stop the Rich Presence client",   cmd_stop),
	"status": Command("status", "Show the status of the client",   cmd_status),
	"config": Command("config", "Configure the client",            cmd_config)
}


# ===============================
# Parser
# ===============================

def parser() -> tuple[Command, argparse.Namespace] | None:
	global list_commands

	_parser = argparse.ArgumentParser(description="42 Rich Presence Client")
	subparsers = _parser.add_subparsers(dest="command", required=True)

	# Crée un subparser pour chaque commande
	for name, cmd in list_commands.items():
		sp = subparsers.add_parser(name, help=cmd._description)
		if name == "config":
			sp.add_argument("key", type=str, help="Config key")
			sp.add_argument("value", type=str, help="Config value")

	args = _parser.parse_args()

	if args.command not in list_commands:
		print(f"Unknown command: {args.command}", file=sys.stderr)
		_parser.print_help()
		return None

	return list_commands[args.command], args


# ===============================
# Main
# ===============================

if __name__ == "__main__":
	result = parser()
	if result:
		cmd, args = result
		cmd._handler(args)
	sys.exit(0)
