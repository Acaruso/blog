from flask import *
from flask.ext.mysqldb import MySQL

mysql = MySQL()

main = Blueprint('main', __name__, template_folder='views')

@main.route('/')
def main_route():
	options = {
		"str": "hi"
	}
		
	return render_template("index.html", **options)

