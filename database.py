import pymysql

class connection():
	def __init__(self):
		self.connection = pymysql.connect(user='user1', password='0000', db='205CDE', cursorclass=pymysql.cursors.DictCursor)
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
	'changePassword':'''
UPDATE `client` SET password = '{p}' WHERE clientID = {id}
''',
	'signup':'''
INSERT INTO client (email, nickname, password) value ('{e}','{n}','{p}')
''',
	'newArticle':'''
INSERT INTO article (`title`, `price`, `description`, `content`, `date`, `owner`,`category`) value ('{t}','{p}','{des}','{c}','{date}','{o}','{category}')
''',
	'articleInfo':'''
SELECT * FROM article WHERE articleID = '{ID}'
''',
	'articleInfo_owner':'''
SELECT * FROM article WHERE owner = '{ID}' ORDER BY `date` DESC
''',
	'record_owner':'''
SELECT `recordID`,`articleID`,`title`,record.`date`,`price`,`description`,`content`,`sales`,`category` FROM record LEFT JOIN article ON record.article = article.articleID WHERE record.owner = {ID} ORDER BY `date` DESC
''',
	'cart_owner':'''
SELECT `inCartID`,`articleID`, article.`owner`,`title`,`price`,`category` FROM cart LEFT JOIN article ON cart.article = article.articleID WHERE cart.owner = {ID}
''',
	'hot_item':'''
SELECT * FROM article ORDER BY `sales` DESC LIMIT 8
''',
	'checkRecord':'''
SELECT * FROM record WHERE owner = {clientID} and article = {articleID}
''',
	'checkCart':'''
SELECT * FROM cart WHERE article = {articleID} and owner = {clientID}
''',
	'add2cart':'''
INSERT INTO cart (`article`, `owner`) value ({articleID}, {clientID})
''',
	'buyone':'''
INSERT INTO record (`article`, `owner`, `date`) value ({articleID}, {clientID}, '{date}')
''',
	'cart_del':'''
DELETE FROM cart WHERE `owner` = {clientID} and `article` = {articleID}
''',
	'cart_delAll':'''
DELETE FROM cart WHERE `owner` = {clientID}
''',
	'cartInfo':'''
SELECT * FROM cart WHERE `owner` = {clientID}
''',
	'categoryResult':'''
SELECT * FROM article WHERE `category` = '{c}' ORDER BY `date` DESC
''',
	'searching_title':'''
SELECT * FROM article WHERE `title` LIKE '%{q}%' ORDER BY `date` DESC
''',
	'searching_title_byPriceL2H':'''
SELECT * FROM article WHERE `title` LIKE '%{q}%' ORDER BY `price` ASC
''',
	'searching_title_byPriceH2L':'''
SELECT * FROM article WHERE `title` LIKE '%{q}%' ORDER BY `price` DESC
''',
	'searching_title_bySales':'''
SELECT * FROM article WHERE `title` LIKE '%{q}%' ORDER BY `sales` ASC
''',
	'adminInfo_ac':'''
SELECT adminID,account,password FROM admin WHERE account = '{ac}'
''',
	'adminInfo_id':'''
SELECT * FROM admin WHERE adminID = {id}
''',
	'allClient':'''
SELECT * FROM client
''',
	'allArticle':'''
SELECT * FROM article
''',
	'allRevenue':'''
SELECT * FROM revenue
''',
	'allComment':'''
SELECT * FROM comment
''',
	'allNews':'''
SELECT * FROM news
''',
	'allNews_desc':'''
SELECT * FROM news ORDER BY `date` DESC
''',
	'allNews_desc_event':'''
SELECT * FROM news WHERE type = 'event' ORDER BY `date` DESC
''',
	'allNews_desc_system':'''
SELECT * FROM news WHERE type = 'system' ORDER BY `date` DESC
''',
	'allAdmin':'''
SELECT * FROM admin
''',
	'updateClient':'''
UPDATE client SET email = '{e}', nickname = '{n}', password = '{p}' WHERE clientID = '{ID}'
''',
	'updateArticle':'''
UPDATE article SET category = '{cate}',title = '{t}',price = '{p}',description = "{d}",content = "{cont}" WHERE articleID = {ID}
''',
	'revenueInfo':'''
SELECT * FROM revenue WHERE `date` = '{date}'
''',
	'newRevenue':'''
INSERT INTO revenue (`date`,`revenue`) VALUE ('{d}',{r})
''',
	'newNews':'''
INSERT INTO news (`title`,`content`,`date`,`author`,`type`) VALUE ('{t}','{c}','{d}','{a}','{type}')
''',
	'newAdmin':'''
INSERT INTO admin (`account`,`password`,`client`,`article`,`comment`,`carousel`,`news`,`revenue`) VALUE ('{ac}','{p}','{client}','{article}','{comment}','{carousel}','{news}','{r}')
''',
	'newsInfo':'''
SELECT * FROM news WHERE newsID = {ID}
''',
	'updateNews':'''
UPDATE news SET type = '{type}',title = '{t}', content = '{c}' WHERE newsID = {ID}
''',
	'updateRevenue':'''
UPDATE revenue SET `revenue` = {r}
''',
	'updateAdmin':'''
UPDATE admin SET account = '{ac}', password = '{p}', client = '{client}', article = '{article}', comment = '{comment}', carousel = '{carousel}', news = '{news}', revenue = '{revenue}' WHERE adminID = {ID}
''',
	'comment':'''
INSERT INTO comment (`article`,`author`,`comment`,`date`) VALUE ({a},{o},"{c}","{d}")
''',
	'getComment':'''
SELECT * FROM comment WHERE article = {ID} ORDER BY `date` DESC
''',
	'commentInfo':'''
SELECT * FROM comment WHERE commentID = {ID}
''',
	'updateSales':'''
UPDATE article SET `sales` = {s} WHERE `articleID` = {ID}
''',
	'updateComment':'''
UPDATE comment SET `comment` = '{c}' WHERE `commentID` = {ID}
'''
}
