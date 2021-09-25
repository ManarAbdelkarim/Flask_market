from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo , Email, DataRequired, ValidationError
from .models import User
import re
class RegistrationForm(FlaskForm):
    def validate_username(self,username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError("This username already exists")
    def validate_email(self,email_to_check):
        user = User.query.filter_by(email=email_to_check.data).first()
        if user:
            raise ValidationError("This email already exists")
    def validate_password1(self,password_to_check):
            length_error = len(password_to_check.data) < 8  
            digit_error = re.search(r"\d", password_to_check.data) is None
            uppercase_error = re.search(r"[A-Z]", password_to_check.data) is None
            lowercase_error = re.search(r"[a-z]", password_to_check.data) is None
            symbol_error = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password_to_check.data) is None
            password_to_check_ok = not ( length_error or digit_error or uppercase_error or lowercase_error or symbol_error )

            if not  password_to_check_ok:
                raise ValidationError("Weak Password")

    username = StringField(label='User Name:',validators=[Length(min=2,max=30),DataRequired()])
    email = StringField(label='Email Address:', validators=[Email(),DataRequired()])
    password1= PasswordField(label='Password',validators=[Length(min=6),DataRequired()])
    password2= PasswordField(label='Confirm Password',validators=[EqualTo('password1'),DataRequired()])
    submit = SubmitField(label='Submit')

class LoginForm(FlaskForm):
     username = StringField(label='User Name:',validators=[DataRequired()])
     password= PasswordField(label='Password',validators=[DataRequired()])
     submit = SubmitField(label='Sign In')

class PurshaseForm(FlaskForm): 
    submit = SubmitField(label='Purshase Item!')