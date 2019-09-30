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
mongo = PyMongo(app)

buses = mongo.db.buses
use = mongo.db.user

@app.route("/bus", methods=["POST","GET"])
def bus():
    if request.method == "POST":
        buses.insert_one({"_id":request.json["bus_num"],"reg_no": request.json["RegNo"],"driverDetails":{"name":request.json["driver"],"driver_no":request.json["driver_no"]},"students":[]})
        return jsonify({"message":"bus successfully added"})

    elif request.method == "GET":
        bus_list = buses.find()
        for doc in bus_list:
            print(doc)
        return jsonify({"message":"bus details"})
    
    else:
        return jsonify({"message":"invalid data"})

@app.route("/bus/<id>", methods=["PUT", "GET"])
def bus_update(id):
    if buses.find_one({"_id":id}):
        if request.method == "PUT":
            buses.update({"_id":id},{"$set":{"reg_no": request.json["RegNo"],"driverDetails":{"name":request.json["driver"],  "driver_no":request.json["driver_no"]}}})
            return jsonify({"message":"successfully\ updated"})

        elif request.method == "GET":
            print(buses.find_one({"_id":id}))
            return jsonify({"message":"deatils of bus"})
    else:
        return jsonify({"message":"invalid user"})

@app.route("/bus/<id>", methods=["DELETE"])
def bus_delete(id):
    if buses.find_one({"_id":id}):
        if request.method == "DELETE":
            buses.remove({"_id":id})
            return jsonify({"message":"successfully\ deleted"})
    else:
        return jsonify({"message":"invalid user"})


@app.route("/students", methods=["POST", "GET"])
def students():
    if request.method == "POST":
        bus_id = buses.find_one({"_id":request.json["stu_bus_no"]})
        if bus_id:
            studet_id = request.json["stu_name"]+request.json["parent_phone"]
            buses.update({"_id":request.json["stu_bus_no"]},
                        { "$push":{"students":{"_id":studet_id, "name":request.json["stu_name"],
                                "rollno":request.json["stu_rollno"],
                            "std&sec":request.json["stu_std"]+" "+request.json["stu_sec"]}}})

            use.insert_one({"_id":studet_id,"name": request.json["stu_name"],"std":request.json["stu_std"],"sec":request.json["stu_sec"],"rollno":request.json["stu_rollno"],"busno":request.json["stu_bus_no"],"parent name":request.json["parent_name"],"parent num":request.json["parent_phone"],"blood":request.json["stu_blood"]})
            return jsonify({"message":"student added successfully"})
        else:
            return jsonify({"message":"invalid bus"})

    elif request.method == "GET":
        user_list = use.find()
        for user in user_list:
            print(user)
        return jsonify({"message":"done"})

    else:
        return jsonify({"message":"invalid bus"})


@app.route("/students/<id>", methods=["DELETE","PUT","GET"])
def del_students(id):
    if request.method == "PUT":
        user_id =use.find_one({"_id":id})
        print(user_id)
        buses.update({"_id":user_id["busno"]},{"$pull":{"students":{"_id":id}}})
        buses.update({"_id":request.json["stu_bus_no"]},
                        { "$push":{"students":{"_id":id, "name":request.json["stu_name"],
                                "rollno":request.json["stu_rollno"],
                            "std&sec":request.json["stu_std"]+" "+request.json["stu_sec"]}}})
        use.update({"_id":id},{"name": request.json["stu_name"],"std":request.json["stu_std"],"sec":request.json["stu_sec"],"rollno":request.json["stu_rollno"],"busno":request.json["stu_bus_no"],"parent name":request.json["parent_name"],"parent num":request.json["parent_phone"],"blood":request.json["stu_blood"]})
        return jsonify({"message":"successfully updated"})

    elif request.method == "GET":
            print(use.find_one({"_id":id}))
            return jsonify({"message":"deatils of student"})

    elif request.method == "DELETE":
        user_id =use.find_one({"_id":id})
        buses.update({"_id":user_id["busno"]},{"$pull":{"students":{"_id":id}}})
        use.remove({"_id":id})
        return jsonify({"message":"bus deleted"})
    else:
       return jsonify({"message":"invalid bus"})

if __name__ == "__main__":
    app.run(debug=True)

    