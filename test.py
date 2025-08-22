from pypresence import Presence
import time

RPC = Presence("1408374003411849216")
RPC.connect()
RPC.update(state="Testing", details="This is a test", start=int(time.time()), large_image="42logo", large_text="42 Network")

while True:
	time.sleep(15)