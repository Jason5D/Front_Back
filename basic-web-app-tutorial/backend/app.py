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

@app.route("/users", methods=["GET", "POST", "DELETE"])
def users():
    global user_data  # Access the global user_data list

    print("users endpoint reached...")

    if request.method == "GET":
        with open("users.json", "r") as f:
            data = json.load(f)
            return flask.jsonify(data)

    if request.method == "POST":
        try:
            received_data = request.get_json()
            print(f"Received data: {received_data}")

            # Validate the received data
            if (
                "user_id" not in received_data
                or "username" not in received_data
                or "pets" not in received_data
            ):
                raise ValueError("Invalid data")

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

        except Exception as e:
            return flask.jsonify({"status": "error", "message": str(e)}), 500

    if request.method == "DELETE":
        user_id_to_delete = request.args.get("user_id")
        if user_id_to_delete:
            # Filter out the user with the specified ID from user_data
            user_data = [
                user for user in user_data if user.get("user_id") != user_id_to_delete
            ]

            # Write the updated user_data list to the JSON file
            with open("users.json", "w") as f:
                json.dump(user_data, f, indent=4)

            return flask.jsonify(
                {
                    "status": "success",
                    "message": f"Deleted user with ID: {user_id_to_delete}",
                }
            )

        else:
            return (
                flask.jsonify({"status": "error", "message": "User ID not provided"}),
                400,
            )

if __name__ == "__main__":
    # Load existing user data from the JSON file at startup
    with open("users.json", "r") as f:
        user_data = json.load(f)

    app.run("localhost", 6969)
