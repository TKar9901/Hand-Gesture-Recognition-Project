# DAILY UPDATE

from gcalAPI import returnData
eventData = returnData()

import sqlite3 as sql

con = sql.connect("cal_data.db")
c = con.cursor()

c.execute("DELETE FROM events")

c.executemany("INSERT INTO events VALUES (?, ?, ?, ?, ?, ?)", eventData)

con.commit()
con.close()
