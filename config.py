from app.connections import SqlConnection
from redis import Redis

class Config:

	MYSQL_CONFIG = {
        'host': '127.0.0.1',
        'user': 'root',
        'passwd': 'root@123',
        'db': 'blogger',
        'port': 3306
    }
	MYSQL_CONN = SqlConnection(MYSQL_CONFIG)
	REDIS_CONN = Redis(host='localhost', port=6379, db=0)