"""continuous gesture recognition

only stops when speaker outputs

1
first run gcalAPI and camera at the same time

2
while camera running continuously check if gcalAPI stopped

3
if stopped then every half hour update

4
otherwise leave it running and do not override (via update)

5
whenever gcalAPI returns message then pause camera input (not feed)

"""



import threading
import time


def main_thread(t):
	import mp_gesture_recog.mp_main
	mp_main.main()
	for y in range(t):
		time.sleep(1)
		print(y+1)
	end.set()



end = threading.Event()

x = threading.Thread(target=main_thread, args=(20, ))
x.start()