from flask import Flask, jsonify
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({
        "message": "Hello from Flask API!"
    })

@app.route('/info')
def info():
    return jsonify({
        "status": "Backend running",
        "platform": "AWS EC2 with Docker"
    })

@app.route('/containers')
def containers():
    try:
        result = subprocess.check_output(
            ["docker", "ps", "--format", "{{.ID}} {{.Image}} {{.Status}}"],
            text=True
        )

        containers_list = []

        for line in result.strip().split("\n"):
            if line:
                parts = line.split()

                containers_list.append({
                    "id": parts[0],
                    "image": parts[1],
                    "status": " ".join(parts[2:])
                })

        return jsonify({
            "containers": containers_list
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
