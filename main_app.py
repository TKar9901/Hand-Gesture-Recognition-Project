### MAIN PROGRAM

### import libraries.
from tkinter import *
import tkinter.font
from tkcalendar import *
import datetime
from PIL import ImageTk, Image
import numpy as np
import threading

import cv2
from mp_gesture_recog.hand_class import HandModel

from gcal_and_db.gcalAPI import gAPI
import os, sys
import sqlite3 as sql
import time

### function for updating calendar event output files.
def update():
	obj.eventsUpdate()
	obj.dataProcessing()

	conn = sql.connect(os.path.join("gcal_and_db", "output_files.db"))
	cursor = conn.cursor()

	cursor.execute("""SELECT * FROM files
		""")
	fileData = cursor.fetchall()
	### [file, binary, length, rem]
	conn.commit()
	conn.close()

	return fileData

### function for locking and locking speaker I/O resource and running mp3 files.
def audio_out(file, t):
	audio.set()
	os.system(f"start {file}")
	time.sleep(t+1)
	audio.clear()

### function which acts as a thread for image capture + analysis.
def start_feed():
	global cap
	cap = cv2.VideoCapture(0)
	
	while True:
		ret, frame = cap.read()
		
		### image manipulation.
		frame = cv2.flip(frame, 1)
		
		while audio.is_set():
			time.sleep(3)

		### recognition from preset gestures.
		gesture = mp_model.deterGesture(frame, source=1)
		feedI = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)))
		feedL.configure(image=feedI)
		feedL.update()
	
		### colour format = BGR
		if gesture == "unknown":
			cv2.putText(img=frame, text="unknown", org=(50, 50), fontScale=1,
				fontFace=cv2.FONT_HERSHEY_SIMPLEX, color=(255, 0, 0), thickness=2)

		elif gesture != "none":
			audio_file, audio_len, end = mp_model.gestureOutput(gesture)
			audio_out(audio_file, audio_len)
			os.remove(audio_file)

			if end:
				close()

		feedI = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)))
		feedL.configure(image=feedI)
		feedL.update()

### function which acts as a thread for google calendar API manipulation.
def start_gcal():
	global fileData
	fileData = update()

	for file in fileData:
		with open(file[0], "wb") as f:
			f.write(file[1])

		match, valid = False, False

		while not match:
			timeNow = datetime.datetime.now().strftime("%H.%M")

			if float(file[3]) >= float(timeNow):
				valid = True
			else:
				match = True

			if float(file[3]) <= float(timeNow) and valid:

				while audio.is_set():
					time.sleep(3)

				audio_out(file[0], file[2])
				match = True
				
		os.remove(file[0])

### function which is called by exit button or gesture command to close the
### application and remove any files which were waiting to be output.
def close():
	for f in fileData:
		try:
			os.remove(f[0])
		except:
			pass
	
	cap.release()
	cv2.destroyAllWindows()

	root.destroy()

### main program which contains classes, GUI and threading setup.
if __name__ == "__main__":

	### setup global instances of pre-written classes.
	global mp_model
	mp_model = HandModel(source=1)
	global obj
	obj = gAPI(source=1)

	### setup simple interface ising tkinter library.
	rawDate = datetime.date.today()
	date = [int(i) for i in str(datetime.date.today()).split("-")]

	root = Tk()
	root.title("main app")        
	root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")

	def resetDate():
		cal.selection_set(rawDate)

	feedL = Label(root)
	feedL.grid(row=0, column=0, columnspan=2, rowspan=2, padx=90, pady=15)

	guide = Image.open("gesture_guide.png")
	w, h, factor = guide.width, guide.height, 0.55
	guideI = ImageTk.PhotoImage(guide.resize((int(w*factor), int(h*factor))))
	guideL = Label(root, image=guideI)
	guideL.grid(row=2, column=0, columnspan=3, padx=100, pady=10)

	todayB = Button(root, text=f"reset to today!", command=resetDate, font=tkinter.font.Font(size=15))
	todayB.grid(row=0, column=2, sticky="S")

	cal = Calendar(root, font="Arial 12", selectmode="day", year=date[0], month=date[1], day=date[2])
	cal.grid(row=1, column=2, padx=85, pady=30, sticky="N")

	### setup threading for both sides and audio event for resource locking.
	audio = threading.Event() #(set=lock, clear=unlock)

	feed = threading.Thread(target=start_feed)
	feed.start()

	gcal = threading.Thread(target=start_gcal)
	gcal.start()

	### make sure when closed via command or button all necessary duties are finished
	root.protocol("WM_DELETE_WINDOW", close)
	root.mainloop()



