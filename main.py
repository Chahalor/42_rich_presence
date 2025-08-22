import sys, argparse, os, json
import rp

def _parse() -> str:
	_parser = argparse.ArgumentParser(description="42 Rich Presence Client")
	_subparser = _parser.add_subparsers(dest="command")
	_subparser.add_parser("start", help="Start the rich presence client")
	_subparser.add_parser("stop", help="Stop the rich presence client")
	_subparser.add_parser("status", help="Get the status of the rich presence client")
	_subparser.add_parser("update", help="Update the rich presence client")
	_subparser.add_parser("config", help="Configure the rich presence client")
	_subparser.add_parser("help", help="Show help information")

	_args = _parser.parse_args()

	if _args.command == "help": 
		_parser.print_help()
		sys.exit(0)

	return _args.command

def _create_config() -> bool:
	_json: dict = {
		"large_image": "",
		"small_image": "",
		"state": "",
		"details": "",
		"start_timestamp": 0,
		"end_timestamp": 0,
		"party": {
			"id": "",
			"size": [0, 0]
		},
		"match": {
			"application_id": "",
			"status": ""
		},
	}
	try:
		json.dump(_json, open(os.path.expanduser("~/.rpc/config.json"), "w"), indent=4)
		return True
	except Exception as e:
		print(f"Error creating config file: {e}", file=sys.stderr)
		return False
	
def _create_files() -> bool:
	_files = [
		rp.PID_FILE
	]
	for _file in _files:
		if not os.path.exists(os.path.expanduser(_file)):
			try:
				open(os.path.expanduser(_file), "w").close()
				print(f"Created file {_file}")
			except Exception as e:
				print(f"Error creating file {_file}: {e}", file=sys.stderr)
				return False
	return True

def _init() -> bool:
	if not os.path.exists("~/.rpc/"):
		try:
			os.makedirs("~/.rpc/")
		except Exception as e:
			print(f"Error creating directory: {e}", file=sys.stderr)
			return False
	if not os.path.exists("~/.rpc/config.json"):
		_create_config()
	_create_files()
	rp.config._load(os.path.expanduser(rp.CONFIG_FILE))
	return True

def main() -> int:
	_func: dict = {
		"start": rp.start,
		"stop": rp.stop,
		"status": rp.status,
		"update": rp.update,
		"config": rp.config,
	}
	if not _init():
		return 1
	_order: str = _parse()
	return _func[_order]()

if __name__ == "__main__":
	exit(main())
