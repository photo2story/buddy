from flask import Flask, send_from_directory, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to Buddy Plotter!"})

@app.route('/image/<filename>')
def get_image(filename):
    return send_from_directory('images', filename)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
