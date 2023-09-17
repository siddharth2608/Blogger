from flask.views import MethodView
from flask import render_template,request
from app.users.controllers import UserController
from redis import Redis

redis = Redis(host='localhost', port=6379, db=0)

class Profile(MethodView):

	def get(self):
		token = request.cookies.get('userId')
		user_id = int(redis.get(token))
		posts = UserController().get_all_post_of_user(user_id)
		print(posts)
		user_data = UserController().get_user_detail(user_id)
		return render_template('/users/profile.html',posts=posts,user_data=user_data,user_id=user_id)