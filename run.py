#Author : Yau Siu Fung Brian

#setting
###############################################################################################
from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_mail import Mail, Message
from database import connection, SQL
from pathlib import Path
from werkzeug.utils import secure_filename
import os, datetime
###############################################################################################
#File upload setting
UPLOAD_ICON_FOLDER = os.getcwd()  + '/static/image/icon'
UPLOAD_ARTICLE_FOLDER = os.getcwd()  + '/static/image/article'
UPLOAD_CAROUSEL_FOLDER = os.getcwd()  + '/static/image/Carousel'
ALLOWED_EXTENSIONS = set(['png', 'jpg'])

app = Flask(__name__)

#Session Setting
app.config['SECRET_KEY'] = os.urandom(24)
app.config['UPLOAD_ICON_FOLDER'] = UPLOAD_ICON_FOLDER
app.config['UPLOAD_ARTICLE_FOLDER'] = UPLOAD_ARTICLE_FOLDER
app.config['UPLOAD_CAROUSEL_FOLDER'] = UPLOAD_CAROUSEL_FOLDER

#Flask-Mail Setting
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'cookingdom2019@gmail.com'
app.config['MAIL_PASSWORD'] = 'AaA123123'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

db = connection()
###############################################################################################

#function
###############################################################################################
def allowed_file(filename): # To determain the image format
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

def get_cart(): #get user cart by session
	user = session.get('clientID')
	if user != None:
		items = db.exe_fetch(SQL["cart_owner"].format(ID=user), 'all')
		total = 0
		for i in items:
			ownerName = db.exe_fetch(SQL['clientInfo_ID'].format(clientID=i['owner']))['nickname']
			i['author'] = ownerName
			if Path(os.getcwd()+'/static/image/article/'+str(i['articleID'])+'.png').exists():
				i['image'] = 'image/article/'+str(i['articleID'])+'.png'
			elif Path(os.getcwd()+'/static/image/article/'+str(i['articleID'])+'.jpg').exists():
				i['image'] = 'image/article/'+str(i['articleID'])+'.jpg'
			else:
				i['image'] = 'image/article/default.png'
			total += i['price']

		if items == ():
			items = 'Nothing'
		return [items,total]
	else:
		return 'Guest'
###############################################################################################

#Home
###############################################################################################
@app.route('/index') # The Home page with the 8 hottest item
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
@app.route('/login') #Login page and redirect to home if logged in
def login():
	if session.get('clientID') != None:
		return redirect(url_for('home'))	
	else:
		return render_template('Login.html')

@app.route('/login_done', methods = ["post"]) #Login process
def login_done():
	email = request.form["email"]
	password = request.form["password"]
	checkAdmin = db.exe_fetch(SQL['adminInfo_ac'].format(ac=email))
	checkEmail = db.exe_fetch(SQL['clientInfo_email'].format(email=email))

	if checkAdmin == None: #Check admin
		pass
	elif checkAdmin.get('password') != password:
		pass
	else:
		session['admin'] = checkAdmin['adminID']
		return redirect(url_for('admin'))

	if (checkEmail == None): #Check client
		flash("Invaild")
		return redirect(url_for('login'))
	elif  (checkEmail.get('state') != 'able'):
		message = 'Blocked Account'
		return render_template('back.html',title='Error',message=message)
	elif  (checkEmail.get('password') != password):
		flash("Invaild")
		return redirect(url_for('login'))
	else:
		session['clientID'] = checkEmail['clientID']
		return redirect(url_for('home'))


@app.route('/forgetpassword', methods=['post']) #flask-mail send email if the client exist in database
def forgetpassword():
	email = request.form['forget_email']
	checkEmail = db.exe_fetch(SQL['clientInfo_email'].format(email=email))
	if (checkEmail == None):
		message = 'Email Not Find'
		return render_template('back.html',title='Error',message=message)
	else:
		msg = Message('CooKinGdom - Forget Password',sender = 'cookingdom@gmail.com',recipients=[email])
		msg.body = "Here is your password: " + checkEmail.get('password')
		mail.send(msg)

		message = 'Success! Check You email.'
		return render_template('back.html',title='Success',message=message)


@app.route('/logout') #Logout
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
@app.route('/signup') #Signup page and redirect to home if logged in
def signup():
	if session.get('clientID') != None:
		return redirect(url_for('home'))	
	else:
		return render_template('SignUp.html')


@app.route('/signup_done', methods = ["post"]) #Signup process
def signup_done():
	if session.get('clientID') != None:
		return redirect(url_for('home'))
	else:
		email = request.form["email"]
		name = request.form["name"]
		password = request.form["password"]
		cpassword = request.form["cpassword"]

		checkEmail = db.exe_fetch(SQL['clientInfo_email'].format(email=email))

		if password != cpassword: #check if two password are the same
			flash('Invaild','error')
			return redirect(url_for('signup'))
		else:
			if checkEmail == None: #Check the email is used or not
				db.exe_commit(SQL['signup'].format(e=email,n=name,p=password))
				userInfo = db.exe_fetch(SQL['clientInfo_email'].format(email=email))

				return render_template('SignUp_Done.html',userIcon='image/icon/default.png',userID=userInfo['clientID'],userName=userInfo['nickname'],userEmail=userInfo['email'],userPassword=userInfo['password'])
			else:
				flash('Used email','email')
				return redirect(url_for('signup'))
###############################################################################################
#signup end

#user pages
###############################################################################################
@app.route('/record') #Record page which will show client buying record
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


@app.route('/myarticle') #MyArticle Page which will show acticle that compose by client
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
		
		return render_template('list_article.html',pageTitle='My Article',cart=get_cart(),userInfo=get_user(),articles=articles,My='Yes')
	else:
		return redirect(url_for('login'))
###############################################################################################
#user pages end

#edition
###############################################################################################
@app.route('/edit') #Edit page for client to compose their article and redirect to login page if guest
def edit():
	if session.get('clientID') != None:
		return render_template('Edition.html',userInfo=get_user(),cart=get_cart())	
	else:
		return redirect(url_for('login'))	


@app.route("/edit_done", methods=['post']) #Edit page process
def edit_done():
	if session.get('clientID') != None:
		clientID = session.get('clientID')
		title = request.form['title'].replace('\'','\\\'').replace('\"','\\\"')
		price = request.form['price']
		description = request.form['description'].replace('\'','\\\'').replace('\"','\\\"')
		content = request.form['content'].replace('\'','\\\'').replace('\"','\\\"')
		category = request.form['category'].lower()
		date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

		db.exe_commit(SQL['newArticle'].format(t=title,p=price,des=description,c=content,date=date,o=clientID,category=category))
		articleID = db.cursor.lastrowid

		file = request.files['img']
		if file and allowed_file(file.filename): #Upload Image
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

@app.route("/edit_own_article/<path:aID>", methods=['post']) #Page for Edit existing article which only can edit bt article owner
def edit_own_article(aID):
	if session.get('clientID') != None:
		user = session['clientID']
		a = db.exe_fetch(SQL['articleInfo'].format(ID=aID))
		author = db.exe_fetch(SQL['clientInfo_ID'].format(clientID=a['owner']))['clientID']
		if a['state'] == 'disable': #only can edit if article status is able 
			message = 'Blocked Article'
			return render_template('back.html',title='Error',message=message)
		if user == author:
			return render_template('userEdit.html',userInfo=get_user(),cart=get_cart(),data=a,articleID=aID)
		else: 
			message = 'You don\'t have permission'
			return render_template('back.html',title='Error',message=message)
	else:
		return redirect(url_for('login'))

@app.route("/own_edit_done", methods=['post']) #Process of Edit existing article
def own_edit_done():
	if session.get('clientID') != None:
		user = session['clientID']
		articleID = request.form['articleID']
		a = db.exe_fetch(SQL['articleInfo'].format(ID=articleID))
		author = db.exe_fetch(SQL['clientInfo_ID'].format(clientID=a['owner']))['clientID']
		if user == author:
			file = request.files['img']		
			title = request.form['title'].replace('\'','\\\'').replace('\"','\\\"')
			price = request.form['price']
			description = request.form['description'].replace('\'','\\\'').replace('\"','\\\"')
			content = request.form['content'].replace('\'','\\\'').replace('\"','\\\"')
			category = request.form['category'].lower()

			db.exe_commit(SQL['updateArticle_owner'].format(cate=category,t=title,p=price,d=description,cont=content,ID=articleID))

			if file and allowed_file(file.filename):
				filename = str(articleID) + '.' + secure_filename(file.filename).split('.')[-1]
				if Path(os.getcwd()+'/static/image/article/'+str(articleID)+'.png').exists():
					os.remove(os.getcwd()+'/static/image/article/'+str(articleID)+'.png')
				elif Path(os.getcwd()+'/static/image/article/'+str(articleID)+'.jpg').exists():
					os.remove(os.getcwd()+'/static/image/article/'+str(articleID)+'.jpg')

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
@app.route('/article_description/<path:aID>/') #Page for show article description to client and guest
def article_description(aID):
	a = db.exe_fetch(SQL['articleInfo'].format(ID=aID))
	if a.get('state') == 'able':
		ownerName = db.exe_fetch(SQL['clientInfo_ID'].format(clientID=a['owner']))['nickname']
		comment = db.exe_fetch(SQL['getComment_able'].format(ID=aID),'all')
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

		return render_template('Article_Description.html', userInfo=get_user(),cart=get_cart(),title=a['title'], price=a['price'], description=a['description'].replace('\n','<br>'), date=a['date'], name=ownerName, articleID=a['articleID'],comment=comment,id=a['owner'])
	else:
		message = 'Blocked Article'
		return render_template('back.html',title='Erroe',message=message)

@app.route('/comment', methods=['post']) #Process for client compose comment
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

@app.route('/disable_own_comment', methods=['post']) #Process for client disable own comment
def disable_own_comment():
	if session.get('clientID') != None:
		user = session['clientID']
		commentID = request.form['commentID']
		author = db.exe_fetch(SQL['commentInfo'].format(ID=commentID))['author']
		if user == author:
			db.exe_commit(SQL['disable_own_comment'].format(ID=commentID))
			message = 'Delete Success!'
			return render_template('back.html', title='Success', message=message)
		else:
			message = 'Error'
			return render_template('back.html', title='Error', message=message)

	else:
		return redirect(url_for('login'))

@app.route('/article/<path:aID>/') #Page for show article content to client who brought the it
def article(aID):
	if session.get('clientID') != None:
		user = session['clientID']
		bought = db.exe_fetch(SQL['checkRecord'].format(clientID=user,articleID=aID))
		a = db.exe_fetch(SQL['articleInfo'].format(ID=aID))
		author = a['owner']
		if a.get('state') == 'disable':
			message = 'Blocked Article'
			return render_template('back.html',title='Erroe',message=message)

		if bought != None or user == author:
			ownerName = db.exe_fetch(SQL['clientInfo_ID'].format(clientID=a['owner']))['nickname']
			return render_template('Article.html', userInfo=get_user(),cart=get_cart(),title=a['title'], content=a['content'].replace('\n','<br>'), date=a['date'], name=ownerName,articleID=aID,owner=(user==author),id=author)
		else: 
			flash('buy', 'buy')
			return redirect(url_for('home'))
	else:
		return redirect(url_for('login'))

@app.route('/disable_own_article', methods=['post']) #Process for client disable own article
def disable_own_article():
	if session.get('clientID') != None:
		user = session['clientID']
		articleID = request.form['articleID']
		author = db.exe_fetch(SQL['articleInfo'].format(ID=articleID))['owner']
		if user == author:
			db.exe_commit(SQL['disable_own_article'].format(ID=articleID))
			db.exe_commit(SQL['clearAllCart'].format(ID=articleID))
			return render_template('back.html', title='Success')
		else:
			message = 'Error'
			return render_template('back.html', title='Error', message=message)

	else:
		return redirect(url_for('login'))

###############################################################################################
#article end 		

#Profile function
###############################################################################################
@app.route('/uploadicon', methods=['post']) #Process for client change and upload icon
def uploadicon():
	if session.get('clientID') != None:
		user = str(session['clientID'])
		file = request.files['icon']
		if file and allowed_file(file.filename):
			filename = user + '.' + secure_filename(file.filename).split('.')[-1]
			if Path(os.getcwd()+'/static/image/icon/'+str(user)+'.png').exists():
				os.remove(os.getcwd()+'/static/image/icon/'+str(user)+'.png')
			elif Path(os.getcwd()+'/static/image/icon/'+str(user)+'.jpg').exists():
				os.remove(os.getcwd()+'/static/image/icon/'+str(user)+'.jpg')
			file.save(os.path.join(app.config['UPLOAD_ICON_FOLDER'], filename))
			flash("icon", "iconSuccess")

		else:
			flash("icon","iconError")

		return redirect(url_for('home'))
	else:
		return redirect(url_for('login'))

@app.route('/changePassword', methods=['post']) #Process for client change password
def changePassword():
	if session.get('clientID') != None:
		user = session['clientID']
		new = str(request.form['npassword'])
		db.exe_commit(SQL['changePassword'].format(p=new,id=user))
		flash('passwordSuccess', 'passwordSuccess')
		return redirect(url_for('home'))
	else:
		return redirect(url_for('login'))

@app.route('/addtocart', methods=['post']) #Process for client add article product to their cart
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


@app.route('/buyone', methods=['post']) #Process for client buy the article directly and see content in persent
def buyone():
	if session.get('clientID') != None:
		user = session['clientID']
		article = request.form['articleID']
		articleOwner =  db.exe_fetch(SQL['articleInfo'].format(ID=article))['owner']
		inRecord = db.exe_fetch(SQL['checkRecord'].format(articleID=article, clientID=user))
		date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		today = datetime.datetime.today().strftime("%Y-%m-%d")
		processingFee = 0.3

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

			price = db.exe_fetch(SQL['articleInfo'].format(ID=article))['price']
			todayRevenue = db.exe_fetch(SQL['revenueInfo'].format(date=today))
			if todayRevenue == None:
				db.exe_commit(SQL['newRevenue'].format(d=today,r=(round(price*processingFee))))
			else:
				total = todayRevenue['revenue']
				total += round(price*processingFee)
				db.exe_commit(SQL['updateRevenue'].format(r=total,date=today))

			flash('Thank you for your patronage!','thank')
			return redirect(url_for('article', aID=article))
	else:
		return redirect(url_for('login'))

@app.route('/cart_del', methods=['post']) #Process for client del article product from their cart
def cart_del():
	if session.get('clientID') != None:
		user = session['clientID']
		article = request.form['article']
			
		db.exe_commit(SQL['cart_del'].format(articleID=article,clientID=user))
		flash('opencart','opencart')
		return render_template('back.html',message='Cancel Success',title='Success')

	else:
		return redirect(url_for('login'))

@app.route('/purchase', methods=['post']) #Process for client biy all the article in their cart
def purchase():
	if session.get('clientID') != None:
		user = session['clientID']
		cartInfo = db.exe_fetch(SQL['cartInfo'].format(clientID=user),'all')
		date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		today = datetime.datetime.today().strftime("%Y-%m-%d")
		processingFee = 0.3

		for i in cartInfo:
			db.exe_commit(SQL['buyone'].format(articleID=i['article'],clientID=user,date=date))

			sales = db.exe_fetch(SQL['articleInfo'].format(ID=i['article']))['sales']
			sales += 1
			db.exe_commit(SQL['updateSales'].format(s=sales,ID=i['article']))

			price = db.exe_fetch(SQL['articleInfo'].format(ID=i['article']))['price']
			todayRevenue = db.exe_fetch(SQL['revenueInfo'].format(date=today))
			if todayRevenue == None:
				db.exe_commit(SQL['newRevenue'].format(d=today,r=(round(price*processingFee))))
			else:
				total = todayRevenue['revenue']
				total += round(price*processingFee)
				db.exe_commit(SQL['updateRevenue'].format(r=total,date=today))

		db.exe_commit(SQL['cart_delAll'].format(clientID=user))

		message = 'Purchase Success!'
		return render_template('back.html', title='Success', message=message)
	else:
		return redirect(url_for('login'))
###############################################################################################
#Profile function end

#Category page
###############################################################################################
@app.route('/category/<path:arg>') #Category page which show acticle of that category
def category(arg):
	if arg == 'chinese': #Category Chinese
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

	elif arg == 'europe': #Category Europe
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

	elif arg == 'japanese': #Category Japanese
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

	elif arg == 'other': #Category Other
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
#Category end

#About
###############################################################################################
@app.route('/about') #About page
def about():
	return render_template('About.html',userInfo=get_user(),cart=get_cart())
###############################################################################################
#About end


#Searching
###############################################################################################
@app.route('/search/<path:sort>/', methods=['get']) #Page and process for searching and sorting
def search(sort):
	q = request.args.get('q')
	if sort == 'newest':
		items = db.exe_fetch(SQL['searching_title'].format(q=q),'all')
	elif sort == 'priceL2H':
		items = db.exe_fetch(SQL['searching_title_byPriceL2H'].format(q=q),'all')
	elif sort == 'priceH2L':
		items = db.exe_fetch(SQL['searching_title_byPriceH2L'].format(q=q),'all')
	elif sort == 'sales':
		items = db.exe_fetch(SQL['searching_title_bySales'].format(q=q),'all')

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

	return render_template('Category.html',userInfo=get_user(),cart=get_cart(),category='Search',description='Key: ' + q, result=result,items=itemIn4,q=q)
###############################################################################################s
#Searching end

#News
###############################################################################################
@app.route('/news/<path:arg>') #News Page which show news compose by admin
def news(arg):
	if arg == 'all':
		items = db.exe_fetch(SQL['allNews_desc'],'all')

	if arg == 'event':
		items = db.exe_fetch(SQL['allNews_desc_event'],'all')

	if arg == 'system':
		items = db.exe_fetch(SQL['allNews_desc_system'],'all')

	for i in items:
		i['content'] = i['content'].replace('\n','<br>')
	
	itemIn3 = []
	while len(items) != 0:
		if len(items) >= 3:
			itemIn3.append([items.pop(0),items.pop(0),items.pop(0)])
		else:
			itemIn3.append(items)
			items = []

	return render_template('News.html', userInfo=get_user(),cart=get_cart(),news=itemIn3)

@app.route('/news_content/<path:nID>') #News content page
def news_content(nID):
	news = db.exe_fetch(SQL['newsInfo'].format(ID=nID))
	if news['state'] == 'disable':
		message = 'Blocked News'
		return render_template('back.html',title='Error',message=message)

	news['content'] = news['content'].replace('\n','<br>')
	return render_template('News_content.html',userInfo=get_user(),cart=get_cart(),news=news)

@app.route('/composeNews') #Page for admin compose News
def composeNews():
	if session.get('admin') != None:
		admin = session['admin']
		adminInfo = db.exe_fetch(SQL['adminInfo_id'].format(id=admin))
		if 'W' in adminInfo['article']:
			return render_template('adminForm.html',title='Compose News',type='composeNews',adminData=adminInfo)
		else:
			message = 'You are not allow to edit.'
			return render_template('back.html',title='Error',message=message)


@app.route('/compoeseNews_done', methods=['post']) #Process for admin compose News
def composeNews_done():
	if session.get('admin') != None:
		admin = session['admin']
		adminInfo = db.exe_fetch(SQL['adminInfo_id'].format(id=admin))
		if 'W' in adminInfo['news']:
			newsType = request.form['type']
			title = request.form['title'].replace('\'','\\\'').replace('\"','\\\"')
			content = request.form['content'].replace('\'','\\\'').replace('\"','\\\"')
			date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

			db.exe_commit(SQL['newNews'].format(t=title,c=content,d=date,a=admin,type=newsType))

			return redirect(url_for('admin_manage',arg='news'))
		else:
			message = 'You are not allow to edit.'
			return render_template('back.html',title='Error',message=message)

###############################################################################################
#News end

#Admin
###############################################################################################
@app.route('/admin') #Admin home page
def admin():
	if session.get('admin') != None:
		admin = session['admin']
		adminInfo = db.exe_fetch(SQL['adminInfo_id'].format(id=admin))
		return render_template('adminHome.html',title='Admin',adminData=adminInfo)
	else:
		return redirect(url_for('login'))

@app.route('/admin_manage/<path:arg>') #Page for showing data to admin
def admin_manage(arg):
	if session.get('admin') != None:
		admin = session['admin']
		adminInfo = db.exe_fetch(SQL['adminInfo_id'].format(id=admin))

		if arg == 'client': #Show client data
			if 'R' in adminInfo['client']:
				allClient = db.exe_fetch(SQL['allClient'],'all')
				result = len(allClient)
				th = ['clientID','nickname','email','password','state']
				for i in allClient:
					i['url'] = url_for('admin_edit',arg='client',ID=i['clientID'])

				return render_template('adminTable.html',title='Client',tablehead=th,clientData=allClient,result=result,adminData=adminInfo)
			else:
				message = 'You are not allow to read.'
				return render_template('back.html',title='Error',message=message)

		elif arg == 'article': #Show acticle data
			if 'R' in adminInfo['article']:
				allArticle = db.exe_fetch(SQL['allArticle'],'all')
				result = len(allArticle)
				th = ['articleID','category','owner','title','price','sales','date','state']
				for i in allArticle:
					i['url'] = url_for('admin_edit',arg='article',ID=i['articleID'])

				return render_template('adminTable.html',title='Article',tablehead=th,articleData=allArticle,result=result,adminData=adminInfo)
			else:
				message = 'You are not allow to read.'
				return render_template('back.html',title='Error',message=message)

		elif arg == 'revenue': #Show revenue data
			if 'R' in adminInfo['revenue']: 
				allRevenue = db.exe_fetch(SQL['allRevenue'],'all')
				result = len(allRevenue)
				th = ['date','revenue(HKD)']

				return render_template('adminTable.html',title='Revenue',tablehead=th,revenueData=allRevenue,result=result,adminData=adminInfo)
			else:
				message = 'You are not allow to read.'
				return render_template('back.html',title='Error',message=message)

		elif arg == 'carousel': #Show carousel data
			if 'R' in adminInfo['carousel']: 
				result = 3
				url = {}
				url['C1'] = url_for('admin_edit',arg='carousel',ID=1)
				url['C2'] = url_for('admin_edit',arg='carousel',ID=2)
				url['C3'] = url_for('admin_edit',arg='carousel',ID=3)
				th = ['Carousel Image No.'] 

				return render_template('adminTable.html',title='Carousel',tablehead=th,Carousel=url,result=result,adminData=adminInfo)
			else:
				message = 'You are not allow to read.'
				return render_template('back.html',title='Error',message=message)

		elif arg == 'comment': #Show comment data
			if 'R' in adminInfo['comment']:  
				allComment = db.exe_fetch(SQL['allComment'],'all')
				maxArticle = len(db.exe_fetch(SQL['allArticle'],'all'))
				result = len(allComment)
				th = ['commentID','article','author','date','state']
				for i in allComment:
					i['url'] = url_for('admin_edit',arg='comment',ID=i['commentID'])

				return render_template('adminTable.html',title='Comment',tablehead=th,commentData=allComment,result=result,max=maxArticle,adminData=adminInfo)
			else:
				message = 'You are not allow to read.'
				return render_template('back.html',title='Error',message=message)

		elif arg == 'comment_search': #Show comment data with searching
			if 'R' in adminInfo['comment']: 
				articleID = request.args.get('articleID')
				maxArticle = len(db.exe_fetch(SQL['allArticle'],'all'))
				searchComment = db.exe_fetch(SQL['getComment'].format(ID=articleID),'all')
				result = len(searchComment)
				th = ['commentID','article','author','date','state']
				for i in searchComment:
					i['url'] = url_for('admin_edit',arg='comment',ID=i['commentID'])

				return render_template('adminTable.html',title='Comment',tablehead=th,commentData=searchComment,result=result,max=maxArticle,adminData=adminInfo)
			else:
				message = 'You are not allow to read.'
				return render_template('back.html',title='Error',message=message)

		elif arg == 'news': #Show News data
			if 'R' in adminInfo['news']: 
				allNews = db.exe_fetch(SQL['allNews'],'all')
				result = len(allNews)
				th = ['newsID', 'type','title','author','date','state']
				for i in allNews:
					i['url'] = url_for('admin_edit',arg='news',ID=i['newsID'])

				return render_template('adminTable.html',title='News',tablehead=th,newsData=allNews,result=result,compose='Yes',adminData=adminInfo)
			else:
				message = 'You are not allow to read.'
				return render_template('back.html',title='Error',message=message)

		elif arg == 'record': #Show record data
			if 'R' in adminInfo['record']: 
				allRecord = db.exe_fetch(SQL['allRecord'],'all')
				result = len(allRecord)
				th = ['recordID','article','owner','date']
				for i in allRecord:
					i['url'] = url_for('admin_edit',arg='record',ID=i['recordID'])

				return render_template('adminTable.html',title='Record',tablehead=th,recordData=allRecord,result=result,adminData=adminInfo)
			else:
				message = 'You are not allow to read.'
				return render_template('back.html',title='Error',message=message)

		elif arg == 'admin': #Show admin data
			if 'Super' in adminInfo['admin']: 
				allAdmin = db.exe_fetch(SQL['allAdmin'],'all')
				result = len(allAdmin)
				th = ['adminID', 'account','password','client','article','comment','carousel','news','revenue','admin']
				for i in allAdmin:
					i['url'] = url_for('admin_edit',arg='admin',ID=i['adminID'])

				return render_template('adminTable.html',title='Admin',tablehead=th,allAdminData=allAdmin,result=result,adminData=adminInfo)
			else:
				message = 'You are not allow to read.'
				return render_template('back.html',title='Error',message=message)

	else:
		return redirect(url_for('login'))

@app.route('/admin_edit/<path:arg>/<path:ID>') #Page for admin ti edit different data in datbase
def admin_edit(arg,ID):
	if session.get('admin') != None:
		admin = session['admin']
		adminInfo = db.exe_fetch(SQL['adminInfo_id'].format(id=admin))

		if arg == 'client': #Show detail client data in a form
			if 'R' in adminInfo['client']: 
				clientData = db.exe_fetch(SQL['clientInfo_ID'].format(clientID=ID))
				return render_template('adminForm.html',title='Client',type='client',data=clientData,adminData=adminInfo)
			else:
				message = 'You are not allow to read.'
				return render_template('back.html',title='Error',message=message)

		elif arg == 'article': #Show detail article data in a form
			if 'R' in adminInfo['article']: 
				articleData = db.exe_fetch(SQL['articleInfo'].format(ID=ID))

				if Path(os.getcwd()+'/static/image/article/'+str(articleData['articleID'])+'.png').exists():
					articleData['image'] = 'image/article/'+str(articleData['articleID'])+'.png'
				elif Path(os.getcwd()+'/static/image/article/'+str(articleData['articleID'])+'.jpg').exists():
					articleData['image'] = 'image/article/'+str(articleData['articleID'])+'.jpg'
				else:
					articleData['image'] = 'image/article/default.png'
				
				return render_template('adminForm.html',title='Article',type='article',data=articleData,adminData=adminInfo)
			else:
				message = 'You are not allow to read.'
				return render_template('back.html',title='Error',message=message)

		elif arg == 'carousel': #Show detail carousel data in a form
			if 'R' in adminInfo['carousel']:
				carouselData = {}
				carouselData['num'] = str(ID)

				if Path(os.getcwd()+'/static/image/Carousel/'+'C'+str(ID)+'.png').exists():
					carouselData['image'] = 'image/Carousel/'+'C'+str(ID)+'.png'
				elif Path(os.getcwd()+'/static/image/Carousel/'+'C'+str(ID)+'.jpg').exists():
					carouselData['image'] = 'image/Carousel/'+'C'+str(ID)+'.jpg'

				return render_template('adminForm.html',title='Carousel',type='carousel',data=carouselData,adminData=adminInfo)
			else:
				message = 'You are not allow to read.'
				return render_template('back.html',title='Error',message=message)

		elif arg == 'comment': #Show detail comment data in a form
			if 'R' in adminInfo['comment']: 
				commentData = db.exe_fetch(SQL['commentInfo'].format(ID=ID))
		
				return render_template('adminForm.html',title='Comment',type='comment',data=commentData,adminData=adminInfo)
			else:
				message = 'You are not allow to read.'
				return render_template('back.html',title='Error',message=message)				

		elif arg == 'news': #Show detail news data in a form
			if 'R' in adminInfo['comment']: 
				newsData = db.exe_fetch(SQL['newsInfo'].format(ID=ID))
		
				return render_template('adminForm.html',title='News',type='news',data=newsData,adminData=adminInfo)
			else:
				message = 'You are not allow to read.'
				return render_template('back.html',title='Error',message=message)

		elif arg == 'record': #Show detail record data in a form
			if 'R' in adminInfo['comment']: 
				recordData = db.exe_fetch(SQL['recordInfo'].format(ID=ID))
		
				return render_template('adminForm.html',title='record',type='record',data=recordData,adminData=adminInfo)
			else:
				message = 'You are not allow to read.'
				return render_template('back.html',title='Error',message=message)

		elif arg == 'admin': #Show detail admin data in a form
			if 'Super' in adminInfo['admin']: 
				oneAdminData = db.exe_fetch(SQL['adminInfo_id'].format(id=ID))
		
				return render_template('adminForm.html',title='Admin',type='admin',data=oneAdminData,adminData=adminInfo)
			else:
				message = 'You are not allow to read.'
				return render_template('back.html',title='Error',message=message)

	else:
		return redirect(url_for('login'))

@app.route('/edit_client', methods=['post']) #Process for admin edit client data
def edit_client():
	if session.get('admin') != None:
		admin = session['admin']
		adminInfo = db.exe_fetch(SQL['adminInfo_id'].format(id=admin))
		if 'W' in adminInfo['client']:
			clientID = request.form['clientID']
			nickname = request.form['name']
			email = request.form['email']
			password = request.form['password']
			state = request.form['state']

			db.exe_commit(SQL['updateClient'].format(e=email,n=nickname,p=password,s=state,ID=clientID))

			return redirect(url_for('admin_manage',arg='client'))
		else:
			message = 'You are not allow to edit.'
			return render_template('back.html',title='Error',message=message)

@app.route('/edit_article', methods=['post']) #Process for admin edit article data
def edit_article():
	if session.get('admin') != None:
		admin = session['admin']
		adminInfo = db.exe_fetch(SQL['adminInfo_id'].format(id=admin))
		if 'W' in adminInfo['article']:
			articleID = request.form['articleID']
			category = request.form['category']
			title = request.form['title'].replace('\'','\\\'').replace('\"','\\\"')
			price = request.form['price']
			description = request.form['description'].replace('\'','\\\'').replace('\"','\\\"')
			content = request.form['content'].replace('\'','\\\'').replace('\"','\\\"')
			state = request.form['state']
			file = request.files['img']

			if file and allowed_file(file.filename):
				filename = str(articleID) + '.' + secure_filename(file.filename).split('.')[-1]

				if Path(os.getcwd()+'/static/image/article/'+str(articleID)+'.png').exists():
					os.remove(os.getcwd()+'/static/image/article/'+str(articleID)+'.png')
				elif Path(os.getcwd()+'/static/image/article/'+str(articleID)+'.jpg').exists():
					os.remove(os.getcwd()+'/static/image/article/'+str(articleID)+'.jpg')

				file.save(os.path.join(app.config['UPLOAD_ARTICLE_FOLDER'], filename))
			elif file.filename == '':
				pass
			else:
				message = 'Invaild format of Image'
				return render_template('back.html',title='Error',message=message)
			
			db.exe_commit(SQL['updateArticle'].format(cate=category,t=title,p=price,d=description,cont=content,s=state,ID=articleID))
			if state == 'disable':
				db.exe_commit(SQL['clearAllCart'].format(ID=articleID))

			return redirect(url_for('admin_manage',arg='article'))
		else:
			message = 'You are not allow to edit.'
			return render_template('back.html',title='Error',message=message)


@app.route('/edit_comment',methods=['post']) #Process for admin edit comment data
def edit_comment():
	if session.get('admin') != None:
		admin = session['admin']
		adminInfo = db.exe_fetch(SQL['adminInfo_id'].format(id=admin))
		if 'W' in adminInfo['article']:
			commentID = request.form['commentID']
			comment = request.form['comment'].replace('\'','\\\'').replace('\"','\\\"')
			state = request.form['state']

			db.exe_commit(SQL['updateComment'].format(c=comment,s=state,ID=commentID))

			return redirect(url_for('admin_manage',arg='comment'))
		else:
			message = 'You are not allow to edit.'
			return render_template('back.html',title='Error',message=message)


@app.route('/edit_news',methods=['post']) #Process for admin edit news data
def edit_news():
	if session.get('admin') != None:
		admin = session['admin']
		adminInfo = db.exe_fetch(SQL['adminInfo_id'].format(id=admin))
		if 'W' in adminInfo['news']:
			newsID = request.form['newsID']
			newsType = request.form['type']
			title = request.form['title'].replace('\'','\\\'').replace('\"','\\\"')
			content = request.form['content'].replace('\'','\\\'').replace('\"','\\\"')
			state = request.form['state']

			db.exe_commit(SQL['updateNews'].format(t=title,c=content,type=newsType,s=state,ID=newsID))

			return redirect(url_for('admin_manage',arg='news'))
		else:
			message = 'You are not allow to edit.'
			return render_template('back.html',title='Error',message=message)


@app.route('/edit_carousel',methods=['post']) #Process for admin edit carousel data
def edit_carousel():
	if session.get('admin') != None:
		admin = session['admin']
		adminInfo = db.exe_fetch(SQL['adminInfo_id'].format(id=admin))
		if 'W' in adminInfo['carousel']:
			num = request.form['num']
			file = request.files['img']

			if file and allowed_file(file.filename):
				filename = 'C' + str(num) + '.' + secure_filename(file.filename).split('.')[-1]

				if Path(os.getcwd()+'/static/image/Carousel/'+ 'C' + str(num)+'.png').exists():
					os.remove(os.getcwd()+'/static/image/Carousel/'+ 'C' + str(num)+'.png')
				elif Path(os.getcwd()+'/static/image/Carousel/'+ 'C' + str(num)+'.jpg').exists():
					os.remove(os.getcwd()+'/static/image/Carousel/'+ 'C' + str(num)+'.jpg')
				file.save(os.path.join(app.config['UPLOAD_CAROUSEL_FOLDER'], filename))

				return redirect(url_for('admin_manage',arg='carousel'))
			elif file.filename == '':
				message = 'Image Not Found'
				return render_template('back.html',title='Error',message=message)
			else:
				message = 'Invaild format of Image'
				return render_template('back.html',title='Error',message=message)
		else:
			message = 'You are not allow to edit.'
			return render_template('back.html',title='Error',message=message)

@app.route('/newAdmin') #Page for super admin to create new admin account
def newAdmin():
	if session.get('admin') != None:
		admin = session['admin']
		adminInfo = db.exe_fetch(SQL['adminInfo_id'].format(id=admin))
		if 'Super' in adminInfo['admin']:
			return render_template('adminForm.html',title='New Admin',type='newAdmin',adminData=adminInfo)
		else:
			message = 'You are not allow to edit.'
			return render_template('back.html',title='Error',message=message)
	else:
		return redirect(url_for('login'))

@app.route('/edit_admin', methods=['post']) #Process for super admin edit admin data
def edit_admin():
	if session.get('admin') != None:
		admin = session['admin']
		adminInfo = db.exe_fetch(SQL['adminInfo_id'].format(id=admin))
		if 'Super' in adminInfo['admin']:
			adminID = request.form['adminID']
			account = request.form['account']
			password = request.form['password']
			client = request.form['client']
			article = request.form['article']
			comment = request.form['comment']
			carousel = request.form['carousel']
			news = request.form['news']
			revenue = request.form['revenue']

			if '@' not in account:
				db.exe_commit(SQL['updateAdmin'].format(ac=account,p=password,client=client,article=article,comment=comment,carousel=carousel,news=news,revenue=revenue,ID=adminID))
			else:
				message = "@ should not be in account"
				return render_template('back.html',title='Error',message=message)

			return redirect(url_for('admin_manage',arg='admin'))
		else:
			message = 'You are not allow to edit.'
			return render_template('back.html',title='Error',message=message)
	else:
		return redirect(url_for('login'))

@app.route('/newAdmin_create', methods=['post']) #Process for super admin create new admin account
def newAdmin_create():
	if session.get('admin') != None:
		admin = session['admin']
		adminInfo = db.exe_fetch(SQL['adminInfo_id'].format(id=admin))
		if 'Super' in adminInfo['admin']:
			account = request.form['account']
			password = request.form['password']
			client = request.form['client']
			article = request.form['article']
			comment = request.form['comment']
			carousel = request.form['carousel']
			news = request.form['news']
			revenue = request.form['revenue']

			if '@' not in account:
				db.exe_commit(SQL['newAdmin'].format(ac=account,p=password,client=client,article=article,comment=comment,carousel=carousel,news=news,r=revenue))
			else:
				message = "@ should not be in account"
				return render_template('back.html',title='Error',message=message)

			return redirect(url_for('admin_manage',arg='admin'))
		else:
			message = 'You are not allow to edit.'
			return render_template('back.html',title='Error',message=message)
	else:
		return redirect(url_for('login'))

@app.route('/admin_out') #Admin logout
def admin_out():
	if session.get('admin') != None:
		session.pop('admin')
		return redirect(url_for('home'))
	else:
		return redirect(url_for('login'))
###############################################################################################
#Admin end

#Errorhandler
###############################################################################################
@app.errorhandler(404) #Error Handler for 404 Not Found
def error404(e):
	return redirect(url_for('home'))

@app.errorhandler(405) #Error Handler for 405 Method Not Allowed
def error405(e):
	return redirect(url_for('home'))

@app.errorhandler(500) #Error Handler for 500 Internal Server Error
def error500(e):
	return redirect(url_for('home'))
###############################################################################################

if __name__ == "__main__":
	app.run(debug = True)

