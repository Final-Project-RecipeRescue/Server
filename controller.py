from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/create', methods=['POST'])
def create():
    data = request.json  # Assuming the request body is JSON
    # Process the data...
    return jsonify({"message": "Data received successfully", "data": data}), 200

if __name__ == '__main__':
    app.run(debug=True, port=8085)