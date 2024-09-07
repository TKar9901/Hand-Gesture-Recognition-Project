#temp gcal_main.py

from gcal_and_db.gcalAPI import gAPI
import os
import sqlite3 as sql
import datetime
import time

obj = gAPI(source=1)

# print("updating events...")
obj.eventsUpdate()
# print("filing data...")
obj.dataProcessing()
# print("making output files...")

#data output
conn = sql.connect(os.path.join("gcal_and_db", "output_files.db"))
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
			time.sleep(file[2]+1)
			match = True
			
	os.remove(file[0])
	# os.system("taskkill /f mediaplayer.exe")