from config import Config


class AuthController:

	def __init__(self):
		self.db_conn = Config.SQLITE_CONN

	def save_registration_form(self, register_data):
		query = '''insert into users (username, email, password,instagram,twitter,quora,avatar) 
					values ("{username}", "{email}", "{password}", "{instagram}", "{twitter}", "{quora}", "{avatar}")'''.format(**register_data)

		self.db_conn.write_db(query)

	def save_registration_form_without_image(self, register_data):
		query = '''insert into users (username, email, password,instagram,twitter,quora) 
					values ("{username}", "{email}", "{password}", "{instagram}", "{twitter}", "{quora}")'''.format(**register_data)

		self.db_conn.write_db(query)

	def get_user_data(self, login_data):
		query = '''select * from users where email = "{email}" and password = "{password}"'''.format(**login_data)
		result = self.db_conn.query_db_one(query)
		return result

	def get_user_detail(self, user_id):
		query = '''select * from users where id = "{}"'''.format(user_id)
		result = self.db_conn.query_db_one(query)
		return result

	def update_user_with_image(self,user_data):
		query = '''update users set username = "{username}", instagram="{instagram}", avatar="{avatar}", twitter="{twitter}", quora="{quora}"  where id = "{id}"'''.format(**user_data)
		return self.db_conn.write_db(query)	

	def update_user_without_image(self,user_data):
		query = '''update users set username = "{username}", instagram="{instagram}", twitter="{twitter}", quora="{quora}" where id = "{id}"'''.format(**user_data)
		return self.db_conn.write_db(query)	
	

	def save_token(self,email,token):
		query = '''insert into verify_tokens (email, token, is_used)
					values("{}", "{}","0")'''.format(email,token)
		self.db_conn.write_db(query)

	def get_email_from_token(self,tokenn):
		query = '''select email from verify_tokens where token = "{}"'''.format(tokenn)
		print(query)
		return self.db_conn.query_db_one(query)

	def marks_token_used(self,tokenn):
		query = '''update verify_tokens set	is_used = "1" where token = "{}"'''.format(tokenn)
		self.db_conn.write_db(query)

	def update_password(self,email,password):
		query = '''update users	set password = "{}" where email = "{}"'''.format(password,email)
		self.db_conn.write_db(query)

	def get_user_data_by_email(self,email):
		query = '''select email from users where email = "{}"'''.format(email)
		print(query)
		return self.db_conn.query_db_one(query)

	def get_user_detail_by_username(self,username):
		query = '''select username from users where username = "{}"'''.format(username)
		return self.db_conn.query_db_one(query)	

	def deactivate_user(self,user_id):
		query = '''delete from users where id = "{}" '''.format(user_id)
		return self.db_conn.write_db(query)	