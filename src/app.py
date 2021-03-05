from flask import Flask, jsonify, request
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS
from os import environ

# initialization
app = Flask(__name__)
CORS(app)

#Mongo Connection
app.config["MONGO_URI"] = environ.get("MONGO_URI", "mongodb://localhost:27017/student")
mongo = PyMongo(app)
db = mongo.db

base_route = '/api/v1/'

@app.route(base_route+'students', methods=['GET'])
def get_all_students():
    _students = db.student.find()
    item = {}
    data = []
    for student in _students:
        item = {
            'id': str(student['_id']),
            'student': student['student']
        }
        data.append(item)

    return jsonify(data), 200

@app.route(base_route+'students/<string:id>', methods=['GET'])
def get_student_by_id(id:str):
    _student = db.student.find_one({"_id": ObjectId(id)})
    item = {
        'id': str(_student['_id']),
        'student': _student['student']
    }

    return jsonify(item), 200

@app.route(base_route+'students', methods=['POST'])
def create_new_student():
    data = request.get_json(force=True)
    item ={
        "student": data.copy()
    }
    test = db.student.insert_one(item)
    id = str(test.inserted_id)
    return jsonify(location=base_route+"students/"+id), 201

@app.route(base_route+'/students/<string:id>', methods=['PUT'])
def update_student(id:str):
    data = request.get_json(force=True)
    db.student.update_one({"_id": ObjectId(id)}, {"$set": data})

    return "", 204

@app.route(base_route+'/students/<string:id>', methods=['DELETE'])
def delete_student(id: str):
    db.student.delete_one({"_id": ObjectId(id)})

    return "", 204
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)