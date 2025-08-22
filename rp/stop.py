import os
import rp

def stop() -> int:
	try:
		os.kill(int(open(rp.PID_FILE).read().strip()), 15)
	except ProcessLookupError:
		print("Rich presence client is not running.")
		return 1
	except PermissionError:
		print("Insufficient permissions to stop Rich presence client.")
		return 1
	except Exception as e:
		print(f"Error stopping Rich presence client: {e}")
		return 1
	print("Rich presence stopped")
	return 0
