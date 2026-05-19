from flask import Flask, jsonify
from flask_cors import CORS
import subprocess
import platform
import datetime

app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return jsonify({
        "message": "Flask Virtualization API is running",
        "status": "ok",
        "timestamp": datetime.datetime.utcnow().isoformat()
    })


@app.route('/info')
def info():
    return jsonify({
        "status": "Backend running",
        "platform": "AWS EC2 with Docker",
        "python_version": platform.python_version(),
        "os": platform.system(),
        "timestamp": datetime.datetime.utcnow().isoformat()
    })


@app.route('/containers')
def containers():
    try:
        result = subprocess.check_output(
            ["docker", "ps", "--format", "{{.ID}} {{.Image}} {{.Status}} {{.Ports}}"],
            text=True
        )
        containers_list = []
        for line in result.strip().split("\n"):
            if line:
                parts = line.split()
                containers_list.append({
                    "id": parts[0],
                    "image": parts[1],
                    "status": " ".join(parts[2:4]) if len(parts) > 3 else parts[2],
                    "ports": parts[-1] if len(parts) > 3 else "N/A"
                })
        return jsonify({
            "containers": containers_list,
            "count": len(containers_list)
        })
    except FileNotFoundError:
        return jsonify({
            "error": "Docker not found. Is Docker installed and running?",
            "containers": []
        }), 500
    except subprocess.CalledProcessError as e:
        return jsonify({
            "error": f"Docker command failed: {str(e)}",
            "containers": []
        }), 500
    except Exception as e:
        return jsonify({
            "error": str(e),
            "containers": []
        }), 500


@app.route('/health')
def health():
    """Simple health check endpoint."""
    return jsonify({"healthy": True}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
