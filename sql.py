from database import connection,SQL

db = connection()

data = db.exe_fetch(SQL['hot_item'],'all')
a = data[:4]
b = data[4:]
print(a)
print(b)

db.close()
