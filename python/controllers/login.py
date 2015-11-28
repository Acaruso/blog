from flask import *
from flask.ext.mysqldb import MySQL

mysql = MySQL()

login = Blueprint('login', __name__, template_folder='views')

@login.route('/login')
def login_route():
	options = {
		"str": "hi",
	}
		
	return render_template("login.html", **options)

