# main.py
from flask import Flask, jsonify
from flask_cors import CORS
from threading import Thread
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route("/api/data")
def get_data():
    sample_data = {"message": "Hello from Flask!"}
    return jsonify(sample_data)

def run():
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    server = Thread(target=run)
    server.start()

if __name__ == '__main__':
    keep_alive()
