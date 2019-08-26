from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv
import pymysql

load_dotenv()

sqlid= os.getenv("mysql_id")
sqlpwd = os.getenv("mysql_pwd")
dbname = os.getenv("database_name")
key = os.getenv("secret_key")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]= 'mysql+pymysql://'+ sqlid +':'+ sqlpwd +'@localhost:3306/'+ dbname
app.config["SECRET_KEY"]= key
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from project import routes