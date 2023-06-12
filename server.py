from flask import Flask, request, jsonify
from flask_cors import CORS
from old_school_retrieval import get_answer

app = Flask(__name__)
CORS(app)


@app.route('/api/process_text', methods=['POST'])
def process_text():
    print("called server")
    data = request.get_json()
    input_text = data.get('text', '')
    print('input_text: ', input_text)

    # Process the input_text here as needed
    response_text = get_answer(input_text)
    print('response_text: ', response_text)
    return jsonify({"message": response_text})


app.run(debug=True)
