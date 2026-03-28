# === IMPORTS ===
from flask import Flask, jsonify
from flask_cors import CORS
import json
import os
import time

# === CREATE THE FLASK APP ===
app = Flask(__name__)
CORS(app)

# === PATH TO THE JSON FILE THAT detect.py WRITES ===
# detect.py saves detection results here every frame
JSON_PATH = os.path.join(os.path.dirname(__file__), '..', 'model', 'static', 'detection_data.json')
# Adjust this path based on where your detect.py saves the file


# === THE ROUTE ===
@app.route("/crowd", methods=["GET"])
def crowd():
    """
    This route simply READS the JSON file that detect.py keeps updating.
    
    Flow:
    detect.py (runs separately) → writes detection_data.json every frame
    app.py (this file)          → reads detection_data.json when website asks
    website (React/HTML)        → calls /crowd every 2 seconds
    """
    try:
        # Check if the JSON file exists
        if not os.path.exists(JSON_PATH):
            return jsonify({
                "people": 0,
                "status": "Unknown",
                "time": time.strftime("%H:%M:%S"),
                "error": "Detection not running. Start detect.py first!"
            })

        # Read the latest data from JSON file
        with open(JSON_PATH, "r") as f:
            data = json.load(f)

        # Return the data to the website
        return jsonify({
            "people": data.get("people_count", 0),
            "status": data.get("status", "Unknown"),
            "time": data.get("time", "N/A"),
            "timestamp": data.get("timestamp", "N/A")
        })

    except Exception as e:
        return jsonify({
            "people": 0,
            "status": "Error",
            "error": str(e)
        })


# === HEALTH CHECK ROUTE (optional but useful) ===
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Smart Campus API is running!",
        "endpoints": {
            "/crowd": "GET - Returns current people count and status"
        }
    })


# === START THE SERVER ===
if __name__ == "__main__":
    print("=" * 50)
    print("🌐 Starting Smart Campus API Server...")
    print(f"📄 Reading data from: {JSON_PATH}")
    print("⚠️  Make sure detect.py is running separately!")
    print("=" * 50)
    app.run(debug=True, port=5000)