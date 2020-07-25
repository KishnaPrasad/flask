from flask_wtf import FlaskForm
from wtforms import (StringField,
	TextAreaField,
	SubmitField,
	PasswordField)
from wtforms.validators import (DataRequired,
	InputRequired,
	Email,
	EqualTo,
	Length)
from wtforms import validators
from wtforms.fields.html5 import EmailField


class SignupForm(FlaskForm):
	"""Sign up for a user account."""
	name = StringField('Name',[DataRequired(), Length(min=4, max=26)])
	email = StringField('Email',[InputRequired()])
	password = PasswordField('Password',[InputRequired(),EqualTo('confirmpassword',message='Passwords must match')])
	confirmpassword = PasswordField('Repeat Password',[InputRequired(), EqualTo(password, message='Passwords must match')])
	submit = SubmitField('Submit')
	

 	#, [
     #    Email(message="Not a valid email address."),
      #   DataRequired()])
 	# email = EmailField('Email address',[validators.DataRequired(),validators.Email()])