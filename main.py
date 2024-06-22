from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/api/data")
def get_data():
    sample_data = {"message": "Hello from Flask!"}
    return jsonify(sample_data)

if __name__ == "__main__":
    app.run(debug=True)

# .\\.venv\\Scripts\\activate
# python main.py
