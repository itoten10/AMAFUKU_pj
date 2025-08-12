from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import googlemaps
from dotenv import load_dotenv
import polyline

# 環境変数読み込み
load_dotenv()

app = Flask(__name__)
CORS(app)

# Google Maps クライアント初期化
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
gmaps = None
if GOOGLE_MAPS_API_KEY:
    gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

@app.route("/", methods=["GET"])
def root():
    return jsonify({"message": "Welcome to Famoly Drive API"})

@app.route("/health", methods=["GET"])  
def health_check():
    return jsonify({
        "status": "healthy", 
        "google_maps_api": bool(GOOGLE_MAPS_API_KEY),
        "gmaps_client": bool(gmaps)
    })

@app.route("/api/v1/routes/search", methods=["POST"])
def search_route():
    data = request.get_json()
    origin = data.get("origin", "東京駅")
    destination = data.get("destination", "鎌倉駅")
    
    if not gmaps:
        # Google Maps APIが利用できない場合はサンプルデータを返す
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
            "historical_spots": get_sample_historical_spots()
        })
    
    try:
        # Geocoding APIで座標取得
        origin_geocode = gmaps.geocode(origin, language='ja')
        dest_geocode = gmaps.geocode(destination, language='ja')
        
        if not origin_geocode or not dest_geocode:
            return jsonify({"error": "Location not found"}), 404
            
        origin_coords = {
            'lat': origin_geocode[0]['geometry']['location']['lat'],
            'lng': origin_geocode[0]['geometry']['location']['lng']
        }
        dest_coords = {
            'lat': dest_geocode[0]['geometry']['location']['lat'],
            'lng': dest_geocode[0]['geometry']['location']['lng']
        }
        
        # Directions APIでルート取得
        directions = gmaps.directions(
            origin,
            destination,
            mode="driving",
            language="ja"
        )
        
        if not directions:
            return jsonify({"error": "Route not found"}), 404
            
        route = directions[0]
        route_polyline = route['overview_polyline']['points']
        
        # ルート周辺の歴史スポットを検索
        historical_spots = get_historical_spots_along_route(route_polyline)
        
        return jsonify({
            "route": {
                "origin": origin,
                "destination": destination,
                "origin_coords": origin_coords,
                "dest_coords": dest_coords,
                "distance": route['legs'][0]['distance']['text'],
                "duration": route['legs'][0]['duration']['text'],
                "polyline": route_polyline
            },
            "historical_spots": historical_spots
        })
        
    except Exception as e:
        print(f"Error in route search: {e}")
        return jsonify({"error": str(e)}), 500

def get_historical_spots_along_route(route_polyline):
    if not gmaps:
        return get_sample_historical_spots()
    
    try:
        # ポリラインをデコードして座標を取得
        route_coords = polyline.decode(route_polyline)
        
        # ルート上のサンプリングポイントを取得
        sample_interval = max(1, len(route_coords) // 5)
        sample_points = route_coords[::sample_interval][:5]
        
        historical_spots = []
        spot_ids = set()
        
        search_keywords = ["神社", "寺", "城", "史跡", "博物館"]
        
        for i, point in enumerate(sample_points):
            keyword = search_keywords[i % len(search_keywords)]
            
            # Places APIで近くの歴史スポットを検索
            places_result = gmaps.places_nearby(
                location=(point[0], point[1]),
                radius=3000,  # 3km radius
                keyword=keyword,
                language='ja'
            )
            
            for place in places_result.get('results', [])[:2]:
                place_id = place.get('place_id')
                if place_id and place_id not in spot_ids:
                    spot_ids.add(place_id)
                    
                    historical_spots.append({
                        "place_id": place_id,
                        "name": place.get('name', '不明な場所'),
                        "address": place.get('vicinity', ''),
                        "lat": place['geometry']['location']['lat'],
                        "lng": place['geometry']['location']['lng'],
                        "types": place.get('types', []),
                        "description": generate_description(place.get('name', ''))
                    })
                    
                if len(historical_spots) >= 5:
                    break
            
            if len(historical_spots) >= 5:
                break
        
        return historical_spots if historical_spots else get_sample_historical_spots()
        
    except Exception as e:
        print(f"Error getting historical spots: {e}")
        return get_sample_historical_spots()

def generate_description(name):
    descriptions = {
        "神社": f"{name}は地域の守り神として古くから信仰されている神社です。",
        "寺": f"{name}は歴史ある寺院で、多くの参拝者が訪れます。",
        "城": f"{name}は戦国時代の歴史を今に伝える貴重な史跡です。",
        "博物館": f"{name}では地域の歴史や文化について学ぶことができます。",
    }
    
    for key, desc in descriptions.items():
        if key in name:
            return desc
    
    return f"{name}は歴史的に重要な場所として知られています。"

def get_sample_historical_spots():
    return [
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

@app.route("/api/v1/routes/save", methods=["POST"])
def save_route():
    data = request.get_json()
    route_data = data.get("route", data)
    
    # 仮のルートIDを生成して返す（実際にはデータベースに保存）
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
    
    # 難易度別のポイント設定
    points_map = {"小学生": 10, "中学生": 15, "高校生": 20}
    points = points_map.get(difficulty, 10)
    
    # スポット名に基づいてクイズを生成
    quiz_data = generate_quiz_for_spot(spot_name, difficulty)
    
    return jsonify({
        "spot_id": data.get("place_id", "sample_1"),
        "spot_name": spot_name,
        "question": quiz_data["question"],
        "options": quiz_data["options"],
        "correct_answer": quiz_data["correct_answer"],
        "explanation": quiz_data["explanation"],
        "difficulty": difficulty,
        "points": points
    })

def generate_quiz_for_spot(spot_name, difficulty):
    # スポット名に基づいてクイズを生成
    if "大仏" in spot_name:
        return {
            "question": f"{spot_name}について正しいものはどれでしょう？",
            "options": [
                "鎌倉時代に建立された",
                "江戸時代に建立された", 
                "明治時代に建立された",
                "昭和時代に建立された"
            ],
            "correct_answer": 0,
            "explanation": f"{spot_name}は13世紀の鎌倉時代に建立された国宝の仏像です。"
        }
    elif "八幡宮" in spot_name:
        return {
            "question": f"{spot_name}の主祭神は誰でしょう？",
            "options": [
                "応神天皇",
                "天照大神",
                "菅原道真",
                "徳川家康"
            ],
            "correct_answer": 0,
            "explanation": f"{spot_name}は応神天皇（八幡神）を主祭神とする神社です。"
        }
    else:
        return {
            "question": f"{spot_name}について正しいものはどれでしょう？",
            "options": [
                "歴史的に重要な場所である",
                "最近建設された施設である", 
                "海外から移築された建物である",
                "架空の場所である"
            ],
            "correct_answer": 0,
            "explanation": f"{spot_name}は長い歴史を持つ重要な文化遺産です。"
        }

if __name__ == "__main__":
    print(f"Google Maps API Key: {'設定済み' if GOOGLE_MAPS_API_KEY else '未設定'}")
    app.run(host="0.0.0.0", port=8000, debug=True)