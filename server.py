from flask import Flask, json, request, jsonify

app = Flask(__name__)

@app.route('/generalinformation', methods=['POST'])
def general_information():
    data = request.json
    with open('general_information_log.json', 'a') as file:
        file.write(json.dumps(data) + '\n')
    return jsonify({'message': 'General information received'}), 200

@app.route('/quizanswers', methods=['POST'])
def quiz_answers():
    answers = request.json
    with open('quiz_answers_log.json', 'a') as file:
        file.write(json.dumps(answers) + '\n')
    return jsonify({'message': 'Quiz answers received'}), 200

if __name__ == '__main__':
    app.run(debug=True)
