from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= "sqlite:///test.db"
app.config["SECRET_KEY"]="testdb"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from sql import routes
