from config import Config
from datetime import datetime

class PostController:

	def __init__(self):
		self.db_conn = Config.SQLITE_CONN

	def save_post_data(self, post_data):
		current_datetime = datetime.now().strftime("%Y-%m-%d")
		post_data.update({'created_at': current_datetime})
		query = '''insert into posts (title, content,created_at, user_id, video)
					values ("{title}","{content}","{created_at}","{user_id}","{video}")'''.format(**post_data)
		self.db_conn.write_db(query)

	def save_post_data_with_image(self,post_data):
		current_datetime = datetime.now().strftime("%Y-%m-%d")
		post_data.update({'created_at': current_datetime})
		query = '''insert into posts (title, content,created_at, user_id, video,photo1)
					values ("{title}","{content}","{created_at}","{user_id}","{video}","{photo1}")'''.format(**post_data)
		self.db_conn.write_db(query)

	def fetch_paginated_post(self, page):
		query = '''select p.*, u.instagram, u.username, u.avatar,u.twitter,u.quora, ri.rating_action
					from posts as p 
					left join users u on u.id = p.user_id
					left join rating_info ri on ri.user_id = p.user_id and ri.post_id = p.id 
					order by p.created_at desc
					limit 5 offset {}'''.format((page-1)*5)
		return self.db_conn.query_db(query)

	def fetch_posts_count(self):
		query = '''select count(1) as posts_count from posts'''
		return self.db_conn.query_db_one(query)

	def get_detail(self,post_id):
		query = '''select * from posts where id = "{}"'''.format(post_id)
		return self.db_conn.query_db_one(query)	

	def del_post(self,post_id):
		query = '''delete from posts where id = "{}"'''.format(post_id)
		return self.db_conn.write_db(query)

	def get_post_by_id(self,post_id):
		query = '''select * from posts where id = "{}"'''.format(post_id)
		print(query)
		return self.db_conn.query_db_one(query)

	def update_post(self,post_data):
		query = '''update posts set title="{title}",content="{content}","video"="{video}" where id = "{id}"'''.format(**post_data)
		return self.db_conn.write_db(query)

	def update_post_with_image(self,post_data):
		query = '''update posts set title="{title}",content="{content}","video"="{video}","photo1"="{photo1}" where id = "{id}"'''.format(**post_data)
		return self.db_conn.write_db(query)

	def get_postid_by_userid(self,user_id):
		query = '''select post_id from rating_info where user_id={}'''.format(user_id)
		return self.db_conn.query_db(query)	

	def get_status_of_rating(self,post_id,user_id):
		query = '''select rating_action from rating_info where post_id = {} and user_id = {}'''.format(post_id,user_id)
		print(query)
		return self.db_conn.query_db_one(query) 

	def insert_reaction(self,user_id,post_id,action):
		query = '''insert into rating_info (user_id,post_id,rating_action)	values ({},{},"{}")'''.format(user_id,post_id,action)
		print(query)
		return self.db_conn.write_db(query)

	def update_like(self,post_id,action):
		if action=='like':
			query = '''update posts set like=like+1 where id = {}'''.format(post_id)
			print(query)
			return self.db_conn.write_db(query)
		elif action=='dislike':
			query = '''update posts set unlike=unlike+1 where id = {}'''.format(post_id)
			print(query)
			return self.db_conn.write_db(query)	

	def update_reaction(self,user_id,post_id,action):
		query = '''update rating_info set user_id={}, post_id={}, rating_action="{}"'''.format(user_id,post_id,action)
		print(query)
		return self.db_conn.write_db(query)

	def del_reaction(self,user_id,post_id):
		query = '''delete from rating_info where user_id = {} and post_id = {} '''.format(user_id,post_id)
		print(query)
		return self.db_conn.write_db(query)

	def delete_like(self,post_id,action):
		if action=='unlike':
			query = '''update posts set like=like-1 where id = {}'''.format(post_id)
			print(query)
			return self.db_conn.write_db(query)
		elif action=='undislike':
			query = '''update posts set unlike=unlike-1 where id = {}'''.format(post_id)
			print(query)
			return self.db_conn.write_db(query)
