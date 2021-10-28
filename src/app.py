from flask import Flask, jsonify, request
from flask_mongoengine import MongoEngine

app = Flask(__name__)

app.config["MONGO_URI"] = {
    "db": "personsData",
    "host": "localhost",
    "port": 27017
}

db = MongoEngine()
db.init_app(app)


class User(db.Document):
    name = db.StringField()
    age = db.IntField()
    birthday = db.StringField()

    def to_json(self):
        return {"name": self.name, "age": self.age, "birthday": self.birthday}


@app.route("/api/", methods=["GET"])
def getAllData():
    user = User.objects()
    return user.to_json()


@app.route("/api/<string:name>", methods=["GET"])
def getOneFromData(name):
    user = User.objects(name=name).first()
    if not user:
        return jsonify({"Error": "Data not found."})
    else:
        return user.to_json()



@app.route("/api/", methods=["POST"])
def addOneToData():
    user = User(
        name=request.json["name"],
        age=request.json["age"],
        birthday=request.json["birthday"]
    )

    user.save()
    return user.to_json()


@app.route("/api/<string:name>/", methods=["PUT"])
def updateOneFromData(name):
    user = User.objects(name=name).first()
    if not user:
        return jsonify({"Error": "Data not found."})
    else:
        user.update(
            name=request.json["name"],
            age=request.json["age"],
            birthday=request.json["birthday"])

    users = User.objects()
    return users.to_json()


@app.route("/api/<string:name>/", methods=["DELETE"])
def deleteOneFromData(name):
    user = User.objects(name=name).first()
    if not user:
        return jsonify({"Error": "Data not found."})
    else:
        user.delete()

    users = User.objects()
    return users.to_json()


if __name__ == "__main__":
    app.run(debug=True)
