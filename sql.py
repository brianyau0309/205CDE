from database import connection,SQL
from pathlib import Path
import os

'''db = connection()

data = db.exe_fetch(SQL['hot_item'],'all')
a = data[:4]
b = data[4:]
print(a)
print(b)

db.close()'''
user = 1
print(Path(os.getcwd()+'/static/image/icom/'+str(user)+'.png').exists())