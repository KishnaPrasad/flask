from flask import Flask, render_template, redirect, url_for, request, flash, session
from signupforms import SignupForm
from datetime import datetime
from hashlib import md5
import pyrebase
import os

SECRET_KEY = os.urandom(32)

firebaseConfig = {
    "apiKey": "AIzaSyBKgvQ9Lvp-Q4KqN1kzUfMK7bvulCxf4Zc",
    "authDomain": "babydocs.firebaseapp.com",
    "databaseURL": "https://babydocs.firebaseio.com",
    "projectId": "babydocs",
    "storageBucket": "babydocs.appspot.com",
    "messagingSenderId": "310654851506",
    "appId": "1:310654851506:web:849daa929f8ca8745d6cab",
    "measurementId": "G-JG656E9G3M"
  }

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


firebase = pyrebase.initialize_app(firebaseConfig)

auth = firebase.auth()
db = firebase.database()
global user
@app.route('/', methods=['GET','POST'])
def index():
	unsuccessfull = "please check your Credentials"
	try:
		print(session['usr'])
		return redirect(url_for('home'))
		
		# return redirect(url_for('home'))
	except:

		if request.method == 'POST':
			email = request.form.get('emailtext')
			password = request.form.get('passtext')
			try:
				session['email'] = email
				session['password'] = password
				user = auth.sign_in_with_email_and_password(email,password)
				user = auth.refresh(user['refreshToken'])
				user_id = user['idToken']
				session['usr'] = user_id
				return redirect(url_for("home"))
			except:
				return render_template("index.html", us=unsuccessfull)

	return render_template("index.html")

# @app.route('/welcome')
# def welcome():
# 	return render_template("welcome.html")

# @app.route('/login', methods=['GET','POST'])
# def login():
# 	error = None
# 	if request.method == 'POST':
# 		if request.form['username']!= 'admin' or request.form['password']!='admin':
# 			error = 'Invalid Credentials. Please try again.'
# 		else:
# 			return redirect(url_for('welcome'))

# 	return render_template('login.html', error=error)

@app.route('/signup', methods=['GET','POST'])
def signup():
	form = SignupForm()
	if not session['email'] is None:
		if form.validate_on_submit():
			name = request.form.get('name')
			email=request.form.get('email')
			passw = request.form.get('password')
			try:
				session['email'] = email
				session['password'] = passw
				user = auth.create_user_with_email_and_password(email, passw)
				user = auth.refresh(user['refreshToken'])
				user_id = user['idToken']
				session['usr'] = user_id
				hashed_email = md5(email.lower().encode('utf-8')).hexdigest()
				data = {"name": name,"email": email}
				ref="user_data/"+hashed_email+"/"
				db.child(ref).set(data)
				return redirect(url_for("home"))
			except Exception as e:
				return render_template('signup.html',form=form, error=str(e))
		return render_template('signup.html',form=form)
	else:
		return render_template('home.html')

@app.route('/home',methods=['GET','POST'])
def home():
	un="successfully logge out"
	if request.method=='POST':
			if request.form["log"] == 'Logout':
				try:
					session.pop('email',None)
					session.pop('password',None)
					session.pop('usr',None)
					auth.signOut()
					return redirect(url_for("index"))
				except Exception as e:
					return render_template("index.html",error=str(e))
		

	if not session.get("email") is None:
		email = session.get("email")
		passw = session.get("password")

		user = auth.sign_in_with_email_and_password(email,passw)
		
		ref = "user_data/"
		s=""
		all_users = db.child(ref).get()
		for user in all_users.each():
			if email in user.val().values():
				name = user.val().values()
				s=name[1]
		hashed_email = md5(email.lower().encode('utf-8')).hexdigest()
		ref = "users/"+hashed_email+"/"
		start_date = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
		data={"email":email,"name":s,"time_stamp":start_date}
		db.child(ref).set(data)

		ref_status = "users/"
		email_lists=[]
		all_user_status = db.child(ref_status).get()
		for user in all_user_status.each():
			count_email = user.val().values()
			email_lists.append(md5(count_email[1].lower().encode('utf-8')).hexdigest())
			# email_lists.append(count_email[1])
			# print(count_email[1])
			
		pass_Data_tooltip = "Name :"+s+"\n"+"Last visited:"+start_date
		
				
		#user_data = db.child(ref).get().val()
		#name = user_data.values()
		
		# data={"name":"","time_stamp":time_now}
		# db.child("users").push(data)

		return render_template("home.html",email_lists=email_lists, data = pass_Data_tooltip)
	else:
		return redirect(url_for("index"))

# @app.route('/test')
# def test():
# 	if request.method == 'GET':
# 		sessionsRef = firebase.database().ref("sessions");
# 		sessionsRef.push({
#   		startedAt: firebase.database.ServerValue.TIMESTAMP
# 		});


if __name__ == '__main__':
	app.run(debug=True)