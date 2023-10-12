import sqlite3

connect = sqlite3.connect('dataBase.db')
cursor = connect.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS "users" (
			         "id" INTEGER NOT NULL UNIQUE,
			         "tg_id" INTEGER NOT NULL UNIQUE,
			         PRIMARY KEY("id" AUTOINCREMENT)
			        )''')
connect.commit()

cursor.execute('''CREATE TABLE IF NOT EXISTS "categories" (
	         "id" INTEGER NOT NULL,
	         "name" TEXT NOT NULL,
	         "rus_name"	TEXT,
	         PRIMARY KEY("id" AUTOINCREMENT)
	        )''')
connect.commit()

cursor.execute('''CREATE TABLE IF NOT EXISTS "subscribes" (
     "id_user" INTEGER NOT NULL,
     "id_category" INTEGER NOT NULL,
     FOREIGN KEY("id_category") REFERENCES "categories"("id"),
     FOREIGN KEY("id_user") REFERENCES "users"("id")
    )''')
connect.commit()

def insert(tg_id):
	connect = sqlite3.connect('dataBase.db')
	cursor = connect.cursor()
	cursor.execute('INSERT INTO users(tg_id) VALUES (?);', (tg_id,))
	connect.commit()
	# user = cursor.execute("SELECT * FROM users WHERE tg_id = ?",(tg_id,)).fetchone()
	# if user == None:
	# 	cursor.execute('INSERT INTO users(tg_id) VALUES (?);', (tg_id,))
	# 	connect.commit()

def get_category():
	connect = sqlite3.connect('dataBase.db')
	cursor = connect.cursor()
	return cursor.execute('SELECT * FROM categories').fetchall()

def get_user(tg_id):
	connect = sqlite3.connect('dataBase.db')
	cursor = connect.cursor()
	return cursor.execute('SELECT * FROM users WHERE tg_id = ?;', (tg_id,)).fetchone()

#def add_category(id_user, id_category):
	#connect = sqlite3.connect('dataBase.db')
	#cursor = connect.cursor()
	#cursor.execute('INSERT INTO subscribes (id_user, id_category) VALUES (?,?);', (id_user, id_category))

def getIdCat(rus_name):
    connect = sqlite3.connect('dataBase.db')
    cursor = connect.cursor()
    return cursor.execute('SELECT id FROM categories WHERE rus_name = ?;',(rus_name,)).fetchone()

def isSub(id_user, id_category):
    connect = sqlite3.connect('dataBase.db')
    cursor = connect.cursor()
    if type(id_category) is int:
        return cursor.execute('SELECT id_category FROM subscribes WHERE id_user = ? AND id_category = ?;',
                              (id_user, id_category)).fetchone()
    else:
        return cursor.execute('SELECT id_category FROM subscribes WHERE id_user = ? AND id_category = ?;', (id_user, id_category[0])).fetchone()

def insertSub(id_user, id_category):
    connect = sqlite3.connect('dataBase.db')
    cursor = connect.cursor()
    cursor.execute('''INSERT INTO subscribes('id_user', 'id_category') VALUES(?,?);''', (id_user,id_category,))
    connect.commit()

def getSubUser(id_user):
    connect = sqlite3.connect('dataBase.db')
    cursor = connect.cursor()
    return cursor.execute('SELECT categories.rus_name FROM subscribes INNER JOIN categories ON id_category = categories.id '
                          'WHERE id_user = ?;', (id_user,)).fetchall()

def delSub(id_user, id_category):
    connect = sqlite3.connect('dataBase.db')
    cursor = connect.cursor()
    cursor.execute('''DELETE FROM subscribes WHERE id_user = ? AND id_category = ?;''', (id_user, id_category[0],))
    connect.commit()
