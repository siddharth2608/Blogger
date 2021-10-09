from config import Config


class UserController:
	def __init__(self):
		self.db_conn = Config.SQLITE_CONN

	def get_all_post_of_user(self,user_id):
		query = '''select * from posts where user_id = "{}"'''.format(user_id)
		return self.db_conn.query_db(query)

	def get_user_detail(self,user_id):
		query = '''select * from users where id = "{}"'''.format(user_id)
		return self.db_conn.query_db_one(query)