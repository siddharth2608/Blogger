from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.auth.controllers import AuthController

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    instagram = StringField('Instagram(Optional)')
    twitter = StringField('Twitter(Optional)')
    picture = FileField('Change Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    quora = StringField('Quora(Optional)')

    submit = SubmitField('Sign Up')

    def validate_email(self,email):
        mail = email.data
        user = AuthController().get_user_data_by_email(mail)
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

    def validate_username(self, username):
        username = username.data
        user = AuthController().get_user_detail_by_username(username)
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')
        

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    instagram = StringField('Instagram(Optional)')
    twitter = StringField('Twitter(Optional)')
    quora = StringField('Quora(Optional)')
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')


class ResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset')


class ResetTokenForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')
