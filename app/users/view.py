from flask.views import MethodView
from flask import render_template,request
from app.users.controllers import UserController


class Profile(MethodView):

	def get(self):
		user_id = request.cookies.get('userId')
		posts = UserController().get_all_post_of_user(user_id)
		user_data = UserController().get_user_detail(user_id)
		return render_template('/users/profile.html',posts=posts,user_data=user_data,user_id=user_id)
