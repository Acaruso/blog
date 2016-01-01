import hashlib
from flask import *
from flask import request
from flask.ext.mysqldb import MySQL

mysql = MySQL()

login = Blueprint('login', __name__, template_folder='views')

@login.route('/login', methods=['GET','POST'])
def login_route():
	
	internal_error = None
	
	if request.method == 'POST':
		req = request.form
		username = req['username']
		usr_pass = req['password']
		
		cur = mysql.connection.cursor()
		
		query = "SELECT password FROM blog.User WHERE username = '" + username + "'"
		cur.execute(query)
		result = cur.fetchall()
		if not result:
			print "user does not exist!"
			internal_error = "Error: user does not exist"
		else:
			db_pass = result[0][0]
			usr_pass = hashlib.sha1(usr_pass).hexdigest()
			if usr_pass == db_pass:
				session['username'] = username

				print "authentication successful!"
				print "username: " + session['username']

				return redirect("/")
			else:
				print "authentication failed!"
				internal_error = "Error: invalid password"
	
	return render_template("login.html", internal_error=internal_error)

