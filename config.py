from app.connections import SQLiteConnection


class Config:

	DB_FILE_PATH = 'blogger.db'
	SQLITE_CONN = SQLiteConnection(DB_FILE_PATH)
