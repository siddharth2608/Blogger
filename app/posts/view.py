import os
import secrets
from flask.views import MethodView
from flask import render_template, redirect, url_for,request,json, flash
from app.posts.forms import PostForm,UpdatePostForm,StartForm, SearchForm,UploadFileForm
from app.posts.controllers import PostController
from app.users.controllers import UserController
import math
from PIL import Image
import random, string
from flask import render_template,make_response, current_app, Response
from redis import Redis
from werkzeug.utils import secure_filename
from app.aws_connections import *
import pika
import base64


connection = pika.BlockingConnection(pika.URLParameters("amqps://vdmysoyb:UPUOLzZyoAzNBZ051hSYvK1HEOhbtQkI@armadillo.rmq.cloudamqp.com/vdmysoyb"))
channel = connection.channel()
channel.queue_declare(queue='image_queue')

S3_BUCKET = "bloggapp"
redis = Redis(host='localhost', port=6379, db=0)


def parse_txt_data(file):
	lines = file.read().decode('utf-8').splitlines()
	token = request.cookies.get('userId')
	user_id = int(redis.get(token))
	posts_data =[]
	for line in lines:
		data = {}
		post = line.strip().split('~')
		data['title']=post[0]
		data['content']=post[1]
		data['photo1']=post[2]
		data['video']=post[3]
		data['user_id'] = user_id
		posts_data.append(data)
	posts_data.pop(0)
	return posts_data
		

class CreatePost(MethodView):
	def get(self):
		form = PostForm()
		token = request.cookies.get('userId')
		if token is not None:
			user_id = int(redis.get(token))
		return render_template('/posts/create.html',form=form,user_id=user_id,title='New Post')

	def post(self):
		form = PostForm()
		token = request.cookies.get('userId')
		user_id = int(redis.get(token))
		if form.validate_on_submit():
			post_data = {'title':form.title.data, 'content':form.content.data,'video':form.video.data, 'user_id': user_id} #, 'photo1': images
			postid = PostController().save_post_data_with_image(post_data)
			img_list_count = len(request.files.getlist('photo1'))
			if img_list_count>0:
				image_lst = []
				for file in request.files.getlist('photo1'):
					if file and is_file_type_allowed(file.filename):
						encoded_image_bytes = base64.b64encode(file.read())
						encoded_image_str = encoded_image_bytes.decode("utf-8")
						image_lst.append(encoded_image_str)

				upload_data = {
					"post_id": postid,
					"image_data": ",".join(image_lst)
				}
				channel.basic_publish(exchange='', routing_key='image_queue', body=json.dumps(upload_data))
			return redirect(url_for('bp.posts_list',page=1))
		return render_template('/posts/create.html',form=form,user_id=user_id,title='New Post')
	  

class PostList(MethodView):
	def get(self,page):

		arr = []
		token=''
		user_id=''
		posts = PostController().fetch_paginated_post(page)
		posts_count = PostController().fetch_posts_count()
		if request.cookies.get('userId') is not None:
			token = request.cookies.get('userId')
		if token:
			user_id = int(redis.get(token))
		if user_id:
			action_performed_by_user = PostController().get_postid_by_userid(user_id)
			for i in action_performed_by_user:
				arr.append(i.get('post_id'))
			posts_count = posts_count.get('posts_count')/5
			page_num = math.ceil(posts_count)+1
			return render_template('/posts/home.html', posts=posts,user_id=user_id,page_num=page_num,arr=arr,title='Home')

		posts_count = posts_count.get('posts_count')/5
		page_num = math.ceil(posts_count)+1
		return render_template('/posts/home.html', posts=posts,page_num=page_num,title='Home')

	

class ReactPost(MethodView):
	def post(self):
		params=dict(request.form)
		print(params)
		token = request.cookies.get('userId')
		user_id = redis.get(token)
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
		return Response(json.dumps(params),status=200,content_type='application/json')


class PostDetail(MethodView):
	def get(self,post_id):
		token = request.cookies.get('userId')
		user_id = int(redis.get(token))
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
			img_list_count = len(request.files.getlist('photo1'))
			token = request.cookies.get('userId')
			user_id = int(redis.get(token))
			if img_list_count>0:
				image_lst = []
				for file in request.files.getlist('photo1'):
					if file and is_file_type_allowed(file.filename):
						provided_file_name = secure_filename(file.filename)
						stored_file_name = upload_file_to_s3(file,provided_file_name)
						# url = get_presigned_file_url(stored_file_name,provided_file_name)
						url1 = f"https://{S3_BUCKET}.s3.amazonaws.com/{stored_file_name}"
						image_lst.append(url1)
				images = ",".join(image_lst)
				post_data= {'title':form.title.data, 'content':form.content.data,'video':form.video.data, 'id':post_id,'photo1':images}
				PostController().update_post_with_image(post_data)
				return redirect(url_for('bp.posts_list',page=1))
			else:
				post_data= {'title':form.title.data, 'content':form.content.data,'video':form.video.data, 'id':post_id}	
				PostController().update_post(post_data)
				return redirect(url_for('bp.posts_list',page=1))
		return render_template('/posts/updatepost.html',form=form,title='Update Post')
			
class Home(MethodView):
	def get(self):
		form = StartForm()
		return render_template('/posts/start.html',form=form)

	def post(self):
		form = StartForm()
		if form.validate_on_submit():
			return redirect(url_for('bp.posts_list',page=1))

class SearchPost(MethodView):
	def post(self):
		token=''
		user_id=''
		if request.cookies.get('userId') is not None:
			token = request.cookies.get('userId')
		if token:
			user_id = int(redis.get(token))
		form = SearchForm()
		searchword = form.search.data
		form_data = {
			"search" : searchword
		}
		if redis.get(searchword) is None:
			posts = PostController().get_search_data(form_data)
			redis.set(searchword,json.dumps(posts))
			redis.expire(searchword,1800)
		else:
			posts = json.loads(redis.get(searchword))
		return render_template('/posts/searchresult.html', form=form, posts=posts,user_id=user_id,title='Search')

class CreatePostFromFile(MethodView):

	def get(self):
		form=UploadFileForm()
		return render_template('/posts/upload_file.html',title='Upload File',form=form)

	def post(self):
		form=UploadFileForm()
		if 'file' not in request.files:
			return "No file part"
		file = request.files['file']
		if file:
			datas = parse_txt_data(file)
			PostController().save_data_from_file(datas)
			return redirect(url_for('bp.posts_list',page=1))
		return render_template('/posts/upload_file.html',title='Upload File',form=form)



