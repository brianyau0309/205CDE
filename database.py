import pymysql

class connection():
	def __init__(self):
		self.connection = pymysql.connect(user='user1', password='0000', db='205Assignment', cursorclass=pymysql.cursors.DictCursor)
		self.cursor = self.connection.cursor()

	def exe_fetch(self, SQL, fetch = 'one'):
		self.cursor.execute(SQL)
		if fetch == 'one':
			return self.cursor.fetchone()
		elif fetch == 'all':
			return self.cursor.fetchall()
	def exe_commit(self, SQL):
		self.cursor.execute(SQL)
		self.connection.commit()

	def close(self):
		self.connection.close()

SQL = {
	'clientInfo_email':'''
SELECT * FROM client WHERE email = '{email}'
''',
	'clientInfo_ID':'''
SELECT * FROM client WHERE clientID = {clientID}
''',
	'signup':'''
INSERT INTO client (email, nickname, password) value ('{e}','{n}','{p}')
''',
	'newArticle':'''
INSERT INTO article (`title`, `price`, `description`, `content`, `date`, `owner`) value ('{t}','{p}','{des}','{c}','{date}','{o}')
''',
	'articleInfo':'''
SELECT * FROM article WHERE articleID = '{ID}'
''',
	'articleInfo_owner':'''
SELECT * FROM article WHERE owner = '{ID}' ORDER BY `date` DESC
''',
	'hot_item':'''
SELECT * from article ORDER BY `sales` DESC LIMIT 8
'''
}
