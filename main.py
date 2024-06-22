# main.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from threading import Thread
import os
from dotenv import load_dotenv
import sys

# 콘솔 출력 인코딩을 UTF-8로 설정
sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route("/api/data")
def get_data():
    sample_data = {"message": "Hello from Flask!"}
    return jsonify(sample_data)

def run():
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8080)))

# Make sure to call keep_alive() before starting the Discord bot
def keep_alive():
    server = Thread(target=run)
    server.start()

keep_alive()

if __name__ == '__main__':
    app.run(debug=True)
