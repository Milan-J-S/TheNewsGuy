#DBview

import sqlite3
con = sqlite3.connect("database.db")

rows = con.execute("SELECT * FROM UserData").fetchall()
print("ALL DATA")
print(rows)

rows = con.execute("SELECT * FROM UserData WHERE LEVEL = 1 ").fetchall()
print("LEVEL 1 DATA")
print(rows)

rows = con.execute("SELECT * FROM UserData WHERE LEVEL = 2 ").fetchall()
print("LEVEL 2 DATA")
print(rows)

rows = con.execute("SELECT * FROM Validation ").fetchall()
print("VALIDATION DATA")
print(rows)

rows = con.execute("SELECT * FROM TrainingSet ").fetchall()
print("TRAINING SET DATA")
print(rows)


