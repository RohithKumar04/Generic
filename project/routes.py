from flask import Flask, render_template, request, redirect, url_for, jsonify
from project import app, db, bcrypt
from project.models import users
import jwt

@app.route('/', methods=['POST','GET'])
def main():
    return "successfully logged in"

@app.route("/signup", methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        user = request.form['username']
        mail = request.form['emailID']
        real_pwd = request.form['passwd']
        hash_pwd = bcrypt.generate_password_hash(real_pwd)
        new_data = users(user, mail, hash_pwd)

        try:
            db.session.add(new_data)
            db.session.commit()
            return "added to databse"
        except:
            return "sorry!"
    else:
        return render_template("register.html")

@app.route("/login", methods=['POST','GET'])
def login():
    if request.method == 'POST':
        mail = request.form['emailID']
        pwd = request.form['passwd']
        user = users.query.filter_by(email= mail).first()
        if user and bcrypt.check_password_hash(user.passwd,request.form['passwd']):
            token = jwt.encode({"username":user.name, "Email":user.email},app.config["SECRET_KEY"])
            return jsonify({"token":token.decode("UTF-8")})
        else:
            return "wrong password"

    else:
        return render_template("login.html")
