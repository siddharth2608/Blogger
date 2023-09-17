import mysql.connector as MySQLdb


MYSQL_CONFIG = {
        'host': '127.0.0.1',
        'user': 'root',
        'passwd': 'root@123',
        'db': 'blogger',
        'port': 3306
    }

def save_imageurl_in_posts(data):
	connection = MySQLdb.connect(**MYSQL_CONFIG)
	cursor = connection.cursor()
	query = '''UPDATE posts SET photo1="{url}" where id={post_id}'''.format(**data)
	cursor.execute(query)
	connection.commit()
	cursor.close()
	connection.close()