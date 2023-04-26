from __future__ import print_function
import sys
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo

class Register(FlaskForm):
    username = StringField('Username',validators = [DataRequired(), Length(min=3,max=20)])
    #print(username, file=sys.stderr)
    password = PasswordField('Password',validators = [DataRequired()])
    conpassword = PasswordField('Confirm Password',validators = [DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign_Up')
    #cursor.execute('INSERT INTO `user` (`userID`, `username`, `password`, `picture`) VALUES (, , );')

class Login(FlaskForm):
    username = StringField('Username',validators = [DataRequired(), Length(min=3,max=20)])
    password = PasswordField('Password',validators = [DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField('Login')

class Post(FlaskForm):
    post = StringField('Post', validators=[DataRequired()])