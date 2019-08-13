from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import jwt
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= "sqlite:///test.db"
app.config["SECRET_KEY"]="testdb"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class users(db.Model):
    #id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False, primary_key=True)
    passwd = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return "user(name:{}, mailID:{})".format(self.name, self.email)


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
        new_data = users(name= user, email=mail, passwd=hash_pwd)

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
            return token
        else:
            return "wrong password"

    else:
        return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)