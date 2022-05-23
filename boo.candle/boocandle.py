import eel
import sqlite3
import time

"""
Author: https://github.com/akula12345
"""
@eel.expose
def auth(login, password):
	if login == "Rii" and  password == "Batsman":
		return "Данні вірні!"
	else:
		return "Невірні данні!"

def checkdb():
	db = sqlite3.connect('shop.db')
	sql = db.cursor()
	sql.execute("""CREATE TABLE IF NOT EXISTS purchase (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    material TEXT,
    amount INT,
    timePurchase TEXT,
    price INT
)
""")
	sql.execute("""CREATE TABLE IF NOT EXISTS catalog (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    type TEXT,
    material TEXT,
    smell TEXT,
    colour TEXT,
    timeAdd TEXT,
    price INT
)
""")
	sql.execute("""CREATE TABLE IF NOT EXISTS sale (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    timeSale TEXT,
    price INT
)
""")
	sql.close()

@eel.expose
def purchase(namep, amountp, pricep):
	try:
		checkdb()
		db = sqlite3.connect('shop.db')
		sql = db.cursor()
		named_tuple = time.localtime()
		time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
		sql.execute(f'INSERT INTO purchase(material, amount, timePurchase, price) VALUES (?, ?, ?, ?)', (namep, amountp, time_string, pricep))
		db.commit()
		sql.close()
		return "Товар був доданний до закупівлі!"
	except:
		return "Помилка! :("




@eel.expose
def catalog():
	try:
		checkdb()
		db = sqlite3.connect('shop.db')
		sql = db.cursor()
		catalog = []
		for i in sql.execute('SELECT * FROM catalog'):
			catalog += [i]
		sql.close()
		return catalog
	except:
		return "Помилка!"

@eel.expose
def addCatalogItem(namep, typep, materials, smell, colour, pricep):
	try:
		checkdb()
		db = sqlite3.connect('shop.db')
		sql = db.cursor()
		named_tuple = time.localtime()
		time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
		sql.execute(f'INSERT INTO catalog(name, type, material, smell, colour, timeAdd, price) VALUES (?, ?, ?, ?, ?, ?, ?)', (namep, typep, materials, smell, colour, time_string, pricep))
		db.commit()
		sql.close()
		return "Товар був доданний до закупівлі!"
	except:
		return "Помилка!"

@eel.expose
def saleProduct(id):
	try:
		checkdb()
		db = sqlite3.connect('shop.db')
		sql = db.cursor()
		named_tuple = time.localtime()
		time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
		product = []
		for i in sql.execute("SELECT * FROM catalog WHERE id={}".format(id)):
			product = i
		sql.execute("DELETE FROM catalog WHERE id={}".format(id))
		sql.execute(f'INSERT INTO sale(name, timeSale, price) VALUES (?, ?, ?)', (product[1], time_string, product[7]))
		db.commit()
		sql.close()
		return catalog
	except:
		return "Помилка!"

@eel.expose
def analysisSale():
	try:
		checkdb()
		db = sqlite3.connect('shop.db')
		sql = db.cursor()
		sale = []
		for i in sql.execute('SELECT * FROM sale'):
			sale += [i]
		sql.close()
		return sale
	except:
		return "Помилка!"

@eel.expose
def analysisPurchase():
	try:
		checkdb()
		db = sqlite3.connect('shop.db')
		sql = db.cursor()
		purchase = []
		for i in sql.execute('SELECT * FROM purchase'):
			purchase += [i]
		sql.close()
		return purchase
	except:
		return "Помилка!"

@eel.expose
def analytics():
		checkdb()
		db = sqlite3.connect('shop.db')
		sql = db.cursor()
		purchase = 0
		sale = 0
		res = 0
		for i in sql.execute('SELECT amount, price FROM purchase'):
			purchase += i[0] * i[1]
		for i in sql.execute('SELECT price FROM sale'):
			sale += i[0]
		sql.close()
		res = sale - purchase
		return [purchase, sale, res]

eel.init("web")
eel.start("index.html", size=(1280, 720))