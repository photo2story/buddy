from flask import Flask, send_from_directory, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify(message="Welcome to Buddy Plotter!")

@app.route('/image/<filename>')
def send_image(filename):
    return send_from_directory('static/images', filename)

if __name__ == '__main__':
    app.run(debug=True)
