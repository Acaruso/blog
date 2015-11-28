from flask import *
from flask.ext.mysqldb import MySQL

mysql = MySQL()

main = Blueprint('main', __name__, template_folder='views')

def get_entry(id):
	cur = mysql.connection.cursor()
	query = "SELECT * FROM blog.BlogEntry WHERE entryid = " + str(id)
	cur.execute(query)
	return cur.fetchall()

def get_entries():
	cur = mysql.connection.cursor()
	query = "SELECT * FROM blog.BlogEntry"
	cur.execute(query)
	return cur.fetchall()

@main.route('/')
def main_route():
	options = {
		"str": "hi",
		"str2": '''hello<br/>
		<iframe width="420" height="315"
		src="https://www.youtube.com/embed/ybqDzhaKH4A?autoplay=1">
		</iframe><br/>
		asdf
		'''
	}
	print get_entries()
		
	return render_template("index.html", **options)

