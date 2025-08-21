import argparse
import rp

def main():
	parser = argparse.ArgumentParser(description="42 Rich Presence Client")
	subparsers = parser.add_subparsers(dest="command", required=True)

	subparsers.add_parser("start", help="Start the client")
	subparsers.add_parser("stop", help="Stop the client")
	subparsers.add_parser("status", help="Show status")

	cfg = subparsers.add_parser("config", help="Configure the client")
	cfg.add_argument("key", type=str, help="Config key")
	cfg.add_argument("value", type=str, help="Config value")

	args = parser.parse_args()

	if args.command == "start":
		rp.start()
	elif args.command == "stop":
		rp.stop()
	elif args.command == "status":
		rp.status()
	elif args.command == "config":
		rp.config(args.key, args.value)

if __name__ == "__main__":
	main()
