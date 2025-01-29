import sqlite3

class Database():

    def __init__():
        self.initDbCursor()
        self.app_names = list[str]

    def findAppNames():
        self.cursor.execute("SELECT appname FROM applications")
        self.app_names = self.cursor.fetchall()
        return None

    def initDbCursor() -> sqlite3.Cursor:
        self.connect = sqlite3.connect("../data/appman.db")
        self.cursor = connect.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS applications ( \
            id INTEGER PRIMARY KEY AUTOINCREMENT, \
            appname TEXT NOT NULL, \
            file TEXT NOT NULL, \
            active BOOLEAN NOT NULL \
        )")
