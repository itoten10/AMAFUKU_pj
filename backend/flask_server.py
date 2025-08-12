from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def root():
    return jsonify({"message": "Welcome to Famoly Drive API"})

@app.route("/health", methods=["GET"])  
def health_check():
    return jsonify({
        "status": "healthy", 
        "google_maps_api": bool(os.getenv("GOOGLE_MAPS_API_KEY"))
    })

@app.route("/api/v1/routes/search", methods=["POST"])
def search_route():
    data = request.get_json()
    origin = data.get("origin", "東京駅")
    destination = data.get("destination", "鎌倉駅")
    
    return jsonify({
        "route": {
            "origin": origin,
            "destination": destination,
            "origin_coords": {"lat": 35.6812, "lng": 139.7671},
            "dest_coords": {"lat": 35.3197, "lng": 139.5516},
            "distance": "55.2 km",
            "duration": "1時間 15分",
            "polyline": "o}jaEucanQKqAMcAQeAOmABG{@sAUc@"
        },
        "historical_spots": [
            {
                "place_id": "sample_1",
                "name": "鎌倉大仏",
                "address": "神奈川県鎌倉市長谷",
                "lat": 35.3169,
                "lng": 139.5359,
                "types": ["tourist_attraction"],
                "description": "鎌倉大仏は13世紀に建立された国宝の仏像です。"
            },
            {
                "place_id": "sample_2", 
                "name": "鶴岡八幡宮",
                "address": "神奈川県鎌倉市雪ノ下",
                "lat": 35.3249,
                "lng": 139.5565,
                "types": ["shrine"],
                "description": "鶴岡八幡宮は鎌倉の守護神として古くから信仰されています。"
            }
        ]
    })

@app.route("/api/v1/routes/save", methods=["POST"])
def save_route():
    data = request.get_json()
    route_data = data.get("route", data)
    
    # 仮のルートIDを生成して返す
    return jsonify({
        "id": 1,
        "origin": route_data.get("origin", "東京駅"),
        "destination": route_data.get("destination", "鎌倉駅"),
        "origin_lat": route_data.get("origin_coords", {}).get("lat", 35.6812),
        "origin_lng": route_data.get("origin_coords", {}).get("lng", 139.7671),
        "dest_lat": route_data.get("dest_coords", {}).get("lat", 35.3197),
        "dest_lng": route_data.get("dest_coords", {}).get("lng", 139.5516),
        "distance": route_data.get("distance", "55.2 km"),
        "duration": route_data.get("duration", "1時間 15分"), 
        "polyline": route_data.get("polyline", "o}jaEucanQKqAMcAQeAOmABG{@sAUc@"),
        "created_at": "2024-01-01T00:00:00",
        "historical_spots": data.get("historical_spots", [])
    })

@app.route("/api/v1/quizzes/generate", methods=["POST"])
def generate_quiz():
    data = request.get_json()
    spot_name = data.get("name", "歴史スポット")
    difficulty = request.args.get("difficulty", "中学生")
    
    return jsonify({
        "spot_id": data.get("place_id", "sample_1"),
        "spot_name": spot_name,
        "question": f"{spot_name}について正しいものはどれでしょう？",
        "options": [
            f"{spot_name}は鎌倉時代に建立されました",
            f"{spot_name}は江戸時代に建立されました", 
            f"{spot_name}は明治時代に建立されました",
            f"{spot_name}は昭和時代に建立されました"
        ],
        "correct_answer": 0,
        "explanation": f"{spot_name}は鎌倉時代に建立された歴史ある建造物です。",
        "difficulty": difficulty,
        "points": 10
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)