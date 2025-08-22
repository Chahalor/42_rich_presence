import rp
from pypresence import Presence

rpc = None

class RPCNotConnectedError(Exception):
	pass

def connect() -> bool:
	global rpc
	rpc = Presence(rp.APP_ID)
	return rpc.connect()

def update() -> bool:
	if not rpc:
		raise RPCNotConnectedError("RPC not connected")
	try:
		rpc.update(
			details="Details",
			state="State",
			start=rp.config.start,
			large_image="42logo"
			# pid=rp.config.pid,
			# state=rp.config.state,
			# start=rp.config.start,
			# end=rp.config.end,
			# large_image=rp.config.large_image,
			# large_text=rp.config.large_text,
			# small_image=rp.config.small_image,
			# small_text=rp.config.small_text,
			# party_id=rp.config.party_id,
			# party_size=rp.config.party_size,
			# join=rp.config.join,
			# spectate=rp.config.spectate,
			# match=rp.config.match,
			# # buttons=rp.config.buttons,
			# instance=rp.config.instance
		)
		return True
	except Exception as e:
		print(f"Error updating RPC: {e}")
		return False