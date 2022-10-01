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


class RegisterUser(MethodView):
	def get(self):
		form = RegistrationForm()
		title = 'register'
		return render_template('auth/register.html', form=form, title=title)

	def post(self):
		form = RegistrationForm()
		print(form)
		if form.validate_on_submit():
			if form.picture.data:
				filename = self.save_picture(form.picture.data)
				register_data = {'username': form.username.data,'email': form.email.data,'password': form.password.data,'instagram': form.instagram.data, 'twitter':form.twitter.data, 'quora':form.quora.data, 'avatar':filename}
				AuthController().save_registration_form(register_data)
				flash('Your account has been created! You are now able to log in', 'success')
				return redirect(url_for('bp.login_user'))
			else:	
				register_data = {'username': form.username.data,'email': form.email.data,'password': form.password.data,'instagram': form.instagram.data, 'twitter':form.twitter.data, 'quora':form.quora.data}
				AuthController().save_registration_form_without_image(register_data)
				flash('Your account has been created! You are now able to log in', 'success')
				return redirect(url_for('bp.login_user'))
		return render_template('auth/register.html',form=form)	

	def save_picture(self, form_picture):
		random_hex = secrets.token_hex(8)
		_, f_ext = os.path.splitext(form_picture.filename)
		picture_fn = random_hex + f_ext
		picture_path = os.path.join(current_app.root_path, 'static/profile', picture_fn)

		output_size = (125, 125)
		i = Image.open(form_picture)
		i.thumbnail(output_size)
		i.save(picture_path)
		return picture_fn


class LoginUser(MethodView):

	def get(self):
		form = LoginForm()
		return render_template('auth/login.html',form=form,title='Login')

	def post(self):
		form = LoginForm()
		if form.validate_on_submit():
			login_data = {'email': form.email.data,'password': form.password.data}
			user_data = AuthController().get_user_data(login_data)
			print(user_data)
			if user_data:
				response = make_response(redirect(url_for('bp.posts_list',page=1)))
				response.set_cookie('userId', str(user_data.get('id')))
				return response
			else:
				flash('Login Unsuccessful. Please check email and password', 'danger')	
		return render_template('/auth/login.html', title='Login', form=form)


class UpdateUser(MethodView):
	def get(self):
		user_id = request.cookies.get('userId')
		user = AuthController().get_user_detail(user_id)
		form = UpdateAccountForm()
		form.username.data = user.get('username')
		form.instagram.data = user.get('instagram')
		form.twitter.data = user.get('twitter')
		form.quora.data = user.get('quora')
		return render_template('/auth/update_account.html',form=form,user_id=user_id,title='Update Account')

	def save_picture(self, form_picture):
		random_hex = secrets.token_hex(8)
		_, f_ext = os.path.splitext(form_picture.filename)
		picture_fn = random_hex + f_ext
		picture_path = os.path.join(current_app.root_path, 'static/profile', picture_fn)

		output_size = (125, 125)
		i = Image.open(form_picture)
		i.thumbnail(output_size)
		i.save(picture_path)
		return picture_fn

	def post(self):
		form = UpdateAccountForm()
		if form.validate_on_submit():
			if form.picture.data:
				filename = self.save_picture(form.picture.data)	
			user_id = request.cookies.get('userId')
			print(request.files)
			if form.picture.data:
				user_data = {'username': form.username.data, 'instagram': form.instagram.data, 'id':user_id, 'avatar': filename, 'twitter':form.twitter.data, 'quora':form.quora.data}
				AuthController().update_user_with_image(user_data)
			else:
				user_data = {'username': form.username.data, 'instagram': form.instagram.data, 'twitter':form.twitter.data, 'quora':form.quora.data, 'id':user_id}
				AuthController().update_user_without_image(user_data)	
		return redirect(url_for('bp.posts_list',page=1))	

class LogoutUser(MethodView):
	def get(self):
		resp = make_response(redirect(url_for('bp.posts_list',page=1)))
		# Delete cookie
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
		print(email)
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