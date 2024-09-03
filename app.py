from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_pymongo import PyMongo

app = Flask(__name__)

# Configure MongoDB Atlas with a database name
app.config["MONGO_URI"] = "mongodb+srv://jayantrawat02:Bugbounty22@clusterdpia.zk1cf.mongodb.net/users?retryWrites=true&w=majority"
mongo = PyMongo(app)

# Check connection
try:
    mongo.cx.server_info()  # Attempt to get server info to test connection
    print("Successfully connected to MongoDB Atlas!")
except Exception as e:
    print("Failed to connect to MongoDB Atlas", e)

# Registration route
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if mongo.db.users.find_one({"username": username}):
        return jsonify({"message": "Username already exists"}), 400

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    mongo.db.users.insert_one({"username": username, "password": hashed_password})

    return jsonify({"message": "User registered successfully"}), 200

# Login route
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = mongo.db.users.find_one({"username": username})
    if user and check_password_hash(user['password'], password):
        return jsonify({"message": "Login successful!"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# Route to handle general information
@app.route('/generalinformation', methods=['POST'])
def general_information():
    data = request.json
    print(f"Received general information: {data}")
    return jsonify({"message": "General information received"}), 200

# Route to handle quiz answers
@app.route('/quizanswers', methods=['POST'])
def quiz_answers():
    data = request.json
    print(f"Received quiz answer: {data}")
    return jsonify({"message": "Quiz answer received"}), 200

if __name__ == '__main__':
    app.run(debug=True)
