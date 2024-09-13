from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_pymongo import PyMongo
import random

app = Flask(__name__)

# Configure MongoDB Atlas for users database
app.config["MONGO_URI_USERS"] = "mongodb+srv://jayantrawat02:Bugbounty22@clusterdpia.zk1cf.mongodb.net/users?retryWrites=true&w=majority"
mongo_users = PyMongo(app, uri=app.config["MONGO_URI_USERS"])

# Configure MongoDB Atlas for answers database
app.config["MONGO_URI_ANSWERS"] = "mongodb+srv://jayantrawat02:Bugbounty22@clusterdpia.zk1cf.mongodb.net/answers?retryWrites=true&w=majority"
mongo_answers = PyMongo(app, uri=app.config["MONGO_URI_ANSWERS"])

# Check connection for users database
try:
    mongo_users.cx.server_info()  # Attempt to get server info to test connection
    print("Successfully connected to MongoDB Atlas (users)!")
except Exception as e:
    print("Failed to connect to MongoDB Atlas (users)", e)

# Check connection for answers database
try:
    mongo_answers.cx.server_info()  # Attempt to get server info to test connection
    print("Successfully connected to MongoDB Atlas (answers)!")
except Exception as e:
    print("Failed to connect to MongoDB Atlas (answers)", e)

def generate_user_id():
    """Generate a unique 4-digit user ID."""
    while True:
        user_id = str(random.randint(1000, 9999))
        if not mongo_users.db.users.find_one({"user_id": user_id}):
            return user_id

# Registration route
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if mongo_users.db.users.find_one({"username": username}):
        return jsonify({"message": "Username already exists"}), 400

    user_id = generate_user_id()
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    mongo_users.db.users.insert_one({
        "username": username, 
        "password": hashed_password, 
        "user_id": user_id
    })

    return jsonify({"message": "User registered successfully", "user_id": user_id}), 200

# Login route
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = mongo_users.db.users.find_one({"username": username})
    if user and check_password_hash(user['password'], password):
        return jsonify({"message": "Login successful!", "user_id": user['user_id']}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# Route to handle general information
@app.route('/generalinformation', methods=['POST'])
def general_information():
    data = request.json
    user_id = data.get('user_id')
    print(f"Received general information from user {user_id}: {data}")
    return jsonify({"message": "General information received"}), 200

# Route to handle quiz answers
@app.route('/quizanswers', methods=['POST'])
def quiz_answers():
    data = request.json
    user_id = data.get('user_id')
    question = data.get('question')
    answer = data.get('answer')

    # Save the answer in the 'answers' collection of the 'answers' database
    mongo_answers.db.answers.insert_one({
        "user_id": user_id,
        "question": question,
        "answer": answer
    })
    
    print(f"Received quiz answer from user {user_id}: {data}")
    return jsonify({"message": "Quiz answer received"}), 200

if __name__ == '__main__':
    app.run(debug=True)
