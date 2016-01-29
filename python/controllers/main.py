from flask import *
from flask import request
from flask import redirect
import datetime


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
	id_str = str(id)
	cur.execute("SELECT * FROM blog.BlogEntry WHERE entryid = %s", (id_str))
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
	
def process_date(date):
	format = "%b %d %Y"
	return date.strftime(format)
	
def get_range_entries(begin, end):
	cur = mysql.connection.cursor()
	begin_str = str(begin)
	end_str = str(end)
	size = cur.execute("SELECT * FROM blog.BlogEntry WHERE entryid >= %s AND entryid <= %s", (begin_str, end_str))
	res = cur.fetchall()
	entries = []
	for i in range (size-1, -1, -1):
		entry = Entry(res[i][0], process_date(res[i][1]), res[i][2])
		entries.append(entry)
	return entries

def get_num_entries():
	cur   = mysql.connection.cursor()
	query = "SELECT COUNT(*) FROM blog.BlogEntry"
	cur.execute(query)
	return cur.fetchall()[0][0]
	
def get_entry_ids():
	cur   = mysql.connection.cursor()
	query = "SELECT entryid FROM blog.BlogEntry"
	size = cur.execute(query)
	res = cur.fetchall();
	entries = []
	
	for i in range (size-1, -1, -1):
		entries.append(res[i][0])
		
	return entries
	
def check_username():
	if(session.has_key('username') == True):
		username = session['username']
		
def handle_new_blog_post():

	req = request.form
	
	new_post = req.get('new_post')

	cur = mysql.connection.cursor()
	
	date = datetime.datetime.now()
	time_str = date.strftime('%Y-%m-%d')

	#query = "INSERT INTO blog.BlogEntry (entrydate, content) VALUES ('" + str_time + "', '" + #new_post + "')"
	
	cur.execute("INSERT INTO blog.BlogEntry (entrydate, content) VALUES ('%s', '%s')", (time_str, new_post))
	mysql.connection.commit()
	return redirect("/")


@main.route('/', methods=['GET','POST'])
def main_route():
	
	if request.method == 'POST':
		handle_new_blog_post()

	page = request.args.get('page')
	if page == None or page == '':
		page = 0
	else:
		page = int(page)

	num_entries = get_num_entries()
	
	entry_ids = get_entry_ids()
		
	begin = page * 5
	end   = begin + 4

	if end >= num_entries:
		end = num_entries - 1

	entries = get_range_entries(entry_ids[end], entry_ids[begin])

	older = False
	newer = False

	if page > 0:
		newer = True
	if end < num_entries-1 and num_entries > 5:
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

