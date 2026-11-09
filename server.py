import os
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

API_KEY = os.getenv("OTCHARTS_API_KEY")
BASE_URL = "https://otcharts.com/v1"

def api_get(path, params=None):
    if not API_KEY:
        return {"error": "OTCHARTS_API_KEY is not set"}, 500

    try:
        r = requests.get(
            BASE_URL + path,
            headers={"Authorization": f"Bearer {API_KEY}"},
            params=params,
            timeout=20
        )
        return r.json(), r.status_code
    except Exception as e:
        return {"error": str(e)}, 500

@app.route("/")
def home():
    return jsonify({"status": "Trading Signal Server is running"})

@app.route("/api/venues")
def venues():
    data, status = api_get("/venues")
    return jsonify(data), status

@app.route("/api/symbols")
def symbols():
    venue = request.args.get("venue", "quotex")
    data, status = api_get("/symbols", {"venue": venue})
    return jsonify(data), status

@app.route("/api/candles")
def candles():
    venue = request.args.get("venue", "quotex")
    symbol = request.args.get("symbol")
    tf = request.args.get("tf", "60")
    limit = request.args.get("limit", "300")

    if not symbol:
        return jsonify({"error": "symbol is required"}), 400

    data, status = api_get("/candles", {
        "venue": venue,
        "symbol": symbol,
        "tf": tf,
        "limit": limit
    })
    return jsonify(data), status
