from flask import *
from flask.ext.mysqldb import MySQL

mysql = MySQL()

main = Blueprint('main', __name__, template_folder='views')

class Entry:
	def __init__(self, id, date, content):
		self.id      = id
		self.date    = date
		self.content = content
	
def get_entry(id):
	cur   = mysql.connection.cursor()
	query = "SELECT * FROM blog.BlogEntry WHERE entryid = " + str(id)
	cur.execute(query)
	res   = cur.fetchall()
	entry = Entry(id, res[0][1], res[0][2])
	return entry

def get_all_entries():
	cur     = mysql.connection.cursor()
	query   = "SELECT * FROM blog.BlogEntry"
	size    = cur.execute(query)
	res     = cur.fetchall()
	entries = []
	for i in range (0, size):
		entry = Entry(res[i][0], res[i][1], res[i][2])
		entries.append(entry)
	return entries

def get_range_entries(begin, end):
	cur     = mysql.connection.cursor()
	query   = "SELECT * FROM blog.BlogEntry WHERE entryid >= " + str(begin)
	query  += " AND entryid <= " + str(end)
	size    = cur.execute(query)
	res     = cur.fetchall()
	entries = []
	for i in range (0, size):
		entry = Entry(res[i][0], res[i][1], res[i][2])
		entries.append(entry)
	return entries

def get_num_entries():
	cur   = mysql.connection.cursor()
	query = "SELECT COUNT(*) FROM blog.BlogEntry"
	cur.execute(query)
	return cur.fetchall()[0][0]
	
def check_username():
	if(session.has_key('username') == True):
		username = session['username']

@main.route('/')
def main_route():

	page = request.args.get('page')
	if page == None or page == '':
		page = 0
	else:
		page = int(page)

	num_entries = get_num_entries()

	begin = (page * 5) + 1
	end   = begin + 4

	if end > num_entries:
		end = num_entries

	entries = get_range_entries(begin, end)

	older = False
	newer = False

	if page > 0:
		newer = True
	if end < num_entries and num_entries > 5:
		print(end)
		print(num_entries)
		older = True
	
	username  = None
	logged_in = False
	if(session.has_key('username') == True):
		username  = session['username']
		logged_in = True

	options = {
		"entries"	: entries,
		"older"  	: older,
		"newer"  	: newer,
		"plus1"	 	: page+1,
		"minus1" 	: page-1,
		"username"	: username,
		"logged_in"	: logged_in
	}
	return render_template("index.html", **options)

