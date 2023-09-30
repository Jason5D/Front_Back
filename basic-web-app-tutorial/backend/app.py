from flask import Flask, request
import flask
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Initialize an empty list to store user data
user_data = []

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/users", methods=["GET", "POST"])
def users():
    global user_data  # Access the global user_data list

    print("users endpoint reached...")
    if request.method == "GET":
        with open("users.json", "r") as f:
            data = json.load(f)
            return flask.jsonify(data)

    if request.method == "POST":
        received_data = request.get_json()
        print(f"received data: {received_data}")

        # Append the received data to the user_data list
        user_data.append(received_data)

        # Write the updated user_data list to the JSON file
        with open("users.json", "w") as f:
            json.dump(user_data, f, indent=4)

        return_data = {
            "status": "success",
            "message": "User data added successfully"
        }
        return flask.Response(response=json.dumps(return_data), status=201)

if __name__ == "__main__":
    # Load existing user data from the JSON file at startup
    with open("users.json", "r") as f:
        user_data = json.load(f)

    app.run("localhost", 6969)

