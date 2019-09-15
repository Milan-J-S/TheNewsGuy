#DBops

import sqlite3
con = sqlite3.connect("database.db")

con.execute("DROP TABLE UserData")
con.execute("CREATE TABLE UserData (user TEXT, word TEXT, level NUMBER)")
print("Table created succesfully")

con.execute("DROP TABLE Validation")
con.execute("CREATE TABLE Validation (user TEXT, term TEXT, score NUMBER)")
print("Table created succesfully")

con.execute("DROP TABLE TrainingSet")
con.execute("CREATE TABLE TrainingSet (user TEXT, term TEXT, score NUMBER, lv1score NUMBER, lv2score NUMBER)")
print("Table created succesfully")