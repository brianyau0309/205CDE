#Author : Yau Siu Fung Brian

#setting
###############################################################################################
from flask import Flask, render_template, redirect, url_for, request, session, flash
from database import connection, SQL
from pathlib import Path
from werkzeug.utils import secure_filename
import os, datetime
###############################################################################################
UPLOAD_ICON_FOLDER = os.getcwd()  + '/static/image/icon'
UPLOAD_ARTICLE_FOLDER = os.getcwd()  + '/static/image/article'
UPLOAD_CAROUSEL_FOLDER = os.getcwd()  + '/static/image/Carousel'
ALLOWED_EXTENSIONS = set(['png', 'jpg'])

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['UPLOAD_ICON_FOLDER'] = UPLOAD_ICON_FOLDER
app.config['UPLOAD_ARTICLE_FOLDER'] = UPLOAD_ARTICLE_FOLDER
app.config['UPLOAD_CAROUSEL_FOLDER'] = UPLOAD_CAROUSEL_FOLDER

db = connection()
###############################################################################################

#function
###############################################################################################
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_user(): #get user by session
	user = session.get('clientID')
	if user != None:
		info = db.exe_fetch(SQL["clientInfo_ID"].format(clientID=user), 'one')
		if Path(os.getcwd()+'/static/image/icon/'+str(user)+'.png').exists():
			info['icon'] = 'image/icon/'+str(user)+'.png'
		elif Path(os.getcwd()+'/static/image/icon/'+str(user)+'.jpg').exists():
			info['icon'] = 'image/icon/'+str(user)+'.jpg'
		else:
			info['icon'] = 'image/icon/default.png'

		return info
	else:
		return 'Guest'

def get_cart(): #get user by session
	user = session.get('clientID')
	if user != None:
		items = db.exe_fetch(SQL["cart_owner"].format(ID=user), 'all')
		for i in items:
			ownerName = db.exe_fetch(SQL['clientInfo_ID'].format(clientID=i['owner']))['nickname']
			i['author'] = ownerName
			if Path(os.getcwd()+'/static/image/article/'+str(i['articleID'])+'.png').exists():
				i['image'] = 'image/article/'+str(i['articleID'])+'.png'
			elif Path(os.getcwd()+'/static/image/article/'+str(i['articleID'])+'.jpg').exists():
				i['image'] = 'image/article/'+str(i['articleID'])+'.jpg'
			else:
				i['image'] = 'image/article/default.png'

		if items == ():
			items = 'Nothing'
		return items
	else:
		return 'Guest'
###############################################################################################

#Home
###############################################################################################
@app.route('/index')
@app.route('/')
def home():
	items = db.exe_fetch(SQL['hot_item'],'all')
	for i in items:
		ownerName = db.exe_fetch(SQL['clientInfo_ID'].format(clientID=i['owner']))['nickname']
		i['ownerName'] = ownerName
		if Path(os.getcwd()+'/static/image/article/'+str(i['articleID'])+'.png').exists():
			i['image'] = 'image/article/'+str(i['articleID'])+'.png'
		elif Path(os.getcwd()+'/static/image/article/'+str(i['articleID'])+'.jpg').exists():
			i['image'] = 'image/article/'+str(i['articleID'])+'.jpg'
		else:
			i['image'] = 'image/article/default.png'

	hot_1 = items[:4]
	hot_2 = items[4:]
	return render_template('Home.html', userInfo=get_user(), cart=get_cart(), hot_1=hot_1, hot_2=hot_2)
###############################################################################################
#Home end


#login
###############################################################################################
@app.route('/login')
def login():
	if session.get('clientID') != None:
		return redirect(url_for('home'))	
	else:
		return render_template('Login.html')

@app.route('/login_done', methods = ["post"])
def login_done():
	email = request.form["email"]
	password = request.form["password"]
	checkAdmin = db.exe_fetch(SQL['adminInfo_ac'].format(ac=email))
	checkEmail = db.exe_fetch(SQL['clientInfo_email'].format(email=email))

	if checkAdmin == None:
		pass
	elif checkAdmin.get('password') != password:
		pass
	else:
		session['admin'] = checkAdmin['adminID']
		return redirect(url_for('admin'))

	if (checkEmail == None):
		flash("Invaild")
		return redirect(url_for('login'))
	elif  (checkEmail.get('password') != password):
		flash("Invaild")
		return redirect(url_for('login'))
	else:
		session['clientID'] = checkEmail['clientID']
		return redirect(url_for('home'))


@app.route('/logout')
def logout():
	if session.get('clientID') != None:
		session.pop('clientID')
		return redirect(url_for('home'))
	else:
		return redirect(url_for('login'))
###############################################################################################
#login end

#signup
###############################################################################################
@app.route('/signup')
def signup():
	if session.get('clientID') != None:
		return redirect(url_for('home'))	
	else:
		return render_template('SignUp.html')


@app.route('/signup_done', methods = ["post"])
def signup_done():
	if session.get('clientID') != None:
		return redirect(url_for('home'))
	else:
		email = request.form["email"]
		name = request.form["name"]
		password = request.form["password"]
		cpassword = request.form["cpassword"]

		checkEmail = db.exe_fetch(SQL['clientInfo_email'].format(email=email))

		if password != cpassword:
			flash('Invaild','error')
			return redirect(url_for('signup'))
		else:
			if checkEmail == None:
				db.exe_commit(SQL['signup'].format(e=email,n=name,p=password))
				userInfo = db.exe_fetch(SQL['clientInfo_email'].format(email=email))
				icon = url_for('static',filename=userInfo['icon'])

				return render_template('SignUp_Done.html',usericon=icon,userID=userInfo['clientID'],userName=userInfo['nickname'],userEmail=userInfo['email'],userPassword=userInfo['password'])
			else:
				flash('Used email','email')
				return redirect(url_for('signup'))
###############################################################################################
#signup end

#user pages
###############################################################################################
@app.route('/record')
def record():
	if session.get('clientID') != None:
		userID = session.get('clientID')
		records = db.exe_fetch(SQL['record_owner'].format(ID=userID),'all')
		for record in records:
			if Path(os.getcwd()+'/static/image/article/'+str(record['articleID'])+'.png').exists():
				record['image'] = 'image/article/'+str(record['articleID'])+'.png'
			elif Path(os.getcwd()+'/static/image/article/'+str(record['articleID'])+'.jpg').exists():
				record['image'] = 'image/article/'+str(record['articleID'])+'.jpg'
			else:
				record['image'] = 'image/article/default.png'
		
		return render_template('list_article.html',pageTitle='Record',userInfo=get_user(),cart=get_cart(),articles=records)
	else:
		return redirect(url_for('login'))


@app.route('/myarticle')
def myarticle():
	if session.get('clientID') != None:
		userID = session.get('clientID')
		articles = db.exe_fetch(SQL['articleInfo_owner'].format(ID=userID),'all')
		for article in articles:
			if Path(os.getcwd()+'/static/image/article/'+str(article['articleID'])+'.png').exists():
				article['image'] = 'image/article/'+str(article['articleID'])+'.png'
			elif Path(os.getcwd()+'/static/image/article/'+str(article['articleID'])+'.jpg').exists():
				article['image'] = 'image/article/'+str(article['articleID'])+'.jpg'
			else:
				article['image'] = 'image/article/default.png'
		
		return render_template('list_article.html',pageTitle='My Article',cart=get_cart(),userInfo=get_user(),articles=articles)
	else:
		return redirect(url_for('login'))
###############################################################################################
#user pages end

#edition
###############################################################################################
@app.route('/edit')
def edit():
	if session.get('clientID') != None:
		return render_template('Edition.html',userInfo=get_user(),cart=get_cart())	
	else:
		return redirect(url_for('login'))	


@app.route("/edit_done", methods=['post'])
def edit_done():
	if session.get('clientID') != None:
		clientID = session.get('clientID')
		title = request.form['title']
		price = request.form['price']
		description = request.form['description']
		content = request.form['content'].replace('\'','\\\'').replace('\"','\\\"')
		category = request.form['category'].lower()
		date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

		db.exe_commit(SQL['newArticle'].format(t=title,p=price,des=description,c=content,date=date,o=clientID,category=category))
		articleID = db.cursor.lastrowid

		file = request.files['img']
		if file and allowed_file(file.filename):
			filename = str(articleID) + '.' + secure_filename(file.filename).split('.')[-1]
			file.save(os.path.join(app.config['UPLOAD_ARTICLE_FOLDER'], filename))
		elif file.filename == '':
			pass
		else:
			flash('imgError', 'imgError')

		flash('compose','compose')
		return redirect(url_for('home'))
	else:
		return redirect(url_for('login'))

@app.route("/edit_own_article/<path:aID>", methods=['post'])
def edit_own_article(aID):
	if session.get('clientID') != None:
		user = session['clientID']
		a = db.exe_fetch(SQL['articleInfo'].format(ID=aID))
		author = db.exe_fetch(SQL['clientInfo_ID'].format(clientID=a['owner']))['clientID']
		if user == author:
			return render_template('userEdit.html',data=a,articleID=aID)
		else: 
			message = 'You don\'t have permission'
			return render_template('back.html',title='Error',message=message)
	else:
		return redirect(url_for('login'))

@app.route("/own_edit_done", methods=['post'])
def own_edit_done():
	if session.get('clientID') != None:
		user = session['clientID']
		articleID = request.form['articleID']
		a = db.exe_fetch(SQL['articleInfo'].format(ID=articleID))
		author = db.exe_fetch(SQL['clientInfo_ID'].format(clientID=a['owner']))['clientID']
		if user == author:
			file = request.files['img']		
			title = request.form['title']
			price = request.form['price']
			description = request.form['description']
			content = request.form['content'].replace('\'','\\\'').replace('\"','\\\"')
			category = request.form['category'].lower()

			db.exe_commit(SQL['updateArticle'].format(cate=category,t=title,p=price,d=description,cont=content,ID=articleID))
			if file and allowed_file(file.filename):
				filename = str(articleID) + '.' + secure_filename(file.filename).split('.')[-1]
				file.save(os.path.join(app.config['UPLOAD_ARTICLE_FOLDER'], filename))
			elif file.filename == '':
				pass
			else:
				flash('imgError', 'imgError')
				return redirect(url_for('home'))

			flash('compose','compose')
			return redirect(url_for('home'))
		else: 
			message = 'You don\'t have permission'
			return render_template('back.html',title='Error',message=message)
	else:
		return redirect(url_for('login'))

###############################################################################################	
#edition end

#article
###############################################################################################
@app.route('/article_description/<path:aID>/')
def article_description(aID):
	a = db.exe_fetch(SQL['articleInfo'].format(ID=aID))
	ownerName = db.exe_fetch(SQL['clientInfo_ID'].format(clientID=a['owner']))['nickname']
	comment = db.exe_fetch(SQL['getComment'].format(ID=aID),'all')
	counter = len(comment)
	for i in comment:
		authorInfo = db.exe_fetch(SQL['clientInfo_ID'].format(clientID=i['author']))
		i['num'] = '#'+str(counter)
		i['authorName'] = authorInfo['nickname']
		i['comment'] = i['comment'].replace('\n','<br>')
		if Path(os.getcwd()+'/static/image/icon/'+str(i['author'])+'.png').exists():
			i['icon'] = 'image/icon/'+str(i['author'])+'.png'
		elif Path(os.getcwd()+'/static/image/icon/'+str(i['author'])+'.jpg').exists():
			i['icon'] = 'image/icon/'+str(i['author'])+'.jpg'
		else:
			i['icon'] = 'image/icon/default.png'
		counter -= 1

	return render_template('Article_Description.html', userInfo=get_user(),cart=get_cart(),title=a['title'], price=a['price'], description=a['description'].replace('\n','<br>'), date=a['date'], name=ownerName, articleID=a['articleID'],comment=comment)

@app.route('/comment', methods=['post'])
def comment():
	if session.get('clientID') != None:
		user = session['clientID']
		article = request.form['articleID']
		comment = request.form['comment'].replace('\'','\\\'').replace('\"','\\\"')
		date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

		db.exe_commit(SQL['comment'].format(a=article,o=user,c=comment,d=date))

		message = 'Comment Success!'

		return render_template('back.html', title='Success', message=message)
	else:
		return redirect(url_for('login'))

@app.route('/article/<path:aID>/')
def article(aID):
	if session.get('clientID') != None:
		user = session['clientID']
		bought = db.exe_fetch(SQL['checkRecord'].format(clientID=user,articleID=aID))
		a = db.exe_fetch(SQL['articleInfo'].format(ID=aID))
		author = db.exe_fetch(SQL['clientInfo_ID'].format(clientID=a['owner']))['clientID']
		if bought != None or user == author:
			ownerName = db.exe_fetch(SQL['clientInfo_ID'].format(clientID=a['owner']))['nickname']
			return render_template('Article.html', userInfo=get_user(),cart=get_cart(),title=a['title'], content=a['content'].replace('\n','<br>'), date=a['date'], name=ownerName,articleID=aID,owner=(user==author))
		else: 
			flash('buy', 'buy')
			return redirect(url_for('home'))
	else:
		return redirect(url_for('login'))


@app.route('/addtocart', methods=['post'])
def addtocart():
	if session.get('clientID') != None:
		user = session['clientID']
		article = request.form['articleID']
		articleOwner =  db.exe_fetch(SQL['articleInfo'].format(ID=article))['owner']
		inCart = db.exe_fetch(SQL['checkCart'].format(articleID=article, clientID=user))
		inRecord = db.exe_fetch(SQL['checkRecord'].format(articleID=article, clientID=user))
		if articleOwner == user:
			message = 'It is your article!'
			return render_template('back.html', title='Error', message=message)
		elif inCart != None:
			message = 'It is already in your cart!'
			return render_template('back.html', title='Error', message=message)
		elif inRecord != None:
			message = 'Your have already bought this article!'
			return render_template('back.html', title='Error', message=message)
		else:
			db.exe_commit(SQL['add2cart'].format(articleID=article, clientID=user))
			message = 'Your have successfully add this article to cart!'
			return render_template('back.html', title='Success', message=message)
	else:
		return redirect(url_for('login'))


@app.route('/buyone', methods=['post'])
def buyone():
	if session.get('clientID') != None:
		user = session['clientID']
		article = request.form['articleID']
		articleOwner =  db.exe_fetch(SQL['articleInfo'].format(ID=article))['owner']
		inRecord = db.exe_fetch(SQL['checkRecord'].format(articleID=article, clientID=user))
		date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

		if articleOwner == user:
			message = 'It is your article!'
			return render_template('back.html', title='Error', message=message)
		elif inRecord != None:
			message = 'Your have already bought this article!'
			return render_template('back.html', title='Error', message=message)
		else:
			db.exe_commit(SQL['buyone'].format(articleID=article, clientID=user, date=date))
			db.exe_commit(SQL['cart_del'].format(articleID=article,clientID=user))

			sales = db.exe_fetch(SQL['articleInfo'].format(ID=article))['sales']
			sales += 1
			db.exe_commit(SQL['updateSales'].format(s=sales,ID=article))

			flash('Thank you for your patronage!','thank')
			return redirect(url_for('article', aID=article))
	else:
		return redirect(url_for('login'))


@app.route('/cart_del', methods=['post'])
def cart_del():
	if session.get('clientID') != None:
		user = session['clientID']
		article = request.form['article']
			
		db.exe_commit(SQL['cart_del'].format(articleID=article,clientID=user))
		flash('opencart','opencart')
		return render_template('back.html',message='Cancel Success',title='Success')

	else:
		return redirect(url_for('login'))

@app.route('/purchase', methods=['post'])
def purchase():
	if session.get('clientID') != None:
		user = session['clientID']
		cartInfo = db.exe_fetch(SQL['cartInfo'].format(clientID=user),'all')
		date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		today = datetime.datetime.today().strftime("%Y-%m-%d")

		for i in cartInfo:
			db.exe_commit(SQL['buyone'].format(articleID=i['article'],clientID=user,date=date))

			sales = db.exe_fetch(SQL['articleInfo'].format(ID=i['article']))['sales']
			sales += 1
			db.exe_commit(SQL['updateSales'].format(s=sales,ID=i['article']))

			price = db.exe_fetch(SQL['articleInfo'].format(ID=i['article']))['price']
			todayRevenue = db.exe_fetch(SQL['revenueInfo'].format(date=today))
			if todayRevenue == None:
				db.exe_commit(SQL['newRevenue'].format(d=today,r=price))
			else:
				total = todayRevenue['revenue']
				total += price
				db.exe_commit(SQL['updateRevenue'].format(r=total))

		db.exe_commit(SQL['cart_delAll'].format(clientID=user))

		message = 'Purchase Success!'
		return render_template('back.html', title='Success', message=message)
	else:
		return redirect(url_for('login'))

###############################################################################################
#article end 		

#Profile function
###############################################################################################
@app.route('/uploadicon', methods=['post'])
def uploadicon():
	if session.get('clientID') != None:
		user = str(session['clientID'])
		file = request.files['icon']
		if file and allowed_file(file.filename):
			filename = user + '.' + secure_filename(file.filename).split('.')[-1]
			file.save(os.path.join(app.config['UPLOAD_ICON_FOLDER'], filename))
			flash("icon", "iconSuccess")

		else:
			flash("icon","iconError")

		return redirect(url_for('home'))
	else:
		return redirect(url_for('login'))


@app.route('/changePassword', methods=['post'])
def changePassword():
	if session.get('clientID') != None:
		user = session['clientID']
		new = str(request.form['npassword'])
		db.exe_commit(SQL['changePassword'].format(p=new,id=user))
		flash('passwordSuccess', 'passwordSuccess')
		return redirect(url_for('home'))
	else:
		return redirect(url_for('login'))
###############################################################################################
#Profile function end

#Category page
###############################################################################################
@app.route('/category/<path:arg>')
def category(arg):
	if arg == 'chinese':
		category = 'Chinese'
		description = 'The Cooking Style in Chinese'
		items = db.exe_fetch(SQL['categoryResult'].format(c=arg),'all')
		result = len(items)
		for i in items:
			ownerName = db.exe_fetch(SQL['clientInfo_ID'].format(clientID=i['owner']))['nickname']
			i['ownerName'] = ownerName
			if Path(os.getcwd()+'/static/image/article/'+str(i['articleID'])+'.png').exists():
				i['image'] = 'image/article/'+str(i['articleID'])+'.png'
			elif Path(os.getcwd()+'/static/image/article/'+str(i['articleID'])+'.jpg').exists():
				i['image'] = 'image/article/'+str(i['articleID'])+'.jpg'
			else:
				i['image'] = 'image/article/default.png'

		itemIn4 = []
		while len(items) != 0:
			if len(items) >= 4:
				itemIn4.append([items.pop(0),items.pop(0),items.pop(0),items.pop(0)])
			else:
				itemIn4.append(items)
				items = []

		return render_template('Category.html',userInfo=get_user(),cart=get_cart(),category=category,description=description,result=result,items=itemIn4)
	elif arg == 'europe':
		category = 'Europe'
		description = 'The Cooking Style in Europe'
		items = db.exe_fetch(SQL['categoryResult'].format(c=arg),'all')
		result = len(items)
		for i in items:
			ownerName = db.exe_fetch(SQL['clientInfo_ID'].format(clientID=i['owner']))['nickname']
			i['ownerName'] = ownerName
			if Path(os.getcwd()+'/static/image/article/'+str(i['articleID'])+'.png').exists():
				i['image'] = 'image/article/'+str(i['articleID'])+'.png'
			elif Path(os.getcwd()+'/static/image/article/'+str(i['articleID'])+'.jpg').exists():
				i['image'] = 'image/article/'+str(i['articleID'])+'.jpg'
			else:
				i['image'] = 'image/article/default.png'

		itemIn4 = []
		while len(items) != 0:
			if len(items) >= 4:
				itemIn4.append([items.pop(0),items.pop(0),items.pop(0),items.pop(0)])
			else:
				itemIn4.append(items)
				items = []
				
		return render_template('Category.html',userInfo=get_user(),cart=get_cart(),category=category,description=description,result=result,items=itemIn4)
	elif arg == 'japanese':
		category = 'Japanese'
		description = 'The Cooking Style in Japanese'
		items = db.exe_fetch(SQL['categoryResult'].format(c=arg),'all')
		result = len(items)
		for i in items:
			ownerName = db.exe_fetch(SQL['clientInfo_ID'].format(clientID=i['owner']))['nickname']
			i['ownerName'] = ownerName
			if Path(os.getcwd()+'/static/image/article/'+str(i['articleID'])+'.png').exists():
				i['image'] = 'image/article/'+str(i['articleID'])+'.png'
			elif Path(os.getcwd()+'/static/image/article/'+str(i['articleID'])+'.jpg').exists():
				i['image'] = 'image/article/'+str(i['articleID'])+'.jpg'
			else:
				i['image'] = 'image/article/default.png'

		itemIn4 = []
		while len(items) != 0:
			if len(items) >= 4:
				itemIn4.append([items.pop(0),items.pop(0),items.pop(0),items.pop(0)])
			else:
				itemIn4.append(items)
				items = []
				
		return render_template('Category.html',userInfo=get_user(),cart=get_cart(),category=category,description=description,result=result,items=itemIn4)
	elif arg == 'other':
		category = 'Other'
		description = 'The Cooking Style in Other'
		items = db.exe_fetch(SQL['categoryResult'].format(c=arg),'all')
		result = len(items)
		for i in items:
			ownerName = db.exe_fetch(SQL['clientInfo_ID'].format(clientID=i['owner']))['nickname']
			i['ownerName'] = ownerName
			if Path(os.getcwd()+'/static/image/article/'+str(i['articleID'])+'.png').exists():
				i['image'] = 'image/article/'+str(i['articleID'])+'.png'
			elif Path(os.getcwd()+'/static/image/article/'+str(i['articleID'])+'.jpg').exists():
				i['image'] = 'image/article/'+str(i['articleID'])+'.jpg'
			else:
				i['image'] = 'image/article/default.png'

		itemIn4 = []
		while len(items) != 0:
			if len(items) >= 4:
				itemIn4.append([items.pop(0),items.pop(0),items.pop(0),items.pop(0)])
			else:
				itemIn4.append(items)
				items = []
				
		return render_template('Category.html',userInfo=get_user(),cart=get_cart(),category=category,description=description,result=result,items=itemIn4)
###############################################################################################


#About
###############################################################################################
@app.route('/about')
def about():
	return render_template('About.html',userInfo=get_user(),cart=get_cart())
###############################################################################################


#Searching
###############################################################################################
@app.route('/search', methods=['get'])
def search():
	q = request.args.get('q')
	items = db.exe_fetch(SQL['searching_title'].format(q=q),'all')
	result = len(items)
	for i in items:
		ownerName = db.exe_fetch(SQL['clientInfo_ID'].format(clientID=i['owner']))['nickname']
		i['ownerName'] = ownerName
		if Path(os.getcwd()+'/static/image/article/'+str(i['articleID'])+'.png').exists():
			i['image'] = 'image/article/'+str(i['articleID'])+'.png'
		elif Path(os.getcwd()+'/static/image/article/'+str(i['articleID'])+'.jpg').exists():
			i['image'] = 'image/article/'+str(i['articleID'])+'.jpg'
		else:
			i['image'] = 'image/article/default.png'

	itemIn4 = []
	while len(items) != 0:
		if len(items) >= 4:
			itemIn4.append([items.pop(0),items.pop(0),items.pop(0),items.pop(0)])
		else:
			itemIn4.append(items)
			items = []

	return render_template('Category.html',userInfo=get_user(),cart=get_cart(),category='Search',description='Key: ' + q, result=result,items=itemIn4)
###############################################################################################s

#News
###############################################################################################
@app.route('/news/<path:arg>')
def news(arg):
	if arg == 'all':
		return render_template('News.html', userInfo=get_user(),cart=get_cart())
###############################################################################################
#News end

#Admin
###############################################################################################
@app.route('/admin')
def admin():
	if session.get('admin') != None:
		admin = session['admin']
		adminInfo = db.exe_fetch(SQL['adminInfo_id'].format(id=admin))
		return render_template('adminHome.html',title='Admin', ac=adminInfo['account'])
	else:
		return redirect(url_for('login'))

@app.route('/admin_manage/<path:arg>')
def admin_manage(arg):
	if session.get('admin') != None:
		admin = session['admin']
		adminInfo = db.exe_fetch(SQL['adminInfo_id'].format(id=admin))
		if arg == 'client':
			allClient = db.exe_fetch(SQL['allClient'],'all')
			result = len(allClient)
			th = ['clientID','nickname','email','password']
			for i in allClient:
				i['url'] = url_for('admin_edit',arg='client',ID=i['clientID'])

			return render_template('adminTable.html',title='Client',tablehead=th,clientData=allClient,result=result)
		elif arg == 'article':
			allArticle = db.exe_fetch(SQL['allArticle'],'all')
			result = len(allArticle)
			th = ['articleID','category','owner','title','price','sales','date']
			for i in allArticle:
				i['url'] = url_for('admin_edit',arg='article',ID=i['articleID'])

			return render_template('adminTable.html',title='Article',tablehead=th,articleData=allArticle,result=result)
		elif arg == 'revenue': 
			allRevenue = db.exe_fetch(SQL['allRevenue'],'all')
			result = len(allRevenue)
			th = ['date','revenue(HKD)']

			return render_template('adminTable.html',title='Revenue',tablehead=th,revenueData=allRevenue,result=result)
		elif arg == 'carousel':
			result = 3
			url = {}
			url['C1'] = url_for('admin_edit',arg='carousel',ID=1)
			url['C2'] = url_for('admin_edit',arg='carousel',ID=2)
			url['C3'] = url_for('admin_edit',arg='carousel',ID=3)
			th = ['Carousel Image No.'] 

			return render_template('adminTable.html',title='Carousel',tablehead=th,Carousel=url,result=result)
		elif arg == 'comment': 
			allComment = db.exe_fetch(SQL['allComment'],'all')
			maxArticle = len(db.exe_fetch(SQL['allArticle'],'all'))
			result = len(allComment)
			th = ['commentID','article','author','date']
			for i in allComment:
				i['url'] = url_for('admin_edit',arg='comment',ID=i['commentID'])

			return render_template('adminTable.html',title='Comment',tablehead=th,commentData=allComment,result=result,max=maxArticle)
		elif arg == 'comment_search': 
			articleID = request.args.get('articleID')
			maxArticle = len(db.exe_fetch(SQL['allArticle'],'all'))
			searchComment = db.exe_fetch(SQL['getComment'].format(ID=articleID),'all')
			result = len(searchComment)
			th = ['commentID','article','author','date']
			for i in searchComment:
				i['url'] = url_for('admin_edit',arg='comment',ID=i['commentID'])

			return render_template('adminTable.html',title='Comment',tablehead=th,commentData=searchComment,result=result,max=maxArticle)
		elif arg == 'news': 
			pass
	else:
		return redirect(url_for('login'))

@app.route('/admin_edit/<path:arg>/<path:ID>')
def admin_edit(arg,ID):
	if session.get('admin') != None:
		admin = session['admin']
		adminInfo = db.exe_fetch(SQL['adminInfo_id'].format(id=admin))
		if arg == 'client':
			clientData = db.exe_fetch(SQL['clientInfo_ID'].format(clientID=ID))
			return render_template('adminForm.html',title='Client',type='client',data=clientData)
		elif arg == 'article':
			articleData = db.exe_fetch(SQL['articleInfo'].format(ID=ID))
			if Path(os.getcwd()+'/static/image/article/'+str(articleData['articleID'])+'.png').exists():
				articleData['image'] = 'image/article/'+str(articleData['articleID'])+'.png'
			elif Path(os.getcwd()+'/static/image/article/'+str(articleData['articleID'])+'.jpg').exists():
				articleData['image'] = 'image/article/'+str(articleData['articleID'])+'.jpg'
			else:
				articleData['image'] = 'image/article/default.png'
			
			return render_template('adminForm.html',title='Article',type='article',data=articleData)
		elif arg == 'carousel': 
			carouselData = {}
			carouselData['num'] = str(ID)
			if Path(os.getcwd()+'/static/image/Carousel/'+'C'+str(ID)+'.png').exists():
				carouselData['image'] = 'image/Carousel/'+'C'+str(ID)+'.png'
			elif Path(os.getcwd()+'/static/image/Carousel/'+'C'+str(ID)+'.jpg').exists():
				carouselData['image'] = 'image/Carousel/'+'C'+str(ID)+'.jpg'

			return render_template('adminForm.html',title='Carousel',type='carousel',data=carouselData)
		elif arg == 'comment': 
			commentData = db.exe_fetch(SQL['commentInfo'].format(ID=ID))
	
			return render_template('adminForm.html',title='Comment',type='comment',data=commentData)

		elif arg == 'news': 
			pass
	else:
		return redirect(url_for('login'))

@app.route('/edit_client', methods=['post'])
def edit_client():
	if session.get('admin') != None:
		admin = session['admin']
		adminInfo = db.exe_fetch(SQL['adminInfo_id'].format(id=admin))
		if 'W' in adminInfo['client']:
			clientID = request.form['clientID']
			nickname = request.form['name']
			email = request.form['email']
			password = request.form['password']

			db.exe_commit(SQL['updateClient'].format(e=email,n=nickname,p=password,ID=clientID))

			return redirect(url_for('admin_manage',arg='client'))
		else:
			message = 'You are not allow to edit.'
			return render_template('back.html',title=Error,message=message)

@app.route('/edit_article', methods=['post'])
def edit_article():
	if session.get('admin') != None:
		admin = session['admin']
		adminInfo = db.exe_fetch(SQL['adminInfo_id'].format(id=admin))
		if 'W' in adminInfo['article']:
			articleID = request.form['articleID']
			category = request.form['category']
			title = request.form['title']
			price = request.form['price']
			description = request.form['description']
			content = request.form['content'].replace('\'','\\\'').replace('\"','\\\"')
			file = request.files['img']

			if file and allowed_file(file.filename):
				filename = str(articleID) + '.' + secure_filename(file.filename).split('.')[-1]
				file.save(os.path.join(app.config['UPLOAD_ARTICLE_FOLDER'], filename))
			else:
				message = 'Invaild format of Image'
				return render_template('back.html',title='Error',message=message)
			
			db.exe_commit(SQL['updateArticle'].format(cate=category,t=title,p=price,d=description,cont=content,ID=articleID))

			return redirect(url_for('admin_manage',arg='article'))
		else:
			message = 'You are not allow to edit.'
			return render_template('back.html',title=Error,message=message)


@app.route('/edit_comment',methods=['post'])
def edit_comment():
	if session.get('admin') != None:
		admin = session['admin']
		adminInfo = db.exe_fetch(SQL['adminInfo_id'].format(id=admin))
		if 'W' in adminInfo['article']:
			commentID = request.form['commentID']
			comment = request.form['comment'].replace('\'','\\\'').replace('\"','\\\"')
			print(SQL['updateComment'].format(c=comment,ID=commentID))
			db.exe_commit(SQL['updateComment'].format(c=comment,ID=commentID))

			return redirect(url_for('admin_manage',arg='comment'))
		else:
			message = 'You are not allow to edit.'
			return render_template('back.html',title=Error,message=message)


@app.route('/edit_carousel',methods=['post'])
def edit_carousel():
	if session.get('admin') != None:
		admin = session['admin']
		adminInfo = db.exe_fetch(SQL['adminInfo_id'].format(id=admin))
		if 'W' in adminInfo['carousel']:
			num = request.form['num']
			file = request.files['img']

			if file and allowed_file(file.filename):
				filename = 'C' + str(num) + '.' + secure_filename(file.filename).split('.')[-1]
				file.save(os.path.join(app.config['UPLOAD_CAROUSEL_FOLDER'], filename))
				return render_template('admin_manage',arg='carousel')
			else:
				message = 'Invaild format of Image'
				return render_template('back.html',title='Error',message=message)
		else:
			message = 'You are not allow to edit.'
			return render_template('back.html',title='Error',message=message)

@app.route('/admin_out')
def admin_out():
	if session.get('admin') != None:
		session.pop('admin')
		return redirect(url_for('home'))
	else:
		return redirect(url_for('login'))
###############################################################################################

if __name__ == "__main__":
	app.run(debug = True)

