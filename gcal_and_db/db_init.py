### DATABASE INTEGRATION
### --> initialisation of dbs

import sqlite3 as sql

con = sql.connect("cal_data.db")
c = con.cursor()

c.execute("""CREATE TABLE events (
			name TEXT,
			startTime TEXT,
			hrs INTEGER,
			mins INTEGER,
			reminder INTEGER,
			all_day INTEGER
	)""")

con.commit()
con.close()

con = sql.connect("output_files.db")
c = con.cursor()

c.execute("""CREATE TABLE files (
			fileName TEXT,
			audioBinary BLOB,
			length REAL,
			reminder TEXT
	)""")


con.commit()
con.close()