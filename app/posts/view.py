import os
import secrets
from flask.views import MethodView
from flask import render_template, redirect, url_for,request,json
from app.posts.forms import PostForm,UpdatePostForm,StartForm
from app.posts.controllers import PostController
from app.users.controllers import UserController
import math
from PIL import Image
import random, string
from flask import render_template,make_response, current_app, Response

class CreatePost(MethodView):
	def get(self):
		form = PostForm()
		user_id = request.cookies.get('userId')
		return render_template('/posts/create.html',form=form,user_id=user_id,title='New Post')

	def post(self):
		form = PostForm()
		if form.validate_on_submit():
			user_id = request.cookies.get('userId')
			if form.photo1.data:
				filename = self.save_picture(form.photo1.data)
				post_data = {'title':form.title.data, 'content':form.content.data,'video':form.video.data, 'user_id': user_id, 'photo1': filename}
				PostController().save_post_data_with_image(post_data)
			else:
				post_data = {'title':form.title.data, 'content':form.content.data,'video':form.video.data, 'user_id': user_id} 				
				PostController().save_post_data(post_data)
		return redirect(url_for('bp.posts_list',page=1))

	def save_picture(self, form_picture):
		random_hex = secrets.token_hex(8)
		_, f_ext = os.path.splitext(form_picture.filename)
		picture_fn = random_hex + f_ext
		picture_path = os.path.join(current_app.root_path, 'static/profile', picture_fn)

		output_size = (400,300)
		i = Image.open(form_picture)
		i.thumbnail(output_size)
		i.save(picture_path)
		return picture_fn
		  

class PostList(MethodView):
	def get(self,page):
		arr = []
		posts_count = PostController().fetch_posts_count()
		posts = PostController().fetch_paginated_post(page)
		user_id = request.cookies.get('userId')
		if user_id:
			action_performed_by_user = PostController().get_postid_by_userid(user_id)
			print(action_performed_by_user)
			for i in action_performed_by_user:
				arr.append(i.get('post_id'))
			print(arr)	
		posts_count = posts_count.get('posts_count')/5
		page_num = math.ceil(posts_count)+1
		print(posts_count)
		print(page_num)
		return render_template('/posts/home.html', posts=posts,user_id=user_id,page_num=page_num,arr=arr,title='Home')
	

class ReactPost(MethodView):
	def post(self):
		params=dict(request.form)
		print(params)
		user_id = request.cookies.get('userId')
		if params.get('action') == 'like':
			print('like')
			PostController().insert_reaction(user_id,params.get('post_id'),params.get('action'))
			PostController().update_like(params.get('post_id'),params.get('action'))
		elif params.get('action') == 'dislike':	
			print('dislike')
			PostController().update_reaction(user_id,params.get('post_id'),params.get('action'))
			PostController().update_like(params.get('post_id'),params.get('action'))
		elif params.get('action') == 'unlike':
			print('unlike')
			PostController().del_reaction(user_id,params.get('post_id'))
			PostController().delete_like(params.get('post_id'),params.get('action'))
		elif params.get('action') == 'undislike':
			print('undislike')
			PostController().del_reaction(user_id,params.get('post_id'))
			PostController().delete_like(params.get('post_id'),params.get('action'))
		print('Successful')	
		return Response(json.dumps(params),status=200,content_type='application/json')

 



class PostDetail(MethodView):
	def get(self,post_id):
		user_id = request.cookies.get('userId')
		user_data = UserController().get_user_detail(user_id)
		details = PostController().get_detail(post_id)
		details.update({'id': str(details.get('id'))})
		return render_template('/posts/detail.html',post=details,user_data=user_data,user_id=user_id)

class DeletePost(MethodView):
	def post(self,post_id):
		delete = PostController().del_post(post_id)
		return redirect(url_for('bp.posts_list',page=1))

class UpdatePost(MethodView):
	def get(self,post_id):
		post = PostController().get_post_by_id(post_id)
		form = UpdatePostForm()
		form.title.data = post.get('title')
		form.content.data = post.get('content')
		form.video.data = post.get('video')
		form.photo1.data = post.get('photo1')
		return render_template('/posts/updatepost.html',form=form,title='Update Post')

	def post(self,post_id):
		form = UpdatePostForm()
		if form.validate_on_submit():
			if form.photo1.data:
				filename = self.save_picture(form.photo1.data)
				post_data= {'title':form.title.data, 'content':form.content.data,'video':form.video.data, 'id':post_id,'photo1':filename}
				PostController().update_post_with_image(post_data)
			else:
				post_data= {'title':form.title.data, 'content':form.content.data,'video':form.video.data, 'id':post_id}	
				PostController().update_post(post_data)
		return redirect(url_for('bp.posts_list',page=1))


	def save_picture(self, form_picture):
		random_hex = secrets.token_hex(8)
		_, f_ext = os.path.splitext(form_picture.filename)
		picture_fn = random_hex + f_ext
		picture_path = os.path.join(current_app.root_path, 'static/profile', picture_fn)

		output_size = (400,300)
		i = Image.open(form_picture)
		i.thumbnail(output_size)
		i.save(picture_path)
		return picture_fn	
			
class Home(MethodView):
	def get(self):
		form = StartForm()
		return render_template('/posts/start.html',form=form)

	def post(self):
		form = StartForm()
		if form.validate_on_submit():
			return redirect(url_for('bp.posts_list',page=1))	