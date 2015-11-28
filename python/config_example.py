
# Example configuration file

# note that you must change username and password for SQL database

import os
from flask import Flask, render_template
from flask.ext.mysqldb import MySQL

import controllers

app = Flask(__name__, template_folder='views')

UPLOAD_FOLDER = './static/pictures'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mysql = MySQL()
app.config['MYSQL_USER'] ='my_user'
app.config['MYSQL_PASSWORD'] ='my_password'
mysql.init_app(app)

app.secret_key = os.urandom(24).encode('hex')

app.register_blueprint(controllers.main)
