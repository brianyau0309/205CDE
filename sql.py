from database import connection,SQL
from pathlib import Path
import os

db = connection()

items = db.exe_fetch(SQL['categoryResult'].format(c='other'),'all')
itemIn4 = []
while len(items) != 0:
	if len(items) >= 4:
		itemIn4.append([items.pop(0),items.pop(0),items.pop(0),items.pop(0)])
	else:
		itemIn4.append(items)
		items = []

print(itemIn4)