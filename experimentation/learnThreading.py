# learning threading.

import logging
import threading
import time
# import multiprocessing

#test sample.
def repeat_thread():
	logging.info("Thread Repeat --launch request")
	logging.info("Thread Repeat: start")

	while True:
		if end_repeat.is_set():
			logging.info("Thread Repeat --halt request")
			logging.info("Thread Repeat: end")
			break

		else:
			logging.info("repeating thread!")
			time.sleep(2)


def main_thread(t):
	logging.info("Thread Main: start")

	y = threading.Thread(target=repeat_thread)
	y.start()

	time.sleep(t)
	logging.info("Thread Main: end")

	end_repeat.set()


if __name__ == "__main__":
	format = "%(asctime)s: %(message)s"
	logging.basicConfig(format=format, level=logging.INFO,
	                    datefmt="%H:%M:%S")

	end_repeat = threading.Event()

	x = threading.Thread(target=main_thread, args=(20, ))
	x.start()

	
# utilize main loop for functionality, repeating loop as google calendar check

