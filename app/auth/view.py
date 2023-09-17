import os
import secrets
from PIL import Image
from flask.views import MethodView
from flask import request,flash, redirect, url_for
from flask import render_template,make_response, current_app
from app.auth.forms import RegistrationForm, LoginForm,UpdateAccountForm,ResetForm,ResetTokenForm
from app.auth.controllers import AuthController
from app.mailer import send_mail
import random, string
from werkzeug.utils import secure_filename
from app.aws_connections import *
from config import Config


S3_BUCKET = "bloggapp"


class RegisterUser(MethodView):
	def get(self):
		form = RegistrationForm()
		title = 'register'
		return render_template('auth/register.html', form=form, title=title)

	def post(self):
		form = RegistrationForm()
		file=''
		url1 = ''
		if form.validate_on_submit():
			file = form.picture.data
			if file and is_file_type_allowed(file.filename):
				provided_file_name = secure_filename(file.filename)
				stored_file_name = upload_file_to_s3(file,provided_file_name)
				url1 = f"https://{S3_BUCKET}.s3.amazonaws.com/{stored_file_name}"
			if url1 == '':
				url1 = "https://bloggapp.s3.amazonaws.com/default.jpg"
			register_data = {'username': form.username.data,'email': form.email.data,'password': form.password.data,'instagram': form.instagram.data, 'twitter':form.twitter.data, 'quora':form.quora.data, 'avatar':url1}
			AuthController().save_registration_form(register_data)
			flash('Your account has been created! You are now able to log in', 'success')
			return redirect(url_for('bp.login_user'))
			
		return render_template('auth/register.html',form=form)	



class LoginUser(MethodView):

	def get(self):
		form = LoginForm()
		return render_template('auth/login.html',form=form,title='Login')

	def post(self):
		form = LoginForm()
		if form.validate_on_submit():
			login_data = {'email': form.email.data,'password': form.password.data}
			user_data = AuthController().get_user_data(login_data)
			if user_data:
				token = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
				user_id = (user_data.get('id'))
				Config.REDIS_CONN.set(str(token), str(user_id))
				response = make_response(redirect(url_for('bp.posts_list',page=1)))
				response.set_cookie('userId', str(token))
				return response
			else:
				flash('Login Unsuccessful. Please check email and password', 'danger')	
		return render_template('/auth/login.html', title='Login', form=form)

class UpdateUser(MethodView):
	def get(self):
		token = request.cookies.get('userId')
		user_id = int(Config.REDIS_CONN.get(token))
		user = AuthController().get_user_detail(user_id)
		form = UpdateAccountForm()
		form.username.data = user.get('username')
		form.instagram.data = user.get('instagram')
		form.twitter.data = user.get('twitter')
		form.quora.data = user.get('quora')
		return render_template('/auth/update_account.html',form=form,user_id=user_id,title='Update Account')

	def post(self):
		form = UpdateAccountForm()
		if form.validate_on_submit():
			file=''
			url1 = ''
			file = form.picture.data
			if file and is_file_type_allowed(file.filename):
				provided_file_name = secure_filename(file.filename)
				stored_file_name = upload_file_to_s3(file,provided_file_name)
				# url = get_presigned_file_url(stored_file_name,provided_file_name)
				url1 = f"https://{S3_BUCKET}.s3.amazonaws.com/{stored_file_name}"
			if url1 == '':
				url1 = "https://bloggapp.s3.amazonaws.com/default.jpg"
			token = request.cookies.get('userId')
			user_id = int(Config.REDIS_CONN.get(token))
			user_data = {'username': form.username.data, 'instagram': form.instagram.data, 'id':user_id, 'avatar': url1, 'twitter':form.twitter.data, 'quora':form.quora.data}
			AuthController().update_user_with_image(user_data)
			return redirect(url_for('bp.posts_list',page=1))	
		return render_template('/auth/update_account.html',form=form,user_id=user_id,title='Update Account')

class LogoutUser(MethodView):
	def get(self):
		resp = make_response(redirect(url_for('bp.posts_list',page=1)))
		# Delete cookie
		token = request.cookies.get("userId")
		Config.REDIS_CONN.delete(token)
		resp.delete_cookie("userId")
		return resp

class ResetPassword(MethodView):
	def get(self):
		form = ResetForm()
		return render_template('/auth/reset.html',form=form,title='Reset Password')

	def post(self):
		form = ResetForm()
		if form.validate_on_submit():
			email = form.email.data
			token = self.gen_key()
			AuthController().save_token(email,token)
			body = f'''To reset your password, visit the following link:
			{url_for('bp.check_reset_token', token=token, _external=True)}
			If you did not make this request then simply ignore this email and no changes will be made.
			'''
			send_mail(email,body)
			print('Email sent successfully')
		return redirect(url_for('bp.login_user'))

	def gen_key(self):
		x = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
		return x

class CheckResetToken(MethodView):
	def get(self):
		tokenn = request.args.get('token')
		email = AuthController().get_email_from_token(tokenn)
		if email:
			AuthController().marks_token_used(tokenn)
			form = ResetTokenForm()	
			return render_template('/auth/check_reset_token.html',form=form, email=email)

	def post(self):
		form = ResetTokenForm()
		email = form.email.data
		password = form.password.data
		AuthController().update_password(email,password)
		return redirect(url_for('bp.login_user'))


class DeleteUser(MethodView):
	def get(self,user_id):
		AuthController().deactivate_user(user_id)
		resp = make_response(redirect(url_for('bp.posts_list',page=1)))
		resp.delete_cookie("userId")
		return resp