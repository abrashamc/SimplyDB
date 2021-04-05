from flask import Flask, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.SentencesDatabase
users = db.Users


# TODO add check to see if same user tries to register more than once
class Register(Resource):
    def post(self):
        posted_data = request.get_json()

        username = posted_data["Username"]
        password = posted_data["Password"]

        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        users.insert({
            "Username": username,
            "Password": hashed_pw,
            "Note": "",
            "Tokens": 10
        })

        return_json = {
            "Status": 200,
            "Message": "You successfully signed up for the API"
        }

        return return_json


def verify_pw(username, password):
    hashed_pw = users.find({
        "Username": username
    })[0]["Password"]

    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False


def count_tokens(username):
    tokens = users.find({
        "Username": username
    })[0]["Tokens"]
    return tokens


class Store(Resource):
    def post(self):
        posted_data = request.get_json()
        username = posted_data['Username']
        password = posted_data['Password']
        note = posted_data['Note']

        # Verify credentials
        correct_pw = verify_pw(username, password)

        if not correct_pw:
            return_json = {
                "Status": 401,
                "Message": "Invalid credentials"
            }
            return return_json, 401

        # Verify tokens
        num_tokens = count_tokens(username)

        if num_tokens <= 0:
            return_json = {
                "status": 402,
                "message": "Not enough tokens"
            }
            return return_json, 402

        # Update note and token in db
        users.update({
            "Username": username
        }, {
            "$set": {
                "Note": note,
                "Tokens": num_tokens - 1
            }
        })

        return_json = {
            "Status": 200,
            "Message": "Note saved successfully"
        }

        return return_json


class Get(Resource):
    def post(self):
        posted_data = request.get_json()
        username = posted_data['Username']
        password = posted_data['Password']

        # Verify credentials
        correct_pw = verify_pw(username, password)

        if not correct_pw:
            return_json = {
                "Status": 401,
                "Message": "Invalid credentials"
            }
            return return_json, 401

        # Verify tokens
        num_tokens = count_tokens(username)

        if num_tokens <= 0:
            return_json = {
                "status": 402,
                "message": "Not enough tokens"
            }
            return return_json, 402

        # Update note and token in db
        users.update({
            "Username": username
        }, {
            "$set": {
                "Tokens": num_tokens - 1
            }
        })

        note = users.find({
            'Username': username
        })[0]['Note']

        return_json = {
            "Status": 200,
            "Note": note
        }

        return return_json


api.add_resource(Register, '/register')
api.add_resource(Store, '/store')
api.add_resource(Get, '/get')


@app.route('/')
def status():
    return "Welcome to SimplyDB!"


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
