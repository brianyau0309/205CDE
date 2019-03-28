from flask import Flask, render_template, redirect, url_for, request, session, flash
from database import connection, SQL
from pathlib import Path
from werkzeug.utils import secure_filename
import os, datetime

UPLOAD_FOLDER = os.getcwd()  + '/static/image/icon'
ALLOWED_EXTENSIONS = set(['png', 'jpg'])

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = connection()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_user(): #get user by session
	user = session.get('clientID')
	if user != None:
		info = db.exe_fetch(SQL["clientInfo_ID"].format(clientID=user), 'one')
		return info['nickname']
	else:
		return 'Guest'

@app.route('/index')
@app.route('/')
def home():
	items = db.exe_fetch(SQL['hot_item'],'all')
	for i in items:
		ownerName = db.exe_fetch(SQL['clientInfo_ID'].format(clientID=i['owner']))['nickname']
		i['ownerName'] = ownerName
		if Path(os.getcwd()+'/static/image//article/'+str(i['articleID'])+'.png').exists():
			i['image'] = 'image//article/'+str(i['articleID'])+'.png'
		elif Path(os.getcwd()+'/static/image//article/'+str(i['articleID'])+'.jpg').exists():
			i['image'] = 'image/article/'+str(i['articleID'])+'.jpg'
		else:
			i['image'] = 'image//article/default.png'

	hot_1 = items[:4]
	hot_2 = items[4:]

	return render_template('Home.html', username = get_user(),hot_1=hot_1,hot_2=hot_2)

#login
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
	checkEmail = db.exe_fetch(SQL['clientInfo_email'].format(email=email))

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
	session.pop('clientID')
	return redirect(url_for('home'))

#login end

#signup
@app.route('/signup')
def signup():
	if session.get('clientID') != None:
		return redirect(url_for('home'))	
	else:
		return render_template('SignUp.html')

@app.route('/signup_done', methods = ["post"])
def signup_done():
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
			if userInfo.get('icon') == None:
				icon = url_for('static',filename='image/icon/default.png')
			else:
				icon = url_for('static',filename=userInfo['icon'])
			return render_template('SignUp_Done.html',usericon=icon,userID=userInfo['clientID'],userName=userInfo['nickname'],userEmail=userInfo['email'],userPassword=userInfo['password'])
		else:
			flash('Used email','email')
			return redirect(url_for('signup'))

#signup end

#user pages

@app.route('/profile')
def profile():
	pass

@app.route('/record')
def record():
	return render_template('list_article.html')

@app.route('/myarticle')
def myarticle():
	userID = session.get('clientID')
	articles = db.exe_fetch(SQL['articleInfo_owner'].format(ID=userID),'all')

	return render_template('list_article.html',pageTitle='My Article',username=get_user(),articles=articles)

#user pages end

#edition
@app.route('/edit')
def edit():
	return render_template('Edition.html',username=get_user())

@app.route("/edit_done", methods=['post'])
def edit_done():
	clientID = session.get('clientID')
	title = request.form['title']
	price = request.form['price']
	description = request.form['description']
	content = request.form['content']
	date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

	db.exe_commit(SQL['newArticle'].format(t=title,p=price,des=description,c=content,date=date,o=clientID))

	return "OK"
#edition end

#article
@app.route('/article/<id>')
def article(id):
	a = db.exe_fetch(SQL['articleInfo'].format(ID=id))
	ownerName = db.exe_fetch(SQL['clientInfo_ID'].format(clientID=a['owner']))['nickname']
	return render_template('Article.html', username=get_user(),title=a['title'], price=a['price'], description=a['description'], content=a['content'].replace('\n','<br>'), date=a['date'], name=ownerName)
#article end 

@app.route('/news/<arg>')
def news(arg):
	if arg == 'all':
		return render_template('News.html')
		
@app.route('/testing')
def testing():
	return render_template('testing.html')

@app.route('/upload', methods=['post'])
def upload():
	file = request.files['file']
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		return '.' + filename.split('.')[-1]


if __name__ == "__main__":
	app.run(debug = True)

