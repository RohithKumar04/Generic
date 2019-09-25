from flask import Flask, url_for, render_template, request,session, jsonify
from flask_pymongo import PyMongo
from functools import wraps
import os
from dotenv import load_dotenv
import dns

load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/"+os.getenv("mongodbName")
app.config["SECRET_KEY"]= os.getenv("secret_key")
#app.config["MONGO_DBNAME"]= "student_db"
mongo = PyMongo(app)


@app.route("/bus_register", methods=["POST", "GET"])
def bus_register():
    use = mongo.db.buses
    if request.method == "POST":
        use.insert_one({"_id":request.form["bus_num"],"reg_no": request.form["RegNo"],"driverDetails":{"name":request.form["driver"],"driver_no":request.form["driver_no"]},"students":[]})
        return jsonify({"message":"successfully added"})
    else:
        return render_template("bus_register.html")

# def login_required(f):
#     @wraps(f)
#     def wrap(*args, **kwargs):
#         if "user" in session:
#             return f(*args, **kwargs)
#         else:
#             return jsonify({"message":"you need to login first"})
#     return wrap

# @app.route("/ist_login", methods=["POST", "GET"])
# def ist_login():
#     use = mongo.db.user
#     if request.method == "POST":
#         current_user = use.find_one({"_id":request.form["ist_emailID"]})
#         if current_user:
#             if current_user["password"] == request.form["ist_passwd"]:
#                 session["user"] = current_user
#                 return jsonify({"message":"successfully logged in "})
#             else:
#                 return jsonify({"message":"incorrect password"})
#         else:
#             return jsonify({"message":"username unavailable"})
#     else:
#         return render_template("signup.html")



@app.route("/student_register", methods=["POST", "GET"])
def student_register():
    buses = mongo.db.buses
    use = mongo.db.user
    if request.method == "POST":
        bus_id = buses.find_one({"_id":request.form["stu_bus_no"]})
        if bus_id:
            studet_id = request.form["stu_std"]+request.form["stu_sec"]+request.form["stu_rollno"]
            # print(bus_id["students"])
            buses.update({"_id":request.form["stu_bus_no"]},
                        { "$push":{"students":{"_id":studet_id, "name":request.form["stu_name"],
                                "rollno":request.form["stu_rollno"],
                            "std&sec":request.form["stu_std"]+" "+request.form["stu_sec"]}}})

            use.insert_one({"_id":studet_id,"name": request.form["stu_name"],"std":request.form["stu_std"],"sec":request.form["stu_sec"],"rollno":request.form["stu_rollno"],"busno":request.form["stu_bus_no"],"parent name":request.form["parent_name"],"parent num":request.form["parent_phone"],"blood":request.form["stu_blood"]})
            return (bus_id["students"][0])
        else:
            return jsonify({"message":"invalid bus"})
    else:
        return render_template("stu_register.html")

if __name__ == "__main__":
    app.run(debug=True)

    