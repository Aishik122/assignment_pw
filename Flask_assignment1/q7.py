#7. Integrate a SQLite database with Flask to perform CRUD operations on a list of items.


import sqlite3 
conn = sqlite3.connect('database.db')

c = conn.cursor()

# c.execute("""
# CREATE TABLE GG(
#           first_name text,
#           last_name text,
#           mobile text
# )
#c.execute("insert into GG values('aishik','kuchbhi','000000')")

print (c.fetchall())
conn.commit()
conn.close()