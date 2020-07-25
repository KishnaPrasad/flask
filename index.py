from flask import Flask, render_template, redirect, url_for, request
from signupforms import SignupForm
import os
SECRET_KEY = os.urandom(32)


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/welcome')
def welcome():
	return render_template("welcome.html")

@app.route('/login', methods=['GET','POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username']!= 'admin' or request.form['password']!='admin':
			error = 'Invalid Credentials. Please try again.'
		else:
			return redirect(url_for('home'))

	return render_template('login.html', error=error)

@app.route('/signup',methods=('GET','POST'))
def signup():
	form = SignupForm()
	if form.validate_on_submit():
		return redirect(url_for('home'))
	return render_template('signup.html', form=form)

if __name__ == '__main__':
	app.run(debug=True)