### CAL API SERVICE AND DATABASE INTEGRATION

### importing libraries.
import datetime
import collections
import math

import sqlite3 as sql

from gtts import gTTS
from mutagen.mp3 import MP3

import os
import time

import pickle
from apiclient.discovery import build

### define class for google calendar API integration.
class gAPI():

	### access credentials and setup service object via constructor.
	def __init__(self, source):
		self.source = "gcal_and_db/" if source else ""
		self.cred = pickle.load(open(f"{self.source}token.pkl", "rb"))
		self.service = build("calendar", "v3", credentials=self.cred)

	### method for returning raw data from google calendars.
	def returnData(self):
		calendarsInfo = self.service.calendarList().list().execute()
		calendarIds = [calendarsInfo["items"][i]["id"] for i in range(len(calendarsInfo["items"]))]

		today = datetime.date.today()
		tomorrow = today + datetime.timedelta(days=1)
		timeNow = datetime.datetime.now().strftime("%H:%M:%S")

		if str(datetime.datetime.utcnow().astimezone().tzinfo) == "GMT Summer Time":
			offset = "+01:00"
		else:
			offset = "+00:00"

		dailyEvents = self.service.events().list(
			calendarId=calendarIds[0],
			singleEvents=True,
			timeMax=f"{str(tomorrow)}T00:00:00{offset}",
			timeMin=f"{str(today)}T{timeNow}{offset}",
			timeZone="Europe/London",
			orderBy="startTime"
			).execute()

		dailyEventsInfo = [(dailyEvents["items"][i]["summary"],
							dailyEvents["items"][i]["start"],
							dailyEvents["items"][i]["end"],
							dailyEvents["items"][i]["reminders"]) for i in range(len(dailyEvents["items"]))]

		return dailyEventsInfo

	### parsing through raw data to return ready to process data.
	def cleanData(self, dailyEventsInfo):
		timeNow = datetime.datetime.now().strftime("%H:%M:%S")
		eventData = []
		for eventInfo in dailyEventsInfo:
			data = [eventInfo[0]]
			valid = False
			if len(eventInfo[1]) == 1:
				eventTime = ["None", 0, 0, 0, 1]
				valid = True
			else:
				start, end = eventInfo[1]["dateTime"], eventInfo[2]["dateTime"]
				sT, eT = start.index("T"), end.index("T")
				startTime = [str(i) for i in start[sT+1:sT+6].split(":")]
				endTime = [str(i) for i in end[eT+1:eT+6].split(":")]
				
				if ":".join(startTime) > timeNow:
					valid = True
					hrs = int(endTime[0])-int(startTime[0])
					mins = int(endTime[1])-int(startTime[1])
					
					if mins<0:
						mins += 60
						hrs -= 1
					if hrs<0:
						hrs += 24

					if not eventInfo[3]["useDefault"]:
						rem = eventInfo[3]["overrides"][0]["minutes"]
					else:
						rem = 30


					eventTime = [":".join(startTime), hrs, mins, rem, 0]

			if valid:
				data.extend(eventTime)
				eventData.insert(0, tuple(data))
			
		return eventData

	### collecting eventData from above methods in order to store in "events" database.
	def eventsUpdate(self):
		eventData = self.cleanData(self.returnData())

		conn = sql.connect(f"{self.source}cal_data.db")
		cursor = conn.cursor()

		cursor.execute("DELETE FROM events")
		cursor.executemany("INSERT INTO events VALUES (?, ?, ?, ?, ?, ?)", eventData)

		conn.commit()
		conn.close()

	### pulling eventData from the "events" dababase.
	### --> ready to process and output.
	def dataRetrieval(self):
		conn = sql.connect(f"{self.source}cal_data.db")
		cursor = conn.cursor()

		cursor.execute("""SELECT * FROM events 
			WHERE all_day IS TRUE""")
		all_day = cursor.fetchall()

		cursor.execute("""SELECT * FROM events 
			WHERE all_day IS FALSE""")
		eventData = cursor.fetchall()

		conn.commit()
		conn.close()

		return all_day, eventData

	### uses above methods to interact with database and prepare data for output.
	### --> audio stored as binary data in "output_files" database.
	def dataProcessing(self):

		all_day, eventData = self.dataRetrieval()
		
		inputs = []
		while eventData:
			# valid = []
			# oneHr = (datetime.datetime.now() + datetime.timedelta(hours=1)).strftime("%H:%M")
			
			output1, output2 = "", ""
			
			ev = eventData.pop()
			dur = str(ev[2]) + " hrs and " + str(ev[3]) + " mins"
			output1 += f"you have {ev[0]} event in {ev[4]} mins at {ev[1]} for {dur},"
			output2 = f"you have {ev[0]} event starting now at {ev[1]}"

			if all_day:
				alldayOut = "\nyour all day events include: "
				for a_d in all_day:
					alldayOut += f"{a_d[0]} event, "
				output1 += alldayOut[:-2]

			file1 = f"{self.source}gtts_{ev[0].replace(' ', '')}_1.mp3"
			gTTS(output1, lang="en").save(file1)
			file2 = f"{self.source}gtts_{ev[0].replace(' ', '')}_2.mp3"
			gTTS(output2, lang="en").save(file2)
			
			with open(file1, "rb") as f:
				binary1 = f.read()
				length1 = MP3(f).info.length
				rem = ((datetime.datetime.strptime(ev[1], "%H:%M")
					-datetime.timedelta(minutes=ev[4])).strftime("%H:%M")).replace(":", ".")
			os.remove(file1)
			
			with open(file2, "rb") as f:
				binary2 = f.read()
				length2 = MP3(f).info.length
				start = ev[1].replace(":", ".")
			os.remove(file2)

			db_input = [[file1, binary1, length1, rem],
						[file2, binary2, length2, start]]
			

			inputs.extend(db_input)

		conn = sql.connect(f"{self.source}output_files.db")
		cursor = conn.cursor()

		cursor.execute("DELETE FROM files")
		cursor.executemany("INSERT INTO files VALUES (?, ?, ?, ?)", inputs)

		conn.commit()
		conn.close()


	def dataOutput(self):
		conn = sql.connect(f"{self.source}output_files.db")
		cursor = conn.cursor()

		cursor.execute("""SELECT * FROM files
			""")
		fileData = cursor.fetchall()
		### [file, binary, length, rem]

		conn.commit()
		conn.close()

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
					os.system(f"start {file[0]}")
					time.sleep(file[2]+5)
					match = True
					
			os.remove(file[0])
	



					# os.system("taskkill /f /im zune.exe")


