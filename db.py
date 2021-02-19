import sqlite3

con = sqlite3.connect("testFirst.db")
print("Database opened successfully")
con.execute(
    "create table test"
    " (id INTEGER PRIMARY KEY AUTOINCREMENT, "
    "amb integer NOT NULL,"
    "queue integer NOT NULL,"
    "state integer NOT NULL,"
    "amount int NOT NULL,"
    "task float  NOT NULL,"
    "reason varchar(100),"
    "cdate TEXT DEFAULT CURRENT_TIMESTAMP )")

print("Table created successfully")
con.close()
