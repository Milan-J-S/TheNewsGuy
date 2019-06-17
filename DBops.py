#DBops

import sqlite3
con = sqlite3.connect("database.db")

# con.execute("DROP TABLE UserData")
con.execute("CREATE TABLE UserData (user TEXT, word TEXT, level NUMBER)")
print("Table created succesfully")